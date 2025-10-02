import pandas as pd

basics = pd.read_csv("imdb_datasets/title.basics.tsv/title.basics.tsv", sep="\t", low_memory=False)
ratings = pd.read_csv("imdb_datasets/title.ratings.tsv/title.ratings.tsv", sep="\t", low_memory=False)

dataset = pd.merge(basics, ratings, on="tconst")

dataset['startYear'] = pd.to_numeric(dataset['startYear'], errors='coerce')
dataset['numVotes'] = pd.to_numeric(dataset['numVotes'], errors='coerce')

dataset = dataset.dropna(subset=['numVotes', 'startYear'])

filtered_dataset = dataset[
    ( (dataset['titleType'] == "movie") | (dataset['titleType'] == 'tvSeries')
     & (dataset['startYear'] >= 1980)
     & (dataset['numVotes'] > 100000)
     )
]

filtered_dataset.to_csv("imdb_popular_dataset", index=False)