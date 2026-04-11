from flask import Flask, render_template, redirect, request, session, url_for, flash
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user

app = Flask(__name__)
app.secret_key = 'secret-key'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа к этой странице войдите в систему.'
login_manager.login_message_category = 'warning'


class User(UserMixin):
    def __init__(self, id, login, password):
        self.id = id
        self.login = login
        self.password = password


user = User('1', 'user', 'qwerty')


@login_manager.user_loader
def load_user(user_id):
    if user_id == user.id:
        return user
    return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/visits')
def visits():
    session['count'] = session.get('count', 0) + 1
    return render_template('visits.html', count=session['count'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_value = request.form['login']
        password = request.form['password']
        remember = 'remember' in request.form

        if login_value == user.login and password == user.password:
            login_user(user, remember=remember)
            flash('Вы успешно вошли в систему.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Неверный логин или пароль.', 'danger')

    return render_template('login.html')


@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)