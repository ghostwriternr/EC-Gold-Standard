import sys
import json
from gensim import corpora, models, similarities
from collections import defaultdict


def main(args):
    data1 = {}
    data2 = {}
    try:
        with open('data/wikiContent/animalsJson/' + args[0] + '.json') as jsonFile:
            data1 = json.load(jsonFile)
    except:
        pass
    try:
        with open('data/wikiContent/plantsJson/' + args[0] + '.json') as jsonFile:
            data1 = json.load(jsonFile)
    except:
        pass
    try:
        with open('data/wikiContent/animalsJson/' + args[1] + '.json') as jsonFile:
            data2 = json.load(jsonFile)
    except:
        pass
    try:
        with open('data/wikiContent/plantsJson/' + args[1] + '.json') as jsonFile:
            data2 = json.load(jsonFile)
    except:
        pass
    documents1 = []
    documents2 = []
    for key, value in data1.items():
        documents1.append(key)
    for key, value in data2.items():
        documents2.append(key)
    result = {}
    stoplist = set('for a of the and to in'.split())
    texts = [[word for word in document.lower().split()
              if word not in stoplist]
             for document in documents1]

    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=10)
    for doc in documents2:
        # print('\n' + doc)
        vec_bow = dictionary.doc2bow(doc.lower().split())
        vec_lsi = lsi[vec_bow]  # convert the query to LSI space

        # transform corpus to LSI space and index it
        index = similarities.MatrixSimilarity(lsi[corpus])
        sims = index[vec_lsi]
        temp = []
        for idx, val in enumerate(sims):
            if val > 0.5:
                # print(documents1[idx])
                temp.append(documents1[idx])
        if temp:
            result[doc] = temp
    paraJson = {}
    paraJson['Pairs'] = []
    for key, value in result.items():
        for secondSec in value:
            temp = {}
            temp['first'] = {}
            temp['first']['title'] = key
            temp['first']['content'] = data2[key]
            temp['second'] = {}
            temp['second']['title'] = secondSec
            temp['second']['content'] = data1[secondSec]
            paraJson['Pairs'].append(temp)

    print(json.dumps(paraJson))

if __name__ == '__main__':
    main(sys.argv[1:])
