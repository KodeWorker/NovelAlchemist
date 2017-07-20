""" Novel Scraper
# Description:
    This program scraps the novels on "Manybooks.net" with selected genre cata-
    gory and language option.
# Author: Shin-Fu (Kelvin) Wu
# Date: 2017/07/20
"""
import os
import time
import random
import bs4
import requests

###############################################################################
def sel_genre(url='manybooks.net', select=None):
    """ Select Genre
    This function allows user to select a particular genre from "manybooks.net"
    and it returns the link to the first page of selected genre. 
    
    Parameters
    ----------
    url: string, default='manybooks.net'
        The URL of "Manybooks".
    select: int, default=None
        The number of selection. If the value is None, the console will display
        all the genres and requires an user input.
    
    Return
    ------
    link: string
        The URL of the first page of the selected genre.
    """
    genre_url = 'http://%s/%s' %(url, 'categories')
    genre_dict = {}
    genre_list = []
    
    # Access genre catagories
    print('access genres... %s' %genre_url)
    res = requests.get(genre_url)
    try:
        res.raise_for_status()
    except Exception as exc:
        print('There was a problem accessing genre catagories: %s' %(exc))        
    soup = bs4.BeautifulSoup(res.text)
    
    # Get all genre elements
    elems = soup.select('a[class="larger"]')        
    for elem in elems:
        genre_name = elem.getText()
        genre_link = 'http://%s%s' %(url, elem.get('href'))        
        genre_dict[genre_name] = genre_link
        genre_list.append(genre_name)
    
    # Display Genre Selection
    if select == None:
        for i in range(len(genre_list)):
            print('[%d] : %s' %(i+1, genre_list[i]))
        select = input('Select the Genre (no.) >> ')
        
        if not (int(select) > 0 and int(select) < len(genre_list)+1):
            raise ValueError('Wrong selection number!')
    
    print('genre: %s' %genre_list[int(select)-1])
    
    link = genre_dict[genre_list[int(select)-1]]
    return link
###############################################################################
def sel_language(url, select=None):
    """ Select Language
    This function allows user to select a particular language in the pages of 
    each genre and it returns the link to the page of books with selected
    language.
    
    Parameters
    ----------
    url: string
        The URL of the first selected genre page.
    select: int, default=None
        The number of selection. If the value is None, the console will display
        all the language and requires an user input.
    
    Return
    ------
    link: string
        The URL of the first page of the selected genre and selected language.
    """
    lang_dict = {}
    lang_list = []
    
    # Access language options
    print('access language... %s' %url)
    res = requests.get(url)
    try:
        res.raise_for_status()
    except Exception as exc:
        print('There was a problem accessing language options: %s' %(exc))   
    soup = bs4.BeautifulSoup(res.text)
    
    # Get all language option elements
    elems = soup.select('option')    
    for elem in elems:
        lang_name = elem.getText()
        lang_value = elem.get('value')
        lang_dict[lang_name] = lang_value
        lang_list.append(lang_name)
    
    # Display language Selection
    if select == None:
        for i in range(len(lang_list)):
            print('[%d] : %s' %(i+1, lang_list[i]))
        select = input('Select the Genre (no.) >> ')
        
        if not (int(select) > 0 and int(select) < len(lang_list)+1):
            raise ValueError('Wrong selection number!')
    
    print('language: %s' %lang_list[int(select)-1])
    return lang_dict[lang_list[int(select)- 1]]
###############################################################################
def download_books_in_page(url, soup, file_dir):
    """Download Books in the Genre Pages
    This function downloads all the books in a genre page and raise the stop
    signal if there is no books in the page.
    
    Parameters
    ----------
    url: string
        The root URL address.
    soup: bs4.BeautifulSoup object
        The object contains all the info. in the genre catagory page.
    file_dir: sting
        This is the folder to save the scraped files.        
    """
    try:
        # has books
        # Get book elements in the genre page
        book_elems = soup.select('.grid_6.smallBook a')
        book_links =  [elem.get('href') for elem in book_elems]
        book_names = [elem.getText() for elem in book_elems]
        for i in range(len(book_links)):
            # Download one book at a time
            download_single_book(url, book_links[i], file_dir, book_names[i])
    except:
        # no book
        raise ScraperError('Error: No books in this page!')
