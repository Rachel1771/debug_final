from pypinyin import lazy_pinyin, load_single_dict
from bs4 import BeautifulSoup
import re
import urllib.error,urllib.request
import xlwt
import json
import sqlite3
import threading
global val
val = []


#对于豆瓣top250电影爬取内容的正则表达式
findLink = re.compile(r'<a href="(.*?)">')
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)


#对于豆瓣当前某城市正在上映的电影爬取内容的正则表达式
findnowmovielink = re.compile(r'.*data-psource="poster" href="(.*?)" target="_blank">',re.S)
findnowmovieimg = re.compile(r'src="(.*?)"/>')
findnowmovietitle= re.compile(r'data-title="(.*?)"')
findnowmovieactors= re.compile(r'data-actors="(.*?)"')
findnowmovietime= re.compile(r'data-duration="(.*?)"')
findnowmovieregion= re.compile(r'data-region="(.*?)"')
findnowmoviedirector= re.compile(r'data-director="(.*?)"')
findnowmovieid = re.compile(r'id="(.*?)"')



def main():
    a = input("Enter a number: ")
    if a=="1":
        baseurl = "https://movie.douban.com/top250?start="  #指定的网页超链接
        datalist1 = getData1(baseurl)  #返回一个装有所有数据的列表
        savepath = ".\\top250.xls"  #存储数据的文档路径
        saveData1(datalist1,savepath)  #存储数据
        dbpath = "data.db"
        saveData1DB1(datalist1,dbpath)

    if a=="2":
        b = input("Enter a city: ")
        baseurl = "https://movie.douban.com/cinema/nowplaying/" + b + '/'
        datalist2 = getData2(baseurl)
        savepath = ".\\citymovies.xls"
        saveData2(datalist2,savepath)
        dbpath = "data.db"
        saveData2DB2(datalist2, dbpath)

    if a=="3":      #后台更新柱状图的参数
        updateCitiesData()

def multi_thread(usl1):
    threads = []
    for i in range(0,10):
        threads.append(
            threading.Thread(target = askURL1,args=(usl1+str(i*25),))
        )
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    # print(threads)
    return threads


#用于获得数据
def getData1(baseurl):
    global val
    datalist = []  #将获得的数据装于datalist这个列表
    multi_thread(baseurl)
    for j in range(0,10):
        soup = BeautifulSoup(val[j],"html.parser")  #解析
        for item in soup.find_all('div',class_= "item"):
            #print(item)  #一个测试点
            data = []  #将每一部电影的具体信息装入data列表
            item = str(item)
            link = re.findall(findLink,item)[0]  #详情链接
            data.append(link)
            imgSrc = re.findall(findImgSrc,item)[0]  #图片链接
            data.append(imgSrc)
            titles = re.findall(findTitle,item)  #标题
            if(len(titles) == 2 ):
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/","")
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(" ")
            rating = re.findall(findRating,item)[0]  #评分
            data.append(rating)
            judgeNum = re.findall(findJudge,item)[0]  #评分人数
            data.append(judgeNum)
            bd = re.findall(findBd,item)[0]  #概要
            bd = re.sub('\s',"",bd)
            bd = re.sub(r'/',"",bd)
            bd = re.sub('<br>',"",bd)
            data.append(bd.strip())
            datalist.append(data)  #将data列表装入datalist列表
    print(datalist)
    return datalist

def getData2(baseurl):
    datalist = []  #将获得的数据装于datalist这个列表
    html = askURL2(baseurl)
    soup = BeautifulSoup(html,"html.parser")  #解析
    for item in soup.find_all('li',class_= "list-item"): #一个测试点
            data = []  #将每一部电影的具体信息装入data列表
            item = str(item)
            link = re.findall(findnowmovielink,item)[0]
            data.append(link)
            img = re.findall(findnowmovieimg,item)[0]
            data.append(img)
            title = re.findall(findnowmovietitle,item)[0]
            data.append(title)
            director = re.findall(findnowmoviedirector, item)[0]
            data.append(director)
            actors = re.findall(findnowmovieactors,item)[0]
            data.append(actors)
            time = re.findall(findnowmovietime, item)[0]
            data.append(time)
            region = re.findall(findnowmovieregion, item)[0]
            data.append(region)
            id = re.findall(findnowmovieid,item)[0]
            data.append(id)
            datalist.append(data)  #将data列表装入datalist列表
    return datalist

