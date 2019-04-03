import urllib.request
import json

baseURL = 'https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/MUX/'

# Trawl that catalog!
def main():

	# Let's test that we can get one JSON object...
	# test_json = urllib.request.urlopen('https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/MUX/057/095/CBERS_4_MUX_20171121_057_095_L2.json').read()
	# print("\n" + str(test_json) + "\n")


	# Get the MUX catalog object as a Python dictionary
	mux_json_obj = json.loads(urllib.request.urlopen('https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/MUX/catalog.json').read())
	for path_link in mux_json_obj["links"]:
		if path_link['rel'] == 'child':
			# print('https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/MUX/' + path_link['href'])
			path_json_obj = json.loads(urllib.request.urlopen('https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/MUX/' + path_link['href']).read())
			# print(path_json_obj)
			# print(path_link['href'][:3])
			# print(path_link)
			for row_link in path_json_obj["links"]:
				if row_link['rel'] == 'child':
					# print(row_link)

					# Below, we see the ROW JSON with all its items. Yay
					row_json_obj = json.loads(urllib.request.urlopen('https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/MUX/' + path_link['href'][:4] + row_link['href']).read())
					# print(str(json.loads(urllib.request.urlopen('https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/MUX/' + path_link['href'][:4] + row_link['href']).read())))
					# print('https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/MUX/' + path_link['href'][:4] + row_link['href'])

if __name__ == "__main__":
	main()