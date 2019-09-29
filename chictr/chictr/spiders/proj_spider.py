import scrapy
import re
from xml.etree.ElementTree import parse


class QuotesSpider(scrapy.Spider):
    name = 'proj'
    start_urls = []
    # with open('ICTRP-Results-ch.xml') as f:
    #     doc = parse(f)
    #     for item in doc.iterfind('Trial'):
    #         if item.findtext('Source_Register') == 'ChiCTR':
    #             start_urls.append(item.findtext('web_address'))
    #         else:
    #             pass
    with open('ERROR') as f:
        for line in f.readlines():
            start_urls.append(line.strip())

    def parse(self, response):
        tables = []
        for i in response.css('div.ProjetInfo_ms'):
            tables.append(i)

        registration_number = tables[0].css('tr:nth-child(1) .left_title+ td::text').get().strip()
        registration_status = tables[0].css('.cn:nth-child(4) .left_title+ td .cn::text').get().strip()
        public_title = tables[0].css('.cn:nth-child(6) .left_title+ td .cn::text').get().strip()
        applicant = tables[1].css('.cn:nth-child(1) td:nth-child(2) .cn::text').get().strip()
        study_leader = tables[1].css('.cn:nth-child(1) td~ .left_title+ td .cn::text').get().strip()
        applicant_institution = tables[1].css('.cn:nth-child(10) .left_title+ td .cn::text').get().strip()
        approved = tables[2].css('.cn:nth-child(1) .left_title+ td .cn::text').get().strip()
        primary_sponsor = tables[3].css('.cn:nth-child(1) .left_title+ td .cn::text').get().strip()
        source_funding = tables[3].css('.cn:nth-child(6) .left_title+ td .cn::text').get().strip()
        study_type = tables[3].css('.cn:nth-child(12) .left_title+ td .cn::text').get().strip()
        study_objective = " " + tables[3].css('.cn:nth-child(16) .left_title+ td .cn::text').get().strip()
        study_time = tables[3].css('tr:nth-child(26) .left_title+ td::text').re(r'\d{4}-\d{2}-\d{2}')
        if len(study_time) >= 2:
            study_time_from = study_time[0]
            study_time_to = study_time[1]
        elif len(study_time) >= 1:
            study_time_from = study_time[0]
            study_time_to = ' '
        else:
            study_time_from = ' '
            study_time_to = ''

        sample_size = sum([int(i.strip()) for i in tables[4].css('.noComma tr:nth-child(1) td:nth-child(4)::text').getall()])
        outcomes = ' '.join([i.strip() for i in tables[6].css('.cn:nth-child(1) td:nth-child(2) .cn::text').getall()])
        collecting_samples = ' '.join([i.strip() for i in tables[7].css('.cn td:nth-child(2) .cn::text').getall()])
        time_sharing = tables[10].css('tr:nth-child(1) .left_title+ td::text').get().strip()

        yield {
            'url': response.url,
            'registration_number': registration_number,
            'registration_status': registration_status,
            'public_title': public_title,
            'applicant': applicant,
            'study_leader': study_leader,
            'applicant_institution': applicant_institution,
            'approved': approved,
            'primary_sponsor': primary_sponsor,
            'source_funding': source_funding,
            'study_type': study_type,
            'study_objective': study_objective,
            'study_time_from': study_time_from,
            'study_time_to': study_time_to,
            'sample_size': sample_size,
            'outcomes': outcomes,
            'collecting_samples': collecting_samples,
            'time_sharing': time_sharing
        }
