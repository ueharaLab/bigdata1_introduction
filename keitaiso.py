

from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
import re
import mojimoji


def tokenizer(sentence):

	surfaceList=[]
	partList=[]

	t = Tokenizer()
	for token in t.tokenize(sentence):
	
		surfaceList.append(token.surface)
		partList.append(token.part_of_speech.split(',')[0])
	
	return surfaceList,partList
		
def tokenizer_base(sentence):

	strBaseForm=''
	t = Tokenizer()
	word_vector = []
	for token in t.tokenize(sentence):
#		if (token.part_of_speech.split(',')[0] =='名詞') or (token.part_of_speech.split(',')[0] =='動詞') or (token.part_of_speech.split(',')[0] =='形容詞'):
		if token.part_of_speech.split(',')[0] =='名詞':
			word_vector += [token.base_form]
#		strBaseForm = strBaseForm + ',' + token.base_form
	
	return word_vector

	

	
	
	
def tokenizer_customDic(sentence):
	
	
	
	word_vector = ''
	#tokenizerメソッドの初期化（コンストラクタ）にユーザー辞書を指定することができる
	#ユーザー辞書は、.csvのままでもよいし、コンパイル済の辞書でもよい
	#csvを使う場合は、拡張子を付けること。
	#t=Tokenizer("User_Dict1")
	#t=Tokenizer("User_Dict1.csv", udic_enc="CP932")
	t=Tokenizer()
	filter_char=[]
	filter_token=[CompoundNounFilter(),POSKeepFilter(['名詞'])]

	#上のでインスタンス生成
	a=Analyzer(filter_char,t,filter_token)
	for token in a.analyze(sentence):
#		print(token)   #この段階ではまだnanは無し
	
		
		#複合って入ってたら
		if token.part_of_speech.split(',')[1] in ['複合']:
			t=0
			complex_surface=''
			for token2 in Analyzer().analyze(token.surface):
				
				if  '（' or '）' in token2.surface:
					break
				
				else:
					complex_surface+=token2.surface
				t+=1
					
			if t<3 and complex_surface!='':
				word_vector += complex_surface + ','
			#print(word_vector)
        
		#複合名詞以外だったら
		else:
			num = re.compile("([0-9]+)")
			kana = re.compile('([｡ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊｲﾌﾍﾎﾏﾐﾑﾒﾓﾗﾘﾙﾚﾛﾔﾕﾖﾜﾝﾟ]+)')
			#ABCs = re.compile("[A-Z]")
			#ここの仕組みはどうなっているのか。ラカントSが消えた。最初の部分で米粉がはじかれてしまった。
			
			isNum = num.search(token.surface)
			isKana = kana.search(token.surface)
			#isABCs = ABCs.search(token.surface)
			if 'ホットケーキ' in token.surface:   #表層形がホットケーキだったら何もしない。
				continue
			#elif isNum != None or isABCs != None:   #isNumがない場合、またはisKanaがない場合は何もしない。
			#	continue
			elif isKana != None :
				word_zenkaku=mojimoji.han_to_zen(token.surface)
				unique_word=thesaurus_dict.get(word_zenkaku)
				#print(unique_word)
				if unique_word != None:
					word_vector += str(unique_word)+ ','
				else:
					word_vector += word_zenkaku+ ','
				#print(word_vector)
			else:
				unique_word=thesaurus_dict.get(token.surface)
				print(type(unique_word))
				if type(unique_word) == float:
					continue
					
				elif unique_word != None:
					word_vector += str(unique_word)+ ','
				
				else:
					word_vector += token.surface+ ','
				#print(word_vector)
				
	print(word_vector)
	return word_vector[:-1]

def word2yomi(word):

	t = Tokenizer()
	yomi=''
	for token in t.tokenize(word):
	
		if token.reading =='*':
			yomi+=token.surface
		else:
			yomi+=token.reading
	
	return yomi


def wordAnalysis2(sentence):
#	print(sentence)
	surface=''
	
	t = Tokenizer()
	for token in t.tokenize(sentence):
		if token.reading!='*':
			surface=surface+token.surface
		
	return surface
	
if __name__ == '__main__':

	import pandas as pd
	import codecs
	csv_input = pd.read_csv('cookpad_recipe_ingredient.csv', encoding='ms932', sep=',',skiprows=0)
	reciepe_words_df = pd.DataFrame([],columns=['label','text','words'])
		
	csv_input2 = pd.read_csv('thesaurus.csv', encoding='ms932', sep=',',skiprows=0)	
	thesaurus_dict={}
	for key,val in zip(csv_input2['key'],csv_input2['value']):
	
		thesaurus_dict[key] = val
	
	
	
	for label, text in zip(csv_input['label'].values.tolist(),csv_input['ingredient'].values.tolist()):
#		print(text)
		word_vector=tokenizer_customDic(str(text))
		#word_vecorからnanを抜いておいたほうがいいかもしれない。（形態素分解済みのtextにnonが混じっていることがあった。）
#		if word_vector!='':			
			
		df = pd.DataFrame([[label,text,word_vector]], columns=['label','text','words'])
		reciepe_words_df = reciepe_words_df.append(df)
#dfのwordsのみ取り出した。この後これをlist化し、nanをなくしてもう一度dfに戻したい。
#		reciepe_words_list = reciepe_words_df.loc[:,['words']].values.tolist()
#	print(reciepe_words_list)

#	print(reciepe_words_list)
	with codecs.open("cookpad_recipe_words.csv", "w", "ms932", "ignore") as cookpad_file:	
		#header=Trueで、見出しを書き出す
		reciepe_words_df.to_csv(cookpad_file, index=False, encoding="ms932", mode='w', header=True)
		