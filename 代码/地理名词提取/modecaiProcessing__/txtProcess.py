import csv
from mordecai import Geoparser
import json
import requests
import re
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import random

ips = ["58.218.92.86:8655","58.218.92.94:3808","58.218.92.86:8547","58.218.92.87:7513","58.218.92.89:3281","58.218.92.86:7451","58.218.92.87:6257","58.218.92.91:2568","58.218.92.90:9875","58.218.92.91:2576","58.218.92.94:4352","58.218.92.87:5492","58.218.92.86:6208","58.218.92.89:2714","58.218.92.87:5693","58.218.92.86:4413","58.218.92.89:7494","58.218.92.94:8627","58.218.92.91:6313","58.218.92.91:4289","58.218.92.87:2696","58.218.92.89:9257","58.218.92.87:7974","58.218.92.87:8720","58.218.92.87:3146","58.218.92.86:5701","58.218.92.87:2707","58.218.92.91:3854","58.218.92.89:4524","58.218.92.86:8734","58.218.92.89:5075","58.218.92.94:7303","58.218.92.86:7494","58.218.92.87:6152","58.218.92.94:9088","58.218.92.86:6142","58.218.92.86:7540","58.218.92.94:5618","58.218.92.94:3159","58.218.92.94:3081","58.218.92.91:7474","58.218.92.86:8645","58.218.92.91:6210","58.218.92.89:5623","58.218.92.86:5541","58.218.92.86:5036","58.218.92.90:9675","58.218.92.87:7993","58.218.92.94:6144","58.218.92.89:7478"]


def randHeader():
    head_connection = ['Keep-Alive', 'close']
    head_accept = ['text/html, application/xhtml+xml, */*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5', 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']

    ua = UserAgent("fake_useragent.json")

    header = {
        #'Connection': head_connection[0],
        #'Accept': head_accept[0],
        #'Accept-Language': head_accept_language[1],
        'User-Agent': ua.random,

        #'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2716.5 Safari/537.36"
    }
    # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2716.5 Safari/537.36"
    return header

def get_ip():
    """获取代理IP"""
    url = "http://www.xicidaili.com/nn"
    headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
                "Accept-Encoding":"gzip, deflate, sdch",
                "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
                "Referer":"http://www.xicidaili.com",
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
                }
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    data = soup.table.find_all("td")
    ip_compile= re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')    # 匹配IP
    port_compile = re.compile(r'<td>(\d+)</td>')                # 匹配端口
    ip = re.findall(ip_compile,str(data))       # 获取所有IP
    port = re.findall(port_compile,str(data))   # 获取所有端口
    return [":".join(i) for i in zip(ip,port)]  # 组合IP+端口，如：115.112.88.23:8080
# 设置 user-agent列表，每次请求时，可在此列表中随机挑选一个user-agnet

def translate(word,ip):
    # 有道词典 api
    # headers = randHeader()
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    # 传输的参数，其中 i 为需要翻译的内容
    key = {
        'type': "AUTO",
        'i': word,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    proxies = {
        "http": ip,
    }
    # key 这个字典为发送给有道词典服务器的内容
    response = requests.post(url , timeout = 30 , data=key)
    # response = requests.post(url ,  proxies = proxies, timeout = 30 , data=key)
    # 判断服务器是否相应成功
    if response.status_code == 200:
        # 然后相应的结果
        return response.text
    else:
        print("有道词典调用失败")
        # 相应失败就返回空
        return None

def get_reuslt(repsonse):
    # 通过 json.loads 把返回的结果加载成 json 格式
    result = json.loads(repsonse)
    print ("输入的词为：%s" % result['translateResult'][0][0]['src'])
    print ("翻译结果为：%s" % result['translateResult'][0][0]['tgt'])
    return result['translateResult'][0][0]['tgt']


# def mainbodyAnaylsis(line):
#     line = str(line)
#     cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")
#     context = cop.sub('', line).replace("NULL","").strip(digits)
#     print(context)
#     list_trans = translate(context)
#     trans_line = get_reuslt(list_trans)
#     print(trans_line)
#     places = geo.geoparse(list_trans)
#     return places

def senProcessing(line):
    line = str(line)
    cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^。]")
    context = cop.sub('', line).replace("NULL","")
    return context

def main():
    with open('output/output.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(["content", "txt_num", "geo_info"])
        num = 0
        for i in range(339764, 402847):  #339764 402848
            filePlace = "txt/" + str(i) + "——evets.result_before_merge.txt"
            try:
                ip = "58.218.92.94:4352"
                with open(filePlace, mode='r', encoding="utf-8") as f:
                    count = 0
                    for line in f.readlines():
                        try:
                            if (count == 0):
                                places = senProcessing(line)
                                count = count + 1
                                sens = places.split("。")
                                print(sens)
                                for sen in sens:
                                    if sen!="":
                                        try:
                                            list_trans = translate(sen,ip)
                                            trans_line = get_reuslt(list_trans)
                                            places = geo.geoparse(trans_line)
                                            geo_name = ""
                                            for place in places:
                                                geo_name = geo_name + "\t" + place["word"]
                                            writer.writerow([sen, i, geo_name])
                                        except Exception as e:
                                            ip = random.choice(ips)
                                            print(ip)
                                            print(e)
                        except Exception as e:
                            print('except:', e)

            except Exception as e:
                # print('except:', e)
                continue


if __name__ == '__main__':
    geo = Geoparser()
    main()

