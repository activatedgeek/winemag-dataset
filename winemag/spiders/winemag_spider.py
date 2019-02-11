import scrapy
from scrapy.loader import ItemLoader

from winemag.items import ReviewItem


class WinemagSpider(scrapy.Spider):
  name = 'winemag'
  url_prefix = 'https://www.winemag.com/?s=&drink_type=wine&page={}'
  total_pages = 12772

  def start_requests(self):
    start_page = int(self.start_page) if hasattr(self, 'start_page') else 1
    end_page = int(self.end_page) if hasattr(self,  'end_page') else self.total_pages
    end_page = min(end_page, self.total_pages)

    for page in range(start_page, end_page + 1):
      yield scrapy.Request(url=self.url_prefix.format(page),
                           callback=self.parse,
                           meta=dict(
                             page=page
                           ))

  def parse(self, response):
    for idx, review_item in enumerate(response.css('li.review-item:not(.search-results-ad)')):
      review_listing = review_item.css('a.review-listing')
      url = review_listing.attrib.get('href')

      yield scrapy.Request(url=url, callback=self.parse_single,
                           meta=dict(
                             **response.meta,
                             item=idx
                           ))

  def parse_single(self, response):
    loader = ItemLoader(item=ReviewItem(), response=response)

    title = response.css('div.article-title::text').get()
    rating = response.css('#points::text').get()
    description = response.css('p.description::text').get()

    p_info_fields = [
      f.lower()
      for f in response.css('ul.primary-info div.info-label span::text').getall()
    ]

    p_info = response.css('ul.primary-info div.info')

    price = p_info[p_info_fields.index('price')].css('div.info span::text').get()
    if 'designation' in p_info_fields:
      designation = p_info[p_info_fields.index('designation')].css('div.info span::text').get()
    varietal = p_info[p_info_fields.index('variety')].css('div.info a::text').get()
    appellation = p_info[p_info_fields.index('appellation')].css('span a::text').getall()
    winery = p_info[p_info_fields.index('winery')].css('div.info a::text').get()

    s_info_fields = [
      f.lower()
      for f in response.css('ul.secondary-info div.info-label span::text').getall()
    ]

    s_info = response.css('ul.secondary-info div.info')

    alcohol = s_info[s_info_fields.index('alcohol')].css('div.info span::text').get()
    category = s_info[s_info_fields.index('category')].css('div.info span::text').get()

    loader.add_value('meta_url', response.url)
    loader.add_value('meta_page', response.meta['page'])
    loader.add_value('meta_item', response.meta['item'])

    loader.add_value('title', title)
    loader.add_value('rating', rating)
    loader.add_value('description', description)

    loader.add_value('price', price)
    if 'designation' in p_info_fields:
      loader.add_value('designation', designation)
    loader.add_value('varietal', varietal)
    if len(appellation):
      loader.add_value('country', appellation[-1])
    if len(appellation) > 1:
      loader.add_value('region', appellation[-2])
    if len(appellation) > 2:
      loader.add_value('subregion', appellation[-3])
    if len(appellation) > 3:
      loader.add_value('subsubregion', appellation[-4])
    loader.add_value('winery', winery)
    loader.add_value('vintage', title)

    loader.add_value('alcohol', alcohol)
    loader.add_value('category', category)

    yield loader.load_item()
