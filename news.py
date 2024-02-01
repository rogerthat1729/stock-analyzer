from newsapi import NewsApiClient

def get_stock_news():
    newsapi = NewsApiClient(api_key='3531f62c22134d9eb03a0c325946ed7c')
    top_headlines = newsapi.get_top_headlines(q='stock',
                                          category='business',
                                          language='en',
                                          country='in',)
    return top_headlines