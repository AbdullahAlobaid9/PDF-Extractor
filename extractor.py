import os
import re
import logging
from PIL import Image, ImageFilter, ImageEnhance
from pdf2image import convert_from_path
import pytesseract
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
import multiprocessing

input_directory = 'docs/input/'
output_directory = 'docs/output/'
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

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
    try:
        doc = convert_from_path(filePath, dpi=200)
        fileBaseName = os.path.splitext(os.path.basename(filePath))[0]
        ocr_text_list = []

        for page_data in doc:
            arabic_text = process_pdf_page(page_data)
            ocr_text_list.append(arabic_text)

        output_text_path = os.path.join(output_directory, f'{fileBaseName}_Arabic.txt')
        with open(output_text_path, 'w', encoding='utf-8') as output_text_file:
            output_text_file.write('\n'.join(ocr_text_list))

        logging.info(f"Arabic text saved at: {output_text_path}")
    except Exception as e:
        logging.error(f"Failed to process {filePath}: {e}")


def batch_process(files, batch_size, num_cores):
    total_batches = (len(files) + batch_size - 1) // batch_size  # Calculate total number of batches
    with tqdm(total=total_batches, desc="Overall Progress", position=0) as overall_progress:
        for i in range(0, len(files), batch_size):
            batch = files[i:i+batch_size]
            with tqdm(total=len(batch), desc=f"Processing batch {i//batch_size + 1}", position=1, leave=False) as batch_progress:
                with ProcessPoolExecutor(max_workers=num_cores) as executor:
                    for _ in executor.map(process_pdf_file, batch):
                        batch_progress.update(1)
            overall_progress.update(1)

def main():
    pdf_files = [os.path.join(input_directory, f) for f in os.listdir(input_directory) if f.lower().endswith('.pdf')]
    num_cores = int(multiprocessing.cpu_count() * 0.7)
    batch_size = 10  # Adjust batch size based on available memory and performance

    batch_process(pdf_files, batch_size, num_cores)

if __name__ == "__main__":
    main()
