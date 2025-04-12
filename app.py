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
    try:
        # Get the input data from the request
        data = request.json  # Expecting a list of customer records
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Convert the input data to a DataFrame
        try:
            df = pd.DataFrame(data)
        except Exception as e:
            return jsonify({'error': f'Error creating DataFrame: {str(e)}'}), 400

        # Ensure required columns are present
        required_columns = ['Name', 'Account Industry', 'Net Revenue Per Quarter',
                            'Days Since Last Deal', 'New Customer', 'Successful Deals Closed']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return jsonify({'error': f'Missing columns: {missing_columns}'}), 400

        # Extract the Name column and prepare the input features
        name = df['Name']
        X = df.drop(columns=['Name'])

        # Transform the data using the saved ColumnTransformer
        try:
            X = ct.transform(X)
        except Exception as e:
            return jsonify({'error': f'Error transforming data: {str(e)}'}), 500

        # Standardize the data using the saved StandardScaler
        try:
            X = sc.transform(X)
        except Exception as e:
            return jsonify({'error': f'Error scaling data: {str(e)}'}), 500

        # Make predictions
        try:
            prediction = model.predict(X)
            probability = model.predict_proba(X)[:, 1]  # Assuming binary classification
        except Exception as e:
            return jsonify({'error': f'Error making predictions: {str(e)}'}), 500

        # Prepare the response
        response = []
        for i in range(len(name)):
            response.append({
                'Customer': name.iloc[i],
                'Prediction': 'Will Continue' if probability[i] >= 0.55 else 'Will Not Continue',
                'Probability': probability[i]
            })

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)