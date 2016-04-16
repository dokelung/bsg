import sqlite3
import urllib.request as rst
from bs4 import BeautifulSoup
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Markup
from pygments import highlight, token
from pygments.lexers import HtmlLexer
from pygments.formatters import HtmlFormatter

import pkg.clexer as clexer
import pkg.cformatter as cformatter

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
            db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/soup', methods=['GET'])
def soup():
    error = None
    if request.method == 'GET':
        if not request.args.get('url'):
            error = 'No URL'
        elif not request.args.get('soupstr'):
            error = 'No query string'
        else:
            url = request.args.get('url')
            soupstr = request.args.get('soupstr')

            flash('soup({soupstr}) in {url}'.format(soupstr=soupstr, url=url))
            html = rst.urlopen(url).read()

            # test code
            # with open('test/test.html') as reader:
            #     html = reader.read()

            soup = BeautifulSoup(html, 'html.parser')
            tags = soup(soupstr)

            for t in tags:
                t.wrap(soup.new_tag('bsg-ht'))
            # Garfield: apply pipeline to find other types like content, class, id, url ...

            html_lexer = clexer.BSGHtmlLexer()
            html_formatter = cformatter.BSGHtmlFormatter(linenos=True)
            highlight_html = highlight(soup.prettify(), html_lexer, html_formatter)

            return render_template('soup.html', html=Markup(highlight_html))

    return render_template('soup.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
