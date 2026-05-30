import math
import os
import random
import re
import pytest

from fact import fact_it, fact_rec
from show_employee import show_employee
from sum_and_sub import sum_and_sub
from process_list import process_list, process_list_gen
from my_sum import my_sum
from my_sum_argv import parse_numbers, sum_from_argv, format_sum
from files_sort import sort_files_by_extension
from file_search import find_file, first_lines
from email_validation import fun as email_fun, filter_mail
from fibonacci import fibonacci, cube
from average_scores import compute_average_scores
from plane_angle import Point, plane_angle
from phone_number import normalize_digits, format_ru_phone, sort_phone
from people_sort import name_format
from complex_numbers import Complex
from circle_square_mk import circle_square_mk
from log_decorator import function_logger


# -------------------- Task 1: factorial --------------------

@pytest.mark.parametrize("n, expected", [
    (1, 1),
    (2, 2),
    (3, 6),
    (4, 24),
    (5, 120),
    (6, 720),
    (7, 5040),
    (10, 3628800),
    (12, 479001600),
    (20, 2432902008176640000),
])
def test_fact_small_values(n, expected):
    assert fact_it(n) == expected
    assert fact_rec(n) == expected

@pytest.mark.parametrize("n", [1, 2, 3, 5, 10, 25, 50, 100, 150, 200])
def test_fact_compare_to_math_factorial(n):
    assert fact_it(n) == math.factorial(n)
    assert fact_rec(n) == math.factorial(n)

def test_fact_errors():
    with pytest.raises(ValueError):
        fact_it(0)
    with pytest.raises(ValueError):
        fact_rec(-1)
    with pytest.raises(TypeError):
        fact_it(1.5)
    with pytest.raises(TypeError):
        fact_rec("10")

def test_fact_large_digits_consistency():
    # Проверяем согласованность (не сравниваем целиком с math.factorial по смыслу, но можно)
    n = 500
    assert fact_it(n) == fact_rec(n)
    # число цифр factorial(500) известное свойство
    assert len(str(fact_it(n))) == len(str(math.factorial(n)))


# -------------------- Task 2: show_employee --------------------

@pytest.mark.parametrize("name, salary, expected", [
    ("Иванов Иван Иванович", 30000, "Иванов Иван Иванович: 30000 ₽"),
    ("John Doe", 0, "John Doe: 0 ₽"),
    ("A", 1, "A: 1 ₽"),
])
def test_show_employee_with_salary(name, salary, expected):
    assert show_employee(name, salary) == expected

def test_show_employee_default_salary():
    assert show_employee("Иванов Иван") == "Иванов Иван: 100000 ₽"

def test_show_employee_salary_none_defaults():
    assert show_employee("Иванов Иван", None) == "Иванов Иван: 100000 ₽"


# -------------------- Task 3: sum_and_sub --------------------

@pytest.mark.parametrize("a,b", [
    (1.0, 2.0),
    (-1.5, 3.2),
    (0.0, 0.0),
    (1e9, -1e9),
    (math.pi, math.e),
])
def test_sum_and_sub(a, b):
    s, d = sum_and_sub(a, b)
    assert s == pytest.approx(a + b)
    assert d == pytest.approx(a - b)

def test_sum_and_sub_types():
    s, d = sum_and_sub(1, 2)
    assert isinstance(s, (int, float))
    assert isinstance(d, (int, float))


# -------------------- Task 4: process_list --------------------

@pytest.mark.parametrize("arr, expected", [
    ([1], [1]),
    ([2], [4]),
    ([1,2,3], [1,4,27]),
    ([0, -1, -2], [0, -1, 4]),
    ([10, 11], [100, 1331]),
])
def test_process_list(arr, expected):
    assert process_list(arr) == expected

@pytest.mark.parametrize("arr", [
    [1,2,3,4,5],
    [0,0,0],
    [-3, -2, -1, 0, 1, 2, 3],
    list(range(20)),
])
def test_process_list_gen_matches_list(arr):
    assert list(process_list_gen(arr)) == process_list(arr)

def test_process_list_empty():
    assert process_list([]) == []
    assert list(process_list_gen([])) == []


# -------------------- Task 5: my_sum --------------------

def test_my_sum_no_args():
    assert my_sum() == 0.0

@pytest.mark.parametrize("args, expected", [
    ((1,2,3), 6.0),
    ((1.5, 2.5), 4.0),
    ((-1, -2, -3), -6.0),
    ((0.1, 0.2, 0.3), 0.6),
    ((1e10, -1e10, 5), 5.0),
])
def test_my_sum(args, expected):
    assert my_sum(*args) == pytest.approx(expected)


