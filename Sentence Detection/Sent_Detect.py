import re
from underthesea import chunk
from underthesea import pos_tag
# tách theo dấu chấm 
def split_punctuation(sentence):
	sent_splited =  sentence.split('.')
	sent_splited=[sent.strip() for sent in sent_splited if(len(sent.strip())>0)]
	return sent_splited
	pass
# tách theo dấu chấm phẩy
def split_semicolon(sentence):
	sent_splited =  sentence.split(';')
	sent_splited=[sent.strip() for sent in sent_splited if(len(sent.strip())>0)]
	sent_splits = []
	n = len(sent_splited)
	for i in range(1,n):
		if(sent_splited[i]==''): continue
		sent = sent_splited[i].split()
		word = sent[0].lower()
		if (word=='thì' or word =='nên'):
			sent_splited[i] = sent_splited[i-1]+' '+sent_splited[i]
		elif (word=='và'):
			if not(is_clause(sent_splited[i])):
				sent_splited[i] = sent_splited[i-1]+' '+sent_splited[i]
			else:
				sent_splits.append(sent_splited[i-1])
		else:
			sent_splits.append(sent_splited[i-1])
		pass
	sent_splits.append(sent_splited[n-1])
	pass
	return sent_splits
# tách các theo dấu phẩy
def split_sentence(sentence,delemiter):
	sent_splited =  sentence.split(delemiter)
	sent_splited=[sent.strip() for sent in sent_splited if(len(sent.strip())>0)]
	sent_splits = []
	n = len(sent_splited)
	for i in range(1,n):
		if not(is_clause(sent_splited[i])):
			sent_splited[i] = sent_splited[i-1]+' '+sent_splited[i]
		else:
			sent_splits.append(sent_splited[i-1])
		pass
	sent_splits.append(sent_splited[n-1])
	pass
	return sent_splits
# kiểm tra có là 1 mệnh đề hoàn chỉnh không
def is_clause(sentence):
	pos = pos_tag(sentence.lower())
	typeofword = []
	for i in range(len(pos)):
		typeofword.append(pos[i][1])
		pass
	if (('N' in typeofword) or ('Np' in typeofword) or ('V') in typeofword or ('M') in typeofword or ('Nc' in typeofword)) and ('A' in typeofword):
		if typeofword[0]=='C' or typeofword[0]=='R':
			if typeofword[1]=='N' or typeofword[1] == 'Np' or typeofword[1]=='V' or typeofword[1]=='M' or typeofword[1]=='Nc':
				return True
			if typeofword[1] == 'A':
				if typeofword[2] =='N' or typeofword[2] == 'Np' or typeofword[2] == 'M' or typeofword[2]=='Nc':
					return True
			else:
				return False
		elif typeofword[0]=='X':
			if typeofword[1]=='C' or typeofword[1]=='R':
				if typeofword[2]=='N' or typeofword[2] == 'Np' or typeofword[2]=='V' or typeofword[2]=='M' or typeofword[2]=='Nc':
					return True
				if typeofword[2] == 'A':
					if typeofword[3] =='N' or typeofword[3] == 'Np' or typeofword[3] == 'M' or typeofword[3]=='V' or typeofword[3]=='Nc':
						return True
			else:
				return False
		elif typeofword[0]=='N' or typeofword[0] == 'Np' or typeofword[0]=='V' or typeofword[0]=='M':
			return True
		elif typeofword[0]=='A':
			if typeofword[1] =='N' or typeofword[1] == 'Np' or typeofword[1] == 'M' or typeofword[0]=='V':
				return True
		else:
			return False
	else:
		return False
	return False
	pass
def detect_sentence(sentence):
	sent_split = []
	sent_punc = split_punctuation(sentence)
	for sentencex in sent_punc:
		sent_semicolon = split_semicolon(sentencex)
		for sentenc in sent_semicolon:
			sent_but = split_sentence(sentenc,'nhưng')
			for senten in sent_but:
				sent_and = split_sentence(senten,'và')
				for sente in sent_and:
					sent_comma = split_sentence(sente,',')
					for sent in sent_comma:
						sent_split.append(sent)
						pass
				pass
			pass
		pass
	return sent_split
	pass
def test():
	sentence="Vì thấy quán đang chạy giảm giá giá cả khá hợp lý nên mình cũng quên ko vào đọc bình luận trước khi order"
	sentence1="Lẩu bò thì chỉ có 1 loại bò; hải sản đắt hơn và toàn mấy thứ ôi, mực bé tí, nhũn nhèo, ko có cá lăng như quảng cáo,món ăn thì không ngon."
	sentence2="Đồ ăn nguội và nhân viên thì hơi chậm chạm"
	# sentence = sentence+" "+sentence1+" "+sentence2
	s = 'nhà hàng được trang trí rất đẹp thoáng mát rộng rãi,nhưng nhân viên rất cẩu thả, thái độ không tốt'
	print(detect_sentence(s))
	print(pos_tag('nhân viên rất cẩu thả'))
	# print(split_sentence(sentence2,'và'))
	# for sent in sentences:
	# 	print(split_comma(sent,','))
	# pass
if __name__ == '__main__':
	test()