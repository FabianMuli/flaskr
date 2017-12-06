"""
The backend of the app
"""
#all imports
import os
import feedparser
import sqlite3
from flask import Flask, request, render_template, flash, session, g, redirect, url_for, abort
from .forms import LoginForm, SignupForm

BBC_FEED = "https://feeds.bbci.co.uk/news/rss.xml"
#create the application instance
app = Flask(__name__)

#load config from this file
app.config.from_object(__name__)

#load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flask.db'),
    SECRET_KEY='b\x1f\xe9Z\xf5\x9c\x1dK\x9d\x01h\xca\xa372\xf8\xd0y\x7f\x96W\xdf-\xfc\xf8',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    #connects to the specific datbase
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    #initialize the database
    init_db()
    print("Initialized the database successfully.")

def get_db():
    #opens new database connection if there is none yet
    #  yet gor the current application context
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    #closes the database again at the end of the request
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

#show entries
@app.route('/entries')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.php', title="Home", entries=entries)

#add new entry
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries(title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    flash("New message was successfully send")
    return redirect(url_for('show_entries'))

#login
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = "Invalid username"
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('Successfully logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error, form=form)

#feed
@app.route('/feed', methods=['GET', 'POST'])
def feed():
    feed = feedparser.parse(BBC_FEED)
    first_article = feed['entries'][0]
    title = first_article.get("title")
    time = first_article.get("published")
    summary = first_article.get("summary")
    return render_template('feed.php', summary=summary, time=time,
                           first_article=first_article)

#popular posts
@app.route('/popular_posts', methods=['GET', 'POST'])
def popular_posts():
    error = None
    if not session.logged_in():
        abort(401)
    render_template("popular_posts.php", error=error)

#friends page
@app.route('/friends', methods=['GET', 'POST'])
def friends():
    error = None
    if not session.logged_in():
        abort(401)
    render_template('friends.php', error=error)

#logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You logged out')
    return redirect(url_for('login'))

#404 error
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

#405 error
@app.errorhandler(405)
def method_not_allowed(error):
    error = None
    error = "Oops try that again"
    return render_template('method_not_allowed.html', error=error), 405
