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
    
    res = requests.get(genre_url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text)
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
    
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text)
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
def download_books_in_page(page):
    """UNDER CONSTRUCTION"""
    # has books
    # no book
    pass
###############################################################################
if __name__ == '__main__':
    url = 'manybooks.net'
    # select=54 : Science Fiction
    genre_link = sel_genre(url, select=54)
    # select=10 : English
    lang = sel_language(genre_link, select=10)
    # first page of the selected genre
    page = genre_link + '/' + lang
    
    while True:
        print('access...%s' %page)
        res = requests.get(page)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text)
        try:
            # get "next page" button
            button_elems = soup.select('a[title="next"]')[0]        
            page = 'http://%s%s' %(url, button_elems.get('href')) 
            
            # find books and download .txt files
            download_books_in_page(page)
            
            # employ random delay
            time.sleep(5+random.randint(2,10))
        except:
            # no "next page" button
            print('end of pages')
            break
    