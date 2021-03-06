import os
import sys
import django
import json
import logging
import shutil
from django.core.management import call_command     # use call_command
from django.conf import settings                    # use settings.comfigure()
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer as LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer as LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import sys

#   Timeline module
#   It will 1)  extracted titles from input list
#           2)  classify headlines in date
#           3)  extract top-3 important headlines
#
#   Input: The POSTs list
#   Output: Headlines list
#   P.S: All intermediate files will be stored at ./RawData


# default language
LANGUAGE = "English"
# number of headlines
SENTENCES_COUNT  = 3
# File Not File error handling
error_to_catch = getattr(__builtins__,'FileNotFoundError', IOError)

Dir = "./TimeLine/RawData/"

def getSummarizedList(sqs):
    output = ""
    
    # Directory checking
    if not os.path.exists(Dir):
        os.makedirs(Dir)
        
    try:
        summary = open(Dir + "input.txt", "w", encoding = 'utf-8-sig')
        file = open(Dir + "headline_summary.txt", "w", encoding = 'utf-8-sig')
    except error_to_catch:
        print("!")

    date = ""
    # filtering data
    for i in sqs:
        title = i.title.rstrip()
        pub_date = dateReformat(i.pub_date)

        # Creating new date dataset
        if pub_date != date:
            if date != "":
                local_summary.close()
                sys.stdout = file
                #summarizer = LexRankSummarizer(Stemmer(LANGUAGE))  ＃ LexRankSummarizer not work if # of sentenses > ~25
                summarizer =LsaSummarizer(Stemmer(LANGUAGE))                
                summarizer.stop_words = get_stop_words(LANGUAGE)               
                headline = PlaintextParser.from_file(Dir + date + ".txt", Tokenizer(LANGUAGE))

                for sentence in summarizer(headline.document, SENTENCES_COUNT):
                    print(sentence)

            output = output + pub_date + "\n"
            date = pub_date
            local_summary = open(Dir + date + ".txt", "w", encoding = 'utf-8-sig')
        
        local_summary.write(title + ".\n")
        output = output + title + ".\n"

        #For last post summarization#
        if title == sqs.latest('pub_date').title.rstrip():
            local_summary.close()
            sys.stdout = file
            summarizer =LsaSummarizer(Stemmer(LANGUAGE))                
            summarizer.stop_words = get_stop_words(LANGUAGE)               
            headline = PlaintextParser.from_file(Dir + date + ".txt", Tokenizer(LANGUAGE))
            for sentence in summarizer(headline.document, SENTENCES_COUNT):
                print(sentence)
        #############################

    summary.write(output)
    file.close()
    summary.close()
    testing = readSummarizerResultToList("headline_summary.txt")
    
    return testing

def readSummarizerResultToList(filename):
    headlineSummary = open(Dir + filename, "r", encoding = 'utf-8-sig')
    headlinelist = headlineSummary.read().splitlines()
    headlineSummary.close()
    return headlinelist

def dateReformat(date):
    # Input: datetime class
    fDate = str(date.year) + "-" + str(date.month) + "-" + str(date.day)
    return fDate

#logging.basicConfig(level=logging.INFO)
#logging.info(getSummarizedList())
