from fuzzywuzzy import process
import pandas as pd
import streamlit as st

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

askUserInput = st.selectbox("What would you like to do?", ["", "List top movies/tv shows in a chosen category", "Recommend a title based on input", "Info about a title"])

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
        topList = (topList[["primaryTitle", "averageRating", "numVotes", "startYear"]].reset_index(drop=True))
        topList.index = topList.index + 1
        st.header(f"Top {mediaName} by {sortingMethod}")
        st.dataframe(topList)
   
        
        
elif askUserInput == "Recommend a title based on input":
    st.write("2")
    
elif askUserInput == "Info about a title":
    titles = movies_and_tvShows['primaryTitle']
    search = st.text_input("Which title would you like to search up info for?")
    if st.button("Search"):
        bestMatch = process.extractOne(search, titles)
        movieId = bestMatch[0]
        st.dataframe(movies_and_tvShows[movies_and_tvShows['primaryTitle'] == movieId][["primaryTitle", "averageRating", "numVotes", "startYear"]])