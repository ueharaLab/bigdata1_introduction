import gensim
from gensim import corpora, models
from collections import defaultdict
import pandas as pd
import math

csv_input = pd.read_csv('tabelog_words.csv', encoding='ms932', sep=',',skiprows=0)
review_text_list=[]
#各文書の語彙集合を読み込んで文書行列（各文書の語彙リストを要素とするリスト）作成する
for words in csv_input['words']:
	if isinstance(words, float):
		review_text_list.append(['NA'])
	else:
		
		review_text_list.append(words.split(','))


#print(review_text_list)
# ------------------辞書生成---------------------------------------
#文書語彙の行列を渡すだけで、辞書が生成される（辞書は語彙のリスト形式）
#辞書はgensim Dictonaryクラスのオブジェクト
dictionary = gensim.corpora.Dictionary(review_text_list)

#no_below=2で二回以下しか出現したい単語は無視
#no_above=0.3で全部の文章の30パーセント以上に出現したワードは一般的すぎるワードとして無視
dictionary.filter_extremes(no_below=18, no_above=0.4)
dictionary.save_as_text('tabelog.dict')


corpus = [dictionary.doc2bow(review_morph) for review_morph in review_text_list]


gensim.corpora.MmCorpus.serialize('tabelog_corpus.mm', corpus)  



