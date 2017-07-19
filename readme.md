## Novel Alchemist

This project is for NaNoGenMo 2017.
The goal of this project is to generate a novel that can fool human readers.
This project contains three major parts:

1. Web scraping - scap free or public domain books with given genre
2. Text generaton - use LSTM to generate sentences
3. GAN novel generation - use GAN to build a novel generator

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

### Development Records
- 2017/07/19 - start building the web scraper  
