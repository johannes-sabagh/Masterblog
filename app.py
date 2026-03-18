from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


POSTS_FILE = 'blog_posts.json'


def load_posts():
    """Load and return all blog posts from the JSON file."""
    try:
        with open(POSTS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_posts(posts):
    """Save the list of blog posts to the JSON file."""
    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f, indent=4)



@app.route('/')
def index():
    """Render the homepage with all blog posts."""
    return render_template('index.html', posts=load_posts())


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Display the add post form (GET) or create a new post (POST)."""
    if request.method == 'POST':
        # Extract form data

        author = request.form.get('author','').strip()
        title = request.form.get('title', '').strip()
        content = request.form.get('content').strip()
        if not author or not title or not content:
            return render_template('add.html', error='All field are required')


        blog_posts = load_posts()

        # Build new post, deriving ID from the current max to avoid duplicates after deletions
        new_id = max((p['id'] for p in blog_posts), default=0) + 1
        new_post = {
            'id' : new_id,
            'author' : author,
            'title' : title,
            'content' : content
        }
        blog_posts.append(new_post)
        save_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """Delete a post by ID and redirect to the homepage."""
    blog_posts = load_posts()
    save_posts([p for p in blog_posts if p['id'] != post_id])
    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Display the edit form (GET) or save updated post fields (POST)."""
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        author = request.form.get('author', '').strip()
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not author or not title or not content:
            return render_template('update.html', post=post, error="All fields are required.")

        blog_posts = load_posts()

        # Find the matching post and update its fields in place
        for p in blog_posts:
            if p['id'] == post_id:
                p['author'] = author
                p['title'] = title
                p['content'] = content
                break

        save_posts(blog_posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


def fetch_post_by_id(post_id):
    """Return the post matching post_id, or None if not found."""
    for post in load_posts():
        if post['id'] == post_id:
            return post
    return None

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)