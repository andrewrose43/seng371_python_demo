import urllib.request
import json
# dateutil.parser is also imported, but only in the "if name==main" block at the bottom of this file. This is purely to avoid a PyCharm (Python IDE) glitch which didn't recognize the module.

# The URL for the MUX camera
baseURL = 'https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/MUX/'

# A search bounding box for testing purposes
bbox = [
	53,
	4,
	54,
	5
]
# A bounding time interval for testing purposes
btime = []

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

							# Get each item as a Python dictionary
							item_obj = json.loads(urllib.request.urlopen(baseURL + path_link['href'][:4] + row_link['href'][:4] + item_link['href']).read())

							# Save the Item's timestamp for later. If it's out of the search range,
							# move on to the next Item
							item_time = dateutil.parser.parse(item_obj["properties"]["datetime"])
							if not (item_time > btime[0] and item_time < btime[1]):
								continue

							# Weird for conditions because the actual coordinates are buried a few layers deep.
							# coordinates and layer1 each had only a single thing inside (on the ones I looked at):
							# the next-level-down list (layer1 and layer2, respectively)
							for layer1 in item_obj['geometry']['coordinates']:
								for layer2 in layer1:
									# if any corner of the Item's polygon is inside our search bbox
									# AND the Item is within the desired timeframe, we want it!
									for coordinate in layer2:
										if (coordinate[0] > bbox[0] and coordinate[0] < bbox[2] and coordinate[1] > bbox[1] and coordinate[1] < bbox[3]):
											print(coordinate)
											# process/download/etc the Item
											# once you've done that based on the one coordinate being in the bbox, you've grabbed the Item and don't want to grab it again, so break
											break

if __name__ == "__main__":
	# Get the timeframe defined
	btime = [
		dateutil.parser.parse("2017-01-20T00:00:00Z"),
		dateutil.parser.parse("2017-12-30T00:00:00Z")
	]
	# This line is here to circumvent a PyCharm (Python IDE) bug that wasn't recognizing dateutil
	import dateutil.parser
	main()