import requests
import json
from bs4 import BeautifulSoup
from tablepyxl import tablepyxl





# This function can save article doi and tables as Excel file.
# Argument 1: The sciencedirect URL of article.(string)
# Argument 2: Target Excel file name.(string)
def data_collector_sciencedirect(article_url, excelfile_name):

    # get the source code
    url = "http://localhost:8191/v1"
    headers = {"Content-Type": "application/json"}
    data = {
        "cmd": "request.get",
        "url": article_url,
        "maxTimeout": 60000
    }
    response = requests.post(url, headers=headers, json=data)
    response_dict = json.loads(response.text)
    html_txt = response_dict.get('solution').get('response')
    soup = BeautifulSoup(html_txt, 'html.parser')


    # get the article doi link
    target_element = soup.select('div#article-identifier-links a[class="anchor doi anchor-primary"]')
    doi = target_element[0]["href"]
    doi_table = "<table><thead><tr><th>doi_link</th></tr></thead><tbody><tr><td>" + str(doi) + "</td></tr></tbody></table>"


    # get the tables
    divs = soup.find_all('div')
    required_classes = {'tables', 'colsep-0', 'frame-topbot', 'rowsep-0'}
    result_divs = []
    table_str = doi_table
    for div in divs:
        div_classes = set(div.get('class', []))
        if required_classes.issubset(div_classes):
            result_divs.append(div)

    for result_div in result_divs:
        table_str += str(result_div)


    # save tables as Excel file
    tablepyxl.document_to_xl(table_str, excelfile_name)









# The function can get target article urls on sciencedirect
# Argument 1: URL for referer.(string)
# Argument 2: API link of results.(string)
# Return: links list of articles
def artile_urls_collector_sciencedirect(referer_url, results_api):

    # get the source code
    url = "http://localhost:8191/v1"
    headers = {"Content-Type": "application/json",
               "referer": referer_url
               }
    data = {
        "cmd": "request.get",
        "url": results_api,
        "maxTimeout": 60000
        }

    response = requests.post(url, headers=headers, json=data)
    response_dict = json.loads(response.text)
    list_txt = response_dict.get('solution').get('response')
    soup = BeautifulSoup(list_txt, 'html.parser')

    result_html = soup.select("pre")
    result_json = result_html[0].text
    result_dict = json.loads(result_json)
    articles_list = result_dict.get("searchResults")

    links = []
    for article in articles_list:
        link = "https://www.sciencedirect.com" + article.get("link")
        links.append(link)

    print("Get %d articles" % len(links))

    return links



