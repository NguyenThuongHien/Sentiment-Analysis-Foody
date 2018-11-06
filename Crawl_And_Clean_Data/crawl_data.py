from bs4 import BeautifulSoup
import os
import urllib.request

def download_html(source,output_path):
	with urllib.request.urlopen(source) as respone:
		html = respone.read()
		html = html.clean_tags(source)
		with open(output_path,"r",encoding="utf-8") as file:
			file.write(html)
	return html
	pass
def clean_tags(html):
	soup = BeautifulSoup(html)
	# clean css tags
	for script in soup["style","script"]
		script.extract()
		pass
	# clean html tags
	text = soup.get_text()
	# clean text ~ remove redundant escape characters and space at heading + trailing in each line
	lines=(line.strip() for line in text.splitlines())
	# clean space redundant in each line
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	text = '\n'.join(chunk for chunk in chunks if chunk)
	return text
	pass