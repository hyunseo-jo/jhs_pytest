from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import io
import contextlib

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # 세션용 비밀키

# 퀴즈 문제 목록
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

# 점수 저장소 (이름: 점수)
students_score = {}

# ---------- 라우트 정의 ----------

@app.route('/start', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            session['name'] = name
            session['question_index'] = 0
            if name not in students_score:
                students_score[name] = 0
            return redirect(url_for('index'))
    return render_template('start.html')


@app.route('/')
def index():
    name = session.get('name')
    if not name:
        return redirect(url_for('start'))

    q_index = session.get('question_index', 0)
    if q_index >= len(QUESTIONS):
        q_index = 0
        session['question_index'] = 0  # 다시 처음부터

    question = QUESTIONS[q_index]
    session['code'] = question['code']  # 현재 문제 저장
    return render_template('index.html',
                           code_snippet=question['code'],
                           my_score=students_score.get(name, 0),
                           ranking=get_top_rankings())


@app.route('/check', methods=['POST'])
def check_answer():
    name = session.get('name')
    user_answer = request.json.get("answer", "").strip()
    code_str = session.get("code", "")
    correct_output = execute_code(code_str).strip()

    if user_answer == correct_output:
        students_score[name] += 1
        session['question_index'] = session.get('question_index', 0) + 1
        result = 'correct'
    else:
        result = 'wrong'

    return jsonify({
        "result": result,
        "correct_answer": correct_output,
        "my_score": students_score[name],
        "ranking": get_top_rankings()
    })


def get_top_rankings():
    sorted_scores = sorted(students_score.items(), key=lambda x: x[1], reverse=True)
    return [{"name": n, "score": s} for n, s in sorted_scores[:5]]


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
