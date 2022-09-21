import requests
from bs4 import BeautifulSoup


def get_total_results():
	url = 'https://search.polder.info/search?text='



	res = requests.get(url)


	data = BeautifulSoup(res.text, 'html.parser')
	total_result = data.find_all('p', class_='results__number')[0].get_text()
	split = total_result.split()
	total_result = split[len(split)-1]
	return total_result