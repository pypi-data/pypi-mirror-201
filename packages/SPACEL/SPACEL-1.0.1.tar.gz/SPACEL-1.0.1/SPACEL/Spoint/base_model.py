from . import model
from . import data_utils
import numpy as np
import pandas as pd
import scanpy as sc
import scvi
import anndata
from . import metrics
import matplotlib.pyplot as plt
import os
from copy import deepcopy
import logging
import itertools
from functools import partial
from tqdm import tqdm
from time import strftime, localtime
from scipy.sparse import issparse
from sklearn.decomposition import PCA

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, BatchSampler
from torch.nn.parameter import Parameter
from torch.nn.modules.module import Module
from torch.utils.data.dataloader import default_collate

def guassian_kernel(source, target):
    n_samples = int(source.shape[0])+int(target.shape[0])
    total = np.concatenate((source, target), axis=0)
    total0 = np.expand_dims(total,axis=0)
    total0= np.broadcast_to(total0,[int(total.shape[0]), int(total.shape[0]), int(total.shape[1])])
    total1 = np.expand_dims(total,axis=1)
    total1=np.broadcast_to(total1,[int(total.shape[0]), int(total.shape[0]), int(total.shape[1])])
    L2_distance_square = np.cumsum(np.square(total0-total1),axis=2)
    bandwidth = np.sum(L2_distance_square) / (n_samples**2-n_samples)
    kernel_val = np.exp(-L2_distance_square / bandwidth)
    return kernel_val

def MMD(source, target):
    batch_size = int(source.shape[0])
    kernels = guassian_kernel(source, target)
    loss = 0
    for i in range(batch_size):
        s1, s2 = i, (i + 1) % batch_size
        t1, t2 = s1 + batch_size, s2 + batch_size
        loss += kernels[s1, s2] + kernels[t1, t2]
        loss -= kernels[s1, t2] + kernels[s2, t1]
    n_loss= loss / float(batch_size)
    return np.mean(n_loss)

def compute_kernel(x, y):
    x_size = x.size(0)
    y_size = y.size(0)
    dim = x.size(1)
    tiled_x = torch.tile(torch.reshape(x, (x_size, 1, dim)), (1, y_size, 1))
    tiled_y = torch.tile(torch.reshape(y, (1, y_size, dim)), (x_size, 1, 1))
    return torch.exp(-torch.square(tiled_x - tiled_y).mean(2) / dim)

def compute_mmd(x, y):
    x_kernel = compute_kernel(x, x)
    y_kernel = compute_kernel(y, y)
    xy_kernel = compute_kernel(x, y)
    return x_kernel.mean() + y_kernel.mean() - 2 * xy_kernel.mean()

class PredictionModel(nn.Module):
    def __init__(
        self, 
        input_dims,
        latent_dims,
        hidden_dims,
        celltype_dims,
        dropout
    ):
        super(PredictionModel, self).__init__()
        
        self.encoder = nn.Sequential(
            nn.Linear(input_dims, hidden_dims),
            nn.LeakyReLU(),
            nn.BatchNorm1d(hidden_dims),
            nn.Linear(hidden_dims, hidden_dims),
            nn.LeakyReLU(),
            nn.BatchNorm1d(hidden_dims),
            nn.Linear(hidden_dims, hidden_dims),
            nn.LeakyReLU(),
            nn.BatchNorm1d(hidden_dims),
            nn.Dropout(dropout),
            nn.Linear(hidden_dims, latent_dims)
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_dims, hidden_dims),
            nn.LeakyReLU(),
            nn.BatchNorm1d(hidden_dims),
            nn.Linear(hidden_dims, hidden_dims),
            nn.LeakyReLU(),
            nn.BatchNorm1d(hidden_dims),
            nn.Linear(hidden_dims, hidden_dims),
            nn.LeakyReLU(),
            nn.BatchNorm1d(hidden_dims),
            nn.Dropout(dropout),
            nn.Linear(hidden_dims, input_dims)
        )
        self.pred = nn.Sequential(
            nn.Linear(latent_dims, hidden_dims),
            nn.LeakyReLU(),
            nn.Linear(hidden_dims, celltype_dims),
            nn.Softmax(dim=1),
        )
                
        nn.init.kaiming_normal_(self.encoder[0].weight)
        nn.init.kaiming_normal_(self.encoder[3].weight)
        nn.init.kaiming_normal_(self.encoder[6].weight)
        nn.init.xavier_uniform_(self.encoder[-1].weight)
        
        nn.init.kaiming_normal_(self.decoder[0].weight)
        nn.init.kaiming_normal_(self.decoder[3].weight)
        nn.init.kaiming_normal_(self.decoder[6].weight)
        nn.init.xavier_uniform_(self.decoder[-1].weight)

        nn.init.kaiming_normal_(self.pred[0].weight)
        nn.init.xavier_uniform_(self.pred[2].weight)
        
    @staticmethod
    def l2_activate(x,dim):
        
        def scale(z):
            zmax = z.max(1, keepdims=True).values
            zmin = z.min(1, keepdims=True).values
            z_std = torch.nan_to_num(torch.div(z - zmin,(zmax - zmin)),0)
            return z_std
        
        x = scale(x)
        x = F.normalize(x, p=2, dim=1)
        return x

    def forward(self, x):
        z = self.l2_activate(self.encoder(x),dim=1)
        pred = self.pred(z)
        decoded = self.decoder(z)
        return z, pred, decoded