# -------------------- Task 6: argv sum --------------------

@pytest.mark.parametrize("argv, expected", [
    (["1","2","3","4","5"], 15.0),
    (["1.5","2.5"], 4.0),
    (["-1","2"], 1.0),
    (["0"], 0.0),
])
def test_sum_from_argv(argv, expected):
    assert sum_from_argv(argv) == pytest.approx(expected)

@pytest.mark.parametrize("argv, expected", [
    (["1","2","3"], [1.0,2.0,3.0]),
    (["1.25"], [1.25]),
    (["-0.5","0.5"], [-0.5,0.5]),
])
def test_parse_numbers(argv, expected):
    assert parse_numbers(argv) == expected

@pytest.mark.parametrize("value, expected", [
    (15.0, "15"),
    (15.5, "15.5"),
    (0.0, "0"),
    (-2.0, "-2"),
])
def test_format_sum(value, expected):
    assert format_sum(value) == expected


# -------------------- Task 7: files sort --------------------

def test_sort_files_by_extension_basic(tmp_path):
    # create files and directories
    (tmp_path/"a.py").write_text("x")
    (tmp_path/"b.py").write_text("x")
    (tmp_path/"c.py").write_text("x")
    (tmp_path/"a.txt").write_text("x")
    (tmp_path/"b.txt").write_text("x")
    (tmp_path/"c.txt").write_text("x")
    (tmp_path/"subdir").mkdir()
    (tmp_path/"subdir"/"z.py").write_text("x")

    res = sort_files_by_extension(str(tmp_path))
    assert res == ["a.py","b.py","c.py","a.txt","b.txt","c.txt"]

def test_sort_files_by_extension_multiple_ext(tmp_path):
    for name in ["b.md","a.md","c.txt","a.py","b.py","a", "z.tar.gz", "k.gz"]:
        (tmp_path/name).write_text("x")
    (tmp_path/"dir").mkdir()
    (tmp_path/"dir"/"inside.txt").write_text("x")
    res = sort_files_by_extension(str(tmp_path))
    # ext ordering: '' then '.gz' then '.md' then '.py' then '.txt'
    assert res == ["a", "k.gz", "z.tar.gz", "a.md", "b.md", "a.py", "b.py", "c.txt"]

def test_sort_files_by_extension_empty_dir(tmp_path):
    assert sort_files_by_extension(str(tmp_path)) == []


# -------------------- Task 8: file search --------------------

def test_find_file_found_and_first_lines(tmp_path):
    # structure
    (tmp_path/"a").mkdir()
    target = tmp_path/"a"/"target.txt"
    target.write_text("1\n2\n3\n4\n5\n6\n", encoding="utf-8")
    found = find_file(str(tmp_path), "target.txt")
    assert found is not None
    assert os.path.basename(found) == "target.txt"
    assert first_lines(found, 5) == ["1","2","3","4","5"]

def test_find_file_not_found(tmp_path):
    (tmp_path/"x.txt").write_text("hi")
    assert find_file(str(tmp_path), "missing.txt") is None

def test_first_lines_short_file(tmp_path):
    p = tmp_path/"s.txt"
    p.write_text("only\none\n", encoding="utf-8")
    assert first_lines(str(p), 5) == ["only", "one"]


# -------------------- Task 9: email validation --------------------

@pytest.mark.parametrize("email", [
    "lara@mospolytech.ru",
    "brian-23@mospolytech.ru",
    "britts_54@mospolytech.ru",
    "a@b.ccc",
    "A_Z-9@SITE123.com",
])
def test_email_valid(email):
    assert email_fun(email) is True

@pytest.mark.parametrize("email", [
    "noatsign.com",
    "a@b",
    "a@b.cdef",          # ext too long
    "a@b.12",            # ext must be letters
    "a!@b.cc",           # invalid char in username
    "a@b-1.cc",          # invalid char in website
    "a@b_.cc",           # invalid char in website
    "a@b.c_c",           # invalid char in extension
    "a@.cc",             # empty website
    "@b.cc",             # empty username
])
def test_email_invalid(email):
    assert email_fun(email) is False

def test_filter_mail_sorts_and_filters():
    emails = [
        "lara@mospolytech.ru",
        "bad@@mospolytech.ru",
        "brian-23@mospolytech.ru",
        "britts_54@mospolytech.ru",
        "a@b.cdef",
    ]
    filtered = filter_mail(emails)
    assert sorted(filtered) == ["brian-23@mospolytech.ru", "britts_54@mospolytech.ru", "lara@mospolytech.ru"]


