from PIL import Image, ImageFilter
import os

# The path where the source thumbnails are located
source_path = "thumbnails/"
# The path where the filtered thumbnails are deposited
dump_path = "thumbnails_blurred/"

size = 100, 100

def main():

    # The list where the average R, G, and B values of
    # every pixel in all the photos will be dumped
    #average = [0,0,0]
    #pixel_count = 0;
    
    for filename in os.listdir(source_path):
        im = Image.open(source_path + filename)

        im = im.filter(ImageFilter.BLUR)
        
        im.save(dump_path + filename, "JPEG")    

if __name__ == "__main__":
    main()
