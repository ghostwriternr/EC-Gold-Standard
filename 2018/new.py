import os
import json
import re
from math import log
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from itertools import zip_longest
import numpy as np

DIRECTORIES = [
    '/home/ghost_000/github/EC-Gold-Standard/data/wikiContent/animalsJson',
    '/home/ghost_000/github/EC-Gold-Standard/data/wikiContent/plantsJson'
]

def split_sentences(data_json):
    all_sentences = ''
    for key in data_json:
        all_sentences += data_json[key].strip()
    sentence_list = all_sentences.split(". ")
    for sentence in sentence_list:
        sentence = sentence.strip()
        sentence = sentence.replace('\n', '')
    return sentence_list

def getcooccurence(str1, str2, sentence_list, scores, filename):
    # if 'Dog.json' in filename or 'Cat.json' in filename:
    #     print(filename)
    #     print("*** before ***", scores)
    for sentence in sentence_list:
        if str1 in sentence:
            scores['first'] += 1
        if str2 in sentence:
            scores['second'] += 1
        if str1 in sentence and str2 in sentence:
            scores['both'] += 1
    # if 'Dog.json' in filename or 'Cat.json' in filename:
    #     print("+++ after +++", scores)

def calculatepmi(scores, total_sentences):
    # print("=== final ===", scores)
    try:
        pmi_score = log((scores['both']*total_sentences)/(scores['first']*scores['second']))
    except (ValueError, ZeroDivisionError):
        pmi_score = 0
    return pmi_score

def getpmi(str1, str2):
    # print("\nsentence1: " + str1 + "\nsentence2: " + str2)
    scores = {
        'both': 0,
        'first': 0,
        'second': 0
    }
    total_sentences = 0
    for directory in DIRECTORIES:
        for file in os.listdir(directory):
            if file.endswith(".json"):
                with open(os.path.join(directory, file)) as data_file:
                    data = json.load(data_file)
                sentence_list = split_sentences(data)
                total_sentences += len(sentence_list)
                getcooccurence(str1, str2, sentence_list, scores, file)
    return calculatepmi(scores, total_sentences)

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

class eav_sentence:
    e = ''
    a = ''
    v = ''
    vlist = []
    eav_obj = {}

    def __init__(self, e, a, v):
        self.e = e
        self.a = a
        self.v = v
        self.alist = a.split(' ')
        self.vlist = re.split(r', |\. |and|\.', v)
        self.vlist = list(filter(None, self.vlist))
        self.eav_obj = {
            'entity': self.e,
            'aspect': self.a,
            'value': self.vlist
        }

    def __repr__(self):
        return str(self.eav_obj)

    def __str__(self):
        return str(self.eav_obj)

def penn_to_wn(tag):
    if tag.startswith('N'):
        return 'n'

    if tag.startswith('V'):
        return 'v'

    if tag.startswith('J'):
        return 'a'

    if tag.startswith('R'):
        return 'r'

    return None

def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None

    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None

def sentence_similarity(sentence1, sentence2):
    # Tokenize and tag
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(word_tokenize(sentence2))

    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]

    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]

    score, count = 0.0, 0

    # For each word in the first sentence
    for synset in synsets1:
        # Get the similarity value of the most similar word in the other sentence
        similarities = [synset.path_similarity(ss) for ss in synsets2]
        similarities = [0.001 if x is None else x for x in similarities]
        try:
            best_score = max(similarities)
        except ValueError:
            best_score = 0.001

        # Check that the similarity could have been computed
        if best_score is not None:
            score += best_score
            count += 1

    # Average the values
    try:
        score /= count
    except ZeroDivisionError:
        score = 0.001
    return score

def symmetric_sentence_similarity(sentence1, sentence2):
    return (sentence_similarity(sentence1, sentence2) + sentence_similarity(sentence2, sentence1)) / 2

def wn_similarity(word1, word2):
    ss1 = wn.synsets(word1)[0]
    ss2 = wn.synsets(word2)[0]
    return wn.lch_similarity(ss1, ss2)

def val_similarity(list1, list2):
    maxx = 0
    avg = 0
    for s1 in list1:
        for s2 in list2:
            sim_score = symmetric_sentence_similarity(s1, s2)
            avg += sim_score
            if sim_score > maxx:
                maxx = sim_score
    avg = avg / (len(list1)*len(list2))
    return maxx, avg

def get_list_pmi(asp_list, val_list):
    avg_pmi = 0
    for aspect in asp_list:
        for val in val_list:
            avg_pmi += getpmi(aspect, val)
    avg_pmi = avg_pmi / (len(val_list)*len(asp_list))
    return(avg_pmi)

def parse_file(filename, num_lines=7):
    final_array = []
    result_array = []
    with open(filename, 'r') as infile:
        for lines in grouper(infile, num_lines, ''):
            sentence1 = eav_sentence(lines[0].strip(), lines[1].strip(), lines[2].strip())
            sentence2 = eav_sentence(lines[3].strip(), lines[4].strip(), lines[5].strip())
            print(sentence1)
            print(sentence2)
            aspect_similarity = symmetric_sentence_similarity(sentence1.a, sentence2.a)
            # print(aspect_similarity)
            max_sim, avg_sim = val_similarity(sentence1.vlist, sentence2.vlist)
            # print(max_sim)
            # print(avg_sim)
            avg_pmi1 = get_list_pmi(sentence1.alist, sentence1.vlist)
            # print(avg_pmi1)
            avg_pmi2 = get_list_pmi(sentence2.alist, sentence2.vlist)
            # print(avg_pmi2)
            pair_array = [aspect_similarity, max_sim, avg_sim, avg_pmi1, avg_pmi2]
            result_array.append(int(lines[6].strip()))
            print("pair_array", pair_array)
            # input()
            final_array.append(pair_array)
    return np.array(final_array), np.array(result_array)

def main():
    np_array, res_array = parse_file('testMod.txt')
    np.save("test_array", np_array)
    np.save("test_res_array", res_array)
    print(np_array)

if __name__ == "__main__":
    main()
