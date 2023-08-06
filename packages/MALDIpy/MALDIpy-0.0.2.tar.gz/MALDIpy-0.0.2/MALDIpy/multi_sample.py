import pandas as pd
import scanpy as sc
import scanpy.external as sce
sc.settings.verbosity = 3
sc.settings.set_figure_params(dpi=100, facecolor='white',fontsize=12)
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager
import matplotlib.font_manager as fm
import numpy as np
from matplotlib_venn import venn3, venn3_circles, venn2
import anndata

def plot3tissues(df1,df2,df3,title='',cmap = "magma_r"):

    fig, (ax1, ax2, ax3, axcb) = plt.subplots(1, 4, figsize = (15,5),dpi = 100,gridspec_kw={'width_ratios':[1,1,1, 0.05]})
    max_num= max(df1.max().max(),df2.max().max(),df3.max().max())######key change

    g1 = sns.heatmap(df1, vmax=max_num,
                    mask=(df1==0),cmap=cmap,
                    ax=ax1,cbar=False)
    g1.set_ylabel('')
    g1.set_xlabel('')
    g1.set_xticks([])
    g1.set_yticks([])

    g2 = sns.heatmap(df2,vmax=max_num,
                     mask=(df2==0),cmap=cmap,
                     ax=ax2,cbar=False)
    g2.set_ylabel('')
    g2.set_xlabel('')
    g2.set_xticks([])
    g2.set_yticks([])

    g3 = sns.heatmap(df3,vmax=max_num,
                     mask=(df3==0),cmap=cmap,
                     cbar_kws={"shrink": 0.5},
                     ax=ax3,cbar_ax=axcb)
    g3.set_ylabel('')
    g3.set_xlabel('')
    g3.set_xticks([])
    g3.set_yticks([])

    plt.suptitle(title, fontsize = 14)
    scalebar1 = AnchoredSizeBar(ax1.transData,30, '300 µm', 'lower right',frameon=False,size_vertical=2,sep=5,
                               fontproperties=fm.FontProperties(size=10))
    scalebar2 = AnchoredSizeBar(ax2.transData, 30, '300 µm', 'lower right',frameon=False,size_vertical=2,sep=5,
                               fontproperties=fm.FontProperties(size=10))
    scalebar3 = AnchoredSizeBar(ax3.transData, 30, '300 µm', 'lower right',frameon=False,size_vertical=2,sep=5,
                               fontproperties=fm.FontProperties(size=10))
    ax1.add_artist(scalebar1);ax2.add_artist(scalebar2);ax3.add_artist(scalebar3)

    plt.show()
    
def maldi_concat(raw_file1,raw_file2,raw_file3, suffix1='data1',suffix2='data2',suffix3='data3'):
    df1 = raw_file1.set_index('mz').iloc[:,4:]
    df1 = df1.add_suffix("_"+suffix1)
    #print(df1.shape)
    df2 = raw_file2.set_index('mz').iloc[:,4:]
    df2 = df2.add_suffix("_"+suffix2)
    #print(df2.shape)
    df3 = raw_file3.set_index('mz').iloc[:,4:]
    df3 = df3.add_suffix("_"+suffix3)
    #print(df3.shape)
    combined_df = pd.concat([df1,df2,df3],axis=1,join="outer")
    combined_df = combined_df.fillna(0)
    #print(combined_df.shape)
    adata = anndata.AnnData(combined_df.T.values)
    adata.obs_names =  combined_df.columns 
    adata.var_names =  combined_df.index.astype(str)
    data_id=[]
    for i in adata.obs.index:
        if suffix1 in i:
            data_id.append(suffix1)
        elif suffix2 in i:
            data_id.append(suffix2)
        elif suffix3 in i:
            data_id.append(suffix3)
    adata.obs['data_id']=data_id
    return adata