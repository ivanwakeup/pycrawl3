import spacy
from sense2vec import Sense2VecComponent

nlp = spacy.load('en')
s2v = Sense2VecComponent('/home/ivanwakeup/data/reddit_vectors-1.1.0')
nlp.add_pipe(s2v)


def get_similar_words(word):
    doc = nlp(u"{}".format(word))
    print(doc[0])
    assert doc[0].text == u"{}".format(word)
    freq = doc[0]._.s2v_freq
    vector = doc[0]._.s2v_vec
    most_similar = doc[0]._.s2v_most_similar(15)
    print(most_similar)