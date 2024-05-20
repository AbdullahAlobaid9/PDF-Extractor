import os
import re
import logging
from PIL import Image, ImageFilter, ImageEnhance
from pdf2image import convert_from_path
import pytesseract
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

input_directory = 'docs/input/'
output_directory = 'docs/output/'
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Setup basic configuration for logging
logging.basicConfig(filename='ocr_processing.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_image(page_image):
    image = page_image.convert('L')
    image = image.filter(ImageFilter.SHARPEN)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    return image

def post_process_text(ocr_text):
    return re.sub(r'\s+', ' ', ocr_text)

def process_pdf_page(page_data):
    image = preprocess_image(page_data)
    arabic_text = pytesseract.image_to_string(image, lang='ara', config='--psm 6 --oem 3')
    return post_process_text(arabic_text)

def process_pdf_file(filePath):
    doc = convert_from_path(filePath, dpi=200)
    fileBaseName = os.path.splitext(os.path.basename(filePath))[0]
    ocr_text_list = []

    for page_data in doc:
        arabic_text = process_pdf_page(page_data)
        ocr_text_list.append(arabic_text)

    output_text_path = os.path.join(output_directory, f'{fileBaseName}_Arabic.txt')
    with open(output_text_path, 'w', encoding='utf-8') as output_text_file:
        output_text_file.write('\n'.join(ocr_text_list))

    # Log instead of print
    logging.info(f"Arabic text saved at: {output_text_path}")

def main():
    pdf_files = [os.path.join(input_directory, f) for f in os.listdir(input_directory) if f.lower().endswith('.pdf')]
    with ProcessPoolExecutor() as executor:
        list(tqdm(executor.map(process_pdf_file, pdf_files), total=len(pdf_files), desc="Processing PDF files"))

if __name__ == "__main__":
    main()