#用来得到一个指定URL的网页内容(豆瓣top250)
def askURL1(url):
    #伪装为浏览器
    global val
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.55"
    }
    resquest = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(resquest)
        html = response.read().decode("utf-8")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    val.append(html)
    # print(html)
    # return html

def askURL2(url):
    # 伪装为浏览器
    head = {
        "User-Agent": " Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.36"
    }
    resquest = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(resquest)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html

def init_tb1(dbpath):
    sql = '''
          create table if not exists movie250     
          (
          info_link text,
          pic_link text,
          cname varchar ,
          ename varchar ,
          score numeric ,
          rated numeric ,
          info text
          )
    '''
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()

    cursor.execute(sql)
    cursor.execute("delete from movie250 where 1=1;")
    conn.commit()
    conn.close()

def init_tb2(dbpath):
    sql = '''
          create table if not exists citymovies 
          (
          link text,
          img text,
          title varchar ,
          director varchar ,
          actors varchar ,
          times varchar ,
          region varchar ,
          id varchar 
          )
    '''
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.execute("delete from citymovies where 1=1;")
    conn.commit()
    conn.close()

def saveData1DB1(datalist,dbpath):
    init_tb1(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index] = '"'+data[index].strip()+'"'
        sql = '''
              insert into movie250(info_link,pic_link,cname,ename,score,rated,info)
              values(%s)'''%",".join(data)

        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()

def saveData2DB2(datalist,dbpath):
    init_tb2(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    for data in datalist:
        for index in range(len(data)):
            data[index] = '"'+data[index].strip()+'"'
        sql = '''
              insert into citymovies(link,img,title,director,actors,times,region,id)
              values(%s)'''%",".join(data)


        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()

def saveData1(datalist,savepath):
    print("save...")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet = book.add_sheet("豆瓣电影Top250",cell_overwrite_ok=True)
    col = ("电影详情链接","图片链接","影片中文名字","影片外国名字","评分","评价数","相关信息")
    for i in range(0,7):
        sheet.write(0,i,col[i])
    for i in range(0,250):
        print("第%d条"%(i+1))
        data = datalist[i]
        for j in range(0,7):
            sheet.write(i,j,data[j])
    book.save(savepath)

def saveData2(datalist,savepath):
    print("save...")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet = book.add_sheet("豆瓣电影Top250",cell_overwrite_ok=True)
    col = ("电影详情链接","图片链接","影片中文名字","导演","演员","时长","制片地区","电影id")
    for i in range(0,8):
        sheet.write(0,i,col[i])
    for i in range(len(datalist)):
        print("第%d条"%(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i,j,data[j])
    book.save(savepath)

def updateCitiesData():      #用于后台更新柱状图的参数
    f = open("./static/assets/json/citiesData.json", "r" ,encoding = "utf-8")
    data_dict = (dict(json.load(f)))

    print(data_dict)
    feature_list = data_dict["features"]
    load_single_dict({ord('重'): 'chong'})
    for item in feature_list:

        item["properties"]["名称"] = "".join(lazy_pinyin(item["properties"]["名称"]))

        cityname = item["properties"]["名称"][0:len(item["properties"]["名称"]) - 3]

        print(cityname+':', end=" ")

        item["properties"]["Yuanxian"] = len(getData2("https://movie.douban.com/cinema/nowplaying/" + cityname + '/'))
        print(item["properties"]["Yuanxian"])

    f.close()
    f = open("./static/assets/json/citiesData.json", "w", encoding="GBK")
    json.dump(data_dict,f)
    f.close()

if __name__ == "__main__":
    main()
    print("爬取完成!")