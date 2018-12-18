import sys
sys.path.append("../Sentence Detection")
sys.path.append("../Classifier")
from keras_text_classifier import *
from Sent_Detect import *
# Detect Aspect and Sentiment for a cmt
def das(cmt):
	# split to sentences in order to detect both sentiment and aspect
	sentences = detect_sentence(cmt)
	# print(sentences)
	# set parameter
	label_sentiment={0: 'tích cực', 1: 'tiêu cực'}
	model_path_sentiment='../pretrained_models/pretrained_sentiment_model1.h5'
	label_aspect = {0: 'Không liên quan', 1: 'Chất lượng',2: 'Giá cả',3: 'Vị trí',4: 'Không gian',5: 'Phục vụ'}
	model_path_aspect='../pretrained_models/pretrained_aspect_model.h5'
	# get label aspect for every sentence in cmt
	aspects=predict(label_aspect,sentences,model_path_aspect,50)
	# get sentence corresponding its aspect
	concatnated_sent = concatnate(sentences,aspects)
	concatnated_sent = [sent.strip() for sent in concatnated_sent]
	# 
	# sentiment for every aspect
	list_sentiment=[]
	for i in range(len(concatnated_sent)):
		aspect=concatnated_sent[i]
		if(aspect==''):
			list_sentiment.append(0)
		else:
			if(predict(label_sentiment,[aspect],model_path_sentiment,100)[0]=='tích cực'):
				if(i==0):
					print('Chất lượng # tích cực')
				elif(i==1):
					print('Giá cả # tích cực')
				elif(i==2):
					print('Vị trí # tích cực')
				elif(i==3):
					print('Không gian # tích cực')
				elif(i==4):
					print('Phục vụ # tích cực')
				list_sentiment.append(1)
			else:
				if(i==0):
					print('Chất lượng # tiêu cực')
				elif(i==1):
					print('Giá cả # tiêu cực')
				elif(i==2):
					print('Vị trí # tiêu cực')
				elif(i==3):
					print('Không gian # tiêu cực')
				elif(i==4):
					print('Phục vụ # tiêu cực')
				list_sentiment.append(-1)
		pass
	pass
# Concatenate all sentence if we have the same aspect
def concatnate(sentences,labels):
	n = len(sentences)
	quality = ''
	price =''
	position =''
	space=''
	service=''
	for i in range(n):
		if labels[i]=='Chất lượng':
			if quality!='':
				quality= quality+' '+sentences[i]
			else:
				quality=sentences[i]
		elif labels[i]=='Giá cả':
			if price!='':
				price= price+' '+sentences[i]
			else:
				price=sentences[i]
		elif labels[i]=='Vị trí':
			if position!='':
				position= position+' '+sentences[i]
			else:
				position=sentences[i]
		elif labels[i]=='Không gian':
			if space!='':
				space= space+' '+sentences[i]
			else:
				space=sentences[i]
		elif labels[i]=='Phục vụ':
			if service!='':
				service= service+' '+sentences[i]
			else:
				service=sentences[i]
		pass
	return[quality,price,position,space,service]
	pass
def review_about_food(path):
	# get all comments about specific food
	with open(path,'r',encoding='utf-8') as f:
		cmts=f.read()
		pass
	n = len(cmts)
	# get review for food every cmt
	matrix_sentiment=[]
	for cmt in cmts:
		matrix_sentiment.append(das(cmt))
		pass
	# 
	number_positive = [0,0,0,0,0]
	number_negative = [0,0,0,0,0]
	# get sentiment of all user about product
	for i in range(5):
		for j in xrange(n):
			if matrix_sentiment[j][i]>0:
				number_posive[i]+=1
			elif matrix_sentiment[j][i]<0:
				number_negative+=1
			pass
		pass
	return number_posive,number_negative
	pass
def test():
	das('nhà hàng được trang trí rất đẹp thoáng mát rộng rãi,nhưng nhân viên rất cẩu thả, thái độ không tốt,đồ ăn ăn rât ngon,tuyệt vời')
	pass
if __name__ == '__main__':
	test()

