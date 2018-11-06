import sys
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
# add path that containing chromedriver.exe
sys.path.append('../chromedriver.exe')

# Hide Chrome browser open new window


def crawl_comment(dish_url):
	options = webdriver.ChromeOptions()
	options.add_argument("headless")
	# Create a driver to perform actions in website as: crawl,event
	browser = webdriver.Chrome(chrome_options=options)
	#
	path = "https://www.foody.vn"
	# dish_path = "/ho-chi-minh/mi-goi-xao-bo"
	# Go to the site https:https://www.foody.vn/dish_url
	browser.get(path + dish_url)
	browser.implicitly_wait(20)
	# load 30 comments
	number_comment = 0
	actions = webdriver.ActionChains(browser)
	while(1):
		try:
			if(len(browser.find_elements_by_xpath("//span[@ng-bind-html='Model.Description'][@class='ng-binding']")) >= 30):
				break
			wait = WebDriverWait(browser, 3)
			load_more = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@ng-click='LoadMore()']")))
			actions.move_to_element(load_more).perform()
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			browser.execute_script("arguments[0].click();", load_more)
			pass
		except Exception as e:
			break
			pass
		pass
	# find in html element that containing comment and get text
	count = 0
	element_cmts = browser.find_elements_by_xpath("//span[@ng-bind-html='Model.Description'][@class='ng-binding']")
	element_scores = browser.find_elements_by_xpath("//li/div/div/div/span[@class='ng-binding']")
	comments=[]
	scores=[]
	for cmt,sc in zip(element_cmts,element_scores):
		count += 1
		print(count)
		comment = cmt.text
		score = sc.text
		print(comment)
		comments.append(comment)
		scores.append(score)
		pass
	# close browser
	browser.quit()
	return comments
	pass
def test_crawl_comment(dish_url="/ho-chi-minh/mi-goi-xao-bo"):
	print(crawl_comment(dish_url))
	pass
if __name__ == '__main__':
	test_crawl_comment()
	pass