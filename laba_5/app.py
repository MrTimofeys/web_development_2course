from functools import wraps
from datetime import datetime
import re
import sqlite3
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

from flask import Flask, flash, g, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash


BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / 'instance' / 'laba_5.sqlite'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
app.config['TIMEZONE'] = ZoneInfo('Europe/Moscow')
sys.modules.setdefault('app', sys.modules[__name__])

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа к этой странице войдите в систему.'
login_manager.login_message_category = 'warning'


class User(UserMixin):
    def __init__(self, row):
        self.id = str(row['id'])
        self.login = row['login']
        self.password_hash = row['password_hash']
        self.last_name = row['last_name']
        self.first_name = row['first_name']
        self.middle_name = row['middle_name']
        self.role_id = row['role_id']
        self.created_at = row['created_at']
        self.role_name = row['role_name'] if 'role_name' in row.keys() else None


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def query_one(sql, params=()):
    return get_db().execute(sql, params).fetchone()


def query_all(sql, params=()):
    return get_db().execute(sql, params).fetchall()


def local_now():
    return datetime.now(app.config['TIMEZONE']).isoformat(timespec='seconds')


def init_db():
    DATABASE.parent.mkdir(exist_ok=True)
    db = get_db()
    db.executescript(
        '''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        );

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            last_name TEXT,
            first_name TEXT NOT NULL,
            middle_name TEXT,
            role_id INTEGER REFERENCES roles(id) ON DELETE SET NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS visit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path VARCHAR(100) NOT NULL,
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        '''
    )

    if query_one('SELECT id FROM roles LIMIT 1') is None:
        db.executemany(
            'INSERT INTO roles (name, description) VALUES (?, ?)',
            [
                ('Администратор', 'Полный доступ к управлению пользователями'),
                ('Пользователь', 'Обычная учетная запись пользователя'),
            ],
        )

    if query_one('SELECT id FROM users LIMIT 1') is None:
        admin_role = query_one('SELECT id FROM roles WHERE name = ?', ('Администратор',))
        user_role = query_one('SELECT id FROM roles WHERE name = ?', ('Пользователь',))
        db.execute(
            '''
            INSERT INTO users (login, password_hash, last_name, first_name, middle_name, role_id)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (
                'admin',
                generate_password_hash('Admin123'),
                'Иванов',
                'Админ',
                'Петрович',
                admin_role['id'] if admin_role else None,
            ),
        )
        db.execute(
            '''
            INSERT INTO users (login, password_hash, last_name, first_name, middle_name, role_id)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (
                'student',
                generate_password_hash('Student123'),
                'Петров',
                'Студент',
                'Иванович',
                user_role['id'] if user_role else None,
            ),
        )

    db.commit()


@app.before_request
def ensure_db():
    init_db()


@app.before_request
def write_visit_log():
    if request.endpoint == 'static':
        return

    get_db().execute(
        'INSERT INTO visit_logs (path, user_id, created_at) VALUES (?, ?, ?)',
        (
            request.path[:100],
            int(current_user.id) if current_user.is_authenticated else None,
            local_now(),
        ),
    )
    get_db().commit()


@login_manager.user_loader
def load_user(user_id):
    row = query_one(
        '''
        SELECT users.*, roles.name AS role_name
        FROM users
        LEFT JOIN roles ON users.role_id = roles.id
        WHERE users.id = ?
        ''',
        (user_id,),
    )
    return User(row) if row else None


def full_name(user):
    if hasattr(user, 'login'):
        parts = [user.last_name, user.first_name, user.middle_name]
        return ' '.join(part for part in parts if part) or user.login

    parts = [user['last_name'], user['first_name'], user['middle_name']]
    return ' '.join(part for part in parts if part) or user['login']


def is_admin():
    return current_user.is_authenticated and current_user.role_name == 'Администратор'


def is_regular_user():
    return current_user.is_authenticated and current_user.role_name == 'Пользователь'


def can_create_user():
    return is_admin()


def can_view_user(user_id):
    return is_admin() or (is_regular_user() and int(current_user.id) == int(user_id))


def can_edit_user(user_id):
    return is_admin() or (is_regular_user() and int(current_user.id) == int(user_id))


def can_delete_user():
    return is_admin()


def can_view_visit_logs():
    return is_admin() or is_regular_user()


def can_view_visit_reports():
    return is_admin()


