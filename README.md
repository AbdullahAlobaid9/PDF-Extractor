# Arabic PDF OCR Processing

This project processes PDF files containing Arabic text, converting them into editable text files using Optical Character Recognition (OCR) technology powered by Tesseract.

## Features

- Converts each page of a PDF document to an image.
- Performs OCR on the image to extract Arabic text.
- Saves the extracted text to a corresponding text file.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.6+
- pip (Python package installer)

## Installation

To install the necessary Python packages, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://your-repository-url.git
   cd your-repository-directory

2. Install the required packages:
    pip install -r requirements.txt

3. Make sure Tesseract OCR is installed and properly set up on your system. For Ubuntu:
    sudo apt install tesseract-ocr tesseract-ocr-ara

Configuration

- Update the input_directory and output_directory in the script to point to the correct folders where your PDF files are stored and where you want the output text files to be saved.
-    Verify the path to the Tesseract command if different from /usr/bin/tesseract.


## Usage

To run the script, use the following command:



python extractor.py
