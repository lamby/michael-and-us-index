#!/usr/bin/env python3

import click
import daiquiri
import hashlib
import itertools
import logging
import os
import re
import requests
import sys
import time
import urllib
import yaml

from bs4 import BeautifulSoup

@click.command()
@click.argument("url")
def main(url):
    r = requests.get(url)
    r.raise_for_status()

    soup = BeautifulSoup(r.content, features='xml')

    episodes = []
    bonus = []

    for x in soup.findAll('item'):
        title = x.find('title').text
        link = x.find('link').text
        published = x.find('pubDate').text
        description = x.find('description').text

        # Try and parse episode number out of title
        number = None
        m = re.search(r'^\#(?P<number>\d+)\s*-\s*(?P<title>.+)', title)
        if m is not None:
            number = int(m.group("number"))
            title = m.group("title")

        # Try and strip "BONUS" from title
        m = re.search(r'^BONUS(?:\s+CONTENT)?\s*[-:]\s+(?P<title>.+)', title)
        if m is not None:
            title = m.group("title")

        # Treat episodes without a number as bonus content
        if not number:
            bonus.append({
                "title": title,
                "link": link,
                "date": published,
            })
            continue

        # Try and parse films out of the description
        films = []
        for m in re.finditer(r"\b(?P<title>[A-Z][A-Z'\.:]+(?:\s+[A-Z'\.:\&]+)+)\b(?:\s\((?P<year>\d\d\d\d)\))?", description):
            film_title = m.group("title").strip()
            film_year = m.group("year")

            # Ignore some false positives
            for needle in ("PLUS", "NOTE"):
                if film_title.startswith(needle):
                    continue

            films.append({
                "title": film_title,
                "year": film_year,
            })

        if not films:
            print("-")
            print(description)


        episodes.append({
            'number': number,
            'title': title,
            'link': link,
            'date': published,
            'films': films,
        })

    episodes.reverse()
    bonus.reverse()

    with open("_data/episodes.yml", "w") as f:
        f.write(yaml.dump(episodes))

    with open("_data/bonus.yml", "w") as f:
        f.write(yaml.dump(bonus))


if __name__ == "__main__":
    sys.exit(main())