###############################################################################
class ScraperError(Exception):
    """ Scraper Error
    A custom error raised when there are troubles.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
###############################################################################
def download_single_book(url, book_link, file_dir, book_name):
    """Download a single Book
    This function download the particular book according to its book_link. We 
    use URL (see -> # Text file download link) instead of using selenium module
    for better program control.
    
    Parameters
    ----------
    url: string
        The root URL address.
    book_link: string
        The href of the book.
    file_dir: string
        This is the folder to save the scraped files. 
    book_name
        This is the name(filename) of the book. 
    """
    # Text file download link
    book_id = book_link[8:-5]
    download_page = 'http://' + url + '/download-ebook?tid=' + book_id + \
    '&book=1%3Aepub%3A.epub%3Aepub'
    
    # Access the download page
    print('-> access... %s' %(book_name))
    res = requests.get(download_page)
    try:
        res.raise_for_status()
    except Exception as exc:
        print('There was a problem accessing download page: %s' %(exc))   
    soup = bs4.BeautifulSoup(res.text)
    
    # Get downloadable elements
    download_elems = soup.select('a[rel="nofollow"]')
    epub_link = [elem.get('href') for elem in download_elems if \
                elem.get('href').endswith('.epub')][0]
    
    # Download .epub file
    download_link = 'http://%s%s' %(url, epub_link)
    print('->-> access download link... %s' %(download_link))
    res = requests.get(download_link, allow_redirects=True)  # redirected!  
    try:
        res.raise_for_status()
    except Exception as exc:
        print('There was a problem accessing download link: %s' %(exc))
    print('->-> download... %s' %(book_name))
    
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
    
    # Write .epub file
    cachesize = 1024
    with open('%s/%s.epub' %(file_dir, book_name), 'wb') as write_file:
        for chunk in res.iter_content(cachesize):
            if len(chunk) % cachesize != 0:
                chunk += b' ' * ( cachesize - len(chunk))
            write_file.write(chunk)
    
    # Employ random delay
    time.sleep(3+random.randint(0,5))
###############################################################################
def continue_from_last_item(url, soup, file_dir, last_item):
    """Continue from Last Item
    This function finds the page of the last unfinish item, and downloads all 
    the remaining items.
    
    Parameters
    ----------
    url: string
        The root URL address.
    soup: bs4.BeautifulSoup object
        The object contains all the info. in the genre catagory page.
    file_dir: sting
        This is the folder to save the scraped files. 
    last_item: string
        The book name of the last unfinished download item.
    """
    try:
        # Has books
        # Get book elements in the genre page
        book_elems = soup.select('.grid_6.smallBook a')
        book_links =  [elem.get('href') for elem in book_elems]
        book_names = [elem.getText() for elem in book_elems]
        if last_item not in book_names:
            # Skip the page
            pass
        else:            
            book_links = book_links[book_names.index(last_item):]
            book_names = book_names[book_names.index(last_item):]
            for i in range(len(book_links)):
                # Download one book at a time
                download_single_book(url, book_links[i], file_dir, book_names[i])
            last_item = None
    except:
        # No book
        raise ScraperError('Error: No books in this page!')
    return last_item
###############################################################################
if __name__ == '__main__':
    
    # Settings
    
    # The path to save .epub files
    file_dir = os.path.join(os.path.dirname(__file__),'epub')
    # The "Manybooks" website
    url = 'manybooks.net'    
    # Last unfinished download item (book name)
    last_item = None
    
    # Create the folder to save scraped files
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    
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
            if last_item == None:
                # Find books and download .epub files
                download_books_in_page(url, soup, file_dir)
            else:
                # Search for the last unfinished download item
                last_item = continue_from_last_item(url, soup, file_dir, last_item)
            
            # Get "next page" button
            button_elems = soup.select('a[title="next"]')[0]        
            page_link = 'http://%s%s' %(url, button_elems.get('href')) 
        except Exception as e:
            # No "next page" button
            print(e)
            print('end of pages')
            break
    