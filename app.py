from flask import Flask, render_template, request, redirect, url_for, session
from supabase import create_client
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

SUPABASE_URL = "https://ocgkkizcykkwsdzxjrzc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9jZ2traXpjeWtrd3NkenhqcnpjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDk2Nzc2MTcsImV4cCI6MjAyNTI1MzYxN30.t0Nq2cc8ty3A727BtdC_jluOj_znVMM5AgN7VxVvQ70"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = supabase.auth.sign_up({"email": email, "password": password})
        return redirect(url_for('login_page'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return redirect(url_for('index_page',email=email))
    return render_template('login.html')


@app.route('/index/<email>', methods=['GET', 'POST'])
def index_page(email):
    return render_template('index.html',email=email)

@app.route('/rooms', methods=['GET', 'POST'])
def rooms_page():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    print('Received message:', message)
    socketio.emit('message', message)


if __name__ == '__main__':
    app.run(debug=True)

