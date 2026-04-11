import re

from flask import Flask, make_response, render_template, request

app = Flask(__name__)

ALLOWED_PHONE_RE = re.compile(r'^[\d\s().+-]*$')


def validate_phone(raw_phone):
    phone = raw_phone.strip()

    if not ALLOWED_PHONE_RE.fullmatch(phone):
        return (
            'Недопустимый ввод. В номере телефона встречаются недопустимые символы.',
            None
        )

    digits = re.sub(r'\D', '', phone)

    if phone.startswith('+7') or phone.startswith('8'):
        expected_len = 11
    else:
        expected_len = 10

    if len(digits) != expected_len:
        return 'Недопустимый ввод. Неверное количество цифр.', None

    if len(digits) == 11:
        local_digits = digits[1:]
    else:
        local_digits = digits

    normalized = (
        '8-' +
        local_digits[0:3] + '-' +
        local_digits[3:6] + '-' +
        local_digits[6:8] + '-' +
        local_digits[8:10]
    )

    return None, normalized


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/url-params')
def url_params():
    return render_template('url_params.html', params=request.args)


@app.route('/headers')
def headers_page():
    return render_template('headers.html')


@app.route('/cookies')
def cookies_page():
    resp = make_response(render_template('cookies.html', cookies=request.cookies))
    if 'demo_cookie' not in request.cookies:
        resp.set_cookie('demo_cookie', 'flask-demo-value', max_age=60 * 60 * 24)
    return resp


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_data = None

    if request.method == 'POST':
        form_data = {
            'username': request.form.get('username', ''),
            'password': request.form.get('password', '')
        }

    return render_template('login.html', form_data=form_data)


@app.route('/phone', methods=['GET', 'POST'])
def phone():
    phone_value = ''
    error = None
    normalized_phone = None

    if request.method == 'POST':
        phone_value = request.form.get('phone', '')
        error, normalized_phone = validate_phone(phone_value)

    return render_template(
        'phone.html',
        phone_value=phone_value,
        error=error,
        normalized_phone=normalized_phone
    )


if __name__ == '__main__':
    app.run(debug=True)