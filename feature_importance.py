
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

# Load the dataset
df = pd.read_csv("data/student-mat.csv", sep=";")

# Remove grades G1, G2 and G3 from the input features
X = df.drop(columns=["G1", "G2", "G3"])
y = df["G3"]

# Identify categorical and numerical columns
categorical_cols = X.select_dtypes(
    include=["object"]
).columns.tolist()

numerical_cols = X.select_dtypes(
    exclude=["object"]
).columns.tolist()

# Prepare the data
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"),
         categorical_cols),
        ("num", "passthrough", numerical_cols)
    ]
)

# Create and train the model
model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=200,
        random_state=42
    ))
])

model.fit(X, y)

# Get importance of each encoded feature
importance = model.named_steps[
    "regressor"
].feature_importances_

feature_names = model.named_steps[
    "preprocessor"
].get_feature_names_out()

# Match each encoded feature to its original column
results = pd.DataFrame({
    "Encoded_Feature": feature_names,
    "Importance": importance
})

# Combine encoded categories into their original feature
results["Original_Feature"] = results[
    "Encoded_Feature"
].apply(
    lambda name: name.split("__", 1)[1].split("_")[0]
    if name.startswith("cat__")
    else name.split("__", 1)[1]
)

summary = results.groupby(
    "Original_Feature"
)["Importance"].sum().sort_values(
    ascending=False
)

print("\nFEATURE IMPORTANCE RANKING")
print(summary.head(10).round(4))

summary.sort_values().plot(
    kind="barh",
    title="Feature Importance for Predicting Final Grade",
    xlabel="Importance",
    figsize=(10, 7)
)

import matplotlib.pyplot as plt
plt.tight_layout()
plt.savefig("feature_importance.png")
plt.show()

summary.to_csv("feature_importance.csv")
print("\nSaved feature_importance.csv and feature_importance.png")
