#returns a string containing the abstract of a wikipedia entry, from the url of the wikipedia pag
def abstract(url):
    import requests
    import urllib.request
    import time
    from bs4 import BeautifulSoup

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #select article body, use find all for indexing
    body = soup.find("div", {"class": "mw-parser-output"})
    if body is None:
        return [None, None]
    tags = body.find_all()

    #select first occurance of h2 as end of abstract, use to split body up to that point
    pend = body.find('h2')
    if pend is None:
        return [None, None]
    tags = tags[:tags.index(pend)]
    #count number of paragraphs in abstract
    paras = 0
    for tag in tags:
        if "<p>" in str(tag):
            paras += 1

    #create string of abstract
    abstract = ''
    for p in body.find_all('p',{'class': None})[:paras]:
        abstract = abstract + p.text

    title = soup.find('h1').text

    return [abstract, title]

