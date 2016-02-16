import os
import io
import sys
import numpy as np

def read_dict(filename):
    d = {}
    for line in io.open(filename, encoding='utf8'):
        w1, w2, p = line.split()
        if w1 in d:
            d[w1].append((w2,p))
        else:
            d[w1] = [(w2,p)]
    return d


def read_embs(filename):
    d = {}
    for line in io.open(filename, encoding='utf8'):
        ls = line.split()
        w1 = ls[0]
        if ls[1] == u':':
            del ls[1]
        v = np.array([float(n) for n in ls[1:]])
        if w1 in d:
            print w1, "is already in dictionary. replacing former embedding with new one"
        d[w1] = v
    return d


def check_dims(embeddings):
    dim = None
    for v in embeddings:
        if dim is None:
            dim = len(embeddings[v])
        else:
            if len(embeddings[v]) != dim:
                print "Mismatched dimensions"
                ipy.embed()
    return True


def save_embs(filename, embs):
    with io.open(filename, encoding='utf8', mode='w') as f:
        for w in embs:
            f.write(w + u' ' +  u' '.join([unicode(n) for n in embs[w]]) + u'\n')


def new_from_average(dictfile, embsfile, newfile):
    translations = read_dict(dictfile) #f->e
    embs = read_embs(embsfile)
    new_embs = {}
    dim = len(embs.values()[0])
    tot, miss = 0., 0.
    missed = []
    for w in translations:
        v = np.zeros(dim)
        c = 0.
        for tup in translations[w]:
            tr,p = tup
            p = np.float(p)
            tot += 1
            if tr in embs:
                v += p*embs[tr]
                c += p
            else:
                miss += 1
                missed.append((w,tr))
        if c > 0:
            new_embs[w] = v/c
    check_dims(new_embs)
    save_embs(newfile, new_embs)
    print "Average vocab coverage (% of translations present in embeddings): {}/{} ({}%)".format(tot-miss, tot, (tot-miss)/tot)
    #print missed


if __name__=="__main__":
    dict_filename = sys.argv[1] #should go foreign->english for ease of averaging
    embeddings_filename = sys.argv[2]
    new_filename = sys.argv[3]
    print "Dictionary: {}\t Embeddings: {}".format(dict_filename, embeddings_filename)
    new_from_average(dict_filename, embeddings_filename, new_filename)
