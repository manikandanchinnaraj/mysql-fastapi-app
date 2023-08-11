import json
import random
from random import randrange

import requests


def generate_books_authors():
    books_author = []
    choices = ["Mani", "Manikandan", "Chinn", "Chinnaraj", "Human", "Robot"]
    for i in range(100, 200):
        books_author.append(
            {"title": f"Writing-Book-{i}",
             "number_of_pages": randrange(100, 500),
             "first_name": random.choice(choices),
             "last_name": random.choice(choices),
             }
        )

    return books_author


def add_books_authors():
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    book_authors = generate_books_authors()

    for book_auth in book_authors:
        print(book_auth, end="\n")
        payload = {
            "book": {
                "title": book_auth['title'],
                "number_of_pages": book_auth['number_of_pages']
            },
            "author": {
                "first_name": book_auth['first_name'],
                "last_name": book_auth['last_name']
            }
        }

        response = requests.post(
            url="http://127.0.0.1:8000/book", headers=headers, data=json.dumps(payload), verify=False
        )

        if response.status_code == 200:
            "The post request is successful"

        response.raise_for_status()

        print(response.json())


if __name__ == '__main__':
    add_books_authors()
