def wikiclust(corpus,dist=1.5,save_directory='wiki_clusters.csv',plotting=False):

    import numpy as np 
    import pandas as pd
    import re
    import matplotlib.pyplot as plt 
    from mpl_toolkits.mplot3d import Axes3D

    #drop NaN entries from empty abstracts
    corpus = corpus.dropna().reset_index(drop=True)

    #converting string list to appropriate sparse matrix of occurence count
    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = CountVectorizer()
    abstracts = corpus['Abstract'].tolist()
    counts = vectorizer.fit_transform(abstracts)

    #converting counts matrix to tf-idf format
    from sklearn.feature_extraction.text import TfidfTransformer
    transformer = TfidfTransformer(smooth_idf=False)
    tf_idf = transformer.fit_transform(counts)

    #specific packages for hierarchical clustering 
    from sklearn.cluster import AgglomerativeClustering

    import scipy
    from scipy.cluster.hierarchy import dendrogram, linkage
    from scipy.cluster.hierarchy import fcluster
    from scipy.cluster.hierarchy import cophenet
    from scipy.spatial.distance import pdist

    X = tf_idf 

    #generating hierarchical cluters
    Hclustering = AgglomerativeClustering(n_clusters= None,affinity='euclidean',linkage='ward',distance_threshold=dist,compute_full_tree=True)
    Hclustering.fit(X.todense())
    labels = pd.DataFrame(Hclustering.labels_,columns=['Cluster'])
    n_clusters = int(labels.max()) + 1

    #combine titles with cluster labels to get results
    results = pd.concat([corpus['Title'],labels],axis=1)
    for i in range(n_clusters):
        group = pd.DataFrame(results['Title'][results['Cluster'] == i].tolist())
        if i == 0:
            Clusters = group
        else:
            Clusters = pd.concat([Clusters,group], ignore_index=True, axis=1)

    print("check")
    Clusters.to_csv(save_directory, index = False)

    #use Principal Component Analysis to reduce the dimensionality of X to two dimensions
    from sklearn.decomposition import PCA
    plotX = X


    #plotting
    if plotting:
        color_palette = np.array(['tab:blue','tab:orange','tab:green','tab:red','tab:purple'
                                    ,'tab:brown','tab:pink','tab:gray','tab:olive','tab:cyan'])
        color_theme=color_palette[:n_clusters]
        
        if len(corpus)>30:
            annotate_plot = False
        else:
            annotate_plot = True

        plot_dimensions = 3

        if plot_dimensions == 2:
            #2d dimension reduction
            pca_2d = PCA(n_components=2)
            PCs_2d = pd.DataFrame(pca_2d.fit_transform(plotX.todense()))
            PCs_2d.columns = ["PC1", "PC2"]

            #2d reduced plot
            fig, ax = plt.subplots()
            if n_clusters > 10:
                ax.scatter(PCs_2d['PC1'],PCs_2d['PC2'],c='tab:blue')
            else:          
                ax.scatter(PCs_2d['PC1'],PCs_2d['PC2'],c=color_theme[Hclustering.labels_])

            #annotations
            if annotate_plot == True:
                for i, txt in enumerate(corpus['Title']):
                    ax.annotate(txt, (PCs_2d['PC1'][i], PCs_2d['PC2'][i]))

        elif plot_dimensions ==3:
            #3d dimension reduction
            pca_3d = PCA(n_components=3)
            PCs_3d = pd.DataFrame(pca_3d.fit_transform(plotX.todense()))
            PCs_3d.columns = ["PC1", "PC2", "PC3"]

            #3d reduced plot
            fig = plt.figure()
            ax = Axes3D(fig)
            for i in range(len(PCs_3d)): #plot each point + it's index as text above
                if n_clusters>10:
                    ax.scatter(PCs_3d['PC1'][i],PCs_3d['PC2'][i],PCs_3d['PC3'][i],color='tab:blue') 
                else:
                    ax.scatter(PCs_3d['PC1'][i],PCs_3d['PC2'][i],PCs_3d['PC3'][i],color=color_theme[Hclustering.labels_[i]]) 
                if annotate_plot == True:
                    ax.text(PCs_3d['PC1'][i],PCs_3d['PC2'][i],PCs_3d['PC3'][i],  '%s' % (results['Title'][i]), size=5, zorder=1,  color='k') 
        plt.show()
