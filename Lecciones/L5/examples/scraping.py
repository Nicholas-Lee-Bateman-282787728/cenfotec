import requests
import bs4
from bs4 import BeautifulSoup

page = requests.get('http://dataquestio.github.io/web-scraping-pages/simple.html')
soup = BeautifulSoup(page.content,'html.parser')

for el in list(soup.children):
	if type(el) == bs4.element.Tag:
		print list(el.children )


# metodos en soup https://gist.github.com/yoki/b7f2fcef64c893e307c4c59303ead19a

# page = requests.get('http://dataquestio.github.io/web-scraping-pages/simple.html')
# # print page.content

# # print(soup.prettify())

# for el in list(soup.children):
# 	if type(el) == b

# print [type(item) for item in list(soup.children)]

# print html = list(soup.children)[2]

# print list(html.children)

# print body = list(html.children)[3]

# print list(body.children)

# p = list(body.children)[1]

# print p.get_text()

# ### alternativa
# print soup.find_all('p')

# print soup.find_all('p')[0].get_text()

# print soup.find('p')

# ############ ids y clases

# page = requests.get("http://dataquestio.github.io/web-scraping-pages/ids_and_classes.html")

# soup = BeautifulSoup(page.content, 'html.parser')

# print soup

# print soup.find_all('p', class_='outer-text')

# print soup.find_all(class_="outer-text")

# print soup.find_all(id="first")

# #### selectors

# print soup.select("div p")

# # usar este url http://www.fabpedigree.com/james/mathmen.htm
# # ejemplo navigation https://gist.github.com/yoki/b7f2fcef64c893e307c4c59303ead19a


# """
# .parent
# .children
# """

# # print soup.prettify()
# # for item in list(soup.children):
# # 	print item

# # for item in list(soup.children):
# # 	print type(item)

# # for item in list(soup.children):
# # 	print item.name

# for item in list(soup.children):
# 	if item.name == 'html':
# 		for x in list(item.children):
# 			# print type(x)
# 			# print x.name
# 			# print x.findNext('p')
# 			print x.parent


# page = requests.get('https://www.rottentomatoes.com')
# soup = BeautifulSoup(page.content, 'html.parser')

# print(soup.prettify())

# print list(soup.children)

# for item in list(soup.children):
# 	print type(item)
# DocType es info de document
# nacigable string es text en HTML
# tag contiene otros nested tags y texts

# for item in list(soup.children):
# 	if type(item) == bs4.element.Tag:
# 		for x in list(item.children):
# 			if type(item) == bs4.element.Tag:
# 				for x in list(item.children):
# 					print x

# divs= soup.find_all('div')

# name_box = soup.find('h1', attrs={'class': 'name'})

# for div in divs:
# 	print div.get_text()

# article_links = soup.find_all('a',class_='unstyled articleLink')
# for link in article_links:
# 	print link
# 	print '-----'

### strip() es para remove starting and tailing spaces

# base_url = 'https://www.rottentomatoes.com'
# article_links = soup.find_all('a',class_='unstyled articleLink')
# for link in article_links:
# 	if 'Top Movies' in link.text:
# 		print link.attrs
# 		print link.name

# 		print requests.get(base_url + link['href'])


