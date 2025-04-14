# we need requests to talk to the internet / APIs
import requests

# pandas is for making tables (DataFrames)
import pandas as pd

# this is our secret API key from NYT
API_KEY = 'KNVit4usmN7fBgGdWNGZUGtToCxifzn0'

# this is the special link to ask for movie reviews
url = 'https://api.nytimes.com/svc/movies/v2/reviews/search.json'

# we tell the API what we want. here we want reviews about "comedy"
params = {
    'api-key': API_KEY,  # our key so they know it's us
    'query': 'comedy'    # change "comedy" to any word like "action" or "barbie"
}

# now we send a GET request to the url, asking for info
response = requests.get(url, params=params)

# check if it worked (status code 200 means OK)
if response.status_code == 200:
    # get the json data (like a dictionary)
    data = response.json()

    # go to the "results" part of the json
    results = data.get('results', [])

    # make a DataFrame (like Excel table) from the results
    df = pd.DataFrame([{
        'Title': movie.get('display_title'),               # name of the movie
        'Rating': movie.get('mpaa_rating'),                # G, PG, R etc
        'Critic': movie.get('byline'),                     # who wrote the review
        'Headline': movie.get('headline'),                 # title of the article
        'Summary': movie.get('summary_short'),             # small description
        'Publication Date': movie.get('publication_date'), # when it was published
        'Review Link': movie.get('link', {}).get('url')    # link to full review
    } for movie in results])

    # show the first 5 rows of the table
    print(df.head())

    # also save it to a csv file so we can open in Excel
    df.to_csv('nyt_movie_reviews.csv', index=False)

else:
    # if something went wrong, show the error
    print(f"Error: {response.status_code} - {response.text}")
