# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChictrItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    registration_number = scrapy.Field()
    experimental_state = scrapy.Field()
    drug_name = scrapy.Field()
    indication = scrapy.Field()
    public_data = scrapy.Field()
    applicant = scrapy.Field()
    title = scrapy.Field()
    objective = scrapy.Field()
    classification = scrapy.Field()
    stage = scrapy.Field()
    group = scrapy.Field()
    attend_date = scrapy.Field()
    end_data = scrapy.Field()
    main_leader = scrapy.Field()
    company = scrapy.Field()
    committee = scrapy.Field()
    approved = scrapy.Field()
    approved_date = scrapy.Field()
