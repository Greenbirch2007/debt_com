# -*- coding:utf-8 -*-
import datetime
import re
import time

import pymysql

from lxml import etree
from selenium import webdriver






def get_first_page(url):

    driver.get(url)
    html = driver.page_source
    return html



# 可以尝试第二种解析方式，更加容易做计算
def parse_stock_note(html):
    big_list = []
    last_list = []
    selector = etree.HTML(html)
    name_cn = selector.xpath('/html/body/div[2]/div[5]/h1/text()')
    name_eg =selector.xpath('/html/body/div[2]/div[5]/h3/text()')
    assets= selector.xpath('/html/body/div[2]/div[7]/div[2]/table[2]/tbody/tr[14]/td[1]/text()')
    debts= selector.xpath('/html/body/div[2]/div[7]/div[2]/table[2]/tbody/tr[25]/td[1]/text()')
    mk = selector.xpath('//*[@id="quote_detail_wrap"]/table/tbody/tr[2]/td[3]/text()')

    contents = name_cn + name_eg+assets+debts+mk
    big_tuple_list = list(contents)
    for i in big_tuple_list:
        b = "".join(re.split(r'亿|万|市值:|\s',i))  #同时去除了空格，亿，万３个标签
        big_list.append(b)
    big_list_tuple = tuple(big_list)
    last_list.append(big_list_tuple)
    return last_list







def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='us_stock',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        cursor.executemany('insert into nas100_det (name_cn,name_eg,assets,debts,mk) values (%s,%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass






#
if __name__ == '__main__':
    nasdap100 = 'AAPL,MSFT,AMZN,GOOG,GOOGL,FB,INTC,CMCSA,PEP,CSCO,ADBE,NVDA,NFLX,TSLA,COST,PYPL,AMGN,AVGO,TXN,CHTR,SBUX,QCOM,GILD,MDLZ,TMUS,FISV,BKNG,INTU,ADP,ISRG,VRTX,MU,CSX,BIIB,AMAT,AMD,ATVI,EXC,MAR,LRCX,WBA,ADI,ROST,ADSK,REGN,ILMN,CTSH,XEL,JD,MNST,MELI,NXPI,BIDU,KHC,SIRI,PAYX,EA,LULU,EBAY,CTAS,WDAY,ORLY,VRSK,WLTW,CSGP,PCAR,KLAC,SPLK,NTES,MCHP,VRSN,ANSS,IDXX,CERN,ALXN,ASML,SNPS,FAST,DLTR,CPRT,XLNX,CDNS,ALGN,SGEN,WDC,UAL,SWKS,CDW,CHKP,ULTA,INCY,TCOM,BMRN,EXPE,MXIM,CTXS,TTWO,FOXA,AAL,NTAP,FOX,LBTYK,LBTYA'
    # f_nasdap100 = [x for x in nasdap100 if x != ","]
    f_nasdap100 = nasdap100.split(",")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome()

    for url_code in f_nasdap100:

        url_f = 'http://quotes.sina.com.cn/usstock/hq/balance.php?s={0}'.format(url_code)



        html = get_first_page(url_f)
        time.sleep(1)
        content = parse_stock_note(html)
        print(content)
        time.sleep(1)
        insertDB(content)
        print(datetime.datetime.now())
        time.sleep(1)



#name_cn,name_eg,assets,debts,mk
# create table nas100_det(
# id int not null primary key auto_increment,
# name_cn varchar(80),
# name_eg varchar(80),
# assets varchar(80),
# debts varchar(80),
# mk varchar(80)
#  ) engine=InnoDB default charset=utf8;

#
# drop table nas100_det;





# a= ['6亿','6万','8亿']
# t = []
# for i in a:
#     b = "".join(re.split(r'亿|万|\s',a))
#     t.append(b)
#
# print(t)  # t = [6,6,8]