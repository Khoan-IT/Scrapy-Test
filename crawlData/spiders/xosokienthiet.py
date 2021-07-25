import scrapy
import calendar
import datetime

from scrapy.spiders import CrawlSpider
from ..items import XsktItem

def get_total_date_month(year,month):
    now = datetime.datetime.now()
    total_date = calendar.monthrange(year,month)[1]

    if year ==now.year and month==now.month and now.day < total_date:
        return now.day
    return total_date

class SoxokienthietSpider(CrawlSpider):
    name = 'xosokienthiet'
    allowed_domains = ['xskt.com.vn']
    start_urls = ['https://xskt.com.vn/xsmn/ngay-8-5-2018.html']

    month_to_scrap = 5
    year_to_scrap = 2018
    total_date = get_total_date_month(year_to_scrap,month_to_scrap)

    def start_requests(self):
        # for i in range(1,self.total_date):
        #     self.start_urls.append('https://xskt.com.vn/xsmn/ngay-{0}-{1}-{2}.html'.format(i,self.month_to_scrap,self.year_to_scrap))

        # for i in range(len(self.start_urls)):
            yield scrapy.Request(self.start_urls[0], callback = self.parse)

    # for i in range(1,total_date):
    #     start_urls.append('https://xskt.com.vn/xsmn/ngay-{0}-{1}-{2}.html'.format(i,month_to_scrap,year_to_scrap))

    def parse(self,response):
        xs_item  = XsktItem()
        tmp_data = {}
        data_resp = scrapy.Selector(response)

        xs_item['xs_info'] = [
            data_resp.xpath("//*[@id='MN0']/tr[1]/th[1]/a/text()").extract_first(),
            data_resp.xpath("//*[@id='MN0']/tr[1]/th[1]/text()").extract_first()
        ]

        for i in range(2,5):
            tmp_location = data_resp.xpath("//*[@id='MN0']/tr[1]/th[{0}]/a/text()".format(i)).extract_first()
            tmp_data[tmp_location] = {}

            for j in range(2,11):
                tmp_giai = data_resp.xpath("//*[@id='MN0']/tr[{0}]/td[1]/text()".format(j)).extract_first()
                tmp_number = None
                if tmp_giai == 'ĐB' or tmp_giai == 'G.8':
                    tmp_number = data_resp.xpath("//*[@id='MN0']/tr[{0}]/td[{1}]/b/text()".format(j,i)).extract()
                else:
                    tmp_number = data_resp.xpath("//*[@id='MN0']/tr[{0}]/td[{1}]/text()".format(j,i)).extract()
                tmp_data[tmp_location][tmp_giai] = ", ".join(tmp_number)
        xs_item['xs_data'] = tmp_data
        
        return xs_item

