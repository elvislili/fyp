from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import sys, os
parent_path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(os.path.join(parent_path, 'mysite'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
from django.conf import settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from news.models import Post
from newspaper import Article
import newspaper

from textteaser import TextTeaser
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.sum_basic import SumBasicSummarizer as SumBasicSummarizer
from sumy.summarizers.lsa import LsaSummarizer as LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer as TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer as LexRankSummarizer

from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

#   Here is the script of grabbing single news articles from website
#   and push it to our database automatically
#   1) Copy the url from target news article
#   2) Paste to variable url
#   3) Run the script (e.g.: python3 script_for_single_news.py)
#   4) The results will be stored at "Dir": ./dummy/

LANGUAGE = "English"
SENTENCES_COUNT = 10
number = 0
Dir = "./dummy/"


# Directory checking
if not os.path.exists(Dir):
    os.makedirs(Dir)
    
'''for single news'''
url = 'http://edition.cnn.com/2017/01/26/politics/top-state-department-officials-asked-to-leave-by-trump-administration/index.html'
article = Article(url)
article.download()
article.parse()
article.nlp()

category = "politics"
pub_date = article.publish_date
location = "US"
title = article.title
                                                
content = article.text
photo = article.top_image
link = article.url

getText = open(Dir + "input_article.txt", "w", encoding = 'utf-8-sig')
sys.stdout = getText
print(article.title)
print(article.text)
getText.close()

parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))

stemmer = Stemmer(LANGUAGE)

summarizer = LexRankSummarizer(stemmer)
summarizer.stop_words = get_stop_words(LANGUAGE)

#five-line summary
summary = open(Dir + "five_line_summary.txt", "w", encoding = 'utf-8-sig')
sys.stdout = summary
for sentence in summarizer(parser.document, SENTENCES_COUNT - 5):
    print(sentence)
summary.close()

#ten-line summary
summary = open(Dir + "ten_line_summary.txt", "w", encoding = 'utf-8-sig')
sys.stdout = summary 
for sentence in summarizer(parser.document, SENTENCES_COUNT):
    print(sentence)
    print("")
summary.close()

#sumbasic
summarizer =SumBasicSummarizer(stemmer)
summarizer.stop_words = get_stop_words(LANGUAGE)
summary = open(Dir + "sumbasic.txt", "w", encoding = 'utf-8-sig')
sys.stdout = summary 
for sentence in summarizer(parser.document, SENTENCES_COUNT):
    print(sentence)
    print("")
summary.close()

#LSA
summarizer =LsaSummarizer(stemmer)
summarizer.stop_words = get_stop_words(LANGUAGE)
summary = open(Dir + "LSA.txt", "w", encoding = 'utf-8-sig')
sys.stdout = summary 
for sentence in summarizer(parser.document, SENTENCES_COUNT):
    print(sentence)
    print("")
summary.close()

#textrank
summarizer =TextRankSummarizer(stemmer)
summarizer.stop_words = get_stop_words(LANGUAGE)
summary = open(Dir + "textrank.txt", "w", encoding = 'utf-8-sig')
sys.stdout = summary 
for sentence in summarizer(parser.document, SENTENCES_COUNT):
    print(sentence)
    print("")
summary.close()

#lexrank
summarizer =LexRankSummarizer(stemmer)
summarizer.stop_words = get_stop_words(LANGUAGE)
summary = open(Dir + "lexrank.txt", "w", encoding = 'utf-8-sig')
sys.stdout = summary 
for sentence in summarizer(parser.document, SENTENCES_COUNT):
    print(sentence)
    print("")
summary.close()

#featured-lexrank
with open(Dir + 'input_article.txt', 'r', encoding = 'utf-8-sig') as f:
    first_line = f.readline()
title = first_line
with open(Dir + 'input_article.txt', 'r', encoding = 'utf-8-sig') as f:
    text = f.read()
tt = TextTeaser()

sentences = tt.summarize(title, text)
file = open(Dir + "tt.txt", "w", encoding = 'utf-8-sig')
for sentence in sentences:
    file.write("%s\n" % sentence)
file.close()

parser = PlaintextParser.from_file(Dir + "tt.txt", Tokenizer(LANGUAGE))
summarizer =LexRankSummarizer(stemmer)
summarizer.stop_words = get_stop_words(LANGUAGE)
summary = open(Dir + "featured-lexrank.txt", "w", encoding = 'utf-8-sig')
sys.stdout = summary 
for sentence in summarizer(parser.document, SENTENCES_COUNT):
    print(sentence)
    print("")
summary.close()

with open(Dir + 'five_line_summary.txt', encoding = 'utf8') as f:
    fivelinesummary = f.readlines()

with open(Dir + 'ten_line_summary.txt', encoding = 'utf8') as f:
    tenlinesummary  = f.readlines()

with open(Dir + 'sumbasic.txt', encoding = 'utf8') as f:
    sum_basic = f.readlines()

with open(Dir + 'LSA.txt', encoding = 'utf8') as f:
    LSA  = f.readlines()

with open(Dir + 'textrank.txt', encoding = 'utf8') as f:
    textrank  = f.readlines()

with open(Dir + 'lexrank.txt', encoding = 'utf8') as f:
    lexrank  = f.readlines()

with open(Dir + 'featured-lexrank.txt', encoding = 'utf8') as f:
    featured_lexrank  = f.readlines()


fivelinesummary=''.join(fivelinesummary)
tenlinesummary=''.join(tenlinesummary)
sum_basic=''.join(sum_basic)
LSA=''.join(LSA)
textrank=''.join(textrank)
lexrank=''.join(lexrank)
featured_lexrank=''.join(featured_lexrank)

#post=Post(category=category, pub_date=pub_date, location=location, title=title,content=content, photo=photo,link=link, fivelinesummary=fivelinesummary, tenlinesummary=tenlinesummary, sum_basic=sum_basic, LSA=LSA, textrank=textrank, lexrank=lexrank, featured_lexrank=featured_lexrank)
#post.save()
