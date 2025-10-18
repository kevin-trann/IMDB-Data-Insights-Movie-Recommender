from fuzzywuzzy import process
import pandas as pd

movies_and_tvShows = pd.read_csv("imdb_popular_dataset.csv")
movies_and_tvShows = movies_and_tvShows[movies_and_tvShows['numVotes'] >= 50000]

movies = movies_and_tvShows[movies_and_tvShows['titleType'] == "movie"]
tvShows = movies_and_tvShows[movies_and_tvShows['titleType'].isin(["tvSeries", "tvMiniSeries"])]

sortValue = ""
mediaType = ""
mediaName = ""


intro = True
askUserInput = True

while True:
    if (intro):
        print("---Movie Recommender by Kevin Tran---\n")
        intro = False
        
    if (askUserInput):
        value = input("\nWhat would you like to do?\n\n1.List top movies/tv shows in a chosen category\n2.Recommend a movie based on input\n3.Info about a movie\n\nPlease type in the corresponding number for the option chosen.")
        askUserInput = False
       
        match value:
            case "1":
                
                while True: 
                    mediaType = input("\nWhat media type would you like to sort by?\n1. Movies\n2. Tv Shows\n3. Both\n\nPlease type in the corresponding number for the option chosen.")
                    
                    match mediaType:
                        
                        case "1": 
                            mediaType = movies
                            mediaName = "Movies"
                            break
                        case "2":
                            mediaType = tvShows
                            mediaName = "Tv Shows"
                            break
                        case "3":
                            mediaType = movies_and_tvShows
                            mediaName = "Movies and Tv Shows"
                            break
                        case _:
                            print("Invalid input. Please try again.")
                        
                while True:
                    categoryRanking = input("\nHow would you like to sort the top 10 movies/tv shows?\n1. Rating\n2. Number of voters\n\nPlease type in the corresponding number for the option chosen.")
                    
                    match categoryRanking:
                        
                            case "1":
                                sortValue = "averageRating"
                                break
                            
                            case "2":
                                sortValue = "numVotes"
                                break
                            case _:
                                print("Invalid input. Please try again.")
                
                while True:
                    numberOfEntries = input(f"\nHow many {mediaName} would you like to list?\nPlease type in an integer.")
                    
                    try: 
                        numberOfEntries = int(numberOfEntries)
                        break   
                    except ValueError: 
                        print("\n---Invalid input, please enter an integer.---")            

                topList = mediaType.sort_values(by=sortValue, ascending=False).head(int(numberOfEntries))
                print("")
                print(f"---Top {numberOfEntries} {mediaName} by {sortValue}---")
                print(topList[["primaryTitle", "averageRating", "numVotes", "startYear"]].to_string(index=False))
                cont = input("\nPress any key to continue\n")
                if (cont):
                    askUserInput = True
                
            case "2":
                print("case 2")
            
            case "3":
                
                while True:
                    search = input("\nWhich movie/tv show would you like to search up info for?")
                    titles = movies_and_tvShows['primaryTitle']
                    bestMatch = process.extractOne(search, titles)
                    
                    if bestMatch:
                        movieId = bestMatch[0]
                        print("")
                        print(movies_and_tvShows[movies_and_tvShows['primaryTitle'] == movieId][["primaryTitle", "averageRating", "numVotes", "startYear"]])
                        
                        cont = input("\nPress any key to continue\n")
                        if (cont):
                            askUserInput = True
                            break
                    
                    else:
                        print("\nNo results. Please try again.")
                        
                    cont = input("\nPress any key to continue\n")
                    
                    