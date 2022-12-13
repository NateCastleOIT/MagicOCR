import easyocr
import os
from PIL import Image

def clear_output():
    file = open("output.txt", "w")
    file.close()


def crop_image(image):
    left = 32
    top = 32
    bottom = 110
    right = 650     # Cropping so I only read the card name - drastically improves speed w/o CUDA which I couldn't get working

    cropped = Image.open('../images/' + image)
    cropped = cropped.crop((left, top, right, bottom))
    #cropped.show()
    cropped.save('..\cropped\\' + image)
    return cropped

def read_card(image, reader):
    crop_image(image)                                           # Crop image to just the desired text
    
    results = reader.readtext('..\cropped\\' + image,
                              detail=1,                                 # Detailed gives the coords of the text, the actual text, then the confidence
                              paragraph=True,                           # Groups words better
                              blocklist="!@#$%^&*()_+~`=;<>123456789")
    card_name = results[0][1]   # Grabs the card name
    print(card_name)
    return card_name

def write_card_to_file(reader):
    images = os.listdir('..\images') # Grabs the list of file names in /images/
    
    for image in images:
        card_name = read_card(image, reader)
        file = open("output.txt", "a")
        file.write(card_name + '\n')
    file.close()
        
def run():
    reader = easyocr.Reader(['en'], gpu=1)  # Open a easyOCR reader, only needs to run once
    clear_output()
    write_card_to_file(reader)

def main():  
    run()

    
    
main()