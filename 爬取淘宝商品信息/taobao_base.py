#coding=utf-8
import re
import urllib.request

def spider_taobao(url):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.3',
        'Referer': 'https://item.taobao.com/item.htm',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Connection': 'keep-alive',
    }

    goods_id = re.findall('id=(\d+)', url)[0]

    try:
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req).read().decode('gbk', 'ignore')
    except Exception as e:
        print( '无法打开网页:', e.reason)

    try:
        title = re.findall('<h3 class="tb-main-title" data-title="(.*?)"', res)
        title = title[0] if title else None
        line_price = re.findall('<em class="tb-rmb-num">(.*?)</em>', res)[0]

        # 30-42行为抓取淘宝商品真实价格，该数据是动态加载的
        purl = "https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId={}&modules=price,xmpPromotion".format(goods_id)
        price_req = urllib.request.Request(url=purl, headers=headers)
        price_res = urllib.request.urlopen(price_req).read()
        price_res = price_res.decode('utf-8')  # python3
        ss=re.findall('"price":"(.*?)"', price_res)
        data = list(set(ss))
        # data列表中的价格可能是定值与区间的组合，也可能只是定值，而且不一定有序
        real_price = ""
        for t in data:
            if '-' in t:
                real_price = t
                break
        if not real_price:
            real_price = sorted(map(float, data))[0]

        #主图获取
        m_img = re.compile('<a href="#"><img data-src=\"(.+?)\"')
        mainimgs = re.findall(m_img, res)

        # 颜色图
        s_img = re.compile('<a href="javascript:;" style="background:url\\((.+?)\\) center no-repeat;"')
        spimgs = re.findall(s_img, res)

        #特点说明
        attributes =re.findall('<ul class="attributes-list">(.+?)</ul>', res, re.S)[0]
        attributes = re.findall('<li.*?">(.*?)</li>', attributes, re.S)
        attrstr = ""
        for i in range(len(attributes)):
            attrstr = attrstr + attributes[i]+"\n"


        ####详情图片
        # print(res)
        detail = re.findall(r'var g_config =.*g_config.tadInfo =', res,re.S)[0]
        detail = re.findall(r'{.*}', detail, re.S)[0]
        detail = detail.replace(' ', '').replace("\n", "")
        detail = re.findall('auctionImages:\[(.*?)\]},seller', detail, re.S)[0]
        # detail = json.loads(detail)
        # print(detail)

        # 45-53行为抓取评论数据，该数据也是动态加载的
        # comment_url = "https://rate.tmall.com/list_detail_rate.htm?itemId={}&sellerId=880734502&currentPage=1".format(
        #     goods_id)
        # comment_data = urllib.request.urlopen(comment_url).read().decode("GBK", "ignore")
        # temp_data = re.findall('("commentTime":.*?),"days"', comment_data)
        # temp_data = temp_data if temp_data else re.findall('("rateContent":.*?),"reply"', comment_data)
        # comment = ""
        # for data in temp_data:
        #     comment += data.encode('utf-8')
        # comment = comment if comment else "暂无评论"
    except Exception as e:
        print('数据抽取失败!!!', e)

    print('商品名:', title)
    print('划线价格:', line_price)
    print('真实价格:', real_price)
    print('商品链接:', url)
    print('主图',mainimgs)
    print('颜色图',spimgs)
    print('特性', attrstr)
    print('详情图片', detail)
    # print('部分评论内容:', comment)


if __name__ == '__main__':
    # url = 'https://item.taobao.com/item.htm?spm=a219r.lm944.14.9.7adb3989ykaaJv&id=541598913423&ns=1&abbucket=10#detail'
    url = input("请输入商品链接: ")
    spider_taobao(url)
