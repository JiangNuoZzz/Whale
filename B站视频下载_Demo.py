import requests
from lxml import html
import re
from lxml import etree
def get_cid(aid):
    url="https://api.bilibili.com/x/player/pagelist?aid={aid}&jsonp=jsonp".format(aid=aid)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
    headers = {'User-Agent':user_agent}
    html = requests.get(url,headers = headers).json()
    cid=html["data"][0]["cid"]
    return cid

def get_aid(url):    
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
    headers = {'User-Agent':user_agent}
    r = requests.get(url,headers = headers)
    selector=etree.HTML(r.text)
    oaid=selector.xpath("/html/head/meta[10]/@content")
    naid=re.split('/',str(oaid))
    aid=re.split('av',str(naid[4]))[1]
    print(oaid)
    return aid

def get_bvid(url):
    bvid=re.split('\?',re.split('/',url)[4])[0]
    return bvid

def save_movie(res,name):#保存视频
    chunk_size = 1024
    with open("{name}.flv".format(name = name),"wb") as f:
        for data in res.iter_content(1024):
            f.write(data)           
if __name__ == "__main__":
    url=input("输入B站网址")
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    headers = {'User-Agent':user_agent}
    r = requests.get(url,headers = headers)
    selector=etree.HTML(r.text)

    name=selector.xpath("/html/head/meta[9]/@content")[0][:-26]
    
    bvid=get_bvid(url)
    aid=get_aid(url)
    cid=get_cid(aid)
    url="https://api.bilibili.com/x/player/playurl?cid={cid}&bvid={bvid}&qn=0&type=&otype=json".format(cid=cid,bvid=bvid)
    print(url)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
    headers = {'User-Agent':user_agent}
    html = requests.get(url,headers = headers).json()["data"]["durl"][0]["url"]
    #html = requests.get(url,headers = headers)
    
    
    
    #SAVE 
    headers2 = {
        "host": "",
        "Referer": "https://www.bilibili.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
    }
    h = re.findall("http://(.+)com",html)
    host = h[0]+"com"
    headers2["host"] = host
    print(headers2)
    res = requests.get(html,headers=headers2,stream=True, verify=False)
    print(res.status_code)
    print(name)
    print(html)
    with open("{name}.flv".format(name = name),"wb") as f:
            for data in res.iter_content(1024):
                f.write(data)
                
                

