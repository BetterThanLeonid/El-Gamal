from flask import Flask, request, render_template, session, url_for, redirect
import db_worker
from random import randint
from flask_mail import Mail, Message

db_worker.create_db()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'RSAC_20_GARIPOV_WEBAUTH_LAB2_VAR2'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'itmo.lab2.garipov@gmail.com'  # введите свой адрес электронной почты здесь
app.config['MAIL_DEFAULT_SENDER'] = 'itmo.lab2.garipov@gmail.com'  # и здесь
app.config['MAIL_PASSWORD'] = 'ItMoLaB2G@RiP0V'  # введите пароль
mail = Mail(app)
@app.route('/register/', methods=['post', 'get'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        db_worker.create_user(username, password, email)
    return render_template('register.html')
@app.route('/database/')
def show_db():
    users = db_worker.get_users_data()
    return render_template('database.html', user_list=users)    
@app.route('/auth_success')
def auth_success():
    if session.get('data')['auth'] == 'True':
        username = session['data']['username']
        return render_template('auth_success.html', username=username)
    else:
        return redirect(url_for('index'))
@app.route('/check_temp_code/', methods=['post', 'get'])
def check_temp_code():
    if session.get('data')['auth'] == 'Process':
        username = session['data']['username']
        db_temp_code = str(db_worker.get_temp_code(username)[0][0])
        text_message = 'Ваш временный код для входа: {}'.format(db_temp_code)
        if request.method == 'POST':
            entered_temp_code = request.form.get('temp_code')
            if entered_temp_code == db_temp_code:
                session['data'] = dict(username=username, auth='True')
                return redirect(url_for('auth_success'))
            else:
                return render_template('check_temp_code.html', auth_code = False, message=text_message)
        else:
            return render_template('check_temp_code.html', auth_form=False)
    else:
        return redirect(url_for('index'))

def send_mail(email, temp_code):
    msg = Message("Temporary Code Flask", recipients=[email])
    msg.body = "Your temporary code is {}".format(temp_code)
    mail.send(msg)

@app.route('/', methods=['post', 'get'])
def index():
    session['data'] = dict(auth = 'False')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password') 
        user = db_worker.check_user(username)
        if user:
            if password == user[2]:
                email = user[4]
                temp_code = randint(1000, 9999)
                send_mail(email, temp_code)
                db_worker.set_temp_code(username, temp_code)
                session['data'] = dict(username=username, auth = 'Process')
                return redirect(url_for('check_temp_code'))
            else: return render_template('index.html', auth_password=False)
        else: return render_template('index.html', auth_login=False)
    else: return render_template('index.html', auth_form=False)

if __name__ == "__main__":
    app.run(use_reloader=False, debug=False)
# use_reloader нужен, чтобы избавиться от ошибки с дебаг модом
# подробнее https://stackoverflow.com/questions/51988655/modulenotfounderror-when-running-imported-flask-app