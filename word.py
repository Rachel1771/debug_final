import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import sqlite3

def makeWordcloud(image_name):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    sql = 'select info from movie250 '
    data = cur.execute(sql)
    text = ""
    for item in data:
        text = text + item[0]
    cur.close()
    con.close()
    cut = jieba.cut(text)
    string = ' '.join(cut)
    img = Image.open(image_name)
    img_array = np.array(img)
    wc = WordCloud(
        # background_color = 'white',
        # mask = img_array,
        # font_path = 'simsun.ttc'
        font_path="msyhbd.ttc",
        mask=img_array,
        width=1500,
        height=1000,
        background_color="white",
        min_font_size=5,
        max_font_size=120,
        max_words=600
    )
    wc.generate_from_text(string)
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')
    plt.savefig('output.jpg', dpi=1600)