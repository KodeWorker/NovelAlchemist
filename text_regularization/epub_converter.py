""" EPUD to TXT converter
# Description:
    This program contains a function to convert a single .epub file to .txt
    file.
# Author: Shin-Fu (Kelvin) Wu
# Date: 2017/07/21
"""
import os
import sys
import bs4

sys.path.append(os.path.join(os.path.dirname(__file__), 'ebooklib'))
import ebooklib
from ebooklib import epub

###############################################################################
def convert_epub_to_txt(epub_path, txt_path, encode='utf-8'):
    """ Convert EPUB to TXT
    This function converts the craped .epub files to .txt files.

    Parameters
    ----------
    epub_path: string
        This is the path of a craped .epub file to be parsed.
    txt_path: string
        This is the path of the converted .txt file to be saved.
    encode: string, default='utf-8'
        The encoding method of the character set.
    """
    try:
        book = epub.read_epub(epub_path)
        content = ''
        # Get all html content in .epub
        split = []
        content = []
        for doc in  book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            content.append(str('%s') %(doc.content))
            split.append(doc.file_name)
        # Sort the content by the split number
        content = [x for (y, x) in sorted(zip(split, content))]        
        content = ''.join(content)        
        
        # Select the text part
        soup = bs4.BeautifulSoup(content)
        elems = soup.findAll(['h1', 'h2', 'h3', 'h4', 'p', 'pre'])
        lines = [(elem.getText() + '\n') for elem in elems]
    except Exception as e:
        # BadZipFile -> parse an empty .txt file
        lines = []
        print('%s\n' %e)

    # Write .txt file
    with open(txt_path, 'wb') as write_file:
        write_file.writelines([line.encode(encode) for line in lines])

###############################################################################
if __name__ == '__main__':

    # Settings
    # The .epub file to be converted
    file_name = 'Show-Business'
    # The directory of the scraped .epub files
    epub_dir = os.path.join(os.path.dirname(__file__), '..', 'web_scraping', 'epub')
    # The directory of the converted .txt files
    txt_dir = os.path.join(os.path.dirname(__file__), 'txt')

    epub_path = os.path.join(epub_dir, file_name + '.epub')
    txt_path = os.path.join(txt_dir, file_name + '.txt')

    # Create the folder to save converted files
    if not os.path.exists(txt_dir):
        os.makedirs(txt_dir)

    # Conver .epub to .txt
    convert_epub_to_txt(epub_path, txt_path)