# -------------------- Task 10: fibonacci --------------------

@pytest.mark.parametrize("n, expected", [
    (1, [0]),
    (2, [0,1]),
    (3, [0,1,1]),
    (5, [0,1,1,2,3]),
    (10, [0,1,1,2,3,5,8,13,21,34]),
])
def test_fibonacci(n, expected):
    assert fibonacci(n) == expected

def test_fibonacci_errors():
    with pytest.raises(ValueError):
        fibonacci(0)
    with pytest.raises(TypeError):
        fibonacci(1.2)

@pytest.mark.parametrize("x, expected", [
    (0, 0),
    (1, 1),
    (2, 8),
    (-2, -8),
])
def test_cube_lambda(x, expected):
    assert cube(x) == expected

def test_fibonacci_cubes_example():
    assert list(map(cube, fibonacci(5))) == [0, 1, 1, 8, 27]


# -------------------- Task 11: average scores --------------------

def test_compute_average_scores_example():
    scores = [
        (89, 90, 78, 93, 80),
        (90, 91, 85, 88, 86),
        (91, 92, 83, 89, 90.5),
    ]
    res = compute_average_scores(scores)
    assert res == pytest.approx((90.0, 91.0, 82.0, 90.0, 85.5))

@pytest.mark.parametrize("scores, expected", [
    ([(100,)], (100.0,)),
    ([(0, 100), (100, 0)], (50.0, 50.0)),
    ([(10,20,30), (40,50,60), (70,80,90)], (40.0, 50.0, 60.0)),
])
def test_compute_average_scores_various(scores, expected):
    assert compute_average_scores(scores) == pytest.approx(expected)

def test_compute_average_scores_empty():
    assert compute_average_scores([]) == tuple()


# -------------------- Task 12: plane angle --------------------

def test_plane_angle_90_degrees():
    A = Point(0,0,0)
    B = Point(1,0,0)
    C = Point(1,1,0)
    D = Point(1,1,1)
    assert plane_angle(A,B,C,D) == pytest.approx(90.0)

def test_plane_angle_0_degrees_same_plane():
    A = Point(0,0,0)
    B = Point(1,0,0)
    C = Point(0,1,0)
    D = Point(1,1,0)
    assert plane_angle(A,B,C,D) == pytest.approx(0.0)

def test_plane_angle_acute():
    # ABC: z=0 plane; BCD: plane tilted 45 degrees around BC axis
    A = Point(0,0,0)
    B = Point(1,0,0)
    C = Point(0,1,0)
    D = Point(0,1,1)  # makes second plane vertical-ish
    ang = plane_angle(A,B,C,D)
    assert 0.0 < ang < 180.0

def test_plane_angle_degenerate_raises():
    # A,B,C collinear -> normal is zero
    A = Point(0,0,0)
    B = Point(1,1,1)
    C = Point(2,2,2)
    D = Point(0,1,0)
    with pytest.raises(ValueError):
        plane_angle(A,B,C,D)


# -------------------- Task 13: phone number --------------------

@pytest.mark.parametrize("raw, digits10", [
    ("07895462130", "7895462130"),
    ("89875641230", "9875641230"),
    ("9195969878",  "9195969878"),
    ("+7 919 596 98 78", "9195969878"),
    ("8(999)111-22-33", "9991112233"),
])
def test_normalize_digits(raw, digits10):
    assert normalize_digits(raw) == digits10

@pytest.mark.parametrize("digits10, formatted", [
    ("7895462130", "+7 (789) 546-21-30"),
    ("9195969878", "+7 (919) 596-98-78"),
    ("9875641230", "+7 (987) 564-12-30"),
])
def test_format_ru_phone(digits10, formatted):
    assert format_ru_phone(digits10) == formatted

def test_sort_phone_formats_and_sorts():
    nums = ["07895462130", "89875641230", "9195969878"]
    assert sort_phone(nums) == [
        "+7 (789) 546-21-30",
        "+7 (919) 596-98-78",
        "+7 (987) 564-12-30",
    ]

def test_phone_errors():
    with pytest.raises(ValueError):
        normalize_digits("12345")
    with pytest.raises(ValueError):
        format_ru_phone("123")


# -------------------- Task 14: people sort --------------------

