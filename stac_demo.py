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
	for path_dict in mux_json_obj["links"]:
		if path_dict['rel'] == 'child':
			# print('https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/MUX/' + path_dict['href'])
			path_json_obj = json.loads(urllib.request.urlopen('https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/MUX/' + path_dict['href']).read())
			print(path_json_obj)



if __name__ == "__main__":
	main()