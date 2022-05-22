import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    user_id = scrapy.Field()
    username = scrapy.Field()
    photo = scrapy.Field()
    fullname = scrapy.Field()
    all_info = scrapy.Field()
    _id = scrapy.Field()