import spacy
from sense2vec import Sense2VecComponent
from pycrawl3.utils.logger import log

nlp = spacy.load('en')
s2v = Sense2VecComponent('/home/ivanwakeup/data/reddit_vectors-1.1.0')
nlp.add_pipe(s2v)


def get_similar_words(word):
    doc = nlp(u"{}".format(word))
    log.info("getting similar words for {}...".format(word))
    assert doc[0].text == u"{}".format(word)
    #freq = doc[0]._.s2v_freq
    #vector = doc[0]._.s2v_vec
    try:
        most_similar = doc[0]._.s2v_most_similar(15)
    except KeyError as e:
        log.error("couldn't find similar words for {}....using the input word itself.".format(word))
        return word

    res = []
    for similar in most_similar:
        res.append(similar[0][0])

    log.info("similar words for {} are {}...".format(word, res))
    return ",".join(res)


if __name__ == "__main__":
    import sys
    print(get_similar_words(sys.argv[1]))