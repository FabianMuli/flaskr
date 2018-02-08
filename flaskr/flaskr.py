"""
The backend of the app
"""

#all imports
import os
import sqlite3
from flask import Flask, request, render_template, flash, session, g, redirect, url_for, abort
from urllib.parse import urljoin
from .forms import LoginForm, SignupForm, PostForm, UploadPhoto
#create the application instance
app = Flask(__name__)

#load config from this file
app.config.from_object(__name__)

#load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flask.db'),
    SECRET_KEY='b\x1f\xe9Z\xf5\x9c\x1dK\x9d\x01h\xca\xa372\xf8\xd0y\x7f\x96W\xdf-\xfc\xf8',
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
def show_posts():
    form = PostForm(request.form)
    name = session.get('name')
    db = get_db()
    cur = db.execute('select name, post from comments order by id desc')
    posts = cur.fetchall()
    return render_template('show_posts.php', title="Home", posts=posts, form=form)

#add new entry
@app.route('/add', methods=['POST'])
def add_entry():
    form = PostForm(request.form)
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    if form.validate():
        post = form.post.data
        name = session['name']
        db.execute('''insert into comments(name, post) values(?, ?)''', (name, post))
        db.commit()
        flash("New post was send")
        return redirect(url_for('show_posts'))
    error = "An error occured"
    db = get_db()
    cur = db.execute('select name, post from comments order by id desc')
    posts = cur.fetchall()
    return render_template('show_posts.php', title="Home", posts=posts, form=form)

#upload profile photo
@app.route('/addpic', methods=['GET','POST'])
def profilePhoto():
    return redirect(url_for('Profile'))

#signup
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        name = form.first_name.data + " " + form.second_name.data
        email = form.email.data
        phone = form.mobile_number.data
        password = str(form.password.data)
        db = get_db()
        cur = db.execute('''select name from users where name = ?''', (name,))
        sameName = cur.fetchone()
        cur = db.execute('''select email from users where email = ?''', (email,))
        sameEmail = cur.fetchone()
        cur = db.execute('''select phone from users where phone = ?''', (phone,))
        samePhone = cur.fetchone()
        if sameName != None:
            flash("The username is already taken, pick another!")
            return redirect(url_for('signup'))
        elif sameEmail != None:
            flash("This email is already taken! Choose another.")
            return redirect(url_for('signup'))
        elif samePhone != None:
            flash("This mobile number is already taken! Choose another.")
            return redirect(url_for('signup'))
        else:
            db.execute('''insert into users(name, password, email, phone) values (?, ?, ?, ?)''',
                       (name, password, email, phone))
            db.commit()
            flash("You have successfully signed up!")
            session['logged_in'] = True
            session['name'] = name
            return redirect(url_for('show_posts'))
    return render_template('signup.php', form=form, error=error)

#login
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        db = get_db()
        cur = db.execute('''select email from users where email = ?''', (email,))
        emailExist = cur.fetchone()
        cur = db.execute('''select password from users where password = ? and email = ?''',
                         (password, email))
        userExist = cur.fetchone()
        if emailExist == None:
            error = "The email does not exist."
            session['logged_in'] = False
            return render_template('login.html', error=error, form=form)
        elif userExist == None:
            error = "Invalid password."
            session['logged_in'] = False
            return render_template('login.html', error=error, form=form)
        else:
            session['logged_in'] = True
            cur = db.execute('''select name from users where email = ?''', (email,))
            for row in cur:
                name = row[0]
                session['name'] = name
                break
            else:
                name = "user"
            name = session.get('name')
            welcome = "Welcome back, " + name
            flash(welcome)
            return redirect(request.args.get('next') or url_for('show_posts'))
    return render_template('login.html', error=error, form=form)


#trending
@app.route('/Trending', methods=['POST', 'GET'])
def Trending():
    return render_template('Trending.php')

#profile page
@app.route('/user', methods=['GET','POST'])
def Profile():
    name = session.get('name')
    form = UploadPhoto(request.form)
    picture = form.picture.data
    form.picture.data = ''
    db = get_db()
    if form.validate():
        db.execute('''insert into profile(name,profilePhoto) values (?,?)''', (name, picture))
        flash("Profile photo uploaded successfully")
    return render_template('profile.php', name=name, form=form)

@app.route('/followers')
def Followers():
    db = get_db()
    cur = db.execute('''select name from followers order by id asc''')
    followers = cur.fetchall()
    return render_template('followers.php', followers=followers)

#adding followers
@app.route('/addFollowers')
def addFollowers():
    db = get_db()
    follower = "Fabian muema"
    db.execute('''insert into followers(name) values (?)''', (follower,))
    db.commit()
    return redirect(url_for('Followers'))

#when a user clicks the unfollow button
@app.route('/remove')
def removeFollowers():
    db = get_db()
    follower = "Fabian muema"
    db.execute('''delete from followers where name = ?''', (follower,))
    db.commit()
    return redirect(url_for('Followers'))

#popular posts
@app.route('/popular_posts', methods=['GET', 'POST'])
def popular_posts():
    if session.get('logged_in'):
        return render_template("popular_posts.php")
    elif session.get('logged_out'):
        abort(401)

#logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('name', None)
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

