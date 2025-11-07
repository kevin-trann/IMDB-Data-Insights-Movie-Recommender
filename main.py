from fuzzywuzzy import process
import pandas as pd
import streamlit as st
import random

movies_and_tvShows = pd.read_csv("imdb_popular_dataset.csv")
movies_and_tvShows = movies_and_tvShows[movies_and_tvShows['numVotes'] >= 50000]

movies = movies_and_tvShows[movies_and_tvShows['titleType'] == "movie"]
tvShows = movies_and_tvShows[movies_and_tvShows['titleType'].isin(["tvSeries", "tvMiniSeries"])]

sortValue = ""
mediaType = ""
mediaName = ""
ascendingOrder = False

st.title("IMDB Data Insights & Movie Recommender by Kevin Tran")

st.write("This project only contains titles from 1980-2025 that have more than 50,000 votes on IMDB.")

askUserInput = st.selectbox("What would you like to do?", ["", "Recommend a title based on input", "List top movies/tv shows in a chosen category", "Info about a title"])

if askUserInput == "List top movies/tv shows in a chosen category":
    
    askMediaType = st.selectbox("What type of media would you like to sort?", ["Movies", "Tv Shows", "Both"])
    
    if askMediaType == "Movies":
        mediaType = movies
        mediaName = "Movies"
      
    elif askMediaType == "Tv Shows":
        mediaType = tvShows
        mediaName = "Tv Shows"
       
    elif askMediaType == "Both":
        mediaType = movies_and_tvShows
        mediaName = "Movies and Tv Shows"
     
        
    sortingMethod = st.selectbox(f"How would you like to sort the titles by?", ["Rating", "Number of Votes", "Year of Release", "Alphabetical Order"])
    
    if sortingMethod == "Rating":
        sortValue = "averageRating"
        
    elif sortingMethod == "Number of Votes":
        sortValue = "numVotes"
    
    elif sortingMethod == "Year of Release":
        sortValue = "startYear"
        
    elif sortingMethod == "Alphabetical Order":
        sortValue = "primaryTitle"
        
    numberOfEntries = st.number_input("How many titles would you like to list? Please type an integer.",
    min_value=1,
    max_value=100,
    value=5,
    step=1 
    )
    
    if sortingMethod == "Rating" or sortingMethod == "Number of Votes":
    
        rankingOrder = st.selectbox("What order would you like to display the data?", ["Highest to Lowest", "Lowest to Highest"])
        
        if rankingOrder == "Highest to Lowest":
            ascendingOrder = False
        
        elif rankingOrder == "Lowest to Highest":
            ascendingOrder = True
    
    if sortingMethod == "Year of Release":
        
        rankingOrder = st.selectbox("What order would you like to display the data?", ["Chronological Order", "Reverse Chronological Order"])
        
        if rankingOrder == "Chronological Order":
            ascendingOrder = True
            
        elif rankingOrder == "Reverse Chronological Order":
            ascendingOrder = False
    
    if sortingMethod == "Alphabetical Order":
        
        rankingOrder = st.selectbox("What order would you like to display the data?", ["A-Z", "Z-A"])
        
        if rankingOrder == "A-Z":
            ascendingOrder = True
        
        elif rankingOrder == "Z-A":
            ascendingOrder = False
    
    if st.button("Run"):
        topList = mediaType.sort_values(by=sortValue, ascending=ascendingOrder).head(int(numberOfEntries))
        topList = (topList[["primaryTitle", "titleType", "genres", "averageRating", "numVotes", "startYear"]].reset_index(drop=True))
        topList.index = topList.index + 1
        st.header(f"Top {mediaName} by {sortingMethod}")
        st.dataframe(topList)
   
        
        
elif askUserInput == "Recommend a title based on input":
    titles = movies_and_tvShows['primaryTitle']
    chosenTitle = st.text_input("Which title do you want recommendations based on?")
        
    
    numberOfEntries = st.number_input("How many titles would you like to be recommended? Please type an integer.",
        min_value=1,
        max_value=100,
        value=5,
        step=1 
        )
    
    if st.button("Recommend"):
        bestMatch = process.extractOne(chosenTitle, titles)
        st.info(bestMatch[0])
        movieId = bestMatch[0]
        chosenDataset = movies_and_tvShows['primaryTitle'] == movieId
        
        chosenYear = (movies_and_tvShows[chosenDataset]["startYear"].values[0])
        
        minYear = int(chosenYear) - 10
        maxYear = int(chosenYear) + 10
                        
        chosenGenres = (movies_and_tvShows[chosenDataset]['genres'].values[0])
        chosenGenresList = chosenGenres.split(",")
        
        recommendations = movies_and_tvShows.copy()[
            (movies_and_tvShows['startYear'] >= minYear) 
            & (movies_and_tvShows['startYear'] <= maxYear)
            & (movies_and_tvShows['primaryTitle'] != chosenTitle)]
        
        selectionPool = numberOfEntries * 3
        
        for genre in chosenGenresList:
            recommendations = recommendations[recommendations['genres'].str.contains(genre, na=False)]
            printRecommendations = recommendations.sort_values(by="averageRating", ascending=False).head(int(selectionPool))
            printRecommendations = printRecommendations.sample(n=numberOfEntries)
        st.dataframe(printRecommendations[["primaryTitle", "averageRating", "numVotes", "startYear"]])   
    
elif askUserInput == "Info about a title":
    titles = movies_and_tvShows['primaryTitle']
    search = st.text_input("Which title would you like to search up info for?")
    if st.button("Search"):
        bestMatch = process.extractOne(search, titles)
        st.info(bestMatch[0])
        movieId = bestMatch[0]
        st.dataframe(movies_and_tvShows[movies_and_tvShows['primaryTitle'] == movieId][["primaryTitle", "titleType", "genres", "averageRating", "numVotes", "startYear"]])