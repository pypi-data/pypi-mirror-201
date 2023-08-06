import pandas as pd
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline
import seaborn as sns
import scanpy as sc
import scanpy.external as sce
import matplotlib 
from matplotlib import rcParams
import matplotlib.font_manager
import matplotlib.font_manager as fm
import anndata
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import math
from scipy import ndimage
from scipy.spatial import distance_matrix
from matplotlib_venn import venn3, venn3_circles, venn2
import requests
sc.settings.verbosity = 3

class msi_data():
    
    def __init__(self,data,scale = '10um'):
        
        self.data = data
        self.loc = data.iloc[:,5:]
        self.mzs = data.mz.tolist()
        self.coords = self.loc.columns
        self.scale = scale

    def to_loc_mtx(self,df):
        df_loc = df.copy()
        df_loc.columns = pd.MultiIndex.from_tuples(df_loc.columns.str.split('_').map(tuple))
        df_loc = df_loc.stack()
        df_loc = df_loc.reset_index()
        df_loc.index = df_loc["level_1"]
        df_loc = df_loc.iloc[:,2:]
        df_loc.index = df_loc.index.str[1:].astype(int)
        df_loc.columns = df_loc.columns.str[1:].astype(int)
        df_loc = df_loc.sort_index(axis=0)
        df_loc = df_loc.sort_index(axis=1)
        
        return df_loc
        
    def plt(self,figsize = (6,5),dpi = 300, cmap = "magma_r",scale = 10, pos = 'lower left',
            remove_hs = True, q=0.999, smooth=True, mz='', smooth_size=2,
            save = '', scalebar=True, plttitle=''):
        fig = plt.figure(figsize = figsize,dpi = dpi)
        img_show = self.to_img_mtx(remove_hs=remove_hs,smooth=smooth,q=q,mz=mz,smooth_size=smooth_size)
        ax = sns.heatmap(img_show,
                         cmap=cmap,
                         mask=(img_show == 0.0))
        
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        ax.set_xticks([])
        ax.set_yticks([])
        

        sc = 500/scale
            
        if scalebar:
            scalebar = AnchoredSizeBar(ax.transData,
                                       sc, '500 µm', pos, 
                                       pad=0.5,
                                       sep=5,
                                       color='black',
                                       frameon=False,
                                       size_vertical=4,
                                       fontproperties=fm.FontProperties(size=12))


            ax.add_artist(scalebar)

        plt.ylabel('')
        plt.title(plttitle, fontsize = 14)
        plt.tight_layout()
        plt.show()
        if save:
            save_file = save + '.jpg'
            plt.savefig(save_file,dpi=500,bbox_inches='tight')
            
        
        
    def to_img_mtx(self,remove_hs = True,q=0.999,smooth=True,mz='',smooth_size=2):
        img_data = self.data.copy()
            
        loc_data = img_data.iloc[:,5:]
        loc_sum = pd.DataFrame(loc_data.sum()).T
        loc_sum = self.to_loc_mtx(loc_sum)
        
        if mz:
            img_data = img_data[img_data.mz==mz]
            img_data = img_data.iloc[:,5:]
            img_data = self.to_loc_mtx(img_data)
        else:
            img_data = loc_sum
            
        ## replace top 0.999 intensity pixel by 0.999 quantile value
        if remove_hs:
            #print("removing hot spot...")
            df_q = np.quantile(img_data.values.flatten(),q) 
            img_data[img_data>df_q] = df_q  #update pixel value
            
        ## median filter
        if smooth:
            #print("smoothing...")
            img_data = ndimage.filters.median_filter(img_data,size=smooth_size)
        return img_data
    
    def to_img_mtx_norm(self,remove_hs = True,q=0.999,smooth=True,mz='',smooth_size=2, norm_factor=1):
        img_data = self.data.copy()
            
        loc_data = img_data.iloc[:,5:]
        loc_sum = pd.DataFrame(loc_data.sum()).T
        loc_sum = self.to_loc_mtx(loc_sum)
        
        if mz:
            img_data = img_data[img_data.mz==mz]
            img_data = img_data.iloc[:,5:]
            img_data = self.to_loc_mtx(img_data)
        else:
            img_data = loc_sum
            
        ## replace top 0.999 intensity pixel by 0.999 quantile value
        if remove_hs:
            #print("removing hot spot...")
            df_q = np.quantile(img_data.values.flatten(),q) 
            img_data[img_data>df_q] = df_q  #update pixel value
            
        ## median filter
        if smooth:
            #print("smoothing...")
            img_data = ndimage.filters.median_filter(img_data,size=smooth_size)
        return img_data.mul(norm_factor)
    
    def to_adata(self, add_meta=False, csv_file=''):
        
        adata = anndata.AnnData(self.loc.T.values)
        adata.obs_names =  self.loc.columns 
        adata.var_names =  self.data.mz.astype(str)
        if add_meta==True:
            adata.var['mz_raw']=adata.var.index
            mz_dict={}
            for pair in list(zip(csv_file['mol_formula'],csv_file['mz'])):
                x=pair[0]
                y=pair[1]
                if y in mz_dict.keys():
                    if x != mz_dict[y]:
                        print(y,': One mz; multiple formula')
                else:
                    mz_dict[y]=x     
            formula_list=[]
            for i in adata.var.mz_raw:
                formula_list.append(mz_dict[float(i)])
            adata.var['mol_formula']=formula_list
            
            meta_dict={}
            for pair in list(zip(csv_file['adduct'],csv_file['mz'],csv_file['moleculeNames'],csv_file['moleculeIds'])):
                y=pair[1]
                x1=pair[0]
                x2=pair[2]
                x3=pair[3]
                if y in meta_dict.keys():
                    if [x1,x2[:-1][1:],x3[:-1][1:]] != meta_dict[y]:
                        print(y,': One mz; multiple matches')
                else:
                    meta_dict[y]=[x1,x2[:-1][1:],x3[:-1][1:]]
            meta_list=[]
            for i in adata.var.mz_raw:
                meta_list.append(meta_dict[float(i)][0])
            adata.var['adduct']=meta_list
            meta_list=[]
            for i in adata.var.mz_raw:
                meta_list.append(meta_dict[float(i)][1])
            adata.var['moleculeNames']=meta_list

            meta_list=[]
            for i in adata.var.mz_raw:
                meta_list.append(meta_dict[float(i)][2])
            adata.var['moleculeIds']=meta_list
        
        return adata