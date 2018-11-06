import os
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.models import Word2Vec

"""
Load data from output directory and split it into separate word
Convert word to vector n demension (100 dimension)?
"""
def split_word_from_file(input_file):
	words =[]
	with open(input_file,'r',encoding='utf-8') as file:
		lines = file.readlines()
		for line in lines:
			sentence = line.strip().split()
			words.append(sentence)
	return words
	pass
def split_word_from_directory(input_dir):
	files = os.listdir(input_dir)
	for file in files:
		if (file.startswith('.') or file.startswith('..') or os.path.isdir(file)):
			continue
		words=[]
		words+=split_word_from_file(input_dir+file)
		return words
	pass
def training_by_Word2Vec(data_dir="../data/output/",load_data=split_word_from_directory,pretrained_data="../pretrained_models/pretrained_word.bin"):
	sentences = load_data(data_dir)
	model = Word2Vec(sentences, size=100, window=5, min_count=1, workers=4)
	model.save(pretrained_data)
	pass
def test_train_model(pretrained_data="../pretrained_models/pretrained_word.bin",word='thảo_luận'):
	model = Word2Vec.load(pretrained_data)
	vector = model.wv[word]
	sim_words = model.wv.most_similar(word)
	print(sim_words)
	pass
def test_split_word():
	input_file = '../data/output/output_of_data1.txt'
	words = split_word_from_file(input_file)
	print(words)
	pass
if __name__ == '__main__':
 	test_split_word()