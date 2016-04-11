import sqlite3
import urllib.request as rst
from bs4 import BeautifulSoup
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Markup
from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import HtmlFormatter
from pygments.filters import KeywordCaseFilter, NameHighlightFilter
   
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

@app.route('/query', methods=['GET'])
def query():
    error = None
    if request.method == 'GET':
        if not request.args.get('url'):
            error = 'No URL'
        elif not request.args.get('query_string'):
            error = 'No query string'
        else:
            # url = request.args.get('url')
            # query_string = request.args.get('query_string')
            # flash('query!!')
            # html = rst.urlopen(url).read()
            with open('test.html') as reader:
                html = reader.read()
            soup = BeautifulSoup(html, 'html.parser')

            results = soup.find_all('title')
            mark='QUERY' + 100*'-'
            highlight_result_lst = []
            for result in results:
                # hltag = soup.new_tag(mark)
                # hltag.attrs.setdefault('class', mark)
                # result.wrap(hltag)
                # classes = result.attrs.setdefault('class', mark) 
                # if isinstance(classes, list) and mark not in classes:
                #     classes.append(mark)
                # elif not isinstance(classes, list) and classes!=mark:
                #     classes = mark
                highlight_result = highlight(BeautifulSoup(str(result), 'html.parser').prettify(), HtmlLexer(), HtmlFormatter())
                print(highlight_result)
                highlight_result = highlight_result.partition('<div class="highlight"><pre>')[2]
                print(highlight_result)
                print(highlight_result.rpartition('</pre></div>'))
                highlight_result = highlight_result.rpartition('</pre></div>')[0]
                # highlight_result = BeautifulSoup(highlight_result, 'html.parser').prettify()
                print(highlight_result)
                highlight_result_lst.append(highlight_result)

            html = soup.prettify()
            html_lexer = HtmlLexer()
            namefilter = NameHighlightFilter(names=[mark])
            html_lexer.add_filter(namefilter)
            highlight_html = highlight(html,html_lexer, HtmlFormatter())

            print()
            print()
            print()
            print()
            print()

            print(highlight_html)

            for highlight_result in highlight_result_lst:
                highlight_html = highlight_html.replace(highlight_result, '222'+highlight_result+'222')

            return render_template('query.html', html=Markup(highlight_html))

    return render_template('query.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # app.run()
