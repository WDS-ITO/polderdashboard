import requests
import json

def get_total_results():
	link = "https://search.polder.info/api/count"
	response = requests.get(link)

	# Convert JSON data to a python object
	data = json.loads(response.text)
	return data







