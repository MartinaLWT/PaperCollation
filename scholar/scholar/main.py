from scrapy import cmdline

cmdline.execute('scrapy crawl google_spider -a category=https://scholar.google.com.sg/citations?user=XEiWEDAAAAAJ&hl=zh-CN'.split())