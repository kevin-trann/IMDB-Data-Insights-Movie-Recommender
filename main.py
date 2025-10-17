import pandas as pd
movies = pd.read_csv("imdb_popular_dataset.csv")
movies = movies[movies['numVotes'] >= 10000]
top10ByRating = movies.sort_values(by="averageRating", ascending=False).head(10)
top10ByNumberOfVotes = movies.sort_values(by="numVotes", ascending=False).head(10)

intro = True
askUserInput = True


while True:
    if (intro):
        print("---Movie Recommender by Kevin Tran---\n")
        intro = False
    
    
    if (askUserInput):
        value = input("What would you like to do?\n1.List top 10 movies/tv shows in a chosen category\n2.Recommend a movie based on input\n3.Info about a movie\n\nPlease type in the corresponding number for the option chosen.")
        askUserInput = False
       
    
        match value:
            case "1":
                categoryRanking = input("\nHow would you like to sort the top 10 movies/tv shows?\n1. Rating\n2. Number of voters\nPlease type in the corresponding number for the option chosen.")
                
                if categoryRanking == 'b':
                    askUserInput = True
                
                match categoryRanking:
                    
                        case "1":
                            print("\n---Top 10 by Rating---")
                            print(top10ByRating[["primaryTitle", "averageRating", "numVotes", "startYear"]].to_string(index=False))
                        case "2":
                            print("\n---Top 10 by Number of Votes---")
                            print(top10ByNumberOfVotes[["primaryTitle", "averageRating", "numVotes", "startYear"]].to_string(index=False))
            case "2":
                print("case 2")
            
            case "3":
                print("case 3")