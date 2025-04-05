import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pickle

# Load the dataset
df = pd.read_csv('customers.csv')

# Separate features (X) and target (y)
X = df.drop(columns=['Name', 'Account Name', 'Will this customer continue to do business with us?'])
y = df['Will this customer continue to do business with us?']

# Define categorical features
categorical_features = ['Account Industry', 'New Customer']

# Create a ColumnTransformer for one-hot encoding
ct = ColumnTransformer(
    [('encoder', OneHotEncoder(sparse_output=False, handle_unknown='ignore'), categorical_features)],
    remainder='passthrough'
)

# Fit and transform the features
X = ct.fit_transform(X)

# Save the column names for one-hot encoding
one_hot_columns = ct.get_feature_names_out()

# Convert to DataFrame for easier handling
X = pd.DataFrame(X, columns=one_hot_columns)

# Standardize the features
sc = StandardScaler()
X = pd.DataFrame(sc.fit_transform(X), columns=one_hot_columns)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save the model, ColumnTransformer, and StandardScaler
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('column_transformer.pkl', 'wb') as f:
    pickle.dump(ct, f)

with open('scaler.pkl', 'wb') as f:
    pickle.dump(sc, f)