def check_rights(action):
    def decorator(view):
        @wraps(view)
        @login_required
        def wrapper(*args, **kwargs):
            allowed = False

            if action == 'create_user':
                allowed = can_create_user()
            elif action == 'view_user':
                allowed = can_view_user(kwargs.get('user_id'))
            elif action == 'edit_user':
                allowed = can_edit_user(kwargs.get('user_id'))
            elif action == 'delete_user':
                allowed = can_delete_user()
            elif action == 'visit_logs':
                allowed = can_view_visit_logs()
            elif action == 'visit_reports':
                allowed = can_view_visit_reports()

            if not allowed:
                flash('У вас недостаточно прав для доступа к данной странице.', 'danger')
                return redirect(url_for('index'))

            return view(*args, **kwargs)

        return wrapper

    return decorator


@app.context_processor
def inject_helpers():
    return {
        'full_name': full_name,
        'can_create_user': can_create_user,
        'can_view_user': can_view_user,
        'can_edit_user': can_edit_user,
        'can_delete_user': can_delete_user,
        'can_view_visit_logs': can_view_visit_logs,
        'can_view_visit_reports': can_view_visit_reports,
        'is_admin': is_admin,
    }


def roles():
    return query_all('SELECT * FROM roles ORDER BY name')


def form_data(row=None, keep_role=False):
    if request.method == 'POST':
        role_id = str(row['role_id']) if keep_role and row and row['role_id'] is not None else request.form.get('role_id', '')
        return {
            'login': request.form.get('login', '').strip(),
            'last_name': request.form.get('last_name', '').strip(),
            'first_name': request.form.get('first_name', '').strip(),
            'middle_name': request.form.get('middle_name', '').strip(),
            'role_id': role_id,
        }

    return {
        'login': row['login'] if row and 'login' in row.keys() else '',
        'last_name': row['last_name'] if row else '',
        'first_name': row['first_name'] if row else '',
        'middle_name': row['middle_name'] if row else '',
        'role_id': str(row['role_id']) if row and row['role_id'] is not None else '',
    }


def validate_login(login):
    errors = []
    if not login:
        errors.append('Поле не может быть пустым.')
    elif not re.fullmatch(r'[A-Za-z0-9]{5,}', login):
        errors.append('Логин должен состоять только из латинских букв и цифр и иметь длину не менее 5 символов.')
    return errors


def validate_password(password):
    errors = []
    allowed = r'A-Za-zА-Яа-яЁё0-9~!\?@#\$%\^&\*_\-\+\(\)\[\]\{\}><\/\\\|"\'\.,:;'

    if not password:
        errors.append('Поле не может быть пустым.')
    if len(password) < 8:
        errors.append('Пароль должен содержать не менее 8 символов.')
    if len(password) > 128:
        errors.append('Пароль должен содержать не более 128 символов.')
    if not re.search(r'[A-ZА-ЯЁ]', password):
        errors.append('Пароль должен содержать как минимум одну заглавную букву.')
    if not re.search(r'[a-zа-яё]', password):
        errors.append('Пароль должен содержать как минимум одну строчную букву.')
    if not re.search(r'\d', password):
        errors.append('Пароль должен содержать как минимум одну арабскую цифру.')
    if re.search(r'\s', password):
        errors.append('Пароль не должен содержать пробелы.')
    if re.search(fr'[^{allowed}]', password):
        errors.append('Пароль содержит недопустимые символы.')

    return errors


def validate_user(data, is_create=True):
    errors = {}

    if is_create:
        login_errors = validate_login(data['login'])
        if login_errors:
            errors['login'] = login_errors

        password_errors = validate_password(request.form.get('password', ''))
        if password_errors:
            errors['password'] = password_errors

    if not data['last_name']:
        errors['last_name'] = ['Поле не может быть пустым.']
    if not data['first_name']:
        errors['first_name'] = ['Поле не может быть пустым.']

    if data['role_id'] and not query_one('SELECT id FROM roles WHERE id = ?', (data['role_id'],)):
        errors['role_id'] = ['Выбранная роль не найдена.']

    return errors


def flash_form_errors(errors):
    if errors:
        flash('Проверьте правильность заполнения формы.', 'danger')


