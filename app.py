from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    with open('blog_posts.json', 'r') as posts_file:
        blog_posts= json.load(posts_file)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        with open('blog_posts.json', 'r') as posts_file:
            blog_posts = json.load(posts_file)

        new_post = {
            'id' : len(blog_posts)+1,
            'author' : author,
            'title' : title,
            'content' : content
        }
        blog_posts.append(new_post)

        with open('blog_posts.json', 'w') as posts_file:
            json.dump(blog_posts, posts_file, indent=4)
        return redirect(url_for('index'))


    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    with open('blog_posts.json', 'r') as posts_file:
        blog_posts = json.load(posts_file)

    updated_posts = []

    for post in blog_posts:
        if post['id'] != post_id:
            updated_posts.append(post)

    blog_posts = updated_posts
    with open('blog_posts.json', 'w') as posts_file:
        json.dump(blog_posts, posts_file, indent=4)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)