import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Conduct consumer preference analysis using AI-driven surveys
def conduct_consumer_preference_analysis():
    # Load survey data
    df = pd.read_csv(r"C:\Users\Dell\Documents\SmartPlate AI-Powered Dietary Management for Personalized Nutrition\data\survey_data.csv")
    
    # Assume the survey data has columns 'preference' (target) and various features
    print(df.columns)

    # Check if 'preference' column exists before dropping
    if 'preference' in df.columns:
        X = df.drop('preference', axis=1)
        y = df['preference']
        
        # Convert date column to numeric
        if 'date' in X.columns:
            X['date'] = pd.to_datetime(X['date'])
            X['days_since_start'] = (X['date'] - X['date'].min()).dt.days
            X = X.drop(columns=['date'], errors='ignore')

        # Convert non-numeric columns to numeric or exclude them
        X = X.select_dtypes(include=[float, int])  # Keep only numeric columns

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train a Random Forest Classifier
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X_train, y_train)

        # Make predictions
        y_pred = clf.predict(X_test)

        # Evaluate the model
        print("Consumer Preference Analysis Report:")
        print(classification_report(y_test, y_pred))
        print("Accuracy:", accuracy_score(y_test, y_pred))
    else:
        # Handle case where 'preference' column is missing
        print("Error: 'preference' column not found in survey data.")
        return None  # or raise an exception

# Analyze real-world usage data to identify key improvements
def analyze_real_world_usage_data():
    # Load usage data
    df = pd.read_csv(r"C:\Users\Dell\Documents\SmartPlate AI-Powered Dietary Management for Personalized Nutrition\data\usage_data.csv")

    # Perform basic analysis (e.g., summary statistics)
    print("Real-World Usage Data Analysis:")
    print(df.describe())
    
    # Identify key improvements (e.g., correlation analysis)
    print(df.dtypes)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df['days_since_start'] = (df['date'] - df['date'].min()).dt.days
        df = df.drop(columns=['date'], errors='ignore')
    print(df.head())
    print(df.dtypes)
    # Select only numeric columns for correlation analysis
    numeric_df = df.select_dtypes(include=['number'])  # Keep only numeric columns for correlation
    correlation_matrix = numeric_df.corr()  # Calculate correlation on numeric data only
    print("Correlation Matrix:")
    print(correlation_matrix)

# Evaluate the impact of taste enhancement on sodium-restricted diets
def evaluate_taste_enhancement_impact():
    # Load taste enhancement data
    df = pd.read_csv(r"C:\Users\Dell\Documents\SmartPlate AI-Powered Dietary Management for Personalized Nutrition\data\taste_data.csv")
    
    # Assume the data has columns 'sodium_level', 'taste_score', and 'enhancement'
    X = df[['Sodium_Level (mg)', 'Enhancement']]
    y = df['Taste_Score']
    
    # Convert non-numeric columns to numeric or exclude them
    X = X.select_dtypes(include=[float, int])  # Keep only numeric columns

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train a Random Forest Regressor
    from sklearn.ensemble import RandomForestRegressor
    reg = RandomForestRegressor(n_estimators=100, random_state=42)
    reg.fit(X_train, y_train)
    
    # Make predictions
    y_pred = reg.predict(X_test)
    
    # Evaluate the model
    from sklearn.metrics import mean_squared_error, r2_score
    print("Taste Enhancement Impact Evaluation:")
    print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
    print("R^2 Score:", r2_score(y_test, y_pred))

# Main function
if __name__ == "__main__":
    # Example file paths (replace with actual file paths)
    survey_data =(r"C:\Users\Dell\Documents\SmartPlate AI-Powered Dietary Management for Personalized Nutrition\data\survey_data.csv")
    usage_data = (r"C:\Users\Dell\Documents\SmartPlate AI-Powered Dietary Management for Personalized Nutrition\data\usage_data.csv")
    taste_data = (r"C:\Users\Dell\Documents\SmartPlate AI-Powered Dietary Management for Personalized Nutrition\data\taste_data.csv")

    conduct_consumer_preference_analysis()
    analyze_real_world_usage_data()
    evaluate_taste_enhancement_impact()