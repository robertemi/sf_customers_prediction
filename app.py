from flask import Flask, request, jsonify
import pandas as pd
import pickle
import os

app = Flask(__name__)

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

    # Transform the data using the saved ColumnTransformer
    X = ct.transform(df)

    # Standardize the data using the saved StandardScaler
    X = sc.transform(X)

    # Make predictions
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1]  # Assuming binary classification

    # Return predictions and probabilities
    response = []
    for i, prediction in enumerate(predictions):
        response.append({
            'Customer': df.iloc[i]['Name'],  # Assuming 'Name' is in the input data
            'Prediction': 'Will Continue' if prediction == 1 else 'Will Not Continue',
            'Probability': probabilities[i]
        })

    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)