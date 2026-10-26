from flask import Flask, request, jsonify, render_template
import os
import pandas as pd
from ai_analysis import extract_pdf_data, analyze_data, perform_clustering, create_sales_chart  # Import necessary functions

app = Flask(__name__)  # Initialize Flask app


# Homepage route
@app.route('/')
def home():
    return render_template('home.html')


# About page route
@app.route('/about')
def about():
    return render_template('about.html')  # This will serve the "About" page


# Contact page route
@app.route('/contact')
def contact():
    return render_template('contact.html')  # This will serve the "Contact" page


# File upload and analysis route
@app.route('/analyze', methods=['POST'])
def analyze():
    # Ensure a file is uploaded
    if 'uploaded_file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['uploaded_file']
    file_path = os.path.join('data', file.filename)
    file.save(file_path)
    print(f"File saved to: {file_path}")

    # Detect file type and process
    try:
        if file.filename.endswith('.csv'):
            data = pd.read_csv(file_path)
            print("CSV file successfully read!")
        elif file.filename.endswith('.pdf'):
            data = extract_pdf_data(file_path)
            print("PDF file successfully read and processed!")
        else:
            return jsonify({"error": "Unsupported file format. Please upload a CSV or PDF file."}), 400
    except Exception as e:
        print(f"Error reading the file: {e}")
        return jsonify({"error": "Error processing the file. Please check the format and try again."}), 500

    # Perform analysis
    try:
        results = analyze_data(data)
        clusters = perform_clustering(data)
        print("Data analysis and clustering completed!")
    except Exception as e:
        print(f"Error during data analysis: {e}")
        return jsonify({"error": "Error performing data analysis."}), 500

    # Generate charts
    try:
        sales_chart_path = 'static/sales_chart.html'
        create_sales_chart(data, sales_chart_path)
        print("Sales chart created successfully!")
    except Exception as e:
        print(f"Error generating charts: {e}")
        return jsonify({"error": "Error generating visualizations."}), 500

    return render_template('results.html', results=results, clusters=clusters.to_html(), chart_path=sales_chart_path)


# Run Flask application
if __name__ == '__main__':
    app.run(debug=True)
