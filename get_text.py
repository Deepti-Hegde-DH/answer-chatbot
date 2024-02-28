import fitz  
import re

def clean_text(input_path,output_path):
    text= extract_text_from_pdf(input_path)
    text = text.replace('\n', ' ')
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    cleaned_sentences = [sentence for sentence in sentences if sentence and sentence[0].isupper() and sentence[-1] == '.'and len(sentence.split()) >= 5]
    cleaned_text = ' '.join(cleaned_sentences)
    file_path=output_path
    with open(file_path+(input_path.split('/')[-1].replace('.pdf','.txt')), 'w') as file:
        file.write(cleaned_text)
        return cleaned_text
        


def extract_text_from_pdf(pdf_file):
    text_data = ""
    with fitz.open(pdf_file) as pdf_doc:
        for page_num in range(pdf_doc.page_count):
            page = pdf_doc[page_num]
            text_data += page.get_text()

    return text_data



