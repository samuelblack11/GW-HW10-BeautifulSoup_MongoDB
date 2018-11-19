
# coding: utf-8

# In[2]:


# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import os
from splinter import Browser
import pymongo
import re
import html
import pandas as pd


# In[3]:


conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
# Define the 'classDB' database in Mongo
db = client.mars_db
#mars_db=db.mars_db
#facts_images_db=db.facts_images_db.find()


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


# In[70]:

def scrape():
    url = 'https://mars.nasa.gov/news/'
    browser = init_browser()
    browser.visit(url)
    html = browser.html
    
    
    # In[87]:
    
    
    # Retrieve page with the requests module
    response = requests.get(url)
    a = bs(response.text, 'lxml')
    
    main_content=(a.find_all('div', class_='grid_layout'))
    #main_content=(a.find_all('ul', class_='item_list'))
    
    for contents in main_content:
        items =(a.find_all('div', class_="list_date"))
        #print(items)
    
    
    # In[88]:
    
    
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')
    #soup_2 = bs(response.text, 'lxml')
    
    
    # In[89]:
    
    
    browser = init_browser()
    url_visit="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    url_string = "https://www.jpl.nasa.gov"
    browser.visit(url_visit)
    
    html = browser.html
    #soup = bs(html, "html.parser")
        
    # Retrieve page with the requests module
    response = requests.get(url_visit)
    # Create BeautifulSoup object; parse with 'lxml'
    a = bs(response.text, 'html.parser')
    
    
    # In[90]:
    
    
    
    #print(a.prettify())
    results=str(a.find('footer'))
    #a.find_all('a', class_='fancybox')
    results
    #for result in results:
        #featured_image_url = result.find('data-fancybox-href')
    results
    
    
    # In[91]:
    
    
    start = 'data-fancybox-href="'
    end = '" data-link'
    substring= (results[results.find(start)+len(start):results.rfind(end)])
    featured_image_url=f'{url_string}{substring}'

    # https://www.jpl.nasa.govspaceimages/images/mediumsize/PIA16837_ip.jpg
    #https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA07137_ip.jpg
    # In[92]:
    
    
    url = 'https://twitter.com/marswxreport?lang=en'
    browser = init_browser()
    browser.visit(url)
    html = browser.html
    
    # In[93]:
    
    response = requests.get(url)
    a = bs(response.text, 'lxml')
    
    mars_weather=(a.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')).contents
    
    
    # In[94]:
    
    
    url = 'http://space-facts.com/mars/'
    browser = init_browser()
    browser.visit(url)
    html = browser.html
    
    # In[95]:
    
    response = requests.get(url)
    a = bs(response.text, 'lxml')
    
    facts=(a.find('table', class_='tablepress tablepress-id-mars')).contents
    
    # In[96]:
    
    ls = []
    for strong_tag in a.find_all('strong'):
        #print (strong_tag.text)
        ls.append(strong_tag.text)
    
    # In[97]:
    
    ls_2 = []
    for td_tag in a.find_all('td'):
        #print (td_tag.text)
        #td_tag.text.split(":")
        ls_2.append(str(td_tag.text))
    # some_list[start:stop:step]
    ls_3 =ls_2[0::2]
    ls_4 =ls_2[1::2]
    
    
    # In[98]:
    
    ls_3_1=[]
    for obj in ls_3:
        obj_1=obj.replace(":","")
        ls_3_1.append(obj_1)

    equatorial_diameter=ls_3_1[0] 
    polar_diameter=ls_3_1[1]
    mass = ls_3_1[2]
    moons =ls_3_1[3]
    orbit_distance = ls_3_1[4]
    orbit_period = ls_3_1[5]
    surface_temp = ls_3_1[6]
    first_record = ls_3_1[7]
    recorded_by = ls_3_1[8]

    eq_diam_m=ls_4[0]
    pol_diam_m = ls_4[1]
    mass_m=ls_4[2]
    moons_m=ls_4[3]
    orbit_distance_m=ls_4[4]
    orbit_period_m=ls_4[5]
    surface_temp_m=ls_4[6]
    first_record_m=ls_4[7]
    recorded_by_m= ls_4[8]
    
    # In[99]:
    
    df_2 = pd.DataFrame()
    df_2['Measurement']=(ls_3_1)
    df_2['Metric']=(ls_4)
    
    # In[100]:
    
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser = init_browser()
    browser.visit(url)
    html = browser.html
    
    # In[101]:
    
    response = requests.get(url)
    a = bs(response.text, 'lxml')
    
    hemi_1=(a.find('img', class_='thumb'))
    hemi_1_title=str((hemi_1["alt"]))
    hemi_1_title=' '.join(hemi_1_title.split()[:2])
    hemi_1_img='https://astrogeology.usgs.gov/search'+(hemi_1["src"])
    hemi_1_enhanced = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'
    
    hemi_2=(a.find_all('img', class_='thumb')[1])
    hemi_2_title=str((hemi_2["alt"]))
    hemi_2_title=' '.join(hemi_2_title.split()[:2])
    hemi_2_img='https://astrogeology.usgs.gov'+(hemi_2["src"])
    hemi_2_enhanced = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'
    
    hemi_3=(a.find_all('img', class_='thumb')[2])
    hemi_3_title=str((hemi_3["alt"]))
    hemi_3_title=' '.join(hemi_3_title.split()[:2])
    hemi_3_img='https://astrogeology.usgs.gov'+(hemi_3["src"])
    hemi_3_enhanced='https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'
    
    hemi_4=(a.find_all('img', class_='thumb')[3])
    hemi_4_title=str((hemi_4["alt"]))
    hemi_4_title=' '.join(hemi_4_title.split()[:2])
    hemi_4_img='https://astrogeology.usgs.gov'+(hemi_4["src"])
    hemi_4_enhanced='https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'
    
    
    # In[102]:
    
    
    hemi_imgs_ls = [
        {"title": hemi_1_title, "url": hemi_1_enhanced},
        {"title": hemi_2_title, "url": hemi_2_enhanced},
        {"title": hemi_3_title, "url": hemi_3_enhanced},
        {"title": hemi_4_title, "url": hemi_4_enhanced},
        ]
    #facts_images_db=db.facts_images_db.find()
    #db.facts_images_db.update_one
    mars_dict = {
        "featured_image": featured_image_url,
        "weather": mars_weather,
        "eq_diameter":eq_diam_m,
        "polar_diameter":pol_diam_m,
        "mass":mass_m,
        "moons":moons_m,
        "orbit_distance":orbit_distance_m,
        "orbit_period":orbit_period_m,
        "surface_temp":surface_temp_m,
        "first_record":first_record_m,
        "recorded_by":recorded_by_m,
        "hemi_1_title": hemi_1_enhanced,
        "hemi_2_title": hemi_2_enhanced,
        "hemi_3_title": hemi_3_enhanced,
        "hemi_4_title": hemi_4_enhanced,
    }

    #conn = 'mongodb://localhost:27017'
    #client = pymongo.MongoClient(conn)
    ## Define the 'classDB' database in Mongo
    #db = client.classDB
    #mars_db=db.mars_db
    #result = mars_db.insert_one(facts_images_dict)

    return (mars_dict)


#scrape()    
    