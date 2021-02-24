# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def scrape():
    # Set path and browser
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # Put everything scraped in dictionary
    news_title, news_p = mars_news(browser)
    mars_data = {
        'news_title': news_title,
        'news_paragraph': news_p,
        'featured_image': featured_image(browser),
        'weather': mars_weather(browser),
        'facts': mars_facts(),
        'hemispheres': mars_hemispheres(browser)
    }
    
    # Quit and return data
    browser.quit()
    return mars_data
    
    
def mars_news(browser):
    # Define url
    url1 = 'https://mars.nasa.gov/news/'
    
    # Visit first page
    browser.visit(url1)
    time.sleep(1)
    
    # Set html object and parser
    html = browser.html
    soup1 = bs(html, 'html.parser')
    
    # Get news title and text or return error message
    try:
        slide = soup1.select_one('ul.item_list li.slide')
        news_title = slide.find('div', class_='content_title').get_text()
        news_p = slide.find('div', class_='article_teaser_body').get_text()    
    except:
        return "Scrape unsuccessful"
    return news_title, news_p
    
def featured_image(browser):
    # Define url
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    # Visit second page
    browser.visit(url2)
    time.sleep(1)
    
    # Click image link
    browser.find_by_id('full_image').click()
    time.sleep(1)
    
    # Click info link
    browser.find_link_by_partial_text('more info').click()
    time.sleep(1)
    
    # Set html object and parser
    html = browser.html
    soup2 = bs(html, 'html.parser')
    
     # Select image and create url string for it or display error message
    try:
        image = soup2.select_one('figure.lede a img')
        image_string = image.get('src')
        featured_image_url = f"https://www.jpl.nasa.gov{image_string}"
    except:
        return "Image not found"
    return featured_image_url
    
def mars_weather(browser):
    # Define url
    url3 = 'https://twitter.com/marswxreport?lang=en'
    
    # Visit third page
    browser.visit(url3)
    time.sleep(1)
    
    # Set html parser
    html = browser.html
    soup3 = bs(html, 'html.parser')
    
    # Find tweets and grab text from the most recent one or display an error message
    try:
        tweets = soup3.find('div', attrs={'class':'tweet'})
        weather = tweets.select_one('p').get_text()
    except:
        return "Scrape unsuccessful"
    return weather
    
def mars_facts():
    # Define url
    url4 = 'https://space-facts.com/mars/'
    
    # Pandas read html of fourth site into dataframe and return html table or error
    try:
        facts_df = pd.read_html(url4)[0]
        facts_df = facts_df.rename(columns={0: 'Category', 1:'Value'})
        facts_df = facts_df.set_index('Category')
        facts_html_table = facts_df.to_html()
    except:
        return "Scrape unsuccessful"
    return facts_html_table
    
def mars_hemispheres(browser):
    # Define url
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    # Visit fifth page
    browser.visit(url5)
    time.sleep(1)
    
    # Set html object and parser
    html = browser.html
    soup5 = bs(html, 'html.parser')
    
    # Find the results
    hemispheres = soup5.find_all('div', class_='item')
    
    # Empty list to fill
    hemisphere_image_urls = []

    # Loop through, picking out each name and clicking on each link and getting the url for full image
    # Add name and url to dictionary and add that to the empty list
    # Or return error message   
    try:
        for hemisphere in hemispheres:
            hemi_name = hemisphere.find('h3').text
            browser.find_link_by_partial_text('Enhanced').click()
            sample_link = browser.find_link_by_partial_text('Sample').first
            hemi_url = sample_link['href']
            hemi_dict = {'title': hemi_name, 'img_url': hemi_url}
            hemisphere_image_urls.append(hemi_dict)
    except:
        return "Scrape unsuccessful"
    return hemisphere_image_urls