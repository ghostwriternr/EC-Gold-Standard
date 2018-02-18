import os
import json
from math import log

DIRECTORIES = ['./animalsJson', './plantsJson']

def split_sentences(data_json):
    all_sentences = ''
    for key in data_json:
        all_sentences += data_json[key].strip()
    sentence_list = all_sentences.split(".")
    for sentence in sentence_list:
        sentence = sentence.strip()
        sentence = sentence.replace('\n', '')
    return sentence_list

def getcooccurence(str1, str2, sentence_list, scores):
    for sentence in sentence_list:
        if str1 in sentence:
            scores['first'] += 1
        if str2 in sentence:
            scores['second'] += 1
        if str1 in sentence and str2 in sentence:
            scores['both'] += 1

def calculatepmi(scores, total_sentences):
    return log((scores['both']*total_sentences)/(scores['first']*scores['second']))

def getpmi(str1, str2):
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
                getcooccurence(str1, str2, sentence_list, scores)
    return calculatepmi(scores, total_sentences)

def main():
    print(getpmi('the', 'a'))

if __name__ == "__main__":
    main()
