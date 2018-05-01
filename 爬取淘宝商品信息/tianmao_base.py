#conding=utf-8
import re
import json
import urllib.request

def conver_str(string):
    sring = re.sub(r'&nbsp;',' ',string)
    partten = re.compile(r'&#\d+;')
    while True:
        m = partten.search(string)
        if m:
            #找到中文编码
            ch = m.group()
            # 获取数字
            ch = re.search(r'\d+',ch).group()
            # 编码转换为中文
            ch = chr(int(ch))
            # 替换回去
            string = partten.sub(ch,string,1)
        else:
            break
    return string

def spider_tianmao(url):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.3',
        'Referer': 'https://detail.tmall.com/item.htm',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Connection': 'keep-alive',
    }

    try:
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req).read().decode('gbk', 'ignore')
    except Exception as e:
        print( '无法打开网页:', e.reason)

    try:
        title = re.findall('<input type="hidden" name="title" value="(.*?)"', res)
        title = title[0] if title else None
        price = re.findall('<span class="tm_price">(.*?)</span>', res)
        price = price[0] if price else None

        #主图获取
        m_img = re.compile('<a href="#"><img src=\"(.+?)\"')
        mainimgs = re.findall(m_img, res)

        # 颜色图
        s_img = re.compile('<a href="#" style="background:url\\((.+?)\\) center no-repeat;"')
        spimgs = re.findall(s_img, res)

        # 特点说明
        attributes = re.findall('<ul id="J_AttrUL">(.+?)</ul>', res, re.S)[0]
        attributes = re.findall('<li.*?">(.*?)</li>', attributes, re.S)
        attrstr = ""
        for i in range(len(attributes)):
            attrstr = attrstr + conver_str(attributes[i])+ "\n"

        #规格参数
        tableAttr = re.findall('<div id="J_Attrs" class="J_DetailSection">(.+?)</div>', res, re.S)[0]
        tableAttr = re.findall(r'<th.*?>(.*?)</th><td>(.*?)</td>', tableAttr, re.I | re.M)
        attr_params =""
        for i in range(len(tableAttr)):
            key = tableAttr[i][0]
            value = conver_str(tableAttr[i][1])
            attr_params = attr_params + (key +':'+ value)+ "\n"

        #详情图片
        detail_url = re.findall('"descUrl":"(.+?)","fetchDcUrl"', res, re.S)[0]
        req = urllib.request.Request(url="http:"+detail_url, headers=headers)
        detail_html = urllib.request.urlopen(req).read().decode('gbk', 'ignore')
        detail_html = re.findall("var desc='(.+?)'",detail_html, re.S)[0]
        detail_imgs = re.findall('<img src="(.*?)"', detail_html, re.S)

    except Exception as e:
        print('数据抽取失败!!!', e)

    print('商品名:', title)
    print('真实价格:', price)
    print('商品链接:', url)
    print('主图',mainimgs)
    print('颜色图',spimgs)
    print('特性', attrstr)
    print('规格参数', attr_params)
    print('详情图片', detail_imgs)


if __name__ == '__main__':
    url = 'https://detail.tmall.com/item.htm?spm=a230r.1.14.6.5b4833a353RagY&id=563991901042&cm_id=140105335569ed55e27b&abbucket=16'
    # url = input("请输入商品链接: ")
    spider_tianmao(url)




