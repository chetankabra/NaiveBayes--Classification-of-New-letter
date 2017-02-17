# Name : Chetan R Kabra
# Student Id : 10011525872

from __future__ import division
import os
from os import listdir
from nltk.stem.wordnet import WordNetLemmatizer
import math
import codecs
testing_set_labels = []
predicted_set_labels =[]
words_list =[]
words_dict ={}
unique_words = {}
from nltk.stem.porter import *
import re

def remove_stop_words(tokens):
    stop_words = ['a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can','cannot','could','dear','did','do','does','either','else','ever','every','for','from','get','got','had','has','have','he','her','hers','him','his','how','however','i','if','in','into','is','it','its','just','least','let','like','likely','may','me','might','most','must','my','neither','no','nor','not','of','off','often','on','only','or','other','our','own','rather','said','say','says','she','should','since','so','some','than','that','the','their','them','then','there','these','they','this','tis','to','too','twas','us','wants','was','we','were','what','when','where','which','while','who','whom','why','will','with','would','yet','you','your'];
    new_word =[]
    for words in tokens:
        if words.startswith('<') and words.endswith('>'):
            break;
        words = re.sub('[^A-Za-z]+', '', words)
        if (len(words) ==0 or len(words) ==1):
            break;
        #lmtzr = WordNetLemmatizer()
        #words = lmtzr.lemmatize(words.lower())
        words = words.encode("ISO-8859-1")
        if words.lower() not in stop_words:
            stemmer = PorterStemmer()
            words = stemmer.stem(words.lower())
            words_list.append(words.lower());

def count_words_class(list_of_words,class_name):
    new_words_dict = {}
    total_count = 0
    for words in list_of_words:
        total_count = total_count +1;
        if words in new_words_dict:
            new_words_dict[words] +=1
        else:
            new_words_dict[words] =1
    print (class_name,total_count)
    words_dict[class_name] = {}
    for words in new_words_dict:
        words_dict[class_name][words] = (new_words_dict[words]+1)
    words_dict[class_name]['total_words_class'] = total_count

def count_words_probablity(list_of_words,class_name):
    new_words_dict = {}
    total_count = 0
    for words in list_of_words:
        total_count = total_count + 1;
        if words in new_words_dict:
            new_words_dict[words] += 1
        else:
            new_words_dict[words] = 1
    list_of_all_prob = {}
    for keys in words_dict:
        probabilty_word_class = 0;
        for words in list_of_words:
            if not (words_dict[keys].get(words,"null") == "null"):
                #print (keys,words, words_dict[keys].get(words,0.5))
                #working rule
                probabilty_word_class += math.log((words_dict[keys].get(words) + 1) / (words_dict[keys]['total_words_class'] + len(unique_words)))
                #probabilty_word_class += (words_dict[keys].get(words) * (new_words_dict[words]/total_count))/ 0.05
            else:
                probabilty_word_class += math.log( 1 / (words_dict[keys]['total_words_class'] + len(unique_words)))
                #probabilty_word_class +=0
        final_probability = probabilty_word_class * 0.05
        #final_probability = probabilty_word_class
        list_of_all_prob[keys]= final_probability;
    #print list_of_all_prob
    for keys,value in list_of_all_prob.iteritems():
        if max(list_of_all_prob.values()) ==value:
            testing_set_labels.append(class_name)
            predicted_set_labels.append(keys)
            break

def find_accuracy ():
    right_prediction =0;
    false_prediction =0;
    total_lables = len(testing_set_labels);
    #print total_lables
    for i in xrange(0,total_lables):
        if (testing_set_labels[i] == predicted_set_labels[i]):
            right_prediction += 1
        else:
            false_prediction += 1
    print right_prediction
    print false_prediction
    print ("Accuracy",right_prediction / (right_prediction+false_prediction) * 100)

def unique_words_vocab (list_words):
     for words in list_words:
         unique_words[words] =1

if __name__ =="__main__":
    training_set = "20_newsgroups/20_newsgroups/"
    #training_set = "20_newsgroups/Testing_data/"
    #training_set = "HW1T/train"
    for dir in os.listdir(training_set):
       class_name = dir
       print dir
       for files in os.listdir(training_set+"/"+dir):
           content_file = codecs.open(training_set+"/"+dir+"/"+files,"r","ISO-8859-1")
           content_file.next();
           content_file.next();
           #for lines in content_file:
            #   content_lines = lines.strip();
             #  if content_lines.startswith("Newsgroups:"):
              #    break;
           for lines in content_file:
               if not (lines == "\n"):
                   content_lines = lines.strip();
                   token = content_lines.split()
                   remove_stop_words(token)
       count_words_class(words_list,class_name)
       unique_words_vocab(words_list)
       words_list =[]
       #if (class_name == "comp.graphics"):
        #   break
    testing_set = "20_newsgroups/Testing_data/"
    #testing_set = "20_newsgroups/20_newsgroups/"

    #testing_set = "HW1T/test"
    for dir in os.listdir(testing_set):
        class_name = dir
        print dir
        for files in os.listdir(testing_set + "/" + dir):
            content_file = codecs.open(testing_set + "/" + dir + "/" + files, "r", "ISO-8859-1")
            # ignore first line of the file  contains group name
            content_file.next();
            content_file.next();
            #for lines in content_file:
                #content_lines = lines.strip();
                #if content_lines.startswith("Newsgroups:"):
                   #print content_lines
                   #break;
            for lines in content_file:
                if not (lines == "\n"):
                    content_lines = lines.strip();
                    token = content_lines.split()
                    remove_stop_words(token)
            count_words_probablity(words_list, class_name)
            words_list = []
    find_accuracy()
        #if dir == "alt.atheism":
         # break;


