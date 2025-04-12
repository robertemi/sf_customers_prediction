from flask import Flask, request, jsonify
import pandas as pd
import pickle
from dotenv import load_dotenv
import os
from simple_salesforce import Salesforce

load_dotenv()

app = Flask(__name__)

# Get Salesforce credentials from environment variables
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
username = os.environ.get('SF_USERNAME')
password = os.environ.get('PASSWORD')
security_token = os.environ.get('SECURITY_TOKEN')
instance_url = os.environ.get('SALESFORCE_INSTANCE_URL')

# Authenticate with Salesforce
sf = Salesforce(
    username=username,
    password=password,
    security_token=security_token
    #domain='test'  # Use 'test' for sandbox or 'login' for production
)

# Load the trained model, ColumnTransformer, and StandardScaler
model = pickle.load(open('model.pkl', 'rb'))
ct = pickle.load(open('column_transformer.pkl', 'rb'))
sc = pickle.load(open('scaler.pkl', 'rb'))

@app.route('/')
def home():
    return "Welcome to the Prediction API!"

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the request
    data = request.json  # Expecting a list of customer records
    df = pd.DataFrame(data)

    name = df['Name']
    X = df.drop(columns=['Name'])
    # Transform the data using the saved ColumnTransformer
    X = ct.transform(X)


    # Standardize the data using the saved StandardScaler
    X = sc.transform(X)

    # Make predictions
    prediction = model.predict(X)
    probability = model.predict_proba(X)[:, 1]  # Assuming binary classification

    # Return predictions and probabilities
    response = [{'Customer ': name,
                 'Prediction': 'Will Continue' if prediction >= 0.55 else 'Will Not Continue',
                 'Probability': probability}]

    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)