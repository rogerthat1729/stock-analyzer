from newsapi import NewsApiClient
import datetime as dt
import datetime

today = datetime.date.today()
# /v2/top-headlines

                                        
        
def get_stock_news():
    # Init
    newsapi = NewsApiClient(api_key='3531f62c22134d9eb03a0c325946ed7c')
    top_headlines = newsapi.get_top_headlines(q='stock',
                                          category='business',
                                          language='en',
                                          country='in',)
    return top_headlines

# # /v2/top-headlines
# top_headlines = newsapi.get_top_headlines(q='bitcoin',
#                                           sources='bbc-news,the-verge',
#                                           category='business',
#                                           language='en',
#                                           country='in')


# # /v2/everything
# all_articles = newsapi.get_everything(q='bitcoin',
#                                       sources='bbc-news,the-verge',
#                                       domains='bbc.co.uk,techcrunch.com',
#                                       from_param='2017-12-01',
#                                       to='2017-12-12',
#                                       language='en',
#                                       sort_by='relevancy',
#                                       page=2)

# # /v2/top-headlines/sources
# sources = newsapi.get_sources()

# print(top_headlines)
# # Give me code to write all the data to a text file 

# import json

# # Assuming top_headlines is a dictionary containing the news data
# data = top_headlines

# # Convert the dictionary to a JSON string for easier writing to file
# data_string = json.dumps(data, indent=4)

# # Specify the filename
# filename = 'top_headlines.txt'

# # Write the data to a text file
# with open(filename, 'w') as file:
#     file.write(data_string)

# print(f"Data written to {filename}")