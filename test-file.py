import json

with open('blog_posts.json', 'r') as posts_file:
    blog_posts = json.load(posts_file)

for post in blog_posts:
    print(post['author'])