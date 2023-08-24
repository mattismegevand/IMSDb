## IMSDb Scraper

A Python script that scrapes movie script details from the Internet Movie Script Database (IMSDb) website.

### Features:

- Fetches all script links available on IMSDb.
- Retrieves details for each movie script including:
  - Title
  - Poster Image URL
  - IMSDb Opinion
  - IMSDb Rating
  - Average User Rating
  - Writers
  - Genres
  - Script Date
  - Movie Release Date
  - Submitted By
  - Full Script Text

### Installation

1. Clone repository.

2. Install the required Python packages.
```bash
pip install -r requirements.txt
```

### Usage

1. Simply run the script.
```bash
python scraper.py
```

2. After the script runs, the extracted movie script details will be saved to `data.jsonl`.

### Error Handling

If any errors occur during scraping, they will be written to `error.txt` with the respective URL and error message.

### Contributing

Feel free to open issues or PRs if you find any problems or have improvements in mind.

### License

This project is licensed under the MIT License. See `LICENSE` for more details.
