import PyPDF2
from PyPDF2 import PageObject
import nltk
import re
nltk.download('punkt')

####
#This file crops the pdf to remove headers and footers.
#TODO make this automatic for dimesions of doc
####

def crop_pdf(input_file, output_file, top_crop_mm=20, bottom_crop_mm=30, side_crop_mm=15):
    with open(input_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]

            # Calculate crop dimensions in points (1 inch = 72 points)
            top_crop_points = top_crop_mm * 2.83465
            bottom_crop_points = bottom_crop_mm * 2.83465
            side_crop_points = side_crop_mm * 2.83465

            original_width = page.mediabox.width
            original_height = page.mediabox.height

            new_width = original_width - 2 * side_crop_points
            new_height = original_height - top_crop_points - bottom_crop_points

            page.mediabox.upper_right = (new_width, new_height)
            
            lines_text = ''.join(page.extract_text().splitlines()[:]).lower()

            # Check if any keyword is present in the page.
            keywords=['Preface','References','Index',"Contents","glossary","copyrights","copyright"]
            if any(keyword.lower() in lines_text for keyword in keywords):
                continue
            #remove additional reference pages.
            ref_pattern= r'\[\d+\].*?'
            if re.search(ref_pattern, lines_text):
                continue 
        

            #Check if number of sentences is less than 2
            sentences = nltk.sent_tokenize(lines_text)
            if len(sentences) < 2:
                continue 
            
            pdf_writer.add_page(page)


        with open(output_file+input_file.split('/')[-1], 'wb') as output:
            pdf_writer.write(output)





