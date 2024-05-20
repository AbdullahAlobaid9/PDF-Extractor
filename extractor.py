import fitz  # PyMuPDF
import os

def extract_key_pages_text(pdf_path):
    """Extract text from the first two and last two pages of a PDF."""
    doc = fitz.open(pdf_path)
    num_pages = doc.page_count
    # Determine pages to extract: first two and last two, avoiding duplicates
    pages_to_extract = list(range(min(2, num_pages))) + list(range(max(2, num_pages-2), num_pages))
    pages_to_extract = sorted(set(pages_to_extract))  # Remove duplicates if any
    text = []
    
    for page_num in pages_to_extract:
        page = doc.load_page(page_num)  # Load the specific page
        text.append(page.get_text())
    
    doc.close()
    return '\n'.join(text)

def process_pdfs_from_directory(input_directory, output_directory):
    """Process all PDF files in the input directory, extracting text from key pages."""
    for filename in os.listdir(input_directory):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, os.path.splitext(filename)[0] + '_key_pages.txt')
            
            print(f"Processing {filename}...")
            try:
                extracted_text = extract_key_pages_text(pdf_path)
                
                with open(output_path, 'w', encoding='utf-8') as file:
                    file.write(extracted_text)
                print(f"Saved extracted text to {output_path}")
            except Exception as e:
                print(f"Failed to process {filename}: {e}")
                
if __name__ == "__main__":
    input_dir = './docs/input/'  # Specify your PDF storage path
    output_dir = './docs/output/'  # Specify your output path for extracted texts
    process_pdfs_from_directory(input_dir, output_dir)
