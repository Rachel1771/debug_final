from flask import *
from flask import Flask
from spider import *
from word import makeWordcloud
from pypinyin import lazy_pinyin, load_single_dict
app = Flask(__name__)
datalist = []
movieScore = []
num = []
page=[1,2,3,4,5,6,7,8,9,10]
@app.route('/')
def index():
    return render_template('first.html')

@app.route('/first')
def first():
    return index()

@app.route('/movie')
def movie():
    if len(datalist) == 0:
        baseurl = "https://movie.douban.com/top250?start="  # 指定的网页超链接
        datalist1 = getData1(baseurl)  # 返回一个装有所有数据的列表

        print(datalist1)
        for item in datalist1:
            datalist.append(item)
        saveData1(datalist1, "top250.xls")

    page=1
    movies=[]
    #对列表进行分�?
    for i in range(25):
        movies.append(datalist[i])
    return render_template('movie.html', movies=movies, page=page)

#进行分页
@app.route('/movie/start=<int:page>')
def movie2(page):
    movies=[]
    #对列表进行分�?
    if page:    #page存在
        first=(page-1)*25   #首页
        last=page*25    #尾页
    else :
        first=0   #首页
        last=25    #尾页
    for i in range(first,last):
        movies.append(datalist[i])
    #列表分割完成
    if page == 1:
        return render_template('movie.html', movies=movies, page=page)
    elif page == 2:
        return render_template('movie.html', movies=movies, page=page)
    elif page == 3:
        return render_template('movie.html', movies=movies, page=page)
    elif page == 4:
        return render_template('movie.html', movies=movies, page=page)
    elif page == 5:
        return render_template('movie.html', movies=movies, page=page)
    elif page == 6:
        return render_template('movie.html', movies=movies, page=page)
    elif page == 7:
        return render_template('movie.html', movies=movies, page=page)
    elif page == 8:
        return render_template('movie.html', movies=movies, page=page)
    elif page == 9:
        return render_template('movie.html', movies=movies, page=page)
    elif page == 10:
        return render_template('movie.html', movies=movies, page=page)
    else :
        return render_template('movie.html', movies=movies, page=page)

@app.route('/score')
def score():
    if (movieScore == [] or num == []):
        # print("关于评分数据库被启动�?!")
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        sql = "select score,count(score) from movie250 group by score"
        data = cur.execute(sql)
        for item in data:
            movieScore.append(item[0])
            num.append(item[1])
        cur.close()
        con.close()
    return render_template('score.html', movieScore=movieScore, num=num)

@app.route('/word')
def word():
    return render_template('word.html')

# 上传文件
@app.route('/upload_file', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        f.filename = 'upload.jpg'
        f.save(f.filename)
    return render_template('word.html')

@app.route('/separate')
def separate():
    return render_template('separate.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/cities')
def cities():
    return render_template('cities.html')

@app.route('/citylist')
def citylist():
    load_single_dict({ord('�?'): 'chong'})
    datalist1 = []
    cityname = request.url
    print("cityname=" + cityname)
    cityname = "".join(lazy_pinyin(cityname))
    cityname = cityname[cityname.index('=') + 1:len(cityname)]
    print("cityname=" + cityname)

    baseurl = "https://movie.douban.com/cinema/nowplaying/" + cityname + '/'
    dbpath = "data.db"

    con = sqlite3.connect(dbpath)
    cur = con.cursor()
    datalist_get = getData2(baseurl)
    saveData2DB2(datalist_get, dbpath)
    saveData2(datalist_get,"citylist.xls")
    sql = "select * from citymovies"
    data = cur.execute(sql)

    for item in data:
        datalist1.append(item)
    cur.close()
    con.close()

    citymovies=[]
    #对列表进行分�?
    for i in range(len(datalist1)):
        citymovies.append(datalist1[i])
    return render_template('citylist.html', citymovies = citymovies)

@app.route('/citylist.xls')
def citylist_xls():
    return send_from_directory("./","citylist.xls")

@app.route('/top250.xls')
def top250_xls():
    return send_from_directory("./","top250.xls")

@app.route('/upload.jpg')
def upldIMG():
    return send_from_directory("./","upload.jpg")

@app.route('/output.jpg')
def outJPG():
    makeWordcloud("upload.jpg")
    return send_from_directory("./","output.jpg")

@app.route('/updateDBTb1')
def updateDBTb1():
    datalist_get = getData1("https://movie.douban.com/top250?start=")
    saveData1DB1(datalist_get, "data.db")
    return "数据库更新成功！"



if __name__ == "__main__":
    app.run(debug=True)