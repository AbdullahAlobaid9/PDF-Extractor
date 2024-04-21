import os
import re
from PIL import Image, ImageFilter, ImageEnhance
from pdf2image import convert_from_path
import pytesseract


input_directory = 'docs/input/'; 
output_directory = 'docs/output/'; 
# Set Tesseract command path
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Function to preprocess the image
def preprocess_image(page_image):
    image = page_image.convert('L')  # Convert to grayscale
    image = image.filter(ImageFilter.SHARPEN)  # Sharpen image
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Increase contrast
    return image

# Function to correct common OCR text errors and format properly
def post_process_text(ocr_text):
    ocr_text = re.sub(r'\s+', ' ', ocr_text)
    return ocr_text

# Process a single PDF file
def process_pdf_file(filePath):
    # Convert PDF to images with high resolution
    doc = convert_from_path(filePath, dpi=250)

    # Extract file info
    fileBaseName = os.path.splitext(os.path.basename(filePath))[0]

    ocr_text_list = []  # To store OCR results for all pages

    # Process each page
    for page_number, page_data in enumerate(doc):
        print(f"Processing page {page_number + 1} of {fileBaseName}")
        image = preprocess_image(page_data)
        arabic_text = pytesseract.image_to_string(image, lang='ara', config='--psm 6 --oem 3')
        arabic_text = post_process_text(arabic_text)
        ocr_text_list.append(arabic_text)

    # Save the extracted OCR text to a text file
    output_text_path = os.path.join(output_directory, f'{fileBaseName}_Arabic.txt')
    with open(output_text_path, 'w', encoding='utf-8') as output_text_file:
        output_text_file.write('\n'.join(ocr_text_list))

    print(f"Arabic text saved at: {output_text_path}")

# Process all PDF files in the input directory
for filename in os.listdir(input_directory):
    if filename.lower().endswith('.pdf'):
        filePath = os.path.join(input_directory, filename)
        process_pdf_file(filePath)
