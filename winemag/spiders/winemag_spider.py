import scrapy
from scrapy.loader import ItemLoader

from winemag.items import PageItem


class WinemagSpider(scrapy.Spider):
  name = 'winemag'
  url_prefix = 'https://www.winemag.com/?s=&drink_type=wine&page={}'
  total_pages = 12772

  def start_requests(self):
    start_page = int(self.start_page) if hasattr(self, 'start_page') else 1
    end_page = int(self.end_page) if hasattr(self,  'end_page') else self.total_pages
    end_page = min(end_page, self.total_pages)

    for page in range(start_page, end_page + 1):
      yield scrapy.Request(url=self.url_prefix.format(page), callback=self.parse)

  def parse(self, response):
    for idx, review_item in enumerate(response.css('li.review-item:not(.search-results-ad)')):
      review_listing = review_item.css('a.review-listing')
      url = review_listing.attrib.get('href')

      yield scrapy.Request(url=url, callback=WinemagSpider.parse_single)

  @staticmethod
  def parse_single(response):
    loader = ItemLoader(item=PageItem(), response=response)

    loader.add_value('url', response.url)

    loader.add_css('title', 'div.article-title')
    loader.add_css('vintage', 'div.article-title')
    loader.add_css('rating', '#points')
    loader.add_css('description', 'p.description')

    primary_info_loader = loader.nested_css('ul.primary-info')
    appellation_loader = primary_info_loader.nested_css('li.row:nth-last-child(2) div.info')

    primary_info_loader.add_css('price', 'li.row:nth-child(1) div.info')
    if len(primary_info_loader.selector.css('li.row')) == 5:
      primary_info_loader.add_css('designation', 'li.row:nth-child(2) div.info')
    primary_info_loader.add_css('varietal', 'li.row:nth-last-child(3) div.info')

    appellation_loader.add_css('subsubregion', 'span a:nth-last-child(4)')
    appellation_loader.add_css('subregion', 'span a:nth-last-child(3)')
    appellation_loader.add_css('region', 'span a:nth-last-child(2)')
    appellation_loader.add_css('country', 'span a:nth-last-child(1)')

    primary_info_loader.add_css('winery', 'li.row:nth-last-child(1) div.info')

    secondary_info_loader = loader.nested_css('ul.secondary-info')

    secondary_info_loader.add_css('alcohol', 'li.row:nth-child(1) div.info')
    secondary_info_loader.add_css('category', 'li.row:nth-child(3) div.info')

    yield loader.load_item()
