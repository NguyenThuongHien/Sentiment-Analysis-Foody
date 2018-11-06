import os
from pyvi import ViTokenizer
"""
	Tokenize word in training directory
	Examples
	sentences = "Phân_tích quan_điểm của 1 bình_luận" - tức là tách 1 câu(đoạn)thành 1 câu có phân ra từ đơn từ ghép
"""
class Tokenizer(object):
	"""docstring for Tokenizer"""
	def __init__(self):
		super(Tokenizer, self).__init__()
	def tokenize(self,sentence):
		sentence = sentence.strip().lower()
		sentence_tokenized = ViTokenizer.tokenize(sentence)
		tokens = sentence_tokenized.split(' ')
		return tokens
		pass
def tokenize_file(input_file, output_file):
	"""
	tokenize a file(tách từ trong 1 file)
	tham số: đường dẫn input, ouput file
	return: file được tách từ
	"""
	if not os.path.exists(output_file):
		raise Exception("Path does not exist")
	with open(input_file, 'r',encoding="utf-8") as fread:
		text = fread.read()
		text = ViTokenizer.tokenize(text)
	with open(output_file,'w',encoding="utf-8") as fwrite:
		fwrite.write(text)
	pass
def tokenize_directory(input_dir,output_dir):
	if not os.path.exists(output_dir):
		 os.makedirs(output_dir)
	input_files = os.listdir(input_dir)
	for file in input_files:
		if(file.startswith('.') or file.startswith('..') or os.path.isdir(file)):
			continue
		else:
			output_file = os.path.join(output_dir,'output_of_'+file)
			f=open(output_file,'a')
			f.close()
			tokenize_file(input_dir+file,output_file)
		pass
	pass
def test_tokenize_file():
	input_dir = '../data/input/'
	output_dir = '../data/output/'
	tokenize_directory(input_dir,output_dir)
	output_files = os.listdir(output_dir)
	for file in output_files:
		if(file.startswith('.') or file.startswith('..') or os.path.isdir(file)):
			continue
		with open(output_dir+file,'r',encoding='utf-8') as f:
			text = f.read()
			print(text)
		pass
def test_tokenize_sentence(sentence):
	tokenizer = Tokenizer()
	print(tokenizer.tokenize(sentence))
	pass
if __name__ == '__main__':
	# test_tokenize_file()
	test_tokenize_sentence('nguyễn phú trọng phát biểu')