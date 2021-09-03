'''
**Web Scraping with Python**


*What is Web Scraping?

Web scraping is an automated method used to extract large amounts of data from websites. The data on the websites are unstructured.
Web scraping helps collect these unstructured data and store it in a structured form. 

*How Do You Scrape Data From A Website?

When you run the code for web scraping, a request is sent to the URL that you have mentioned. As a response to the request,
the server sends the data and allows you to read the HTML or XML page.
The code then, parses the HTML or XML page, finds the data and extracts it. 
To extract data using web scraping with python, you need to follow these basic steps:

1.Find the URL that you want to scrape
2.Inspecting the Page
3.Find the data you want to extract
4.Write the code
5.Run the code and extract the data
6.Store the data in the required format

*Libraries used for Web Scraping:

As we know, Python is has various applications and there are different libraries for different purposes.
In our further demonstration, we will be using the following libraries:
1.Requests: Requests allows you to send HTTP, requests extremely easily. There’s no need to manually add query strings to your URLs, or to form-encode your POST data.
2.BeautifulSoup: Beautiful Soup is a Python package for parsing HTML and XML documents. It creates parse trees that is helpful to extract the data easily.
3.Pandas: Pandas is a library used for data manipulation and analysis. It is used to extract the data and store it in the desired format.

Step 1: Find the URL that you want to scrape

For this example, we are going scrape Amazon website to extract reviews and other columns of an indian webseries called- The Family Man.
The URL for this page is https://www.amazon.com/The-Family-Man-Season-1/product-reviews/B07XGLTVY7/ref=cm_cr_arp_d_paging_btm_next_2?pageNumber=2

Step 2: Inspecting the Page

The data is usually nested in tags. So, we inspect the page to see, under which tag the data we want to scrape is nested.
To inspect the page, just right click on the element and click on “Inspect”or click Ctrl+Shift+I.
When you click on the “Inspect” tab, you will see a “Browser Inspector Box” open.

Step 3: Find the data you want to extract

Let’s extract the Product,Title,Rating,Body/Reviews,which is in the “title”, "a","i" and "span" tag respectively.

Step 4: Write the code

Step 5: Run the code and extract the data

Step 6: Store the data in a required format

After extracting the data, you might want to store it in a format.
This format varies depending on your requirement. For this example, we will store the extracted data in an Excel file.'''


'''
Import the following libraries, make sure you have them installed in your system prior to importing them.
To install , press Win+R ,then write cmd to launch command line, and then write pip install libraryname
'''
import requests
from bs4 import BeautifulSoup
import pandas as pd

''' Creating an empty list , where we will add/append the required data and then finally print it or export its data to a desired file format.'''
reviewlist = []

''' Defining a function to parse data '''
def get_soup(url):
    ''' Using requests library to get data from the url'''
    """ NOTE: We could've simply written r=requests.get(url),but this would show the following error:
        To discuss automated access to Amazon data please contact api-services-support@amazon.com.
        For information about migrating to our APIs refer to our Marketplace APIs at https://developer.amazonservices.com/ref=rm_5_sv,
        or our Product Advertising API at https://affiliate-program.amazon.com/gp/advertising/api/detail/main.html/ref=rm_5_ac for advertising use cases.

        The reason behind this error is that Amazon is very anti-scraping.
        There's an entire industry built around scraping data from Amazon, and Amazon has its own API access to sell,
        so it's in their best interest to stop people from freely grabbing data from their pages.
        Simply put,data is not to be sold for free.

        Based on that code, we make too many requests too quickly and thus our IP may get banned.
        When scraping sites, it's usually best to scrape responsibly by not going too fast, rotating user agents, and rotating IPs through a proxy service.

        To seem less programmatic, you can also try randomizing request timing to seem more human.
        Even with all of that, you'll still likely hit issues with this. Amazon is not an easy site to reliably scrape.

        So in order to counter this problem,the simplest and easiest way to manage it on windows is by using Splash and Docker Desktop.

        Splash is a lightweight browser with an API designed spcifically for web scraping and rendering javascript and dynamic websites.
        We can quickly and easily send requests to Splash instance and have it render the JS for us, and return the HTML to parse.

        To download it -
        Docker Desktop -https://www.docker.com/products/docker-desktop
        Splash -https://splash.readthedocs.io/en/stable/install.html#linux-dock  """
    
    #Using Splash from Docker Desktop. Creating a localhost at 8050 (default) and then using it to render the javascripts.
    r = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait': 2}) 
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

#Extracting the required data from the HTML parsed data, by selecting the correct class names of selected tags.
def get_reviews(soup):
    reviews = soup.find_all('div', {'data-hook': 'review'})
    try:
        for item in reviews:
            review = {
            'product': soup.title.text.strip(),
            'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
            'rating':  item.find('i', {'data-hook': 'review-star-rating'}).text.strip(),
            'body': item.find('span', {'data-hook': 'review-body'}).text.strip(),
            }
            reviewlist.append(review)
    except:
        pass

#You can vary the range based on the no. of loops you want python to run(range(a,b)) , depending on the amount of data to be extracted/scraped.
for x in range(1,999): #Passing the Url of the amazon website of The Family Man reviews

    soup = get_soup(f'https://www.amazon.com/The-Family-Man-Season-1/product-reviews/B07XGLTVY7/ref=cm_cr_arp_d_paging_btm_next_2?pageNumber={x}')
    print(f'Getting page: {x}')
    get_reviews(soup)
    print(len(reviewlist))
    if not soup.find('li', {'class': 'a-disabled a-last'}):
        pass
    else:
        break

#Creating a dataframe from the scraped off data.
df = pd.DataFrame(reviewlist)

#Saving the data to an excel file, write the location where you want it to be saved, here the file will be stored on the Desktop
df.to_excel(r'C:\Users\Asus\Desktop\AMAZON REVIEWS OF- THE FAMILY MAN.xlsx', index=False)
print (soup.title.text)
print('DataFrame is written successfully to Excel Sheet.')
