import spider_functions
import time

article_url = "https://www.sciencedirect.com/science/article/pii/S0141029619324873?via%3Dihub"
excelfile_name_directory = "/Users/liaozhexiong/Documents/"
excelfile_name_pre = "tables_list_"
referer_urls_root = "https://www.sciencedirect.com/search?qs=steel%20fire&show=100"
results_apis_root = "https://www.sciencedirect.com/search/api?qs=steel%20fire&show=100"
results_apis_tail = "&t=93fafea912fef307f7d6acdd10051c93d6c8099bb874ea63ff48c97b9de3b228abc94c4e6ecaffcbc4acae113bf1284617fa4365a3642495efb08986b24d023e2742d3f7decdfbf7ea32df6c01d0ed65ca963bcc9c2d59a4613b1e7b5161e33014cbf85106eba2be3cae9a054f2bb164&hostname=www.sciencedirect.com&navigation=true"
articles_quantity = 100
delay = 5

# Get page info
referer_urls = []
results_apis = []
for i in range(0, articles_quantity - 1 , 100):
    referer_urls.append(referer_urls_root + "&offset=" + str(i))
    results_apis.append(results_apis_root + "&offset=" + str(i) + results_apis_tail)

pages_infos = list(zip(referer_urls, results_apis))

# Get data and save
article_index = 0
for page_info in pages_infos:
    article_urls = spider_functions.artile_urls_collector_sciencedirect(page_info[0], page_info[1])
    for article_url in article_urls:
        article_index += 1
        excelfile_name = excelfile_name_directory + excelfile_name_pre + str(article_index) + ".xlsx"
        spider_functions.data_collector_sciencedirect(article_url, excelfile_name)
        time.sleep(delay)






