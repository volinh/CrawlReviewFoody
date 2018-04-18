from scrapy import spider,Request
from scrapy_splash import SplashRequest
from testSplash.items import TestsplashItem
from scrapy.selector import Selector

# splash:set_result_content_type("text/html;  charset=utf-8")

script_start = """
    function main(splash)
        assert(splash:go(splash.args.url))
        assert(splash:wait(0.5))
        local exits = splash:jsfunc([[
            function () {
                var x = document.getElementsByClassName('fd-btn-more');
                if(x.length>0) {
                    return true;
                }
                return false;
            }
        ]])

        local get_dimensions = splash:jsfunc([[
            function () {
                var rect = document.getElementsByClassName('fd-btn-more')[0].getClientRects()[0];
                return {"x": rect.left, "y": rect.top}
            }
        ]])

        local ex = exits()
        local a = 0
        while ex==true and a<40 do
            local dimensions = get_dimensions()
            splash:mouse_click(dimensions.x, dimensions.y)
            splash:set_viewport_full()
            splash:wait(0.5)
            ex = exits()
            a = a +1
        end

        splash:set_viewport_full()
        splash:wait(0.5)

        return splash:html()
        
    end
    """

script_per_page = """
    function main(splash)
        assert(splash:go(splash.args.url))
        assert(splash:wait(0.5))
        local exits = splash:jsfunc([[
            function () {
                var x = document.getElementsByClassName('fd-btn-more');
                if(x.length>0) {
                    return true;
                }
                return false;
            }
        ]])

        local get_dimensions = splash:jsfunc([[
            function () {
                var rect = document.getElementsByClassName('fd-btn-more')[0].getClientRects()[0];
                return {"x": rect.left, "y": rect.top}
            }
        ]])

        local ex = exits()
        local a = 0
        while ex==true and a<10 do
            local dimensions = get_dimensions()
            splash:mouse_click(dimensions.x, dimensions.y)
            splash:set_viewport_full()
            splash:wait(0.5)
            ex = exits()
            a = a +1
        end

        splash:set_viewport_full()
        splash:wait(1)

        return splash:html()
    end
    """

class SplashSpider(spider.Spider):

    name = "splash"

    start_urls = ['https://www.foody.vn/ha-noi',
                  'https://www.foody.vn/',
                  'https://www.foody.vn/da-nang']

    allowed_domains = ["www.foody.vn"]

    # spash_url = 'http://localhost:8050/render.html?url={}&timeout=100&wait=2&images=0'

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='execute',
                                args={'lua_source': script_start})
            # yield Request(url,self.parse)

    def parse(self, response):
        body = response.body
        # with open("hanoi5.html","wb") as file:
        #     file.write(body)

        urls_item = response.xpath('//div[@class="avatar"]/a/@href').extract()
        print("===============================================================")
        count = 0
        for path in urls_item:
            a = path.split("/")[1]
            if a != "thanh-vien" :
                print(path)
                count +=1
                path = response.urljoin(path) + "/binh-luan"
                yield SplashRequest(path, self.parse_item, endpoint='execute',
                                args={'lua_source': script_per_page})
        print("++++++++++++{}+++++++++++".format(count))
        print("++++++++++++{}+++++++++++".format(len(urls_item)))
        print("===============================================================")



    def parse_item(self,response):
        body = response.body
        page = response.url.split("/")[-2]
        # item = TestsplashItem()
        list_it = response.xpath('//li[contains(@class,"review-item")]').extract()
        list_item = []
        for it in list_it:

            # item = TestsplashItem()
            content = Selector(text=it).xpath('//div[contains(@class,"review-des")]/div[contains(@class,"rd-des")]/span/text()').extract_first()
            if content!=None :
                content = content.replace("\n"," ")
            point = Selector(text=it).xpath('//div[contains(@class,"review-user")]//div[contains(@class,"review-points")]/span/text()').extract_first()
            # print("############################################################")
            # print(it)
            # print(content)
            # print(point)
            # print("############################################################")
            if point!=None and content!=None :
                list_item.append(point + "\t" + content)

        with open("data2/{}.txt".format(page), "w") as file:
            for i in list_item:
                file.write(i+"\n")
            # yield self.parse_detail_item(it)
        # with open("{}.html".format(page), "wb") as file:
        #     file.write(body)

    def parse_detail_item(self,it):
        print("############################################################")
        print(it)
        print("############################################################")
        item = TestsplashItem()
        item['content'] = it.xpath('//div[@class="review-des]/div[@class="rd-des"]/span/text()').extract_first()
        item['point'] = it.xpath('//div[@class="review-user"]/div[@class="review-points"]/span/text()').extract_first()
        print("====================================================================")
        print(item['content'])
        print(item['point'])
        print("====================================================================")
        yield item
