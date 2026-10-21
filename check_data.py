
import pandas as pd

data = pd.read_csv("data/student-mat.csv", sep=";")

print("Dataset loaded successfully!")
print("Number of rows and columns:", data.shape)

print("\nFirst five rows:")
print(data.head())

print("\nColumn names:")
print(data.columns.tolist())

