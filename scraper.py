import requests
from bs4 import BeautifulSoup
import datetime

def fetch_word_of_the_day():
    url = "https://www.merriam-webster.com/word-of-the-day"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract Word
        word_header = soup.find('h2', class_='word-header-txt')
        if not word_header:
            print("Could not find word header")
            return None
        word = word_header.get_text().strip()
        
        # Extract Part of Speech and Pronunciation (usually in the same block)
        # The structure can vary, but usually it's under 'word-attributes'
        attributes = soup.find('div', class_='word-attributes')
        part_of_speech = "N/A"
        if attributes:
            pos_span = attributes.find('span', class_='main-attr')
            if pos_span:
                part_of_speech = pos_span.get_text().strip()

        # Extract Definition
        # Usually under 'wod-definition-container' -> 'p'
        definition_container = soup.find('div', class_='wod-definition-container')
        definition = "No definition found."
        if definition_container:
            # Get the first paragraph or the one starting with " : "
            paragraphs = definition_container.find_all('p')
            for p in paragraphs:
                text = p.get_text().strip()
                if text.startswith(':'): # Standard dictionary definition style
                    definition = text
                    break
                elif text and not text.startswith('//'): # Fallback to first non-example
                     definition = text
                     break
        
        # Extract Example (often marked with //)
        example = "No example found."
        if definition_container:
             paragraphs = definition_container.find_all('p')
             for p in paragraphs:
                 text = p.get_text().strip()
                 if text.startswith('//'):
                     example = text.lstrip('/ ').strip()
                     break

        # Date
        today = datetime.date.today().isoformat()

        return {
            "word": word,
            "part_of_speech": part_of_speech,
            "definition": definition,
            "example": example,
            "date": today,
            "url": url
        }

    except Exception as e:
        print(f"Error fetching word of the day: {e}")
        return None

if __name__ == "__main__":
    data = fetch_word_of_the_day()
    if data:
        print("Successfully fetched Word of the Day:")
        print(f"Word: {data['word']}")
        print(f"Date: {data['date']}")
        print(f"Part of Speech: {data['part_of_speech']}")
        print(f"Definition: {data['definition']}")
        print(f"Example: {data['example']}")
    else:
        print("Failed to fetch data.")
