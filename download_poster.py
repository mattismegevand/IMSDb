#!/usr/bin/env python

import os
import json
import requests

from tqdm import tqdm

def save_poster(title, url, folder='poster'):
  img_data = requests.get(url).content
  safe_title = "".join([c if c.isalnum() else "_" for c in title])
  with open(os.path.join(folder, f"{safe_title}.jpg"), 'wb') as handler:
    handler.write(img_data)

def get_links_from_jsonl(file_path):
  with open(file_path, 'r') as file:
    for line in file:
      data = json.loads(line)
      if data['poster'] == "/images/no-poster.gif":
        continue
      yield data['title'], data['poster']

def main():
  if not os.path.exists('poster'):
    os.makedirs('poster')

  links = list(get_links_from_jsonl('data.jsonl'))
  for title, poster_url in tqdm(links, desc="Downloading posters"):
    try:
      save_poster(title, poster_url)
    except Exception as e:
      with open("error.txt", "a") as error_file:
        error_file.write(f"Error saving poster for {title}: {e}\n")

if __name__ == "__main__":
  main()
