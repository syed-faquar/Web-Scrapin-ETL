# Syed Faquaruddin Quadri (24379388)

import os
import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch 
import inquirer
import re
import mysql.connector as mc


#function for user to select search engine and query
def user_input():
    
    engine = [inquirer.List('Search Engines', 
                            message='Choose Search Engine: ',
                            choices = ['google', 'yahoo', 'bing', 'duckduckgo'],
                            carousel=True),]
    
    #askin user to define the search engine from the given choices
    engine = inquirer.prompt(engine)

    #asing user for the search query
    query = input('Enter your query: ')

    #returing search engine, and query given by the user
    return engine["Search Engines"], str(query)


def bing(query):
    
    #completing the url using user defined query
    url = f'https://www.bing.com/search?q={query}'
    #creating a response object for storing all the information from the url
    resp = requests.get(url)
    #using beautiful soup converting response into a nested data structure
    soup = BeautifulSoup(resp.text, 'html.parser')
    #selecting all the classes which we gonna use to extract info we require
    tags = soup.select('ol#b_results > li.b_algo')

    #creating an empty list to store the results
    results = []

    #iterating over tags 
    for i in tags:
        #selecting url using href tags
        link = (i.select_one('a[href]')).get('href', u'')
        #selecting title using h2 tags
        title = (i.select_one('h2')).text.strip()
        #selecting text using p tags
        text = (i.select_one('p')).text.strip()
        #append this as a dict into the result
        results.append({'query': query,
                       'link': link,
                       'title': title,
                       'text': text})
        
    #returing list of dictionaries
    return results


def yahoo(query):

    #completing the url using user defined query
    url = f'https://search.yahoo.com/search?p={query}&ei=UTF-8&nojs=1'
    #creating a response object for storing all the information from the url
    resp = requests.get(url)
    #using beautiful soup converting response into a nested data structure
    soup = BeautifulSoup(resp.text, 'html.parser')
    #selecting all the classes which we gonna use to extract info we require
    tags = soup.select('div#web li div.dd.algo.algo-sr')

    #creating an empty list to store the results
    results = []

    for i in tags:
        #selecting url using href tags
        link = (i.select_one('div.compTitle h3.title a')).get('href', u'')
        #selecting title using h3_title tags
        title = (i.select_one('div.compTitle h3.title')).text.strip()
        #selecting text using comptext tags
        text = (i.select_one('div.compText')).text.strip()
        #append this as a dict into the result
        results.append({'query': query,
                       'link': link,
                       'title': title,
                       'text': text})
        
    #returing list of dictionaries 
    return results


def duckduckgo(query):

    #completing the url using user defined query
    url = f'https://html.duckduckgo.com/html/'
    #creating a response object for storing all the information from the url
    resp = requests.post(url, data = {'q': query, 'b':'', 'kl':'us-en'}, headers={'user-agent': 'my-app/0.0.1'})
    #using beautiful soup converting response into a nested data structure
    soup = BeautifulSoup(resp.text, 'html.parser')
    #selecting all the classes which we gonna use to extract info we require
    tags = soup.select('div.results div.result.results_links.results_links_deep.web-result')

    #creating an empty list to store the results
    results = []

    for i in tags:
        #selecting url using href tags
        link = (i.select_one('a.result__snippet')).get('href', u'')
        #selecting title using h2 tags
        title = (i.select_one('h2.result__title a')).text
        #selecting text using result__snippet tags
        text = (i.select_one('a.result__snippet')).text
        #append this as a dict into the result
        results.append({'query': query,
                       'link': link,
                       'title': title,
                       'text': text})
        
    #returing list of dictionaries    
    return results


def google(query):
#using API for google search engine as the google changes they classed very frequently 

    params = {
      "engine": "google",
      "num": "100",
      "q": query,
      "api_key": os.environ["SERP_API_KEY"]
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"]
    
    results = []
    for i in organic_results:
        results.append({'query': query,
                        'link': i["link"],
                        'title': i["title"],
                        'text': i["snippet"]
                   })
        
    return results


def search():
    #asking user for the engine and query
    engine, query = user_input()

    if engine == 'bing':
        print("===============================")
        print(f'searching {query} on {engine}')
        ret = bing(query)

    elif engine == 'yahoo':
        print("===============================")
        print(f'searching {query} on {engine}')
        ret = yahoo(query)

    elif engine == 'duckduckgo':
        print("===============================")
        print(f'searching {query} on {engine}')
        ret = duckduckgo(query)

    elif engine == 'google':
        print("===============================")
        print(f'searching {query} on {engine}')
        ret = google(query)


    #creating the connection with the sql database
    conn = mc.connect(host = 'localhost', 
                  port = 3306, 
                  user = 'root', 
                  password = 'root',
                  database = 'MY_CUSTOM_BOT')
    
    #creating an instance of cursor to execute the sql command
    cursor = conn.cursor()

    #empty list for storing values to load in the database
    val = []

    #iterating over the result after 
    for mydict in ret:
        val.append(tuple(mydict.values()))

    #sql command stored in the variable
    sql = f"INSERT INTO {engine} ( search_query, link, title, raw_text ) VALUES (%s, %s, %s, %s);"

    #executing the sql query using cursor
    cursor.executemany(sql,val)
    print("================================")
    print("data is loaded into the database")
    print("================================")

    #commiting data to database
    conn.commit()

    #closing cursor and connection
    conn.close()

if __name__ == '__main__':
    search()