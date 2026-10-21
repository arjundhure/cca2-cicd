
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

data = pd.read_csv("data/student-mat.csv", sep=";")

X = data.drop(columns=["G1", "G2", "G3"])
y = data["G3"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

categorical_cols = X.select_dtypes(include=["str", "object"]).columns.tolist()
numerical_cols = X.select_dtypes(exclude=["str", "object"]).columns.tolist()

def create_model(regressor):
    preprocessor = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", "passthrough", numerical_cols)
    ])

    return Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", regressor)
    ])

models = {
    "Random Forest": RandomForestRegressor(
        n_estimators=200, random_state=42
    ),
    "Gradient Boosting": GradientBoostingRegressor(
        random_state=42
    ),
    "Decision Tree": DecisionTreeRegressor(
        random_state=42
    )
}

results = []

for name, algorithm in models.items():
    model = create_model(algorithm)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    results.append({
        "Model": name,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    })

    print(f"\n{name}")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2 Score: {r2:.3f}")

comparison = pd.DataFrame(results).sort_values("MAE")
comparison.to_csv("early_model_comparison.csv", index=False)

print("\nFINAL COMPARISON")
print(comparison.to_string(index=False))

plt.figure(figsize=(9, 5))
plt.bar(comparison["Model"], comparison["MAE"])
plt.ylabel("Mean Absolute Error (lower is better)")
plt.title("Early Student Grade Prediction: Model Comparison")
plt.tight_layout()
plt.savefig("early_model_comparison.png", dpi=150)
plt.show()