import requests
import bs4
from bs4 import BeautifulSoup

main_url = r'https://www.rottentomatoes.com/'
page = requests.get(main_url)
soup = BeautifulSoup(page.content, 'html.parser')

html = soup.find('html')
links = soup.find_all('a', {'class': 'unstyled articleLink'})
url_top_movies = [link.attrs['href'] for link in links if link.get_text() == 'Top Movies'][0]

#######################################################################################################################

page_top_movies = requests.get(main_url+url_top_movies)
soup = BeautifulSoup(page_top_movies.content, 'html.parser')

span_top_2018 = [s for s in soup.find_all('span') if s.get_text() == 'Best Movies of 2018'][0]
div = span_top_2018.next_element.next_element.next_element
table = [child for child in list(div.children) if child.name == 'table'][0]

#url = [child.find_all('a') for child in list(table.children) if child.name == 'tr']

movies = []

for child in list(table.children):
    if child.name == 'tr':
        url = child.find_all('a')[0].attrs['href']  # .encode('utf-8')
        name = child.find_all('a')[0].get_text()  # .encode('utf-8')
        movies.append({'url': url, 'name': name})

#######################################################################################################################

movie = movies[0]

for movie in movies:

    movie_info_page = requests.get(main_url+movie['url'])
    soup = BeautifulSoup(movie_info_page.content, 'html.parser')
    tomato_meter_score = soup.find_all('a', {'id': 'tomato_meter_link'})[0].get_text().strip()
    audience_score = soup.find_all('div', {'class': 'audience-score meter'})[0].get_text().replace('liked it', '').strip()
    list_info = soup.find_all('ul', {'class': 'content-meta info'})[0]

    for element in list(list_info.children):
        if element.name == 'li':
            info = (element.get_text().replace('\n', '').strip().split(':'))
            movie[info[0]] = info[1].strip()

    movie['Rotten Tomatoes Score'] = tomato_meter_score
    movie['Audience Score'] = audience_score
    movie['Genre'] = [gen.strip() for gen in movie['Genre'].split(',')]
    movie['Runtime'] = movie['Runtime'].strip()
    movie['Studio'] = movie['Studio'].strip()
    movie['Written By'] = [wb.strip() for wb in movie['Written By'].split(',')]

print(movies)


