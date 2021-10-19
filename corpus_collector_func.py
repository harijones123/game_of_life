def corpus_collect(seed_url,Nbranches,random_branch_url_selection=True,save_corpus_csv=True):
    import pandas as pd
    import requests
    import urllib.request
    import time
    from bs4 import BeautifulSoup
    import io
    import random

    #seed_url = 'https://en.wikipedia.org/wiki/Barack_Obama'

    response = requests.get(seed_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    body = soup.find("div", {"class": "mw-parser-output"})
    import re

    hlinks = body.find_all("a", href=re.compile("/wiki/"))

    #create list of all url links on article, condense to unique values
    branch_urls = []
    for link in hlinks:
        if link.get('href').startswith('/wiki/'):
            branch_urls.append('https://en.wikipedia.org' + link.get('href'))

    from collections import OrderedDict
    branch_urls = list(OrderedDict.fromkeys(branch_urls))


    if random_branch_url_selection == True:
        random.shuffle(branch_urls)

    print(str(len(branch_urls))+' branch links from this page')

    #find title and abstract for each branched article
    import wiki_abstract_collector as wac 
    abstracts = []
    titles = []
    i=0
    for url in list(branch_urls)[0:Nbranches]:
        [abs,tit] = wac.abstract(url)
        abstracts.append(abs)
        if abs is None:
            tit = None 
        titles.append(tit)
        i=i+1
        print(str(i) + '/' + str(Nbranches) + ' branches completed')

    #remove none values from weird articles
    nones = [i for i in range(len(abstracts)) if abstracts[i] == ''] 

    for i in range(len(nones)):
        del abstracts[nones[i]]
        del titles[nones[i]]

    #write corpus to dataframe
    corpus = pd.DataFrame(
        {'Title': titles,
        'Abstract': abstracts,
        })
    print(corpus)
    #output the corpus dataframe, and save it as csv 
    if save_corpus_csv == True:
        corpus.to_csv('corpus.csv',index=False)
    return corpus