def test_people_sort_example():
    people = [
        ["Mike", "Thomson", "20", "M"],
        ["Robert", "Bustle", "32", "M"],
        ["Andria", "Bustle", "30", "F"],
    ]
    assert name_format(people) == [
        "Mr. Mike Thomson",
        "Ms. Andria Bustle",
        "Mr. Robert Bustle",
    ]

def test_people_sort_stable_on_ties():
    people = [
        ["A", "X", "10", "M"],
        ["B", "Y", "10", "F"],
        ["C", "Z", "9", "M"],
        ["D", "W", "10", "M"],
    ]
    # C first (age 9), then the age-10 in input order
    assert name_format(people) == [
        "Mr. C Z",
        "Mr. A X",
        "Ms. B Y",
        "Mr. D W",
    ]


# -------------------- Task 15: complex numbers --------------------

def test_complex_str_formatting():
    assert str(Complex(2, 1)) == "2.00+1.00i"
    assert str(Complex(-3, -5)) == "-3.00-5.00i"
    assert str(Complex(0, 2)) == "0.00+2.00i"
    assert str(Complex(2, 0)) == "2.00+0.00i"

def test_complex_add_sub_mul_div_and_mod_example():
    C = Complex(2, 1)
    D = Complex(5, 6)
    assert str(C + D) == "7.00+7.00i"
    assert str(C - D) == "-3.00-5.00i"
    assert str(C * D) == "4.00+17.00i"
    # division approx
    div = C / D
    assert div.real == pytest.approx(0.2622950819)
    assert div.imaginary == pytest.approx(-0.1147540983)
    assert str(C.mod()) == "2.24+0.00i"
    assert str(D.mod()) == "7.81+0.00i"

@pytest.mark.parametrize("a,b,c,d", [
    (1,2,3,4),
    (-1,0,0,2),
    (0,-3,4,0),
    (2.5, -1.5, -3.0, 0.5),
])
def test_complex_operations_consistency(a,b,c,d):
    C = Complex(a,b)
    D = Complex(c,d)
    # addition and subtraction inverse
    E = C + D
    F = E - D
    assert F.real == pytest.approx(C.real)
    assert F.imaginary == pytest.approx(C.imaginary)
    # multiplication by 1+0i
    one = Complex(1,0)
    P = C * one
    assert P.real == pytest.approx(C.real)
    assert P.imaginary == pytest.approx(C.imaginary)

def test_complex_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        Complex(1,1) / Complex(0,0)


# -------------------- Task 16: Monte-Carlo circle area --------------------

def test_circle_square_mk_zero_radius():
    assert circle_square_mk(0, 100, rng=random.Random(0)) == 0.0

def test_circle_square_mk_invalid():
    with pytest.raises(ValueError):
        circle_square_mk(1, 0)
    with pytest.raises(ValueError):
        circle_square_mk(-1, 10)

@pytest.mark.parametrize("n", [1000, 5000, 20000])
def test_circle_square_mk_accuracy_improves_with_n(n):
    rng = random.Random(0)
    r = 1.0
    est = circle_square_mk(r, n, rng=rng)
    true = math.pi * r * r
    # довольно мягкая граница; для n больше, ошибка обычно меньше
    assert abs(est - true) < 0.5

def test_circle_square_mk_deterministic_with_rng():
    r = 2.0
    n = 1000
    est1 = circle_square_mk(r, n, rng=random.Random(123))
    est2 = circle_square_mk(r, n, rng=random.Random(123))
    assert est1 == est2


# -------------------- Task 17: log decorator (optional) --------------------

def test_function_logger_writes_log(tmp_path):
    log_path = tmp_path / "test.log"

    @function_logger(str(log_path))
    def greet(name):
        return f"Hello, {name}!"

    out = greet("John")
    assert out == "Hello, John!"
    text = log_path.read_text(encoding="utf-8")
    assert "greet" in text
    assert "Hello, John!" in text

def test_function_logger_logs_dash_for_none(tmp_path):
    log_path = tmp_path / "none.log"

    @function_logger(str(log_path))
    def do_nothing(x):
        # returns None
        _ = x

    do_nothing(10)
    text = log_path.read_text(encoding="utf-8")
    assert "do_nothing" in text
    # отдельной строкой должна быть '-'
    assert "\n-\n" in text

def test_function_logger_appends(tmp_path):
    log_path = tmp_path / "append.log"

    @function_logger(str(log_path))
    def add(a, b):
        return a + b

    add(1, 2)
    add(3, 4)
    lines = log_path.read_text(encoding="utf-8").splitlines()
    # Каждое выполнение пишет 7 строк
    assert len(lines) == 14
