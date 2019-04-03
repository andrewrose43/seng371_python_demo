import urllib.request
import json

# The URL for the MUX camera
baseURL = 'https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/MUX/'

# Trawl that catalog!
def main():

	# Get the MUX catalog object as a Python dictionary
	mux_json_obj = json.loads(urllib.request.urlopen(baseURL + 'catalog.json').read())
	for path_link in mux_json_obj["links"]:
		if path_link['rel'] == 'child':
			# Get each path's catalog object as a Python dictionary
			path_json_obj = json.loads(urllib.request.urlopen(baseURL + path_link['href']).read())
			for row_link in path_json_obj["links"]:
				if row_link['rel'] == 'child':
					# Get each row's catalog object as a Python dictionary
					# note that the URL has the path's three digits and '/' added in
					row_json_obj = json.loads(urllib.request.urlopen(baseURL + path_link['href'][:4] + row_link['href']).read())
					# Finally, we loop through the actual items
					for item_link in row_json_obj["links"]:
						if item_link['rel'] == 'item':
							# print(item_link)
							# Get each item as a Python dictionary
							item_obj = json.loads(urllib.request.urlopen(baseURL + path_link['href'][:4] + row_link['href'][:4] + item_link['href']).read())
							# print(item_obj)

							# Okay. Here, we need to check each item's bounding box and timestamp to figure out if we want it

if __name__ == "__main__":
	main()