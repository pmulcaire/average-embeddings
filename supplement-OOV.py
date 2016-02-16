import io
import sys
import editdistance
import numpy as np
import IPython as ipy

"""
Creates embeddings for words by taking the average of known embeddings for words
close in edit distance.
"""

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
            ipy.embed()
        d[w1] = v
    print "Read embeddings"
    return d


def save_embs(filename, embs):
    with io.open(newfile, encoding='utf8', mode='w') as f:
        for w in embs:
            f.write(w + u' ' +  u' '.join([unicode(n) for n in embs[w]]) + '\n')


def read_vocab(filename):
    vocab = set()
    with io.open(filename, encoding='utf8') as f:
        for line in f:
            if u' ' in line:
                print "skipping multi-word line"
                continue
            vocab.add(line.strip())
    print "Read vocabulary"
    return vocab


def average_similar(vocab, embs, dist):
    print "Starting average of similar words"
    dim = len(embs.values()[0])
    added = 0
    for i,w1 in enumerate(vocab):
        similar = []
        if i%10==0:
            print "\rVocab word", i,
            sys.stdout.flush()
        if w1 in embs:
            continue
        for w2 in embs:
            if w1[:3] == w2[:3] and editdistance.eval(w1, w2) <= dist:
                #same language
                similar.append(w2)
        if len(similar) > 0:
            added += 1
            print "\r{}".format(added),
            sys.stdout.flush()
            v = np.zeros(dim)
            for w2 in similar:
                if len(v) != len(embs[w2]):
                    print "Mismatched dimensions"
                    ipy.embed()
                v += embs[w2]
            v /= len(similar)
            embs[w1] = v
    return embs


if __name__=="__main__":
    print "takes a (prefixed) vocab and a set of (prefixed) embeddings"
    embfile = sys.argv[1]
    vocabfile = sys.argv[2]
    newfile = sys.argv[3]
    embs = read_embs(embfile)
    vocab = read_vocab(vocabfile)
    #voc50 = [vocab.pop() for i in range(50)]
    #new_embs = average_similar(voc50, embs, 1)
    #ipy.embed()
    new_embs = average_similar(vocab, embs, 1)
    save_embs(newfile, new_embs)
    if len(new_embs) > len(embs) + 100:
        print "vocab size did not increase much"
        ipy.embed()
    print "Done"
