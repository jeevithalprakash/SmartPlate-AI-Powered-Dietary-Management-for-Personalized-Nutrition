import pandas as pd
import food_nlp
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Process user feedback via NLP models to improve personalization algorithms
def process_user_feedback():
    # Load feedback data
    df = pd.read_csv(r"C:\Users\Dell\Documents\SmartPlate AI-Powered Dietary Management for Personalized Nutrition\data\feedback_data.csv")
    
    # Assume the feedback data has columns 'feedback' (text) and 'satisfaction' (target)
    feedback = df['feedback']
    satisfaction = df['satisfaction']
    
    # Preprocess the feedback text
    stop_words = set(stopwords.words('english'))
    feedback_processed = feedback.apply(lambda x: ' '.join([word for word in word_tokenize(x.lower()) if word.isalnum() and word not in stop_words]))
    
    # Vectorize the feedback text using TF-IDF
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(feedback_processed)
    y = satisfaction
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train a Random Forest Classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    # Make predictions
    y_pred = clf.predict(X_test)
    
    # Evaluate the model
    print("User Feedback Sentiment Analysis Report:")
    print(classification_report(y_test, y_pred))
    print("Accuracy:", accuracy_score(y_test, y_pred))

# Detect patterns in user satisfaction levels and adaptation to the device
def detect_user_satisfaction_patterns():
    # Load feedback data
    df = pd.read_csv(r"C:\Users\Dell\Documents\SmartPlate AI-Powered Dietary Management for Personalized Nutrition\data\feedback_data.csv")
    
    # Assume the feedback data has columns 'feedback' (text) and 'satisfaction' (target)
    feedback = df['feedback']
    satisfaction = df['satisfaction']
    
    # Preprocess the feedback text
    stop_words = set(stopwords.words('english'))
    feedback_processed = feedback.apply(lambda x: ' '.join([word for word in word_tokenize(x.lower()) if word.isalnum() and word not in stop_words]))
    
    # Vectorize the feedback text using TF-IDF
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(feedback_processed)
    y = satisfaction
    
    # Train a Random Forest Classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    
    # Detect patterns (e.g., feature importance)
    feature_importances = clf.feature_importances_
    feature_names = vectorizer.get_feature_names_out()
    important_features = sorted(zip(feature_importances, feature_names), reverse=True)[:10]
    
    print("Top 10 Important Features for User Satisfaction:")
    for importance, feature in important_features:
        print(f"{feature}: {importance}")

# Predict potential improvements based on consumer sentiment analysis
def predict_potential_improvements():
    # Load feedback data
    df = pd.read_csv(r"C:\Users\Dell\Documents\SmartPlate AI-Powered Dietary Management for Personalized Nutrition\data\feedback_data.csv")
    
    # Assume the feedback data has columns 'feedback' (text) and 'improvement_score' (target)
    feedback = df['feedback']
    improvement_score = df['improvement_score']
    
    # Preprocess the feedback text
    stop_words = set(stopwords.words('english'))
    feedback_processed = feedback.apply(lambda x: ' '.join([word for word in word_tokenize(x.lower()) if word.isalnum() and word not in stop_words]))
    
    # Vectorize the feedback text using TF-IDF
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(feedback_processed)
    y = improvement_score
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train a Linear Regression model
    reg = LinearRegression()
    reg.fit(X_train, y_train)
    
    # Make predictions
    y_pred = reg.predict(X_test)
    
    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print("Potential Improvements Prediction Evaluation:")
    print("Mean Squared Error:", mse)
    print("R^2 Score:", r2)

# Main function
if __name__ == "__main__":
    # Example file path (replace with actual file path)
    feedback_data = r"C:\Users\Dell\Documents\SmartPlate AI-Powered Dietary Management for Personalized Nutrition\data\feedback_data.csv"
    
    process_user_feedback()
    detect_user_satisfaction_patterns()
    predict_potential_improvements()