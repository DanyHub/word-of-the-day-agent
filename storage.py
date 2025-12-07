import json
import os

WORDS_FILE = 'words.json'

def load_history():
    if not os.path.exists(WORDS_FILE):
        return []
    try:
        with open(WORDS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_word(word_data):
    history = load_history()
    
    # Check if word already exists for this date
    for entry in history:
        if entry['date'] == word_data['date'] and entry['word'] == word_data['word']:
            return False # Already saved
            
    history.append(word_data)
    
    with open(WORDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4, ensure_ascii=False)
    
    return True

def get_history():
    return load_history()
