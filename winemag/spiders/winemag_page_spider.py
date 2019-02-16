import scrapy

from winemag.spiders.winemag_spider import WinemagSpider


# TODO: Do we really need meta vars.

class WinemagPageSpider(scrapy.Spider):
  name = 'winemag_page'
  url_prefix = 'https://www.winemag.com/buying-guide/{}'
  total_pages = 12772

  def start_requests(self):
    if hasattr(self, 'f'):
      with open(self.f, 'r') as f:
        for page in f:
          url = self.url_prefix.format(page.strip())
          yield scrapy.Request(url=url,
                               callback=WinemagSpider.parse_single)
