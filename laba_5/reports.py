import csv
from io import StringIO

from flask import Blueprint, Response, render_template, request
from flask_login import current_user

from app import check_rights, get_db, is_admin, query_all, query_one


reports_bp = Blueprint('reports', __name__, url_prefix='/visits')
PER_PAGE = 10


def user_display_name(row):
    if row['user_id'] is None:
        return 'Неаутентифицированный пользователь'

    parts = [row['last_name'], row['first_name'], row['middle_name']]
    return ' '.join(part for part in parts if part) or row['login']


def visit_filter():
    if is_admin():
        return '', ()
    return 'WHERE visit_logs.user_id = ?', (current_user.id,)


@reports_bp.route('/')
@check_rights('visit_logs')
def index():
    page = request.args.get('page', 1, type=int)
    page = max(page, 1)
    where_sql, params = visit_filter()
    total = query_one(f'SELECT COUNT(*) AS count FROM visit_logs {where_sql}', params)['count']
    pages = max((total + PER_PAGE - 1) // PER_PAGE, 1)
    page = min(page, pages)
    offset = (page - 1) * PER_PAGE

    logs = query_all(
        f'''
        SELECT
            visit_logs.*,
            users.login,
            users.last_name,
            users.first_name,
            users.middle_name,
            strftime('%d.%m.%Y %H:%M:%S', visit_logs.created_at) AS formatted_created_at
        FROM visit_logs
        LEFT JOIN users ON visit_logs.user_id = users.id
        {where_sql}
        ORDER BY visit_logs.created_at DESC, visit_logs.id DESC
        LIMIT ? OFFSET ?
        ''',
        (*params, PER_PAGE, offset),
    )

    return render_template(
        'visits/index.html',
        logs=logs,
        page=page,
        pages=pages,
        per_page=PER_PAGE,
        total=total,
        user_display_name=user_display_name,
    )


@reports_bp.route('/pages')
@check_rights('visit_reports')
def pages_report():
    rows = pages_report_rows()
    return render_template('visits/pages_report.html', rows=rows)


@reports_bp.route('/pages.csv')
@check_rights('visit_reports')
def pages_report_csv():
    rows = pages_report_rows()
    return csv_response(
        'pages_report.csv',
        ['№', 'Страница', 'Количество посещений'],
        [(index, row['path'], row['visits_count']) for index, row in enumerate(rows, start=1)],
    )


@reports_bp.route('/users')
@check_rights('visit_reports')
def users_report():
    rows = users_report_rows()
    return render_template('visits/users_report.html', rows=rows, user_display_name=user_display_name)


@reports_bp.route('/users.csv')
@check_rights('visit_reports')
def users_report_csv():
    rows = users_report_rows()
    return csv_response(
        'users_report.csv',
        ['№', 'Пользователь', 'Количество посещений'],
        [(index, user_display_name(row), row['visits_count']) for index, row in enumerate(rows, start=1)],
    )


def pages_report_rows():
    return query_all(
        '''
        SELECT path, COUNT(*) AS visits_count
        FROM visit_logs
        GROUP BY path
        ORDER BY visits_count DESC, path
        '''
    )


def users_report_rows():
    return query_all(
        '''
        SELECT
            visit_logs.user_id,
            users.login,
            users.last_name,
            users.first_name,
            users.middle_name,
            COUNT(*) AS visits_count
        FROM visit_logs
        LEFT JOIN users ON visit_logs.user_id = users.id
        GROUP BY visit_logs.user_id, users.login, users.last_name, users.first_name, users.middle_name
        ORDER BY visits_count DESC, users.last_name, users.first_name
        '''
    )


def csv_response(filename, headers, rows):
    output = StringIO()
    output.write('\ufeff')
    writer = csv.writer(output)
    writer.writerow(headers)
    writer.writerows(rows)

    return Response(
        output.getvalue(),
        mimetype='text/csv; charset=utf-8',
        headers={'Content-Disposition': f'attachment; filename={filename}'},
    )
