from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    with open('blog_posts.json', 'r') as posts_file:
        blog_posts= json.load(posts_file)
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)