import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score, classification_report

# Collect historical data for S&P 500 using yfinance
data = yf.download('^GSPC', start='2020-01-01', end='2024-01-01')

# Calculate technical indicators: 200-day MA, RSI, MACD, Bollinger Bands
# (You need to implement functions to calculate these indicators)

# Generate labels: 1-week return and binary label indicating up/down
data['1w_return'] = (data['Close'].shift(-5) - data['Close']) / data['Close']
data['Label'] = (data['1w_return'] > 0).astype(int)

# Select features and labels
X = data[['200_MA', 'RSI', 'MACD', 'Upper_BB', 'Lower_BB']].values
y = data['Label'].values

# Data preprocessing: Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train the perceptron model
model = Perceptron()
model.fit(X_train, y_train)

# Predictions
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

# Model evaluation
train_accuracy = accuracy_score(y_train, y_pred_train)
test_accuracy = accuracy_score(y_test, y_pred_test)

print("Training Accuracy:", train_accuracy)
print("Test Accuracy:", test_accuracy)

# Classification report
print("Classification Report:")
print(classification_report(y_test, y_pred_test))