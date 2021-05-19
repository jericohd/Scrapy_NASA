
import scrapy

#Xpath


#link    response.xpath('//a[contains(@href, "blogs.nasa" ) and (parent::h2)]/@href')
#title   response.xpath('//h1[@class="entry-title"]/text()')
#resume  response.xpath('//div[@class="at-above-post addthis_tool"]//p[not(@class)]/text()

class spiderNASA(scrapy.Spider):
    name = 'nasa'
    start_urls =['https://blogs.nasa.gov/']

    custom_setings = {
        'FEED_URI': 'nasa.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        links_nasa = response.xpath('//a[contains(@href, "blogs.nasa" ) and (parent::h2)]/@href').getall()
        for link in links_nasa:
            yield response.follow(
                link, callback = self.parse_link, 
                cb_kwargs={'url': response.urljoin(link)}) 

    def parse_link(self, response, **kwargs):
        link = kwargs['url']
        title = response.xpath('//h1[@class="entry-title"]/text()').get()
        resume = response.xpath('//div[@class="at-above-post addthis_tool"]//p[not(@class)]/text()').get()

        yield {
            'url': link,
            'title': title,
            'resume': resume
        }
