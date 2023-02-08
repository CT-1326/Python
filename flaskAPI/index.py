from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/users')
def get_users():
    return 'users'


@app.route('/users/<username>')
def get_user_info(username):
    return f"username: {username}"


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id


if __name__ == '__main__':
    app.run()
