from flask import Flask, render_template_string, jsonify
import threading
import time
import schedule
from scraper import fetch_word_of_the_day
from storage import save_word, get_history
from notifier import send_daily_word
import datetime

app = Flask(__name__)

def job():
    print(f"Running scheduled job at {datetime.datetime.now()}")
    word_data = fetch_word_of_the_day()
    if word_data:
        if save_word(word_data):
            print(f"New word saved: {word_data['word']}")
            if send_daily_word(word_data):
                print("Notification sent.")
            else:
                print("Failed to send notification.")
        else:
            print("Word already exists in history.")
    else:
        print("Failed to fetch word.")

def run_schedule():
    # Schedule the job every day at 09:00 AM
    schedule.every().day.at("09:00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(60)

# Start scheduler in a separate thread
threading.Thread(target=run_schedule, daemon=True).start()

@app.route('/')
def index():
    history = get_history()
    # Sort by date descending
    history.sort(key=lambda x: x['date'], reverse=True)
    
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Word of the Day History</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f9; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
            h1 { text-align: center; color: #444; }
            .card { background: white; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); padding: 20px; margin-bottom: 20px; }
            .word { font-size: 1.5em; font-weight: bold; color: #2c3e50; }
            .pos { color: #7f8c8d; font-style: italic; }
            .date { float: right; color: #95a5a6; font-size: 0.9em; }
            .definition { margin-top: 10px; line-height: 1.6; }
            .example { margin-top: 10px; background: #f9f9f9; padding: 10px; border-left: 4px solid #3498db; font-style: italic; }
            /*.link { display: block; margin-top: 10px; text-align: right; }*/
            /*a { color: #3498db; text-decoration: none; }*/
            /*a:hover { text-decoration: underline; }*/
            /*.controls { text-align: center; margin-bottom: 20px; }*/
            /*button { background-color: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 1em; }*/
            /* button:hover { background-color: #2980b9; }*/
        </style>
    </head>
    <body>
        <h1>Word of the Day History</h1>
        <div class="controls">
            <button onclick="triggerCheck()">Check for New Word Now</button>
        </div>
        <div id="status" style="text-align: center; margin-bottom: 10px; color: green;"></div>
        
        {% for item in history %}
        <div class="card">
            <div class="date">{{ item.date }}</div>
            <div class="word">{{ item.word }} <span class="pos">({{ item.part_of_speech }})</span></div>
            <div class="definition">{{ item.definition }}</div>
            <div class="example">"{{ item.example }}"</div>
          /*  <div class="link"><a href="{{ item.url }}" target="_blank">Read on Merriam-Webster</a></div> */
        </div>
        {% endfor %}

        <script>
            function triggerCheck() {
                document.getElementById('status').innerText = "Checking...";
                fetch('/run-now')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('status').innerText = data.message;
                        setTimeout(() => location.reload(), 2000);
                    })
                    .catch(err => {
                        document.getElementById('status').innerText = "Error occurred.";
                        console.error(err);
                    });
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html, history=history)

@app.route('/run-now')
def run_now():
    job()
    return jsonify({"message": "Check completed. Refreshing..."})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
