from scrapy import spider,Request

class SplashSpider(spider.Spider):

    name = "splash"

    start_urls = ['https://www.foody.vn/',
                  'https://www.foody.vn/ha-noi',
                  'https://www.foody.vn/da-nang']

    allowed_domains = ["www.foody.vn"]

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
        while ex==true do
            local dimensions = get_dimensions()
            splash:mouse_click(dimensions.x, dimensions.y)
            splash:set_viewport_full()
            splash:wait(0.5)
            ex = exits()
            a = a +1
        end
            
        splash:set_viewport_full()
        splash:wait(1)
          
        return {
            a
        }
    end
    """

    script = """
    function main(splash,args)
        assert(splash:go(args.url))
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
        while ex==true and a<15 do
            local dimensions = get_dimensions()
            splash:mouse_click(dimensions.x, dimensions.y)
            splash:set_viewport_full()
            splash:wait(0.5)
            ex = exits()
            a = a +1
        end
            
        splash:set_viewport_full()
        splash:wait(0.5)
          
        return {
            splash:html()
        }
    end
    """

    def start_requests(self):
        for url in self.start_urls:
            yield Request(self.spash_url.format(url), self.parse)

    def parse(self, response):
        pass

    def parse_item(self,response):
        pass