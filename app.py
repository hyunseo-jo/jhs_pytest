from flask import Flask, render_template, request, jsonify, session
import io
import contextlib

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # 세션 사용을 위한 키 설정

# 파이썬 코드 문제 리스트 (문제: 실제출력)
QUESTIONS = [
    {"code": "print(1 + 2)", "answer": "3"},
    {"code": "print('Hello' + 'World')", "answer": "HelloWorld"},
    {"code": "a = 3\nb = 4\nprint(a * b)", "answer": "12"},
    {"code": "print(len('Python'))", "answer": "6"},
    # 조건문 문제들 (기존 QUESTIONS 리스트에 추가 가능)
    {"code": "x = 10\nif x > 5:\n    print('크다')", "answer": "크다"},
    {"code": "score = 85\nif score >= 90:\n    print('A')\nelif score >= 80:\n    print('B')\nelse:\n    print('C')", "answer": "B"},
    {"code": "num = 3\nif num % 2 == 0:\n    print('짝수')\nelse:\n    print('홀수')", "answer": "홀수"},
    {"code": "a = 5\nb = 7\nif a > b:\n    print(a)\nelse:\n    print(b)", "answer": "7"},
    {"code": "x = -3\nif x > 0:\n    print('양수')\nelif x == 0:\n    print('0')\nelse:\n    print('음수')", "answer": "음수"},
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


@app.route('/')
def index():
    question_index = session.get('question_index', 0)

    if question_index >= len(QUESTIONS):
        question_index = 0  # 모든 문제를 풀었으면 처음부터 다시

    current_question = QUESTIONS[question_index]
    session['question_index'] = question_index  # 현재 인덱스를 저장
    session['code'] = current_question["code"]  # 정답 확인을 위해 코드 저장

    return render_template('index.html', code_snippet=current_question["code"])


@app.route('/check', methods=['POST'])
def check_answer():
    user_answer = request.json.get("answer", "").strip()
    code_str = session.get("code", "")
    correct_output = execute_code(code_str).strip()

    if user_answer == correct_output:
        result = 'correct'
        session['question_index'] = session.get('question_index', 0) + 1  # 다음 문제로 이동
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
            exec(code_str, {})
    except Exception as e:
        return f"Error: {e}"
    return output.getvalue().strip()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
