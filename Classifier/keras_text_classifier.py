import numpy as npy
import keras
from  keras.models import Sequential,load_model
from keras.layers import Dense,LSTM,Bidirectional,Dropout

def get_synonym_dict(synonym_dict_path):
	synonym = dict()
	with open(synonym_dict_path,'r',encoding='utf-8') as fr:
		lines = fr.readline()
	lines = [line.strip() for line in lines if len(line.strip())>0]
	for line in lines:
		line = line.split(',')
		words = []
		words = [word.strip() for word in line]
		for word in words[1:]:
			synonym.update({word:words[0]})
			pass
		pass
	return synonym
	pass
class LSTM_text_Classifier(object):
	"""docstring for Text_Classifier"""
	def __init__(self,tokenizer,word2vec,model_path,model=None,max_length=20,no_epoch=15,batch_size=6,no_class=2,synonym=None):
		super(LSTM_text_Classifier, self).__init__()
		self.tokenizer = tokenizer
		self.word2vec = word2vec
		self.word_dim = self.word2vec[self.word2vec.index2word[0]].shape[0]
		self.model = model
		self.model_path = model_path
		self.max_length = max_length
		self.no_epoch = no_epoch
		self.batch_size = batch_size
		self.no_class= no_class
		self.synonym =  synonym
	def train(self,X,y):
		self.model = self.build_model(input_dim=(X.shape[1],X.shape[2]))
		self.model.fit(X,y,batch_size=self.batch_size,epochs=self.no_epoch)
		self.model.save_weights(self.model_path)
		pass
	def predict(self, X):
		if(self.model is None):
			self.load_model()
		y = self.model.predict(X)
		return y
		pass
	def load_model(self):
		self.model = self.build_model(input_dim=(self.max_length,self.word_dim))
		self.model.load_weights(self.model_path)
		pass
	def build_model(self, input_dim):
		model = Sequential()
		model.add(LSTM(64, return_sequences=True,input_shape=input_dim))
		model.add(Dropout(0.2))
		model.add(LSTM(32))
		model.add(Dense(self.no_class,activation="softmax"))
		model.compile(loss=keras.losses.categorical_crossentropy,
                      optimizer=keras.optimizers.Adadelta(),
                      metrics=['accuracy'])
		return model
		pass
	def embedding_sentences(self,sentences,max_length=20):
		embed_sentences = []
		for sentence in sentences:
			embed_sent = []
			for word in sentence:
				if((self.synonym is not None) and (word in self.synonym)):
					embed_sent.append(self.word2vec[self.synonym[word].lower()])
				elif(word.lower() in self.word2vec):
					embed_sent.append(self.word2vec[word.lower()])
				else:
					embed_sent.append(npy.zeros((self.word_dim, ), dtype=float))
			pass
			if len(embed_sent) > max_length:
				embed_sent = embed_sent[:max_length]
			elif len(embed_sent) < max_length:
				embed_sent = npy.concatenate((embed_sent,npy.zeros((max_length-len(embed_sent),self.word_dim), dtype=float)),axis=0)
			embed_sentences.append(embed_sent)
			pass
		return embed_sentences
		pass
	def classify(self,sentences,label_dict=None):
		# input: list of sentences
		# output: list of label of each sentences
		# process: +tokenize each sentence
		#          +word embbeding sentence
		#          +predict each sentence
		#          +choose maximum of predicted label
		X = [sent.strip() for sent in sentences]
		X = self.tokenize_sentences(X)
		X = self.embedding_sentences(X, max_length=self.max_length)
		y = self.predict(npy.array(X))
		print(y)
		y = npy.argmax(y, axis=1)
		print(y)
		labels = []
		for lab_ in y:
			if label_dict is None:
				labels.append(lab_)
			else:
				labels.append(label_dict[lab_])
			pass
		return labels
		pass
	def tokenize_sentences(self,sentences):
		tokens = []
		for sentence in sentences:
			token = self.tokenizer.tokenize(sentence)
			tokens.append(token)
			pass
		return tokens
		pass
	def load_data(self,data_paths,load_method):
		X=[]
		y=[]
		for i,path in enumerate(data_paths):
			sentences = load_method(path)
			label = [0.0 for x in range(0,self.no_class)]
			label[i] = 1.0
			labels = [label for x in range(0,len(sentences))]
			X+=sentences
			y+=labels
			pass
		X = self.tokenize_sentences(X)
		X = self.embedding_sentences(X,max_length=self.max_length)
		return npy.array(X),npy.array(y)
		pass
	# Why static method?
	@staticmethod
	def load_method(path):
		with open(path,'r',encoding='utf-8') as fr:
			lines = fr.readlines()
			pass
		lines = [line.strip() for line in lines if len(line.strip())>0]
		return lines
		pass

class BidirectionalLSTM_text_classifier(LSTM_text_Classifier):
	"""docstring for Bidirectional_text_classifier"""
	def build_model(self, input_dim):
		model = Sequential()
		model.add(Bidirectional(LSTM(32, return_sequences=True), input_shape=input_dim))
		model.add(Dropout(0.1))
		model.add(Bidirectional(LSTM(16)))
		model.add(Dense(self.no_class, activation="softmax"))
		model.compile(loss=keras.losses.categorical_crossentropy,
                      optimizer=keras.optimizers.Adadelta(),
                      metrics=['accuracy'])
		return model
def test():
	# append PATHPYTHON with '../' ('Sentiment Analysis')
	import sys
	from sys import path
	from os.path import dirname as dir
	path.append(dir(path[0]))
	# import Word_Embedding and Word_Segmentation
	from Word_Embedding import word_to_vector
	from gensim.models import Word2Vec
	from Word_Segmentation.word_segmentation import Tokenizer
	tokenizer = Tokenizer()
	word2vec_model = Word2Vec.load('../pretrained_models/pretrained_word2vec.bin')
	sym_dict = get_synonym_dict('../data/sentiment/synonym.txt')
	# init class text_classifier
	text_classifier = BidirectionalLSTM_text_classifier(tokenizer=tokenizer, word2vec=word2vec_model.wv,
                                                        model_path='../pretrained_models/pretrained_sentiment_model.h5',
                                                        max_length=20, no_epoch=10,
                                                        synonym=sym_dict)
	# load data to X,y format from file
	X, y = text_classifier.load_data(['../data/sentiment/positives.txt',
                                           '../data/sentiment/negatives.txt'],
                                           load_method=text_classifier.load_method)
	# train available data
	# text_classifier.train(X,y)
	# classifier input comment
	label_dict = {0: 'tích cực', 1: 'tiêu cực'}
	test_sentences = ['Dở thế', 'Hay thế', 'phim chán thật', 'nhảm quá','thất vọng','kém cỏi']
	labels=text_classifier.classify(test_sentences,label_dict)
	print(labels)
	pass
if __name__ == '__main__':
	test()