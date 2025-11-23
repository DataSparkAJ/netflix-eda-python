# import kagglehub
# import shutil

# # Download latest version
# path = kagglehub.dataset_download("shivamb/netflix-shows")

# print("Path to dataset files:", path)
# # my custom path
# new_path = r"D:/PythonJourney/Numpy/Netflix_EDA_Project/Data"
# # move downloaded folder to new path
# shutil.move(path,new_path)
# print("Dataset moved to:", new_path)

# Importing necessary libraries

import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("D:/PythonJourney/Netflix_EDA_Project/Data/netflix_titles.csv")

print("Shape:", df.shape)
print("\nPreview:")
print(df.head())
print("\nInfo:")
df.info()
print("\nDuplicate rows:", df.duplicated().sum())

# ===== DATA CLEANING ===== #

# Fill missing categorical values
df['director'].fillna('Unknown', inplace=True)
df['cast'].fillna('Unknown', inplace=True)
df['country'].fillna('Unknown', inplace=True)
df['rating'].fillna('Unknown', inplace=True)

# Remove extra spaces in text columns
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Convert date column and extract features
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['added_year'] = df['date_added'].dt.year
df['added_month'] = df['date_added'].dt.month

# Extract duration number and unit
df['duration_num'] = df['duration'].str.extract('(\d+)').astype(float)
df['duration_unit'] = df['duration'].str.extract('([A-Za-z]+)')

print("\nMissing values after cleaning:")
print(df.isnull().sum())

# ===== EDA ===== #

print("\nType distribution:")
print(df['type'].value_counts())
print("\nType distribution (%):")
print(df['type'].value_counts(normalize=True) * 100)

print("\nYear-wise additions:")
print(df['added_year'].value_counts().sort_index())

print("\nTop countries:")
print(df['country'].value_counts().head(10))

print("\nTop genres:")
print(df['listed_in'].value_counts().head(10))

print("\nAverage movie duration (mins):")
print(np.mean(df[df['type'] == 'Movie']['duration_num']))

print("\nAverage TV show seasons:")
print(np.mean(df[df['type'] == 'TV Show']['duration_num']))

print("\nMost common ratings:")
print(df['rating'].value_counts().head(10))

# Longest and shortest duration ,idxmax() yeh function maximum value ka index (row number) return karta hai.

print("\nLongest title:")
print(df.loc[df['duration_num'].idxmax(), ['title', 'type', 'duration', 'country']])

print("\nShortest title:")
print(df.loc[df['duration_num'].idxmin(), ['title', 'type', 'duration', 'country']])
