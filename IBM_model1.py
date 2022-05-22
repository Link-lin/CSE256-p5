from io import TextIOWrapper
import pickle



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

def EM(en:TextIOWrapper, es:TextIOWrapper, word_count:dict):
    t = {}
    for i in range(5):
        print("itr:" + str(i))
        c2, c1 = {}, {}
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
                    c2[(en_word, es_word)] =  c2.get((en_word, es_word), 0.0) + delta
                    c1[en_word] = c1.get(en_word, 0.0) + delta
    
        # update t according 
        for (en_v,es_v), c_e_s in c2.items():
            t[(en_v,es_v)] = float(c_e_s)/ c1[en_v]

        en.seek(0)
        es.seek(0)
    return t

def output_alignment(t):
    en_dev = open("./dev.en")
    es_dev = open("./dev.es")

    output_file = open("./ibm_model1.out", "w")

    l_number = 1
    for l_en, l_es in zip(en_dev, es_dev):
        en_words = l_en.strip().split()
        en_words = ["_NULL_"] + en_words
        es_words = l_es.strip().split()
        line = find_best_match(en_words, es_words, t)
        c = 1
        for j in line:
            output_file.write("%d %d %d\n" % (l_number, j, c))
            c += 1
        l_number += 1 
    

def find_best_match(en_words, es_words, t):
    res = []
    for i in range(len(es_words)):
        max_j = 0
        max_s = 0
        for j in range(len(en_words)):
           s = t.get((en_words[j], es_words[i]), 0)
           if(s > max_s):
               max_j = j
               max_s = s
        res.append(max_j)
    return res 




if __name__ == "__main__":
    # load english file to count word
    en_corpus = open("./corpus.en")
    es_corpus = open("./corpus.es")

    word_count = word_count(en_corpus)
    # print(word_count)

    en_corpus.seek(0)
    t = EM(en_corpus, es_corpus, word_count)
    #print(t)
    # store t
    pickle.dump(t, open("./ibm_model1", "wb"))
    output_alignment(t)


