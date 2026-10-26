import pandas as pd
from sklearn.cluster import KMeans
from PyPDF2 import PdfReader
import plotly.express as px
import os
from sklearn.preprocessing import LabelEncoder

# Extract text from PDF and convert to structured DataFrame
def extract_pdf_data(file_path):
    """Extracts text from PDF and converts it into a structured DataFrame."""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found. Please check if the file exists.")
        return None  # Return None instead of crashing

    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    # Split text into lines
    lines = text.strip().split("\n")

    # Skip the header line (Customer Name, Age, Product, etc.)
    data_rows = lines[1:]

    # Convert into structured DataFrame
    structured_data = []
    for row in data_rows:
        columns = row.split(",")  # Ensure consistent splitting
        if len(columns) == 6:  # Ensure correct format
            structured_data.append(columns)

    # Define DataFrame with column names
    df = pd.DataFrame(structured_data, columns=["Customer Name", "Age", "Product", "Category", "Occupation", "Purchase Date"])

    # Convert Age to integer
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")

    # Extract Month from Purchase Date
    df["Month"] = pd.to_datetime(df["Purchase Date"], errors="coerce").dt.strftime('%B')

    return df  # Return structured DataFrame

# Analyze data
def analyze_data(data):
    if "Month" not in data.columns:
        data["Month"] = pd.to_datetime(data["Purchase Date"], errors="coerce").dt.strftime('%B')

    results = {
        "most_purchased_product": data["Product"].mode()[0],
        "popular_age_group": data["Age"].value_counts().idxmax(),
        "popular_category": data["Category"].value_counts().idxmax(),
        "popular_occupation": data["Occupation"].value_counts().idxmax(),
        "popular_month": data["Month"].value_counts().idxmax(),
    }
    return results

# Encode categorical variables
def encode_categorical_columns(data):
    """Encodes categorical columns into numeric values"""
    categorical_columns = data.select_dtypes(include=['object']).columns  # Find text columns
    encoder = LabelEncoder()
    for col in categorical_columns:
        data[col] = encoder.fit_transform(data[col])
    return data

# Perform clustering
def perform_clustering(data):
    # Encode categorical variables
    le = LabelEncoder()
    data["Category_Encoded"] = le.fit_transform(data["Category"])

    # Select features for clustering
    features = data[['Age', 'Category_Encoded']]  # Now numeric

    # Apply K-Means
    kmeans = KMeans(n_clusters=3, random_state=42)
    data['Cluster'] = kmeans.fit_predict(features)
def perform_clustering(data):
    # Select only numeric columns
    numeric_data = data.select_dtypes(include=['number'])
    print("Numeric Data for Clustering:")
    print(numeric_data.head())  # Debugging step: Check numeric data
    print(numeric_data.dtypes)  # Check data types of columns

    # Perform clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    data['Cluster'] = kmeans.fit_predict(numeric_data)

    # Verify clusters and grouping
    print("Cluster Labels:", data['Cluster'].unique())
    try:
        cluster_means = numeric_data.groupby(data['Cluster']).mean()
        print("Cluster Means:", cluster_means)
        return cluster_means
    except Exception as e:
        print(f"Error during aggregation: {e}")
        raise


    return data.groupby('Cluster').mean()

# Create a sales chart
def create_sales_chart(data, output_path):
    if "Month" not in data.columns:
        data["Month"] = pd.to_datetime(data["Purchase Date"], errors="coerce").dt.strftime('%B')

    monthly_sales = data['Month'].value_counts()
    fig = px.bar(
        x=monthly_sales.index, y=monthly_sales.values,
   
 title="Monthly Sales Trends",
        color_discrete_sequence=px.colors.qualitative.Set2  # Ensure this line is correct
    )  

    fig.update_layout(template="plotly_white")
    fig.write_html(output_path)