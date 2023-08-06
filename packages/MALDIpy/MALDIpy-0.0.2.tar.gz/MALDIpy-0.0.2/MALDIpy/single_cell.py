import scanpy as sc
import scanpy.external as sce
sc.settings.verbosity = 3
sc.settings.set_figure_params(dpi=100, facecolor='white',fontsize=12)

def maldifilter(adata_name, min_count=40000, min_gene=30):
    sc.pp.calculate_qc_metrics(adata_name, percent_top=None, log1p=False, inplace=True)
    sc.pp.filter_cells(adata_name, min_counts=min_count)
    sc.pp.filter_cells(adata_name, min_genes=min_gene)
    sc.pp.filter_genes(adata_name, min_cells=1)
    return adata_name

def maldi_norm(adata_name, regress_out_key='total_counts', regress_out_njob=4, scale_max_value=10, scale_zero_center=True, pca_svd_solver='arpack'):
    sc.pp.normalize_total(adata_name)
    sc.pp.regress_out(adata_name, [regress_out_key], n_jobs=regress_out_njob)
    sc.pp.scale(adata_name, max_value=scale_max_value, zero_center=scale_zero_center)
    sc.tl.pca(adata_name, svd_solver=pca_svd_solver)
    return adata_name

def maldi_clustering(adata_name, use_harmony=False, harmony_key='patient_id', harmony_theta=5,
                     n_neighbor=30, n_pc=30, umap_min_dist=0.5, umap_spread=1, leiden_res=1, leiden_key_added='leiden'):
    if use_harmony==True:
        sce.pp.harmony_integrate(adata_name, harmony_key, theta=harmony_theta)
        adata_name.obsm['X_pca'] = adata_name.obsm['X_pca_harmony']
    sc.pp.neighbors(adata_name, n_neighbors=n_neighbor, n_pcs=n_pc)
    sc.tl.umap(adata_name, min_dist=umap_min_dist, spread=umap_spread)
    sc.tl.leiden(adata_name, resolution=leiden_res, key_added=leiden_key_added)
    leiden_list=[]
    for i in adata_name.obs[leiden_key_added]:
        leiden_list.append(str(int(i)+1))
    adata_name.obs[leiden_key_added]=leiden_list
    return adata_name