@app.route('/')
def index():
    users = query_all(
        '''
        SELECT users.*, roles.name AS role_name
        FROM users
        LEFT JOIN roles ON users.role_id = roles.id
        ORDER BY users.id
        '''
    )
    return render_template('index.html', users=users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_value = request.form.get('login', '').strip()
        password = request.form.get('password', '')
        remember = 'remember' in request.form
        row = query_one('SELECT * FROM users WHERE login = ?', (login_value,))

        if row and check_password_hash(row['password_hash'], password):
            login_user(User(row), remember=remember)
            flash('Вы успешно вошли в систему.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))

        flash('Неверный логин или пароль.', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>')
@check_rights('view_user')
def show_user(user_id):
    user = query_one(
        '''
        SELECT users.*, roles.name AS role_name
        FROM users
        LEFT JOIN roles ON users.role_id = roles.id
        WHERE users.id = ?
        ''',
        (user_id,),
    )
    if user is None:
        flash('Пользователь не найден.', 'danger')
        return redirect(url_for('index'))
    return render_template('show_user.html', user=user)


@app.route('/users/new', methods=['GET', 'POST'])
@check_rights('create_user')
def create_user():
    data = form_data()
    errors = {}

    if request.method == 'POST':
        errors = validate_user(data, is_create=True)
        flash_form_errors(errors)

        if not errors:
            try:
                get_db().execute(
                    '''
                    INSERT INTO users (login, password_hash, last_name, first_name, middle_name, role_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''',
                    (
                        data['login'],
                        generate_password_hash(request.form.get('password', '')),
                        data['last_name'],
                        data['first_name'],
                        data['middle_name'] or None,
                        data['role_id'] or None,
                    ),
                )
                get_db().commit()
                flash('Пользователь успешно создан.', 'success')
                return redirect(url_for('index'))
            except sqlite3.IntegrityError:
                get_db().rollback()
                errors['login'] = ['Пользователь с таким логином уже существует.']
                flash_form_errors(errors)
            except sqlite3.Error:
                get_db().rollback()
                flash('При сохранении пользователя произошла ошибка.', 'danger')

    return render_template('user_form.html', title='Создание пользователя', data=data, errors=errors, roles=roles(), is_create=True)


@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@check_rights('edit_user')
def edit_user(user_id):
    user = query_one('SELECT * FROM users WHERE id = ?', (user_id,))
    if user is None:
        flash('Пользователь не найден.', 'danger')
        return redirect(url_for('index'))

    role_locked = not is_admin()
    data = form_data(user, keep_role=role_locked)
    errors = {}

    if request.method == 'POST':
        errors = validate_user(data, is_create=False)
        flash_form_errors(errors)

        if not errors:
            try:
                get_db().execute(
                    '''
                    UPDATE users
                    SET last_name = ?, first_name = ?, middle_name = ?, role_id = ?
                    WHERE id = ?
                    ''',
                    (
                        data['last_name'],
                        data['first_name'],
                        data['middle_name'] or None,
                        data['role_id'] or None,
                        user_id,
                    ),
                )
                get_db().commit()
                flash('Пользователь успешно обновлен.', 'success')
                return redirect(url_for('index'))
            except sqlite3.Error:
                get_db().rollback()
                flash('При сохранении пользователя произошла ошибка.', 'danger')

    return render_template(
        'user_form.html',
        title='Редактирование пользователя',
        data=data,
        errors=errors,
        roles=roles(),
        is_create=False,
        role_disabled=role_locked,
    )


@app.route('/users/<int:user_id>/delete', methods=['POST'])
@check_rights('delete_user')
def delete_user(user_id):
    user = query_one('SELECT * FROM users WHERE id = ?', (user_id,))
    if user is None:
        flash('Пользователь не найден.', 'danger')
        return redirect(url_for('index'))

    try:
        get_db().execute('DELETE FROM users WHERE id = ?', (user_id,))
        get_db().commit()
        flash('Пользователь успешно удален.', 'success')
    except sqlite3.Error:
        get_db().rollback()
        flash('При удалении пользователя произошла ошибка.', 'danger')

    return redirect(url_for('index'))


@app.route('/password', methods=['GET', 'POST'])
@login_required
def change_password():
    errors = {}

    if request.method == 'POST':
        old_password = request.form.get('old_password', '')
        new_password = request.form.get('new_password', '')
        repeat_password = request.form.get('repeat_password', '')
        user = query_one('SELECT * FROM users WHERE id = ?', (current_user.id,))

        if not check_password_hash(user['password_hash'], old_password):
            errors['old_password'] = ['Старый пароль указан неверно.']

        password_errors = validate_password(new_password)
        if password_errors:
            errors['new_password'] = password_errors

        if new_password != repeat_password:
            errors['repeat_password'] = ['Новые пароли не совпадают.']

        if errors:
            flash('Проверьте правильность заполнения формы.', 'danger')
        else:
            get_db().execute(
                'UPDATE users SET password_hash = ? WHERE id = ?',
                (generate_password_hash(new_password), current_user.id),
            )
            get_db().commit()
            flash('Пароль успешно изменен.', 'success')
            return redirect(url_for('index'))

    return render_template('change_password.html', errors=errors)


from reports import reports_bp

app.register_blueprint(reports_bp)


if __name__ == '__main__':
    app.run(debug=True)
