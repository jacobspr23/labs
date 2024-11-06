from flask import Flask, render_template, request
from nasa_api import fetch_apod

app = Flask(__name__)

@app.route('/')
def home():
    """Landing Page - Shows the APOD for the current date."""
    try:
        data = fetch_apod()  # Fetch APOD for today by not passing a date
    except Exception as e:
        return f"Error fetching APOD: {e}"
    
    return render_template('home.html', apod=data)

@app.route('/history', methods=['GET', 'POST'])
def history():
    """History Page - Shows APOD for a specific date based on user input."""
    if request.method == 'POST':
        date = request.form.get('date')
        try:
            data = fetch_apod(date)  # Fetch APOD for the specified date
        except Exception as e:
            return f"Error fetching APOD for {date}: {e}"
        
        return render_template('history.html', apod=data, date=date)
    
    # Render the form if no POST request has been made
    return render_template('history.html')

if __name__ == "__main__":
    app.run()