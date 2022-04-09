from pprint import pprint

import requests
from lxml import html
from pymongo import MongoClient


def write_to_database(news):
    client = MongoClient('127.0.0.1', 27017)
    db = client['news_db']
    news_data = db.news
    if news_data.find_one({'link': news['link']}):
        print(f'Duplicated news {news["link"]}')
    else:
        news_data.insert_one(news)
        print(f'Success insert the link {news["link"]}')


def get_response_dom(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)
    return dom


def mail_news(dom, to_write=True):
    main_container = dom.xpath('//div[@data-logger="news__MainTopNews"]')[0]
    links = main_container.xpath(".//td[@class='daynews__items']//a/@href")
    links.extend(main_container.xpath(".//td[@class='daynews__main']//a/@href"))
    links.extend(main_container.xpath(".//li[@class='list__item']/a/@href"))
    news_list = []
    for link in links:
        news_data = {}
        dom = get_response_dom(link)
        resource = dom.xpath("//a[contains(@class,'breadcrumbs__link')]/span/text()")[0]
        title = dom.xpath("//h1[@class='hdr__inner']/text()")[0]
        time = dom.xpath("//span[@class='breadcrumbs__item']//span[@datetime]/@datetime")[0].replace('T', ' ')[:16]
        news_data['link'] = link
        news_data['title'] = title
        news_data['time'] = time
        news_data['resource'] = resource

        if to_write:
            write_to_database(news_data)

        news_list.append(news_data)
    return news_list


def search_news(*arg):
    news_list = []
    for site_name in arg:
        if 'mail' in site_name.lower():
            site = 'https://news.mail.ru/'
            dom = get_response_dom(site)
            news = mail_news(dom)
        else:
            print(f'{site_name} нет в базе данных.')
            news = None
        news_list.append(news)
    return news_list


pprint(search_news('mail'))
