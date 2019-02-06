from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:h7mfGQuWUn5UEsee@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(1000))
    posted = db.Column(db.Boolean)

    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.posted = False

@app.route('/blog', methods=['GET'])
def index(): 

    posts = Blog.query.filter_by(posted=False).all()
    posted_blogs = Blog.query.filter_by(posted=True).all()

    return render_template('blog.html', title = 'Build A Blog',
    posts=posts, posted_blogs=posted_blogs)

@app.route('/completed_posts', methods=['POST'])
def completed_posts():

    title_id = int(request.form['title-id'])
    title_post = Blog.query.get(title_id)
    content_id = int(request.form['content-id'])
    content_post = Blog.query.get(content_id)
    title_post.completed = True
    content_post.completed = True
    db.session.add(title_post)
    db.session.add(content_post)
    db.session.commit()

    return redirect('/blog')

@app.route('/newpost', methods=['POST', 'GET'])
def add_blog_entry():

    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        new_post = Blog(post_title,post_content)
        db.session.add(new_post)
        db.session.commit()

    
    return render_template('newpost.html',title="Add Blog Entry")

if __name__ == '__main__':
    app.run()