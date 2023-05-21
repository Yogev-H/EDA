from flask import Flask, render_template, request
import pandas as pd
from pandas_profiling import ProfileReport
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return render_template('index.html', message='No file selected')

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', message='No file selected')

    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file, encoding='utf-8')
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            return render_template('index.html', message='Invalid file format')
        
        if df.empty:
            return render_template('index.html', message='Empty file')

    except UnicodeDecodeError:
        # Handle encoding error
        df = pd.read_csv(file, encoding='latin-1')
        if df.empty:
            return render_template('index.html', message='Empty file')

    profile = ProfileReport(df)
    profile.to_file("static/report.html")

    return render_template('report.html')

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
