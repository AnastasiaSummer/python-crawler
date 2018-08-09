import requests
import re
import json



query = input('请输入要搜索商品关键字>>>:')
url='https://s.taobao.com/search?q={}'.format(query)

headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}

response=requests.get(url)
html=response.text

data=re.findall(r'g_page_config = (.*?)g_srp_loadCss',html,re.S)[0]
data=data.strip(' \n;')
data=json.loads(data)
data=data['mods']['itemlist']['data']['auctions']

f=open("{}淘宝竞品查找结果.csv".format(query), 'w', encoding='utf-8-sig')
f.write('标题,标价,销量,是否包邮,邮费,是否天猫,地区,店名,商品链接\n')

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
    f.write('{title},{view_price},{view_sales},{view_fee},{isFree},{isTmall},{area},{name},{detail_url}\n'.format(**temp))

f.close()


