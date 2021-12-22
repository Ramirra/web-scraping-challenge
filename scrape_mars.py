#imports
from splinter import Browser
from bs4 import BeautifulSoup as soup
import datetime as dt 
from webdriver_manager.chrome import ChromeDriverManager

#scrape all function
def scrape_all():
    #set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #retrieve information from web page
    news_title, news_p = scrape_news(browser)

    #build a dictionary using the information from scrapes
    marsData  = {
        "newsTitle": news_title,
        "newsParagraph": news_p,
        "featuredImage": scrape_feature_img(browser),
        "facts": scrape_facts(browser),
        "hemispheres": scrape_hemispheres(browser),
        "lastUpdated": dt.datetime.now()
    }

    #stop webdriver
    browser.quit()

    return marsData

#scrape mars news pages 
def scrape_news(browser):
    #Visit URL
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

     #Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')
    
    #retrieves title
    news_title = slide_elem.find("div", class_="content_title").text.strip()
    #retrieves paragraph
    news_p = slide_elem.find("div", class_="article_teaser_body").text.strip()

    #return title and paragraph
    return news_title, news_p

#scrape featured image page 
def scrape_feature_img(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    browser.links.find_by_partial_text("FULL IMAGE").click()
    
    # Parse the resulting html with soup
    space_html = browser.html
    img_soup = soup(space_html, 'html.parser')
    img_elem = img_soup.find("img", class_="headerimage")

    # find the relative image url
    img_url_rel = img_elem["src"]

    # Use the base url to create an absolute url
    img_url = url + "/" + img_url_rel   

    #return image url
    return img_url

#scrape facts page
def scrape_facts(browser):
    #Visit URL
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)

    # Parse the resulting html with soup
    facts_html = browser.html
    facts_soup = soup(facts_html, 'html.parser')

    #find facts location
    facts_location = facts_soup.find('div', class_ = "diagram mt-4")
    #retrieve the html code 
    facts_table = facts_location.find("table")

    #create an empty string 
    facts = ""

    #add text to empty string and return
    facts += str(facts_table)
    return facts

#scrape hemispheres pages
def scrape_hemispheres(browser):
    #Visit URL
    url = 'https://marshemispheres.com/'        
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    #set up for loop
    for i in range(4):
        # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item img")[i].click()
        
        # Next, we find the Sample image anchor tag and extract the href
        sample_elem = browser.find_link_by_text("Sample").first
        img_url = sample_elem["href"]
        
        # Get Hemisphere title
        title = browser.find_by_css("h2.title").text
        
        #create dictionary to stroy data for url and title
        img_url_dict = {
            "title": title,
            "img_url": img_url
        }
        
        # Append hemisphere object to list
        hemisphere_image_urls.append(img_url_dict)
        
        # Finally, we navigate backwards
        browser.back()

    #return hemisphere URLs with titles
    return hemisphere_image_urls

#set up as flask app 
if __name__ == "__main__":
    print(scrape_all())