class SpointModel():
    def __init__(
        self, 
        st_ad, 
        sm_ad, 
        clusters, 
        used_genes, 
        spot_names, 
        use_rep,
        st_batch_key=None,
        scvi_layers=2,
        scvi_latent=64,
        scvi_gene_likelihood='zinb',
        scvi_dispersion='gene-batch',
        latent_dims=32, 
        hidden_dims=512,
        l1=0.01,
        l2=0.01,
        sm_lr=3e-4,
        st_lr=3e-4,
        use_gpu=None,
        seed=42
    ):
        if ((use_gpu is None) or (use_gpu is True)) and (torch.cuda.is_available()):
            self.device = 'cuda'
        else:
            self.device = 'cpu'
        self.use_gpu = use_gpu
        
        self.st_ad = st_ad
        self.sm_ad = sm_ad
        self.scvi_dims=64
        self.spot_names = spot_names
        self.used_genes = used_genes
        self.clusters = clusters
        self.st_batch_key = st_batch_key
        self.scvi_layers = scvi_layers
        self.scvi_latent = scvi_latent
        self.scvi_gene_likelihood = scvi_gene_likelihood
        self.scvi_dispersion = scvi_dispersion
        self.mse_loss_func = F.mse_loss
        self.kl_infer_loss_func = partial(self.kl_divergence, dim=1)
        self.kl_rec_loss_func = partial(self.kl_divergence, dim=0)
        self.cosine_infer_loss_func = partial(F.cosine_similarity, dim=1)
        self.cosine_rec_loss_func = partial(F.cosine_similarity, dim=0)
        self.l1 = l1
        self.l2 = l2
        self.use_rep = use_rep
        if use_rep == 'scvi':
            feature_dims = scvi_latent
        elif use_rep == 'X':
            feature_dims = st_ad.shape[1]
        elif use_rep == 'pca':
            feature_dims = 50
        else:
            raise ValueError('use_rep must be one of scvi, pca and X.')
        self.model = PredictionModel(feature_dims,latent_dims,hidden_dims,len(clusters),0.5).to(self.device)
        self.sm_optimizer = optim.Adam(self.model.parameters(),lr=sm_lr)
        self.st_optimizer = optim.Adam(list(self.model.encoder.parameters())+list(self.model.decoder.parameters()),lr=st_lr)
        self.best_path = None
        self.history = pd.DataFrame(columns = ['sm_train_rec_loss','sm_train_infer_loss','sm_train_total_loss','sm_test_rec_loss','sm_test_infer_loss','sm_test_total_loss','st_train_rec_loss','st_test_rec_loss','is_best'])
        self.batch_size = None
        self.seed = seed
        
    @staticmethod
    def kl_divergence(y_true, y_pred, dim=0):
        y_pred = torch.clip(y_pred, torch.finfo(torch.float32).eps)
        y_true = y_true.to(y_pred.dtype)
        y_true = torch.nan_to_num(torch.div(y_true, y_true.sum(dim, keepdims=True)),0)
        y_pred = torch.nan_to_num(torch.div(y_pred, y_pred.sum(dim, keepdims=True)),0)
        y_true = torch.clip(y_true, torch.finfo(torch.float32).eps, 1)
        y_pred = torch.clip(y_pred, torch.finfo(torch.float32).eps, 1)
        return torch.mul(y_true, torch.log(torch.nan_to_num(torch.div(y_true, y_pred)))).mean(dim)
        
    def get_scvi_latent(
        self,
        n_layers,
        n_latent,
        gene_likelihood,
        dispersion,
        max_epochs,
        early_stopping,
        batch_size,
    ):
        if self.st_batch_key is not None:
            if 'simulated' in self.st_ad.obs[self.st_batch_key]:
                raise ValueError(f'obs[{self.st_batch_key}] cannot include "real".')
            self.st_ad.obs["batch"] = self.st_ad.obs[self.st_batch_key].astype(str)
            self.sm_ad.obs["batch"] = 'simulated'
        else:
            self.st_ad.obs["batch"] = 'real'
            self.sm_ad.obs["batch"] = 'simulated'

        adata = sc.concat([self.st_ad,self.sm_ad])
        adata.layers["counts"] = adata.X.copy()

        scvi.model.SCVI.setup_anndata(
            adata,
            layer="counts",
            batch_key="batch"
        )

        vae = scvi.model.SCVI(adata, n_layers=n_layers, n_latent=n_latent, gene_likelihood=gene_likelihood,dispersion=dispersion)
        vae.train(max_epochs=max_epochs,early_stopping=early_stopping,batch_size=batch_size,use_gpu=self.use_gpu)
        adata.obsm["X_scVI"] = vae.get_latent_representation()

        st_scvi_ad = anndata.AnnData(adata[adata.obs['batch'] != 'simulated'].obsm["X_scVI"])
        sm_scvi_ad = anndata.AnnData(adata[adata.obs['batch'] == 'simulated'].obsm["X_scVI"])

        st_scvi_ad.obs = self.st_ad.obs
        st_scvi_ad.obsm = self.st_ad.obsm

        sm_scvi_ad.obs = self.sm_ad.obs
        sm_scvi_ad.obsm = self.sm_ad.obsm
        
        sm_scvi_ad = data_utils.check_data_type(sm_scvi_ad)
        st_scvi_ad = data_utils.check_data_type(st_scvi_ad)

        self.sm_data = sm_scvi_ad.X
        self.sm_labels = sm_scvi_ad.obsm['label'].values
        self.st_data = st_scvi_ad.X
        
        return sm_scvi_ad,st_scvi_ad

    
    def build_dataset(self, batch_size, device):
        x_train,y_train,x_test,y_test = data_utils.split_shuffle_data(np.array(self.sm_data,dtype=np.float32),np.array(self.sm_labels,dtype=np.float32))
        
        x_train = torch.tensor(x_train).to(device)
        y_train = torch.tensor(y_train).to(device)
        x_test = torch.tensor(x_test).to(device)
        y_test = torch.tensor(y_test).to(device)
        st_data = torch.tensor(self.st_data).to(device)
        
        self.sm_train_ds = TensorDataset(x_train, y_train)
        self.sm_test_ds = TensorDataset(x_test,y_test)
        self.st_ds = TensorDataset(st_data)
        
        self.sm_train_batch_size = min(len(self.sm_train_ds), batch_size)
        self.sm_test_batch_size = min(len(self.sm_test_ds), batch_size)
        self.st_batch_size = min(len(self.st_ds), batch_size)
        
        g = torch.Generator()
        g.manual_seed(self.seed)
        self.sm_train_sampler = BatchSampler(RandomSampler(self.sm_train_ds, generator=g), batch_size=self.sm_train_batch_size, drop_last=True)
        self.sm_test_sampler = BatchSampler(RandomSampler(self.sm_test_ds, generator=g), batch_size=self.sm_test_batch_size, drop_last=True)
        self.st_sampler = BatchSampler(RandomSampler(self.st_ds, generator=g), batch_size=self.st_batch_size, drop_last=True)
    
    def train_sm(self, data, labels, rec_w=0.5, infer_w=1):
        self.model.train()
        self.sm_optimizer.zero_grad()
        latent, predictions, rec_data = self.model(data)
        rec_loss = self.kl_rec_loss_func(data, rec_data).mean() - self.cosine_rec_loss_func(data,rec_data).mean()
        infer_loss = self.kl_infer_loss_func(labels,predictions).mean() - self.cosine_infer_loss_func(labels,predictions).mean()

        regularization_params = torch.cat([
            torch.cat([x.view(-1) for x in self.model.encoder[0].parameters()]),
            torch.cat([x.view(-1) for x in self.model.encoder[3].parameters()]),
            torch.cat([x.view(-1) for x in self.model.encoder[6].parameters()]),
            torch.cat([x.view(-1) for x in self.model.decoder[0].parameters()]),
            torch.cat([x.view(-1) for x in self.model.decoder[3].parameters()]),
            torch.cat([x.view(-1) for x in self.model.decoder[6].parameters()]),
            torch.cat([x.view(-1) for x in self.model.pred[0].parameters()]),
        ])
        l1_regularization = self.l1 * torch.norm(regularization_params, 1)
        l2_regularization = self.l2 * torch.norm(regularization_params, 2)
        l1_l2_loss = l1_regularization + l2_regularization
        
        loss = rec_w*rec_loss + infer_w*infer_loss # + l1_l2_loss
        loss.backward()
        self.sm_optimizer.step()
        return latent , loss, rec_loss, infer_loss

    def train_st(self, data):
        self.model.train()
        self.st_optimizer.zero_grad()
        latent, predictions, rec_data = self.model(data)
        rec_loss = self.kl_rec_loss_func(data,rec_data).mean() - self.cosine_rec_loss_func(data,rec_data).mean()
        regularization_params = torch.cat([
            torch.cat([x.view(-1) for x in self.model.encoder[0].parameters()]),
            torch.cat([x.view(-1) for x in self.model.encoder[3].parameters()]),
            torch.cat([x.view(-1) for x in self.model.encoder[6].parameters()]),
            torch.cat([x.view(-1) for x in self.model.decoder[0].parameters()]),
            torch.cat([x.view(-1) for x in self.model.decoder[3].parameters()]),
            torch.cat([x.view(-1) for x in self.model.decoder[6].parameters()]),
            torch.cat([x.view(-1) for x in self.model.pred[0].parameters()]),
        ])
        l1_regularization = self.l1 * torch.norm(regularization_params, 1)
        l2_regularization = self.l2 * torch.norm(regularization_params, 2)
        l1_l2_loss = l1_regularization + l2_regularization
        loss = rec_loss # + l1_l2_loss
        loss.backward()
        self.st_optimizer.step()
        return latent , rec_loss
        
    def test_sm(self, data, labels, rec_w=0.5, infer_w=1):
        self.model.eval()
        latent, predictions, rec_data = self.model(data)
        rec_loss = rec_w*(self.kl_rec_loss_func(data,rec_data).mean() - self.cosine_rec_loss_func(data,rec_data).mean())
        infer_loss = infer_w*(self.kl_infer_loss_func(labels,predictions).mean() - self.cosine_infer_loss_func(labels,predictions).mean())
        loss = rec_loss + infer_loss
        return latent, loss, rec_loss, infer_loss
        
    def test_st(self, data):
        self.model.eval()
        latent, predictions, rec_data = self.model(data)
        rec_loss = self.kl_rec_loss_func(data,rec_data).mean() - self.cosine_rec_loss_func(data,rec_data).mean()
        return latent , rec_loss
    
    def train_model_by_step(
        self,
        max_steps=5000,
        save_mode='best',
        save_path=None,
        prefix=None,
        sm_step=4,
        st_step=1,
        test_step_gap=10,
        convergence=0.001,
        early_stop=True,
        early_stop_max=20,
        sm_lr=None,
        st_lr=None,
        rec_w=0.5, 
        infer_w=1,
    ):
        if len(self.history) > 0:
            best_ind = np.where(self.history['is_best'] == 'True')[0][-1]
            best_loss = self.history['sm_test_infer_loss'][best_ind]
            best_rec_loss = self.history['st_test_rec_loss'][best_ind]
        else:
            best_loss = np.inf
            best_rec_loss = np.inf
        early_stop_count = 0
        if sm_lr is not None:
            for g in self.sm_optimizer.param_groups:
                g['lr'] = sm_lr
        if st_lr is not None:
            for g in self.st_optimizer.param_groups:
                g['lr'] = st_lr

        pbar = tqdm(range(max_steps))
        mmd_loss = 0
        sm_trainr_iter = itertools.cycle(self.sm_train_sampler)
        st_iter = itertools.cycle(self.st_sampler)
        sm_shuffle_step = max(int(len(self.sm_train_ds)/(self.sm_train_batch_size*sm_step)),1)
        st_shuffle_step = max(int(len(self.st_ds)/(self.st_batch_size*st_step)),1)
        for step in pbar:
            if step % sm_shuffle_step == 0:
                sm_train_iter = itertools.cycle(self.sm_train_sampler)
            if step % st_shuffle_step == 0:
                st_iter = itertools.cycle(self.st_sampler)
            for i in range(st_step):
                exp = self.st_ds[next(st_iter)][0]
                st_latent, st_train_rec_loss = self.train_st(exp)
            for i in range(sm_step):
                exp, proportion = self.sm_train_ds[next(sm_train_iter)]
                sm_latent, sm_train_total_loss, sm_train_rec_loss, sm_train_infer_loss = self.train_sm(exp, proportion, rec_w=rec_w, infer_w=infer_w)
            # mmd_loss = compute_mmd(st_latent,sm_latent)*m_w

            if step % test_step_gap == 0:
                for ind in self.st_sampler:
                    exp = self.st_ds[ind][0]
                    st_latent, st_test_rec_loss = self.test_st(exp)
                for ind in self.sm_test_sampler:
                    exp, proportion = self.sm_test_ds[ind]
                    sm_latent, sm_test_total_loss, sm_test_rec_loss, sm_test_infer_loss = self.test_sm(exp,proportion, rec_w=rec_w, infer_w=infer_w)
                # mmd_loss = compute_mmd(st_latent,sm_latent)*m_w

                current_infer_loss = sm_test_infer_loss.item()

                best_flag='False'
                if best_loss - current_infer_loss > convergence:
                    if best_loss > current_infer_loss:
                        best_loss = current_infer_loss
                    best_flag='True'
                    # print('### Update best model')
                    early_stop_count = 0
                    old_best_path = self.best_path
                    if prefix is not None:
                        self.best_path = os.path.join(save_path,prefix+'_'+f'celleagle_weights_step{step}.h5')
                    else:
                        self.best_path = os.path.join(save_path,f'celleagle_weights_step{step}.h5')
                    if save_mode == 'best':
                        if old_best_path is not None:
                            if os.path.exists(old_best_path):
                                os.remove(old_best_path)
                        torch.save(self.model.state_dict(), self.best_path)
                else:
                    early_stop_count += 1
                    
                if save_mode == 'all':
                    if prefix != '':
                        self.best_path = os.path.join(save_path,prefix+'_'+f'celleagle_weights_step{step}.h5')
                    else:
                        self.best_path = os.path.join(save_path,f'celleagle_weights_step{step}.h5')
                    torch.save(self.model.state_dict(), self.best_path)
                    
                self.history = self.history.append({
                    'sm_train_rec_loss':sm_train_rec_loss.item(),
                    'sm_train_infer_loss':sm_train_infer_loss.item(),
                    'sm_train_total_loss':sm_train_total_loss.item(),
                    'sm_test_rec_loss':sm_test_rec_loss.item(),
                    'sm_test_infer_loss':sm_test_infer_loss.item(),
                    'sm_test_total_loss':sm_test_total_loss.item(),
                    'st_train_rec_loss':st_train_rec_loss.item(),
                    'st_test_rec_loss':st_test_rec_loss.item(),
                    'is_best':best_flag
                }, ignore_index=True)

                pbar.set_description(f"Step {step + 1}: test inf loss={sm_test_infer_loss.item():.3f}, train inf loss={sm_train_infer_loss.item():.3f}, test rec loss={sm_test_rec_loss.item():.3f}, train rec loss={sm_train_rec_loss.item():.3f}, st test rec loss={st_test_rec_loss.item():.3f}",refresh=True)
                
                if (early_stop_count > early_stop_max) and early_stop:
                    print('Stop trainning because of loss convergence')
                    break
            
    def train(
        self,
        max_steps=20000,
        save_mode='best',
        save_path=None,
        prefix=None,
        sm_step=4,
        st_step=1,
        test_step_gap=10,
        convergence=0.001,
        early_stop=True,
        early_stop_max=200,
        sm_lr=None,
        st_lr=None,
        batch_size=4096,
        rec_w=0.5, 
        infer_w=1,
        scvi_max_epochs=100,
        scvi_early_stopping=True,
        scvi_batch_size=4096,
    ):
        """Training Spoint model.
        
        Obtain latent feature from scVI then feed in Spoint model for training until loss convengence.

        Args:
            max_steps: The max step of training. The training process will be stop when achive max step.
            save_mode: A string determinates how the model is saved. It must be one of 'best' and 'all'.
            save_path: A string representing the path directory where the model is saved.
            prefix: A string added to the prefix of file name of saved model.
            convergence: The threshold of early stop.
            early_stop: If True, turn on early stop.
            early_stop_max: The max steps of loss difference less than convergence.
            sm_lr: Learning rate for simulated data.
            st_lr: Learning rate for spatial transcriptomic data.
            disc_lr: Learning rate of discriminator.
            batch_size: Batch size of the data be feeded in model once.
            rec_w: The weight of reconstruction loss.
            infer_w: The weig ht of inference loss.
            m_w: The weight of MMD loss.
            scvi_max_epochs: The max epoch of scVI.
            scvi_batch_size: The batch size of scVI.
        
        Returns:
            ``None``
        """
        if self.use_rep == 'scvi':
            self.get_scvi_latent(
                n_layers=self.scvi_layers,
                n_latent=self.scvi_latent,
                gene_likelihood=self.scvi_gene_likelihood,
                dispersion=self.scvi_dispersion,
                max_epochs=scvi_max_epochs,
                early_stopping=scvi_early_stopping,
                batch_size=scvi_batch_size,
            )
        elif self.use_rep == 'X':
            if issparse(self.sm_ad.X):
                self.sm_data = self.sm_ad.X.toarray()
            else:
                self.sm_data = self.sm_ad.X
            self.sm_labels = self.sm_ad.obsm['label'].values
            if issparse(self.st_ad.X):
                self.st_data = self.st_ad.X.toarray()
            else:
                self.st_data = self.st_ad.X            
        elif self.use_rep == 'pca':
            if issparse(self.sm_ad.X):
                self.sm_data = self.sm_ad.X.toarray()
            else:
                self.sm_data = self.sm_ad.X
            self.sm_labels = self.sm_ad.obsm['label'].values
            if issparse(self.st_ad.X):
                self.st_data = self.st_ad.X.toarray()
            else:
                self.st_data = self.st_ad.X
            
            pca_data = np.concatenate([self.st_data,self.sm_data],axis=0)
            pca = PCA(n_components=50)
            pca.fit(pca_data)
            pca_data = pca.transform(pca_data)
            self.st_data = pca_data[:self.st_data.shape[0],:]
            self.sm_data = pca_data[self.st_data.shape[0]:,:]

        self.build_dataset(batch_size, self.device)
        if save_path is None:
            save_path = 'Spoint_models_'+strftime("%Y%m%d%H%M%S",localtime())
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        self.train_model_by_step(
            max_steps=max_steps,
            save_mode=save_mode,
            save_path=save_path,
            prefix=prefix,
            sm_step=sm_step,
            st_step=st_step,
            test_step_gap=test_step_gap,
            convergence=convergence,
            early_stop=early_stop,
            early_stop_max=early_stop_max,
            sm_lr=sm_lr,
            st_lr=st_lr,
            rec_w=rec_w, 
            infer_w=infer_w,
        )
    
    def eval_model(self,model_path=None,use_best_model=True,batch_size=4096,metric='pcc'):
        if metric=='pcc':
            metric_name = 'PCC'
            func = metrics.pcc
        if metric=='spcc':
            metric_name = 'SPCC'
            func = metrics.spcc
        if metric=='mae':
            metric_name = 'MAE'
            func = metrics.mae
        if metric=='js':
            metric_name = 'JS'
            func = metrics.js
        if metric=='rmse':
            metric_name = 'RMSE'
            func = metrics.rmse
        if metric=='ssim':
            metric_name = 'SSIM'
            func = metrics.ssim
        
        if model_path is not None:
            self.model.load_state_dict(torch.load(model_path))
        elif use_best_model:
            self.model.load_state_dict(torch.load(self.best_path))
        model.eval()
        pre = []
        prop = []
        for exp_batch, prop_batch in self.sm_test_dataloader:
            latent_tmp, pre_tmp, _ = self.model(exp_batch)
            pre.extend(pre_tmp.cpu().detach().numpy())
            prop.extend(prop_batch.cpu().detach().numpy())
        pre = np.array(pre)
        prop = np.array(prop)
        metric_list = []
        for i,c in enumerate(self.clusters):
            metric_list.append(func(pre[:,i],prop[:,i]))
        print('### Evaluate model with simulation data')
        for i in range(len(metric_list)):
            print(f'{metric_name} of {self.clusters[i]}, {metric_list[i]}')
            
    def plot_training_history(self,save=None,return_fig=False,show=True,dpi=300):
        if len(self.history) > 0:
            fig, ax = plt.subplots()
            plt.plot(np.arange(len(self.history)), self.history['sm_test_infer_loss'], label='sm_test_infer_loss')
            plt.plot(np.arange(len(self.history)), self.history['st_test_rec_loss'], label='st_test_rec_loss')
            plt.xlabel('Epochs')
            plt.ylabel('Losses')
            plt.title('Training history')
            plt.legend()
            if save is not None:
                plt.savefig(save,bbox_inches='tight',dpi=dpi)
            if show:
                plt.show()
            plt.close()
            if return_fig:
                return fig
        else:
            print('History is empty, training model first')
            

    def deconv_spatial(self,st_data=None,min_prop=0.01,model_path=None,use_best_model=True,add_obs=True,add_uns=True):
        """Deconvolute spatial transcriptomic data.
        
        Using well-trained Spoint model to predict the cell type porportion of spots in spatial transcriptomic data.
        
        Args:
            st_data: An AnnData object of spatial transcriptomic data to be deconvolute.
            min_prop: A threshold value below which the predicted value will be set to 0. 
            model_path: A string representing the path of saved model file.
            use_best_model: If True, the model with the least loss will be used, otherwise, the last trained model will be used.
            add_obs: If True, the predicted results will be writen to the obs of input AnnData object of spatial transcriptomic data.
            add_uns: If True, the name of predicted cell types will be writen to the uns of input AnnData object of spatial transcriptomic data
        
        Returns:
            A ``DataFrame`` contained deconvoluted results. Each row representing a spot, and each column representing a cell type.
        """
        if st_data is None:
            st_data = self.st_data
        st_data = torch.tensor(st_data).to(self.device)
        if model_path is not None:
            self.model.load_state_dict(torch.load(model_path))
        elif use_best_model:
            self.model.load_state_dict(torch.load(self.best_path))
        self.model.to(self.device)
        self.model.eval()
        latent, pre, _ = self.model(st_data)
        pre = pre.cpu().detach().numpy()
        pre[pre < min_prop] = 0
        pre = pd.DataFrame(pre,columns=self.clusters,index=self.st_ad.obs_names)
        self.st_ad.obs[pre.columns] = pre.values
        self.st_ad.uns['celltypes'] = list(pre.columns)
        return pre