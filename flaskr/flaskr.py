"""
The backend of the app
"""
# all imports
import os
import sqlite3
from flask import Flask, request, render_template, flash, session, g, redirect, url_for, abort
from .forms import LoginForm, SignupForm, PostForm, UploadPhoto, ChangePasswordForm

# create the application instance
app = Flask(__name__)
# load config from this file
app.config.from_object(__name__)
# load default config and override config from an environment variable
app.config.update(
    dict(
        DATABASE=os.path.join(app.root_path, 'flask.db'),
        SECRET_KEY='b\x1f\xe9Z\xf5\x9c\x1dK\x9d\x01h\xca\xa372\xf8\xd0y\x7f\x96W\xdf-\xfc\xf8',
    )
)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


# connecting the database
def connect_db():
    # connects to the specific database
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv




# initializing the database
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()




# initializing the database from the cli
@app.cli.command('initdb')
def initdb_command():
    # initialize the database
    init_db()
    print("Initialized the database successfully.")




# getting the database
def get_db():
    # opens new database connection if there is none yet
    #  yet gor the current application context
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    # closes the database again at the end of the request
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()




# show messages
@app.route('/entries')
def show_posts():
    form = PostForm(request.form)
    db = get_db()
    cur = db.execute('select name, post from comments order by id desc')
    posts = cur.fetchall()
    return render_template('show_posts.html', title="Home", posts=posts, form=form)




# add new messages
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
        redirect(url_for('show_posts'))

    error = "An error occured"
    db = get_db()
    cur = db.execute('select name, post from comments order by id desc')
    posts = cur.fetchall()
    render_template(
        'show_posts.html', title="Home", posts=posts, form=form, error=error
    )




# signup
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
            redirect(url_for('signup'))

        elif sameEmail != None:
            flash("This email is already taken! Choose another.")
            redirect(url_for('signup'))

        elif samePhone != None:
            flash("This mobile number is already taken! Choose another.")
            redirect(url_for('signup'))

        else:
            db.execute(
                '''insert into users(name, password, email, phone) values (?, ?, ?, ?)''',
                (name, password, email, phone),
            )
            db.commit()
            flash("You have successfully signed up!")
            session['logged_in'] = True
            session['name'] = name
            redirect(url_for('show_posts'))

    render_template('signup.html', form=form, error=error)




# login
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
        cur = db.execute(
            '''select password from users where password = ? and email = ?''',
            (password, email),
        )
        userExist = cur.fetchone()
        if emailExist == None:
            error = "Login error."
            session['logged_in'] = False
            render_template('login.html', error=error, form=form)

        elif userExist == None:
            error = "Login Error"
            session['logged_in'] = False
            render_template('login.html', error=error, form=form)

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
            redirect(request.args.get('next') or url_for('show_posts'))

    render_template('login.html', error=error, form=form)




# changing the password if forgotten
@app.route('/change_password', methods=['POST', 'GET'])
def change_password():
    form = ChangePasswordForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        email = form.email.data
        db = get_db()
        cur = db.execute('''select name from users where email = ?''', (email,))
        emailExist = cur.fetchone()
        if emailExist == None:
            error = "Email address not found."
            render_template('change_password.html', form=form, error=error)

    render_template('change_password.html', form=form, error=error)




# logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('name', None)
    return redirect(url_for('login'))




# 404 error
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404




# 405 error
@app.errorhandler(405)
def method_not_allowed(error):
    error = None
    error = "Oops try that again"
    return render_template('method_not_allowed.html', error=error), 405
