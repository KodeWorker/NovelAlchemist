## Novel Alchemist

This project is for NaNoGenMo 2017.
The goal of this project is to generate a novel that can fool human readers.
The project progress can be checked on the development [blog](https://kodeworker.github.io/%E8%A8%88%E7%95%AB/%E7%A7%91%E5%B9%BB%E5%B0%8F%E8%AA%AA%E9%8D%8A%E6%88%90%E8%A8%88%E7%95%AB/) (It's in traditional Chinese :D).
This project contains four major parts:

1. Web scraping - scap free or public domain books with given genre
2. Text regularization - get the regular content from scraped text
2. Text generaton - use LSTM to generate sentences
3. GAN novel generation - use GAN to build a novel generator

### Dependencies
- [BeautifulSoup](http://docs.python-requests.org/en/master/) `bs4`
- [Requests](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) `requests`
- [ebooklib](https://github.com/KodeWorker/ebooklib) `ebooklib` (forked and modified from [ebooklib](https://github.com/aerkalov/ebooklib))
- [Matplotlib](https://matplotlib.org/) `matplotlib`

Clone this project and submodules
```
git clone --recursive https://github.com/KodeWorker/NovelAlchemist.git
```

### Web scrapping

#### Source
My favorite website option is [Project Gutenberg](http://www.gutenberg.org/).
However, the terms of use clearly states...
> **The Project Gutenberg website is for human users only.** Any real or perceived use of automated tools to access our site will result in a block of your IP address. This site utilizes cookies, captchas and related technologies to help assure the site is maximally available for human users only.

The second option is [Feedbooks](http://www.feedbooks.com/publicdomain).
This site also has a similar term to prevent scrapers, but the language is kinda okay.
I would test my luck if things are getting desperate.
> **6.15** use any robot, spider, scraper, or other automated means to access the FeedBooks Website bypass any measures FeedBooks may use to prevent or restrict access to the FeedBooks Website

Finally, I found [Manybooks](http://manybooks.net/).
This site contains books from "Project Gutenberg" and other internet archives.
Most importantly, it has no regulations on web scraping (or I just too blind to read.)

#### Details
- Run the scraper:
The default selection is "English Sci-Fi Novels".
If you want to scrap different genre or language, set the function (`sel_genre` and `sel_language`) parameter `select=None`.
```
python /web_scraping/novel_scraper.py
```

### Text Regularization
(under construction)

### Development Records
- 2017/07/19 - start building the web scraper
- 2017/07/20 - complete the web scraper
- 2017/07/21 - start building the text regularization

### To Do List
- Text generation
- GAN novel generation

### Known Issues
