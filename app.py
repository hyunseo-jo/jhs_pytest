from flask import Flask, render_template, request, jsonify
import random
import io
import contextlib

app = Flask(__name__)

# 파이썬 코드 문제 리스트 (문제: 실제출력)
QUESTIONS = [
    {"code": "print(1 + 2)", "answer": "3"},
    {"code": "print('Hello' + 'World')", "answer": "HelloWorld"},
    {"code": "a = 3\nb = 4\nprint(a * b)", "answer": "12"},
    {"code": "print(len('Python'))", "answer": "6"},
    {"code": "print('파이썬'.upper())", "answer": "파이썬"},
    {"code": "print(10 // 3)", "answer": "3"},
    {"code": "print(10 % 3)", "answer": "1"},
    {"code": "for i in range(2):\n    print('Hi')", "answer": "Hi\nHi"},
    {"code": "def greet():\n    print('Hello')\ngreet()", "answer": "Hello"},
    {"code": "a = [1, 2, 3]\nprint(a[0])", "answer": "1"},
    {"code": "a = [1, 2, 3]\na.append(4)\nprint(len(a))", "answer": "4"},
    {"code": "a = [10, 20, 30]\nprint(sum(a))", "answer": "60"},
    {"code": "s = 'banana'\nprint(s.count('a'))", "answer": "3"},
    {"code": "s = 'Python'\nprint(s[::-1])", "answer": "nohtyP"},
    {"code": "x = 5\ny = x\nx = 10\nprint(y)", "answer": "5"},
    {"code": "def square(n):\n    return n * n\nprint(square(3))", "answer": "9"},
    {"code": "x = [1, 2, 3]\nprint(x[-1])", "answer": "3"},
    {"code": "print(type('3'))", "answer": "<class 'str'>"},
    {"code": "for i in range(1, 4):\n    print(i * '*')", "answer": "*\n**\n***"},
    {"code": "for i in range(3):\n    for j in range(2):\n        print(i, j)", "answer": "0 0\n0 1\n1 0\n1 1\n2 0\n2 1"}
]

# 현재 문제를 저장할 임시 변수 (간단하게 전역 사용)
current_question = {}


@app.route('/')
def index():
    global current_question
    current_question = random.choice(QUESTIONS)
    return render_template('index.html', code_snippet=current_question["code"])


@app.route('/check', methods=['POST'])
def check_answer():
    global current_question
    user_answer = request.json.get("answer", "").strip()

    correct_output = execute_code(current_question["code"]).strip()

    if user_answer == correct_output:
        result = 'correct'
    else:
        result = 'wrong'

    return jsonify({
        "result": result,
        "correct_answer": correct_output
    })


# 실제 코드 실행 결과를 문자열로 반환
def execute_code(code_str):
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            exec(code_str, {})  # 빈 전역 네임스페이스에서 실행
    except Exception as e:
        return f"Error: {e}"
    return output.getvalue().strip()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
