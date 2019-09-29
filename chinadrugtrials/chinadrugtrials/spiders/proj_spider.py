import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'proj'
    max_page = 227
    page_size = 40
    url = 'http://www.chinadrugtrials.org.cn'

    def start_requests(self):
        url = self.url + '/eap/clinicaltrials.searchlist'
        for i in range(1, self.max_page + 1):
            params = {
                'ckm_id': '',
                'ckm_index': '',
                'sort': 'desc',
                'sort2': 'desc',
                'rule': 'CTR',
                'currentpage': str(i),
                'pagesize': str(self.page_size),
                'keywords': '',
                'reg_no': 'CTR',
                'indication': '',
                'case_no': '',
                'drugs_name': '',
                'drugs_type': '',
                'appliers': '',
                'communities': '',
                'researchers': '',
                'agencies': '',
                'state': ''
            }
            yield scrapy.FormRequest(
                url=url,
                method='GET',
                callback=self.search_parse,
                formdata=params,
                meta={
                    'params': params
                }
                # dont_filter=True,
            )

    def search_parse(self, response):
        url = self.url + '/eap/clinicaltrials.searchlistdetail'
        registration_numbers = [i.strip() for i in response.css('#searchfrm td:nth-child(2) a::text').getall()]
        ckm_ids = [i.strip() for i in response.xpath("//tbody//tr/td[2]/a//@id").getall()]
        ckm_indexes = [i.strip() for i in response.xpath("//tbody//tr/td[2]/a//@name").getall()]
        experimental_states = [i.strip() for i in response.xpath("//tbody//tr/td[3]/a/text()").getall()]
        drug_names = [i.strip() for i in response.xpath("//tbody//tr/td[4]/a/text()").getall()]
        indications = [i.strip() for i in response.xpath("//tbody//tr/td[5]/a/text()").getall()]
        for i in range(self.page_size):
            params = response.meta['params']
            params['ckm_id'] = ckm_ids[i]
            params['ckm_index'] = ckm_indexes[i]
            yield scrapy.FormRequest(
                url=url,
                method='POST',
                callback=self.proj_parse,
                formdata=params,
                meta={
                    'registration_number': registration_numbers[i],
                    'experimental_state': experimental_states[i],
                    'drug_name': drug_names[i],
                    'indication': indications[i]
                }
            )

    def proj_parse(self, response):
        registration_number = response.meta['registration_number']
        experimental_state = response.meta['experimental_state']
        drug_name = response.meta['drug_name']
        indication = response.meta['indication']

        public_data = response.xpath("//*[contains(concat(' ', normalize-space(@class), ' '), 'cxtj_tm')]/table/tr[2]/td[4]/text()").get().strip()
        applicant = response.xpath("//*[contains(concat(' ', normalize-space(@class), ' '), 'cxtj_tm')]/table/tr[3]/td[2]/text()").get().strip()

        title = response.xpath('//td[contains(text(), "试验专业题目")]/../td[2]/text()').get().strip()

        objective = response.xpath('//*[@id="div_open_close_01"]/table[3]/tr/td[contains(text(), "试验目的")]/../../tr[2]/td/text()').get().strip()
        classification = response.xpath('//*[@id="div_open_close_01"]/table/tr/td/table/tr/td[contains(text(), "试验分类")]/../../tr[2]/td[3]/text()').get().strip()
        stage = response.xpath('//*[@id="div_open_close_01"]/table/tr/td/table/tr/td[contains(text(), "试验分期")]/../../tr[2]/td[3]/text()').get().strip()
        group = ' '.join([i.strip() for i in response.xpath('//*[@id="div_open_close_01"]/table/tr/td[contains(text(), "目标入组人数")]/../td[2]/text()').getall() if i.strip()])

        attend_date = ' '.join([i.strip() for i in response.xpath('//*[@id="div_open_close_01"]/div[contains(text(), "第一例受试者入组日期")]/../table[4]/tr/td/text()').getall() if i.strip()])
        end_data = ' '.join([i.strip() for i in response.xpath('//*[@id="div_open_close_01"]/div[contains(text(), "试验终止日期")]/../table[5]/tr/td/text()').getall() if i.strip()])

        main_leader = response.xpath('//*[@id="div_open_close_01"]/table/tr/td/table/td[contains(text(), "姓名")]/../td[2]/text()').get().strip()
        company = response.xpath('//*[@id="div_open_close_01"]/table/tr/td/table/tr/td[contains(text(), "单位名称")]/../td[2]/text()').get().strip()

        committee = ' '.join([i.strip() for i in response.xpath('//*[@id="div_open_close_01"]/table/tr/td[contains(text(), "审查结论")]/../../tr[position()>1]/td[position()=2]/text()').getall() if i.strip()])
        approved = ' '.join([i.strip() for i in response.xpath('//*[@id="div_open_close_01"]/table/tr/td[contains(text(), "审查结论")]/../../tr[position()>1]/td[position()=3]/text()').getall() if i.strip()])
        approved_date = ' '.join([i.strip() for i in response.xpath('//*[@id="div_open_close_01"]/table/tr/td[contains(text(), "审查结论")]/../../tr[position()>1]/td[position()=4]/text()').getall() if i.strip()])

        yield {
            'registration_number': registration_number,
            'experimental_state': experimental_state,
            'drug_name': drug_name,
            'indication': indication,
            'public_data': public_data,
            'applicant': applicant,
            'title': title,
            'objective': objective,
            'classification': classification,
            'stage': stage,
            'group': group,
            'attend_date': attend_date,
            'end_data': end_data,
            'main_leader': main_leader,
            'company': company,
            'committee': committee,
            'approved': approved,
            'approved_date': approved_date
        }
