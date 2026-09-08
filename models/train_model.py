import pandas as pd
import sqlite3
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

def train_real_estate_model():
    db_path = "database/real_estate.db"
    if not os.path.exists(db_path):
        print("[ERROR] Database file not found!")
        return

    # Load data from SQLite database
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM tunisia_real_estate", conn)
    conn.close()

    print(f"[INFO] Loaded {len(df)} records for training.")

    # Select Features and Target
    features = ["surface_m2", "rooms", "latitude", "longitude"]
    target = "price_tnd"

    X = df[features]
    y = df[target]

    # Train/Test Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model Training: Random Forest Regressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluation
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print(f"[MODEL EVALUATION] Mean Absolute Error (MAE): {mae:,.2f} TND")
    print(f"[MODEL EVALUATION] R² Score: {r2:.4f}")

    # Save trained model pipeline artifact
    model_dir = "models"
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "real_estate_model.pkl")
    joblib.dump(model, model_path)
    print(f"[SUCCESS] Model successfully saved to {model_path}")

if __name__ == "__main__":
    train_real_estate_model()