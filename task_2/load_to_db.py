"""Import qoutes.json and authors.json into MongoDB Atlas."""
import json
from pymongo import MongoClient
from config import MONGO_URL


def load_json(filename):
    """
    Read a JSON file and return its content as a Python list.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    """
    Load quotes and authors from JSON files into MongoDB Atlas collections without creating duplicates.
    """
    try:
        client = MongoClient(MONGO_URL)
        db = client['quotes_db']

        quotes = load_json('quotes.json')
        authors = load_json('authors.json')

        db['quotes'].delete_many({})
        db['authors'].delete_many({})

        db['quotes'].insert_many(quotes)
        db['authors'].insert_many(authors)

    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()