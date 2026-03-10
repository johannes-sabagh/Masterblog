from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

@app.route('/')
def index():
    """Render the homepage with all blog posts."""
    with open('blog_posts.json', 'r') as posts_file:
        blog_posts= json.load(posts_file)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Display the add post form (GET) or create a new post (POST)."""
    if request.method == 'POST':
        # Extract form data
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        with open('blog_posts.json', 'r') as posts_file:
            blog_posts = json.load(posts_file)

        # Build new post, using list length to generate a simple ID
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
    """Delete a post by ID and redirect to the homepage."""
    with open('blog_posts.json', 'r') as posts_file:
        blog_posts = json.load(posts_file)

    updated_posts = []

    # Keep all posts except the one being deleted
    for post in blog_posts:
        if post['id'] != post_id:
            updated_posts.append(post)

    blog_posts = updated_posts
    with open('blog_posts.json', 'w') as posts_file:
        json.dump(blog_posts, posts_file, indent=4)

    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Display the edit form (GET) or save updated post fields (POST)."""
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Extract updated fields from the form
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        with open('blog_posts.json', 'r') as posts_file:
            blog_posts = json.load(posts_file)

        # Find the matching post and update its fields in place
        for p in blog_posts:
            if p['id'] == post_id:
                p['author'] = author
                p['title'] = title
                p['content'] = content
                break

        with open('blog_posts.json', 'w') as posts_file:
            json.dump(blog_posts, posts_file, indent=4)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)

def fetch_post_by_id(post_id):
    """Return the post matching post_id, or None if not found."""
    with open('blog_posts.json', 'r') as posts_file:
        blog_posts = json.load(posts_file)
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)