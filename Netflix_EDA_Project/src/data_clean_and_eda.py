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
import matplotlib.pyplot as plt


# Step 1: Load & Initial Inspection
df = pd.read_csv(r"D:\PythonJourney\Netflix_EDA_Project\Data\netflix_titles.csv")

# Column names ko clean karna (Sabse pehle taaki handling aasaan ho)
df.columns = df.columns.str.strip().str.lower().str.replace(' ','_')

print('--- Initial Shape ---')
print(df.shape)
print(df.head())
print(df.info())


# STEP 2: TEXT CLEANING (Sabse Pehle)
# Reason: "Movie " (space ke sath) aur "Movie" alag maane jate hain.
# Pehle strip kar denge toh duplicates sahi pakde jayenge.
df = df.apply(lambda x : x.str.strip() if x.dtype == 'object' else x)


# STEP 3: REMOVE DUPLICATES
# Ab clean text ke basis par duplicates check karo
dup_count = df.duplicated().sum()
if dup_count > 0:
  df.drop_duplicates(inplace = True)
  print(f'{dup_count} Duplicates removed!')


# STEP 4: HANDLE MISSING VALUES
# Categorical columns mein 'Unknown' bharna behtar hai delete karne se
cols_to_fill = ['director', 'cast', 'country', 'rating']
for col in cols_to_fill:
  df[col].fillna('Unknown', inplace = True)

# Date aur Duration agar missing hai toh un rows ko hata sakte hain (kyunki wo analysis ke liye crucial hain)
df.dropna(subset= ['duration', 'date_added'], inplace = True)
# STEP 5: TYPE CONVERSION & FEATURE ENGINEERING
# 1. Convert date into datetime
df['date_added'] = pd.to_datetime(df['date_added'])

# 2. Year aur Month alag nikalna (Visualization ke liye kaam ayega)
df['added_year'] = df['date_added'].dt.year
df['added_month'] = df['date_added'].dt.month_name

# 3. Duration se number nikalna (Regex method - Sabse Safe)
# Ye "90 min" ya "2 Seasons" mein se sirf number (90 ya 2) nikalega
df['duration_num'] = df['duration'].str.extract('(\d+)').astype(float)

print("\n--- Cleaning Complete ---")
print(f"Final Shape: {df.shape}")
print(df.isnull().sum()) # Final Inspection

# ==========================================
# STEP 6: STATISTICAL EDA (Investigation Phase)
# ==========================================
print("\n===== EDA REPORT =====")

# 1. Distribution (Kitne Movies vs TV Shows)
print("\nType Distribution (%):")
print(df['type'].value_counts(normalize=True)* 100)

# 2. Content Growth (Kis saal kitna content aaya)
print('\nYear-wise addition (Last 5 Years):')
print(df["added_year"].value_counts().sort_index().tail(5))

# 3. Top Countries
print('\nTop 5 Countries producing contents:')
print(df['country'].value_counts().head(5))

# 4. Averages (Numbers check karna)
avg_movie_time = df[df['type'] == 'Movie']['duration_num'].mean()
print(f'Average movie duration is {avg_movie_time} mins')

# 5. Extremes (Sabse lamba/chota - Anomalies dhundna)
# idxmax() humein wo row number dega jahan value sabse badi hai
longest_movie_idx = df[df['type'] == 'Movie']['duration_num'].idxmax()
shortest_movie_idx = df[df['type'] == 'Movie']['duration_num'].idxmin()

print("\nLongest Movie:")
print(df.loc[longest_movie_idx, ['title', 'duration']])

print("\nShortest Movie:")
print(df.loc[shortest_movie_idx, ['title', 'duration']])

# ==========================================
# STEP 7: VISUALIZATION (Presentation Phase)
# ==========================================
# Ab hume pata hai data clean hai, toh graph confidently bana sakte hain

# ==========================================
# GRAPH 1: Movies vs TV Shows (Bar Chart)
# ==========================================
type_counts = df['type'].value_counts()
plt.figure(figsize = (6,4))
plt.bar(type_counts.index, type_counts.values, color = ['skyblue', 'orange'])
plt.title('Number of TV Shows vs Number of Movies')
plt.xlabel('Type')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('movies vs tv shows.png')
plt.show()

# ==========================================
# GRAPH 2: Ratings Distribution (Pie Chart)
# ==========================================
# Rating column humne pehle hi fillna('Unknown') kar diya tha
rating_counts = df['rating'].value_counts()
top_5 = rating_counts.head(5)
others_count =  rating_counts.iloc[5:].sum()
final_ratings = top_5.copy()
final_ratings['Others'] = others_count 
plt.figure(figsize = (8,8))
plt.pie(final_ratings.values, labels = final_ratings.index, colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6'], autopct= '%1.1f%%', startangle= 90)
plt.title('Percentage of Content Ratings (Top 5 & Others)')
plt.tight_layout()
plt.savefig('Content ratings pie.png')
plt.show()

# ==========================================
# GRAPH 3: Movie Duration (Histogram) 
# ==========================================
movie_only = df[df['type'] == 'Movie']
plt.figure(figsize = (8,6))
plt.hist(movie_only['duration_num'], bins = 30, color ='purple', edgecolor = 'black')
plt.title('Distribution of Movie Duration')
plt.xlabel('Duration(minutes)')
plt.ylabel('Number of Movies')
plt.tight_layout()
plt.savefig('movie_duration_histogram.png')
plt.show()

# ==========================================
# GRAPH 4: Release Year Trend (Scatter/Line)
# ==========================================
release_counts = df['release_year'].value_counts().sort_index()
plt.figure(figsize = (10,5))
plt.plot(release_counts.index, release_counts.values, marker = 'o', linestyle = '--', color = 'red')
plt.legend()
plt.title('Release Year vs Number of Movies')
plt.xlabel('Release Year')
plt.ylabel('Number Of Movies')
plt.grid(linestyle = ':', color = 'blue', alpha = 0.5)
plt.tight_layout()
plt.savefig('release_year_trend.png')
plt.show()

# ==========================================
# GRAPH 5: Top 10 Countries (Horizontal Bar)
# ==========================================
all_countries = df['country'].value_counts()
if 'Unknown' in all_countries.index:
  all_countries = all_countries.drop('Unknown')
  
country_counts = all_countries.head(10)
plt.figure(figsize = (12,6))
plt.barh(country_counts.index, country_counts.values, color = 'teal')
plt.xlabel('Number of Shows') # Label correct kiya
plt.ylabel('Country')
plt.title('Top 10 Countries by Content')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('top10_countries.png')
plt.show()

# ==========================================
# GRAPH 6: Comparison Over Years 
# ==========================================
content_by_year = df.groupby(['release_year', 'type']).size().unstack().fillna(0)
plt.figure(figsize = (12,6))
plt.plot(content_by_year.index, content_by_year['Movie'], color = 'blue', label = 'Movies')
plt.plot(content_by_year.index, content_by_year['TV Show'], color = 'orange', label = 'TV Shows')

plt.title('Comparison of Movies and TV Shows Released Over Years')
plt.xlabel('Year')
plt.ylabel('Count')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('movies_tvShows_comparison.png')
plt.show()