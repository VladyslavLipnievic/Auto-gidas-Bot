import scrapy


carsLinks = []
pagesCount = 0

### settings 
mainurl = "https://autogidas.lt/skelbimai/automobiliai/?f_1[0]=&f_model_14[0]=&f_216=1000&f_2[1]=Dyzelinas&f_50=kaina_asc&page="
motValid = "2026"  
###
class ExampleSpider(scrapy.Spider):
    name = "example"
    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }
    
    def start_requests(self):
        url = mainurl+"1"
        
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        
        global pagesCount
        pages = response.css('div[class="page"]')
        pagesCount = pages[0].xpath('string()').get()
        for pageNum in range(int(pagesCount)):
            pageNumber = pageNum + 1
            yield scrapy.Request(url=mainurl+str(pageNumber), callback=self.getCarsLinks) # TODO do it in loop 
        
        
    def getCarsLinks(self, response):
        links = response.css('a[onclick="showWatchedBadge(this);"]')
        for link in links:
            carLink = "https://autogidas.lt"+str(link.attrib['href'])
            yield scrapy.Request(url=carLink, callback=self.getCarsLinksMot) 
        
    def getCarsLinksMot(self, response):
        
        imgs = response.css('img[src*="https://static.autogidas.lt/static/img/ico/svg/out-of-stock-lt.svg"]')
        
        
        if len(imgs) != 0:
            return
        
        mot = response.css('div.value[class="value"]:contains("'+motValid+'")')
        if motValid in str(mot.xpath('string()').get()):
            carsLinks.append(response.url)
        
        
    def closed(self,reason):
        with open("automobiliai.html", 'w') as f:
            f.write('<html>\n<body>\n')
            for link in carsLinks:
                f.write(f'<a href="{link}">{link}</a><br>\n')
            f.write('</body>\n</html>')