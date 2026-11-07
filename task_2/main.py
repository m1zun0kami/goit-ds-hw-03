"""Scrape quotes.toscrape.com and save quotes and authors to JSON files."""
import requests, json
from bs4 import BeautifulSoup
URL = 'https://quotes.toscrape.com'


def parse_page(soup):
    """
    Extract quotes and author links from one parsed page.
    :return: a list of quote dicts and a set of author page links.
    """
    quotes_list = []
    author_links = set()

    for block in soup.find_all('div', class_='quote'):
        text = block.find('span', class_='text').text
        author = block.find('small', class_='author').text
        tags_list = [t.text for t in block.find_all('a', class_='tag')]
        link = block.find('a')['href']

        quotes_list.append(
            {
                'tags': tags_list,
                'author': author,
                'quote': text
            }
        )
        author_links.add(link)

    return quotes_list, author_links


def scrape_quotes():
    """
    Scrape all pages of the site by following the 'Next' button.
    :return: all quotes and a set of unique author page links.
    """
    all_quotes = []
    all_author_links = set()
    next_page = '/'

    while next_page:
        try:
            response = requests.get(URL + next_page)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')

            quotes_list, author_links = parse_page(soup)
            all_quotes.extend(quotes_list)
            all_author_links.update(author_links)

            next_btn = soup.find('li', class_='next')

            if next_btn:
                next_page = next_btn.find('a')['href']
            else:
                next_page = None
        except requests.RequestException as e:
            print(f'Error: {e}')
            next_page = None

    return all_quotes, all_author_links


def parse_author(link):
    """
    Scrape one author page.
    :return:a dict with fullname, born_date, born_location and description (None if the request fails).
    """
    try:
        response = requests.get(URL + link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        fullname = soup.find('h3', class_='author-title').text.strip()
        born_date = soup.find('span', class_='author-born-date').text.strip()
        born_location = soup.find('span', class_='author-born-location').text.strip()
        description = soup.find('div', class_='author-description').text.strip()

        return {
            'fullname': fullname,
            'born_date': born_date,
            'born_location': born_location,
            'description': description
        }

    except requests.RequestException as e:
        print(f'Error: {e}')
        return None


all_quotes, all_author_links = scrape_quotes()
authors = []

for link in all_author_links:
    author = parse_author(link)
    if author:
        authors.append(author)


try:
    with open('quotes.json', 'w', encoding='utf-8') as f:
        json.dump(all_quotes, f, ensure_ascii=False, indent=2)

    with open('authors.json', 'w', encoding='utf-8') as f:
        json.dump(authors, f, ensure_ascii=False, indent=2)
except OSError as e:
    print(f'Error: {e}')