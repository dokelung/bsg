import sqlite3
import urllib.request as rst
from bs4 import BeautifulSoup
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Markup

from .pkg.soup import BSG

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

@app.route('/home', methods=['GET'])
def home():
    context = {}
    context['active_page'] = 'home'

    flash('Welcome to Beautiful Soup GUI')

    with open('test/test.html') as reader:
        html = reader.read()

    bsg = BSG(html)
    highlight_html = bsg.get_ht_html('"p"')
    context['html'] = Markup(highlight_html)

    return render_template('home.html', **context)

@app.route('/soup', methods=['GET'])
def soup():
    context = {}
    context['active_page'] = 'soup'
    context['errors'] = []
    context['url'] = request.args.get('url', '')
    context['protocol'] = request.args.get('protocol', '')
    context['soupstr'] = request.args.get('soupstr', '')
    context['remember_info'] = request.args.get('remember_info', '')

    # first time
    if not request.args.get('submitted', ''):
        flash('Use soup(find_all) to search in HTML')
        context['submitted'] = True

    # not the first time, check error
    if request.args.get('submitted', ''):
        if not context['protocol']:
            context['errors'].append('No protocol')
        if not context['url']:
            context['errors'].append('No URL')
        if not context['soupstr']:
            context['errors'].append('No query content')

    total_url = context['protocol'] + '://' + context['url']
    # not the first time and no errors
    if not context['errors'] and request.args.get('submitted', ''):
        flash('soup({soupstr}) in {url}'.format(soupstr=context['soupstr'], url=total_url))
        html = rst.urlopen(total_url).read()
        bsg = BSG(html)
        highlight_html = bsg.get_ht_html(context['soupstr'])
        context['html'] = Markup(highlight_html)
        return render_template('soup.html', **context)

    return render_template('soup.html', **context)

@app.route('/css_select', methods=['GET'])
def css_select():
    context = {}
    context['active_page'] = 'css_select'

    return render_template('home.html', **context)

@app.route('/help', methods=['GET'])
def get_help():
    context = {}
    context['active_page'] = 'help'

    return render_template('home.html', **context)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
