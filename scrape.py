#!/usr/bin/env python

import re
import bs4
import json
import requests

from tqdm import tqdm

BASE_URL = "https://imsdb.com"

def get_all_links():
  try:
    response = requests.get(BASE_URL + '/all-scripts.html')
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    links = soup.findAll('td', {'valign': 'top'})[-1].findAll('a')
    return [BASE_URL + l.get('href') for l in links]
  except requests.RequestException as e:
    print(f"Error fetching all links: {e}")
    return []

def retrieve_script(url):
  try:
    response = requests.get(url)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    return soup.find('td', {'class': 'scrtext'}).find('pre').text
  except Exception as e:
    raise ValueError(f"Error retrieving script from {url}: {e}")

def process_link(url):
  try:
    response = requests.get(url)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    table = soup.find('table', {'class': 'script-details'})
    title = table.find('h1').text
    poster = table.find('td', {'align': 'right', 'valign': 'top'}).find('img').get('src')

    texts = table.find('b', string='IMSDb opinion').parent.text
    patterns = {
      'IMSDb_opinion': r"IMSDb opinion\s+(?P<opinion>.+?)\n",
      'IMSDb_rating': r"IMSDb rating\s+(?P<rating>.+?)\n",
      'average_user_rating': r"Average user rating\s+\((?P<rating>[\d.]+)(?: out of \d+)?",
      'writers': r"Writers\s+(?P<writers>.+?)\n",
      'genres': r"Genres\s+(?P<genres>.+?)\n",
      'script_date': r"Script Date : (?P<date>[\w\s]+?)\n",
      'movie_release_date': r"Movie Release Date : (?P<date>[\w\s]+?)\n",
      'submitted_by': r"Submitted by: (?P<submitter>\w+)\n"
    }
    d = {}
    for k, pattern in patterns.items():
      match = re.search(pattern, texts)
      if match:
        if k in ['writers', 'genres']:
          d[k] = re.split(r'\s{2,}', match.group(1))
        else:
          d[k] = match.group(1)
    d['title'] = title[:-len(' Script')]
    d['poster'] = poster
    script_url = BASE_URL + soup.find('a', href=re.compile(r'/scripts/')).get('href')
    d['script'] = retrieve_script(script_url)
    return d
  except Exception as e:
    with open("error.txt", "a") as error_file:
      error_file.write(f"{url}: {e}\n")
    return None

if __name__ == "__main__":
  links = get_all_links()
  data = []

  for link in tqdm(links, desc="Processing links"):
    result = process_link(link)
    if result:
      data.append(result)

  all_keys = set().union(*(d.keys() for d in data))
  keys = data[0].keys()
  with open('data.jsonl', 'w') as file:
    for d in data:
      file.write(json.dumps(d) + '\n')
