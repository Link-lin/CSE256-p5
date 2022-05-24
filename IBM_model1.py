from io import TextIOWrapper
import pickle
import sys

def word_count(file:TextIOWrapper):
    counts = dict()
    for l in file:
        words = l.strip().split()
        words = ["_NULL_"] + words
        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
    return counts

def calculate_denom(t:dict, word_count:dict, en_words:list[str], es_words:list[str], i:int):
    res = 0.0
    es_word = es_words[i]
    for j in range(len(en_words)):
        #print(en_words[j])
        default = 1.0/word_count[en_words[j]]
        res += t.get((en_words[j], es_word), default) 
    return res;

def EM(en:TextIOWrapper, es:TextIOWrapper, word_count:dict, iter_count:int):
    t = {}
    for i in range(iter_count):
        c_ef, c_e = {}, {}
        for l_en, l_es in zip(en, es):
            # add NULL to the english line  
            en_words = l_en.strip().split()
            en_words = ["_NULL_"] + en_words
            es_words = l_es.strip().split()
            for i in range(len(es_words)):
                delta_denom = calculate_denom(t, word_count, en_words, es_words, i)
                for j in range(len(en_words)):
                    # calculate numerator of delta 
                    en_word = en_words[j]
                    es_word = es_words[i]
                    delta_numrt = t.get((en_word, es_word), 1.0/word_count[en_word])
                    # claculate delta
                    delta = float(delta_numrt)/delta_denom
                    # update c and c double
                    c_ef[(en_word, es_word)] =  c_ef.get((en_word, es_word), 0.0) + delta
                    c_e[en_word] = c_e.get(en_word, 0.0) + delta
    
        # update t according 
        for (en_v,es_v), c_e_s in c_ef.items():
            t[(en_v,es_v)] = float(c_e_s)/ c_e[en_v]

        en.seek(0)
        es.seek(0)
    return t

def output_alignment(t):
    en_dev = open("./dev.en")
    es_dev = open("./dev.es")

    output_file = open("./ibm_model1.out", "w")

    sentence_index = 1
    for l_en, l_es in zip(en_dev, es_dev):
        en_words = l_en.strip().split()
        en_words = ["_NULL_"] + en_words
        es_words = l_es.strip().split()
        line = arg_max(en_words, es_words, t)
        f_index = 1
        for en_index in line:
            output_file.write("%d %d %d\n" % (sentence_index, en_index, f_index))
            f_index += 1
        sentence_index += 1 
    

def arg_max(en_words, es_words, t):
    res = []
    for i in range(len(es_words)):
        max_en_index = 0
        max_s = 0
        for j in range(len(en_words)):
           s = t.get((en_words[j], es_words[i]), 0)
           if(s > max_s):
               max_en_index = j
               max_s = s
        res.append(max_en_index)
    return res 

def usage():
    sys.stderr.write("""
     python IBM_model1.py [iteration count]
        Read in the amount of iteration for EM algorithm and output the ordering.
     """)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    
    iter_count = 0;
    try:
      iter_count = int(sys.argv[1])
    except:
        sys.stderr.write("ERROR: cannot parse the iteration number into int.")
        sys.exit(1)

    # load english file to count word
    en_corpus = open("./corpus.en")
    es_corpus = open("./corpus.es")

    word_count = word_count(en_corpus)
    # print(word_count)

    en_corpus.seek(0)
    t = EM(en_corpus, es_corpus, word_count, iter_count)
    #print(t)
    # store t
    pickle.dump(t, open("./ibm_model1", "wb"))
    output_alignment(t)


