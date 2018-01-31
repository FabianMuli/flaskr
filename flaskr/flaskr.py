"""
The backend of the app
"""

#all imports
import os
import feedparser
import sqlite3
from flask import Flask, request, render_template, flash, session, g, redirect, url_for, abort
from urllib.parse import urljoin
from werkzeug.contrib.atom import AtomFeed
from .forms import LoginForm, SignupForm, PostForm

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
    PASSWORD='fabian'
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
    form = PostForm(request.form)
    db = get_db()
    cur = db.execute('select name, post from comments order by id desc')
    posts = cur.fetchall()
    return render_template('show_entries.php', title="Home", posts=posts, form=form)

#add new entry
@app.route('/add', methods=['POST'])
def add_entry():
    form = PostForm(request.form)
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    if form.validate():
        post = form.post.data
        name = app.config['USERNAME']
        db.execute('''insert into comments(name, post) values(?, ?)''', (name, post))
        db.commit()
        flash("New comment was successfully send")
        return redirect(url_for('show_entries'))
    error = "An error occured"
    db = get_db()
    cur = db.execute('select name, post from comments order by id desc')
    posts = cur.fetchall()
    return render_template('show_entries.php', title="Home", posts=posts, form=form)

#signup
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        if form.validate_on_submit():
            name = form.first_name.data + " " + form.second_name.data
            email = form.email.data
            password = str(form.password.data)
            db = get_db()
            db.execute('insert into users(name, password, email) values (?, ?, ?)',
                        [name], [password], [email])
            db.commit()
            flash("You have successfully signed up!")
            session['logged_in'] = True
            session['name'] = name
            return redirect(url_for('show_entries'))
        error = "An error occured"
    return render_template('signup.php', form=form, error=error)

#login
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        if username != app.config['USERNAME']:
            error = "Invalid username"
        elif password != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('Successfully logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error, form=form)

#feed
def make_external(url):
    return urljoin(request.url_root, url)


@app.route('/recent.atom')
def recent_feed():
    feed = AtomFeed('Recent Articles',
                    feed_url=request.url, url=request.url_root)
    articles = Article.query.order_by(Article.pub_date.desc()) \
                      .limit(15).all()
    for article in articles:
        feed.add(article.title, unicode(article.rendered_text),
                 content_type='html',
                 author=article.author.name,
                 url=make_external(article.url),
                 updated=article.last_update,
                 published=article.published)
    return feed.get_response()

#popular posts
@app.route('/popular_posts', methods=['GET', 'POST'])
def popular_posts():
    error = None
    if not session.logged_in():
        abort(401)
    render_template("popular_posts.php", error=error)

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
