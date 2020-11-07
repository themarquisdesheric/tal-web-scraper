import requests
from bs4 import BeautifulSoup
from time import sleep


def get_page_contents(url):
  '''takes a url and returns the contents of the page, skipping the breadcrumbs'''
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')

  drg_number = soup.find('h1', 'pageHeading').get_text()
  page_title = soup.find('h2', 'pageHeading').get_text()
  # construct single-line page title
  page_title = drg_number + ' ' + page_title
  page_content = soup.find('ul', 'list').get_text()
  # return formatted page contents
  return page_title + page_content + '\n'


def scrape(url, path):
  # load table of contents
  page = requests.get(url + path)
  soup = BeautifulSoup(page.content, 'html.parser')
  # get page links
  page_links = soup.find_all('a', class_='identifier')

  for link in page_links:
    current_url = url + link.get('href')

    print('fetching ' + current_url + '...')
    
    # pause so we don't get flagged
    sleep(2.5)

    page_contents = get_page_contents(current_url)
    
    # append to results file
    with open('results.txt', 'a') as results:
      results.write(page_contents)
