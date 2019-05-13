import requests
from lxml import etree


def get_html(url1):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                 "(KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"}
        r = requests.get(url1, timeout=30, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        html_text = r.text.encode("utf8")
    # print(html_text)
    except requests.exceptions.ConnectTimeout:
        html_text = ""
    return html_text


def parse_google_scholar(url1):
    essay_list = []
    html1 = get_html(url1)
    page = etree.HTML(html1)
    person_essay = page.xpath("//tr[@class='gsc_a_tr']/td[@class='gsc_a_t']/a")
    for essay in person_essay:
        essay_list.append(essay.xpath('./text()')[0])
    return essay_list


def get_info_from_google(url1):
    url1 = url1 + "&pagesize=10000"
    lists = parse_google_scholar(url1)
    return lists

