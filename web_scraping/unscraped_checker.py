"""Unscraped Checker
# Description:
    This program finds the names of unscraped books.
# Author: Shin-Fu (Kelvin) Wu
# Date: 2017/07/21
"""
import os
import bs4
import requests
import collections
from novel_scraper import sel_genre, sel_language, ScraperError

###############################################################################
def check_scraped_files(url, soup):
    """Download Books in the Genre Pages
    This function gets all the book (file) names in the genre pages.
    
    Parameters
    ----------
    url: string
        The root URL address.
    soup: bs4.BeautifulSoup object
        The object contains all the info. in the genre catagory page.
    file_dir: sting
        This is the folder to save the scraped files.
        
    Retrurn
    -------
    unscraped: list of strings
        This list contains the names of unscraped books in a genre page.
    """
    # The unscraped book in a genre page
    scraped = []
    
    try:
        # has books
        # Get book elements in the genre page
        book_elems = soup.select('.grid_6.smallBook a')
        book_names = [elem.getText() for elem in book_elems]
        
        for i in range(len(book_names)):
            # Check file name
            book_name = book_names[i]
            
            # Avoid file name errors
            book_name = book_name.replace('/', '-')
            book_name = book_name.replace('\\', '-')
            book_name = book_name.replace(':', '-')
            book_name = book_name.replace('*', '-')
            book_name = book_name.replace('?', '-')
            book_name = book_name.replace('\"', '-')
            book_name = book_name.replace('>', '-')
            book_name = book_name.replace('<', '-')
            book_name = book_name.replace('|', '-')
            # Custom file name
            book_name = book_name.replace(' ', '-')
            book_name = book_name.replace('\'', '')
            book_name = book_name.replace(',', '')
            # EPUB extension
            book_name += '.epub'
            scraped.append(book_name)
    except:
        # no book
        raise ScraperError('Error: No books in this page!')
    return scraped

###############################################################################
if __name__ == '__main__':
    # Settings
    # The path to save .epub files
    file_dir = os.path.join(os.path.dirname(__file__), 'epub')
    # The "Manybooks" website
    url = 'manybooks.net'   
        
    # Get scraped files
    file_list = [x[2] for x in os.walk(file_dir)][0]
    
    # The scraped book name
    scraped = []
    
    # select=54 : Science Fiction
    genre_link = sel_genre(url, select=54)
    # select=10 : English
    lang = sel_language(genre_link, select=10)
    # First page of the selected genre
    page_link = genre_link + '/' + lang
    
    while True:
        
        # Access genre pages
        print('access... %s' %page_link)
        res = requests.get(page_link)
        try:
            res.raise_for_status()
        except Exception as exc:
            print('There was a problem accessing genre page: %s' %(exc))               
        soup = bs4.BeautifulSoup(res.text)
        
        try:
            scraped_book = check_scraped_files(url, soup)
            scraped += scraped_book
            
            # Get "next page" button
            button_elems = soup.select('a[title="next"]')[0]        
            page_link = 'http://%s%s' %(url, button_elems.get('href')) 
        except Exception as e:
            # No "next page" button
            print(e)
            print('end of pages')
            break
    
    print('#. of books: %d' %len(scraped))
    diff = set(file_list) - set(scraped)
    if len(diff) == 0:
        # Books with the same name or duplication
        duplicated = [item for item, count in collections.Counter(scraped).items() if count > 1]
        print('Duplication:')
        for item in duplicated:
            print('- %s' %item)
    else:
        print('Difference:')
        for item in diff:
            print('- %s' %item)
    