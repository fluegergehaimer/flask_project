from datetime import datetime

from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev_db.db'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    text = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow)
    


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts')
def posts():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts)


@app.route('/post')
def post():
    post = Post.query.all()['id']
    return render_template('posts.html', post=post)


@app.route('/create', methods=('post', 'get'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        post = Post(title=title, text=text)
        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except Exception:
            return 'Smth wrng'
    return render_template('create.html')


@app.route('/about')
def about():
    return '<p>About</p>'


if __name__ == '__main__':
    app.run(debug=True)
