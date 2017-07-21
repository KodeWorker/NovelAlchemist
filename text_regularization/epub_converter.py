""" EPUD to TXT converter
# Description:
    This program contains a function to convert a single .epub file to .txt 
    file.
# Author: Shin-Fu (Kelvin) Wu
# Date: 2017/07/21
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'ebooklib'))
from ebooklib import epub


def convert_epub_to_txt(epub_path, txt_path):
    book = epub.read_epub(epub_path)
    print(book)

if __name__ == '__main__':
    
    # Settings
    # The .epub file to be converted
    file_name = 'And-Thats-How-It-Was-Officer'
    # The directory of the scraped .epub files 
    epub_dir = os.path.join(os.path.dirname(__file__), '..', 'web_scraping', 'epub')
    # The directory of the converted .txt files 
    txt_dir = os.path.join(os.path.dirname(__file__), 'txt')
    
    epub_path = os.path.join(epub_dir, file_name + '.epub')
    txt_path = os.path.join(epub_dir, file_name + '.txt')
    
    # Create the folder to save converted files
    if not os.path.exists(txt_dir):
        os.makedirs(txt_dir)
    
    # Conver .epub to .txt
    convert_epub_to_txt(epub_path, txt_path)   
