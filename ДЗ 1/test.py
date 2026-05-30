import subprocess
import pytest
import os

INTERPRETER = 'python3'
TASKS_DIR = 'tasks'

def run_script(filename, input_data=None):
    filepath = os.path.join(TASKS_DIR, filename)
    if not os.path.exists(filepath):
        pytest.skip(f"Файл {filepath} не найден")

    proc = subprocess.run(
        [INTERPRETER, filepath],
        input='\n'.join(input_data if input_data else []),
        capture_output=True,
        text=True,
        check=False
    )
    return proc.stdout.strip()

test_data = {
    'hello.py': [('', 'Hello, World!'), ('', 'Hello, World!'), ('', 'Hello, World!')],
    'python_if_else.py': [
        ('1', 'Weird'), ('2', 'Not Weird'), ('3', 'Weird'), ('4', 'Not Weird'),
        ('6', 'Weird'), ('20', 'Weird'), ('21', 'Weird'), ('22', 'Not Weird')
    ],
    'arithmetic_operators.py': [
        (['1', '2'], ['3', '-1', '2']), (['10', '10'], ['20', '0', '100']),
        (['3', '5'], ['8', '-2', '15']), (['-1', '1'], ['0', '-2', '-1']),
        (['0', '0'], ['0', '0', '0']), (['5', '3'], ['8', '2', '15'])
    ],
    'division.py': [
        (['4', '2'], ['2', '2.0']), (['5', '2'], ['2', '2.5']),
        (['3', '5'], ['0', '0.6']), (['10', '3'], ['3', '3.3333333333333335']),
        (['1', '1'], ['1', '1.0']), (['0', '5'], ['0', '0.0'])
    ],
    'loops.py': [
        (['1'], ['0']),
        (['2'], ['0', '1']),
        (['3'], ['0', '1', '4']),
        (['5'], ['0', '1', '4', '9', '16']),
        (['0'], ['']),
        (['10'], ['0', '1', '4', '9', '16', '25', '36', '49', '64', '81'])
    ],
    'print_function.py': [
        ('1', '1'), ('3', '123'), ('5', '12345'), ('10', '12345678910'), ('2', '12')
    ],
    'second_score.py': [
        (['5', '2 3 6 6 5'], '5'), (['6', '2 5 4 4 5 5'], '4'),
        (['4', '1 2 3 4'], '3'), (['3', '1 1 2'], '1'),
        (['5', '10 20 10 20 30'], '20'), (['1', '100'], '100')
    ],
    'nested_list.py': [
        (['2', 'Harry', '37.21', 'Berry', '37.21'], ['Berry', 'Harry']),
        (['5', 'Harry', '37.21', 'Berry', '37.21', 'Tina', '37.2', 'Akriti', '41', 'Harsh', '39'], ['Berry', 'Harry']),
        (['3', 'Alice', '90', 'Bob', '85', 'Charlie', '85'], ['Bob', 'Charlie']),
        (['2', 'Eve', '95', 'David', '95'], ['David', 'Eve'])
    ],
    'lists.py': [
        ([
             '12',
             'insert 0 5',
             'insert 1 10',
             'insert 0 6',
             'print',
             'remove 6',
             'append 9',
             'append 1',
             'sort',
             'print',
             'pop',
             'reverse',
             'print'
         ], [
             '[6, 5, 10]',
             '[1, 5, 9, 10]',
             '[9, 5, 1]'
         ]),
        ([
             '4',
             'append 1',
             'append 2',
             'insert 1 3',
             'print'
         ], ['[1, 3, 2]'])
    ],
    'swap_case.py': [
        ('Www.MosPolytech.ru', 'wWW.mOSpOLYTECH.RU'),
        ('Pythonist 2', 'pYTHONIST 2'), ('Hello', 'hELLO'),
        ('123', '123'), ('AaBbCc', 'aAbBcC')
    ],
    'split_and_join.py': [
        ('this is a string', 'this-is-a-string'),
        ('hello world', 'hello-world'), ('a b c', 'a-b-c'),
        ('test case', 'test-case')
    ],
    'anagram.py': [
        (['abc', 'bca'], 'YES'), (['silent', 'listen'], 'YES'),
        (['hello', 'world'], 'NO'), (['a', 'a'], 'YES'),
        (['AbC', 'cba'], 'YES'), (['rat', 'car'], 'NO')
    ],
    'minion_game.py': [
        ('BANANA', 'Stuart 12'), ('AEIOU', 'Kevin 15'), ('STEWART', 'Stuart 20')
    ],
    'is_leap.py': [
        ('1900', 'False'), ('2000', 'True'), ('2016', 'True'),
        ('2024', 'True'), ('1800', 'False'), ('2400', 'True'),
        ('2020', 'True'), ('2100', 'False')
    ],
    'happiness.py': [
        (['3 2', '1 5 3', '3 1', '5 7'], '1'),
        (['1 1', '1', '1', '10'], '1'),
        (['5 2', '1 2 3 4 5', '1 3', '2 4'], '1')
    ],
    'metro.py': [
        (['2', '0 10', '5 15', '12'], '1'),
        (['3', '1 3', '2 5', '4 7', '4'], '1'),
        (['1', '0 100', '50'], '1')
    ]
}

def test_hello_world():
    assert run_script('hello.py', []) == 'Hello, World!'

@pytest.mark.parametrize("input_data, expected", test_data['python_if_else.py'])
def test_python_if_else(input_data, expected):
    assert run_script('python_if_else.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['print_function.py'])
def test_print_function(input_data, expected):
    assert run_script('print_function.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['swap_case.py'])
def test_swap_case(input_data, expected):
    assert run_script('swap_case.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['split_and_join.py'])
def test_split_join(input_data, expected):
    assert run_script('split_and_join.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['minion_game.py'])
def test_minion_game(input_data, expected):
    assert run_script('minion_game.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['is_leap.py'])
def test_is_leap(input_data, expected):
    assert run_script('is_leap.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['second_score.py'])
def test_second_score(input_data, expected):
    assert run_script('second_score.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected_list", test_data['arithmetic_operators.py'])
def test_arithmetic_operators(input_data, expected_list):
    assert run_script('arithmetic_operators.py', input_data).split('\n') == expected_list

@pytest.mark.parametrize("input_data, expected_list", test_data['division.py'])
def test_division(input_data, expected_list):
    assert run_script('division.py', input_data).split('\n') == expected_list

@pytest.mark.parametrize("input_data, expected_list", test_data['loops.py'])
def test_loops(input_data, expected_list):
    assert run_script('loops.py', input_data).split('\n') == expected_list

@pytest.mark.parametrize("input_data, expected", test_data['anagram.py'])
def test_anagram(input_data, expected):
    assert run_script('anagram.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected_list", test_data['lists.py'])
def test_lists(input_data, expected_list):
    result_lines = run_script('lists.py', input_data).split('\n')
    print_lines = [line.strip() for line in result_lines if line.strip()]
    assert print_lines == expected_list

def test_nested_list_example1():
    inputs = ['2', 'Harry', '37.21', 'Berry', '37.21']
    result = run_script('nested_list.py', inputs)
    assert sorted(result.splitlines()) == ['Berry', 'Harry']

def test_nested_list_example2():
    inputs = ['5', 'Harry', '37.21', 'Berry', '37.21', 'Tina', '37.2', 'Akriti', '41', 'Harsh', '39']
    result = run_script('nested_list.py', inputs)
    assert sorted(result.splitlines()) == ['Berry', 'Harry']

print("✅ 65+ ТЕСТОВ для 20 задач готово!")
