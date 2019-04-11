import urllib.request
import json
import sys
import dateutil.parser

# The URL for the MUX camera
baseURL = 'https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/MUX/'
# The path to save photos to
img_path = "input/images/"
# The path to save metadata to
metadata_path = "input/metadata/"

# A search bounding box for testing purposes
bbox = [
	53,
	4,
	54,
	5
]

# A bounding time interval for testing purposes
# initially blank; is filled in the starter code
btime = [
        dateutil.parser.parse("2017-02-20T00:00:00Z"),
	dateutil.parser.parse("2017-12-30T00:00:00Z")
]

# Downloads a jpg and stores it in the desired folder
def download_jpg(url, file_path, file_name):
	full_path = file_path + file_name + '.jpg'
	urllib.request.urlretrieve(url, full_path)

# Trawl that catalog!
def main():

	# Counter and limiter used to only grab that many Items
	test_limiter = 3
	grab_count = 0

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
							# If no time zone information is included, don't take it
							# This is necessary in order to avoid causing errors
							# which would occur when you compare datetimes and only one of
							# the datetimes has a time zone
							item_time = dateutil.parser.parse(item_obj["properties"]["datetime"])
							if not item_time.tzinfo:
								continue
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
											
											# download the Item's thumbnail
											download_jpg(item_obj['assets']['thumbnail']['href'], img_path, item_obj['id'])

											# save its metadata in a JSON file
											# make the json thing as a dict
											# the image shares its name with the JSON file
											# so there is no need for an image link/name entry here
											metadata_dict = {
												"coordinates": item_obj['geometry']['coordinates'],
												"timestamp": str(item_time)
											}
											with open(metadata_path + item_obj['id'] + '.json', 'w') as outfile:
												json.dump(metadata_dict, outfile)

											grab_count = grab_count + 1

											# stop if you've grabbed enough things
											if (grab_count == test_limiter):
												print("Done: downloaded " + str(grab_count) + " Items")
												sys.exit()
												# once you've done that based on the one coordinate being in the bbox, you've grabbed the Item and don't want to grab it again, so break
											break

if __name__ == "__main__":

	main()
