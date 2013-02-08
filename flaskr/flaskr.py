#@+leo-ver=5-thin
#@+node:peckj.20130208092851.1378: * @file flaskr.py
#@@language python
#@@tabwidth -2

#@+<< imports >>
#@+node:peckj.20130208092851.1379: ** << imports >>
# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
#@-<< imports >>
#@+<< configuration >>
#@+node:peckj.20130208092851.1381: ** << configuration >>
# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
#@-<< configuration >>
#@+<< declarations >>
#@+node:peckj.20130208092851.1382: ** << declarations >>
# create our application
app = Flask(__name__)
app.config.from_object(__name__)
#@-<< declarations >>

#@+others
#@+node:peckj.20130208092851.1384: ** database
#@+node:peckj.20130208092851.1380: *3* connect_db
def connect_db():
  return sqlite3.connect(app.config['DATABASE'])

#@+node:peckj.20130208092851.1385: *3* init_db
def init_db():
  with closing(connect_db()) as db:
    with app.open_resource('schema.sql') as f:
      db.cursor().executescript(f.read())
    db.commit()
#@+node:peckj.20130208092851.1386: *3* database connection callbacks
@app.before_request
def before_request():
  g.db = connect_db()
  
@app.teardown_request
def teardown_request(exception):
 g.db.close()
#@+node:peckj.20130208092851.1387: ** views
#@+node:peckj.20130208092851.1388: *3* index (show entries)
@app.route('/')
def show_entries():
  cur = g.db.execute('SELECT title, text FROM entries ORDER BY id DESC')
  entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
  return render_template('show_entries.html', entries=entries)
#@+node:peckj.20130208092851.1389: *3* add new entry
@app.route('/add', methods=['POST'])
def add_entry():
  if not session.get('logged_in'):
    abort(401)
  g.db.execute('INSERT INTO entries (title, text) VALUES (?, ?)',
               [request.form['title'], request.form['text']])
  g.db.commit()
  flash('New entry was successfully posted')
  return redirect(url_for('show_entries'))
#@+node:peckj.20130208092851.1390: *3* login
@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME']:
      error = 'Invalid username'
    elif request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid password'
    else:
      session['logged_in'] = True
      flash('You were logged in')
      return redirect(url_for('show_entries'))
  return render_template('login.html', error=error)
#@+node:peckj.20130208092851.1391: *3* logout
@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('show_entries'))
#@-others

#@+<< __main__ >>
#@+node:peckj.20130208092851.1383: ** << __main__ >>
if __name__ == '__main__':
  app.run()
#@-<< __main__ >>


#@-leo
