import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
data = pd.read_csv("data/commands.csv")
X = data["command"]
y = data["label"]

# Convert text to numbers
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# Train Logistic Regression model
model = LogisticRegression()
model.fit(X_vec, y)

# Save model and vectorizer
with open("model/logistic_model.pkl", "wb") as f:
    pickle.dump((model, vectorizer), f)

print("Model trained and saved successfully")