import requests
import re
import json


query = input('请输入要搜索商品关键字>>>:')
f=open("{}淘宝竞品查找结果.csv".format(query), 'a', encoding='utf-8-sig')
f.write('标题,原价,折扣价,销量,是否包邮,邮费,是否天猫,地区,店名,商品链接\n')


headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}
for i in range(6):
    url='https://s.taobao.com/search?q={}&s={}'.format(query,i*44)
    response=requests.get(url,headers=headers)
    html=response.text
    data=re.findall(r'g_page_config = (.*?)g_srp_loadCss',html,re.S)[0]
    # print(data)
    data=data.strip(' \n;')
    data=json.loads(data)
    data=data['mods']['itemlist']['data']['auctions']
    for item in data:
        temp={
            'title':item['raw_title'],
            'view_price':item['view_price'],
            'view_sales':item['view_sales'],
            'view_fee':'否'if float(item['view_fee'])else '是',
            'isFree':item['view_fee'],
            'isTmall':'是'if item['shopcard']['isTmall']else '否',
            'area':item['item_loc'],
            'name':item['nick'],
            'detail_url':item['detail_url']
        }
        urlDetail=temp['detail_url']
        if "http" not in urlDetail:
            urlDetail = "http:"+urlDetail
        print(urlDetail)
        response2=requests.get(urlDetail,headers=headers)
        html2=response2.text
        data2=re.findall(r'TShop.Setup\((.*?)\);',html2,re.S)[0]
        data2=data2.strip(' \n;')
        # print(data2)
        data2=json.loads(data2)
        # trickyKey=data2['valItemInfo']['skuList'][0]['pvs']
        # print(trickyKey)
        # trickyKey=';'+trickyKey+';'
        # data2=data2['valItemInfo']['skuMap'][trickyKey]
        data2=data2['itemDO']
        temp['price']=data2['reservePrice']
        f.write('{title},{price},{view_price},{view_sales},{view_fee},{isFree},{isTmall},{area},{name},{detail_url}\n'.format(**temp))
        print(temp['price'])

f.close()


