import urllib.request
import json

# The URL for the MUX camera
baseURL = 'https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/MUX/'

# A search bounding box for testing purposes
bbox = [
	53,
	4,
	54,
	5
]

# Counter used to only grab that many Items
test_limiter = 5

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
							# Weird for condition because the actual coordinates are buried a few layers deep.
							for layer1 in item_obj['geometry']['coordinates']:
								for layer2 in layer1:
									# if any corner of the Item's polygon is inside our search bbox, we want it!
									for coordinate in layer2:
										# We do get as far as this line. The problem is that our filter lets nothing through...
										# print(coordinate)
										if (coordinate[0] > bbox[0] and coordinate[0] < bbox[2] and coordinate[1] > bbox[1] and coordinate[1] < bbox[3]):
											print(coordinate)
											# process/download/etc the Item
											continue


							# Okay. Here, we need to check each item's bounding box and timestamp to figure out if we want it

if __name__ == "__main__":
	main()