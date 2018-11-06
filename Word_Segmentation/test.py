import os
from pyvi import ViTokenizer
sentence = "Nguyễn thượng hiền \n học máy \n             và    ngày xưa"
# sentence.split('\n')
sentence = ViTokenizer.tokenize(sentence)
print(sentence)