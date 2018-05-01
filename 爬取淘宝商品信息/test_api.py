import taobao_base as tb
from flask import Flask, url_for

app = Flask(__name__)

@app.route('/')
def api_root():
    # tb.spider_taobao("https://item.taobao.com/item.htm?spm=a219r.lm944.14.9.7adb3989ykaaJv&id=541598913423&ns=1&abbucket=10#detail")
    return 'Welcome'

@app.route('/articles')
def api_articles():
    return 'List of ' + url_for('api_articles')

@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid

if __name__ == '__main__':
    app.run()