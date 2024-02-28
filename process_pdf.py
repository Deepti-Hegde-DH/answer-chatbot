#========================================
import os 
from crop import crop_pdf

#*****
#cropping the pdf file to remove headers and footers.
#*****

input_pdf_path = "unprocessed_files/"
output_pdf_path = "cropped_files/"

file_list = [f for f in os.listdir(input_pdf_path) if os.path.isfile(os.path.join(input_pdf_path, f))]

for i in file_list:
    top_margin = 5
    bottom_margin = 10
    left_margin = 5

    crop_pdf(input_pdf_path+i, output_pdf_path, top_margin, bottom_margin, left_margin)
#======================================================
from get_text import clean_text

file_list = [f for f in os.listdir(output_pdf_path) if os.path.isfile(os.path.join(output_pdf_path, f))]
for i in file_list:
    clean_text(output_pdf_path+i)