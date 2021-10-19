#user parameters for scraping
seed_url = 'https://en.wikipedia.org/wiki/London'  #url of wikipedia page used to generate the corpus     

Nbranches = 50                                  #number of branch links to read. 
                                                #These are the most time consuming aspect of the code, selecting over 200 will take considerable time (~5-10 mins)   

random_branches = False                         #if left "False", branch links will be read in the order they appear on the page. If "True", they will be randomly selected
                                                #random branch selection leads to more interesting results but less tidy clusters.

use_default_corpus = False                      #scraping for new branch pages can be time consuming, and so a default corpus can be used by setting this to True.
                                                #can be useful for tesing clustering parameters. 

#user parameters for clustering
cluster_distance = 1.5                              #euclidean distance as minimum distance to seperate clusters, reccommended=1.5
                                                    #larger distance -> fewer clusters, and vice versa

plotting = True                                     #plots 3d distribution of clusters, cannot show colours for more than 10 clusters


#obtaining the corpus: a dataframe of titles and corresponding abstracts from wikipedia entries.
if use_default_corpus:
    import pandas as pd
    corpus = pd.read_csv('corpus_default.csv')
else:
    import corpus_collector_func
    corpus = corpus_collector_func.corpus_collect(seed_url,Nbranches,random_branch_url_selection=random_branches,save_corpus_csv=True)

#cluster the corpus, saves a .csv file as the output. 
import wiki_clustering_func
wiki_clustering_func.wikiclust(corpus,dist=cluster_distance,save_directory='wiki_clusters.csv',plotting=True)