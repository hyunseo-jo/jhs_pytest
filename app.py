from flask import Flask, render_template, request, jsonify
import io
import contextlib

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# 문제 리스트 (input 포함 문제는 코드 실행 없이 처리됨)
QUESTIONS = [
    {"code": "age = 17\nprint(age)", "answer": "17"},
    {"code": "a = 10\nb = a\na = 5\nprint(b)", "answer": "10"},
    {"code": "a = b = c = 2024\na = a + 1\nb = b - 1\nc = a + b\nprint(c)", "answer": "4048"},
    {"code": "변수명으로 사용할 수 없는 것은?\n1.a\n2.A\n3.Stu_num\n4.1st_num\n5._min_num", "answer": "4"},
    {"code": "a = 5\nif a == 5:\n   print(True)", "answer": "True"},
    {"code": "b = 13\nif b > 10:\n   print(b)", "answer": "13"},
    {"code": "a = 10\nb = 5\nif a < b:\n   a = a - b\nprint(a)", "answer": "10"},
    {"code": "for i in range(5):\n   print(i)", "answer": "0\n1\n2\n3\n4"},
    {"code": "for i in range(0,5,2):\n   print(i)", "answer": "0\n2\n4"},
    {"code": "a=int(input())\nfor i in range(2+a):\n   print(i)", "answer": "0\n1\n2\n3\n4\n5"},
    {"code": "semester = ['정보','수학','과학']\nfor subject in semester:\n   print(subject)", "answer": "정보\n수학\n과학"},
    {"code": "name = 'Hong Gil Dong'\nfor i in name:\n   print(i)", "answer": "H\no\nn\ng\n \nG\ni\nl\n \nD\no\nn\ng"},
    {"code": "age = int(input())\nif age < 13:\n   print(\"전체 관람가\")\nelse:\n   if age < 18:\n      print(\"12세 이상 관람가\")\n   else:\n      print(\"성인 관람가\")", "answer": "12세 이상 관람가"},
    {"code": "tem = int(input())\nif tem < 0:\n   print(\"두꺼운 코트\")\nelse:\n   if tem < 20:\n      print(\"가벼운 자켓\")\n   else:\n      print(\"반팔 티셔츠\")", "answer": "반팔 티셔츠"},
    {"code": "rows = 5\ni = 1\nwhile i <= rows:\n   j = 1\n   while j <= i:\n      print(\"*\", end=\" \")\n      j = j + 1\n   print()\n   i = i + 1", "answer": "* *\n* * *\n* * * *\n* * * * *"},
    {"code": "a = [1,2,3,4]\nprint(a)", "answer" : "[1,2,3,4]"},
    {"code": "b = ['딸기',12,7,'복숭아']\nprint(b)", "answer" : "['딸기',12,7,'복숭아']"},
    {"code": "c = 'Hello Python'\nprint(c)", "answer" : "Hello Python"},
    {"code": "과일 = ['딸기','바나나','사과']\nprint(과일[0])", "answer" : "딸기"},
    {"code": "num = [1,2,3,4,5]\nprint(num[-1]+num[2])", "answer":"8"},
    {"code": "char = 'Hello! Python'\nprint(char[7])", "answer":"P or char[-6]"},
    {"code": "def hello():\n   print('hi')\n   print(\"hello\")\n\nhello()", "answer":"hi\nhello"},
    {"code": "def even(number):\n   return number % 2 == 0\n\nprint(even(4))\nprint(even(7))", "answer":"True\nFalse"},
    {"code": "def factorial(n):\n   if n == 1:\n      return 1\n   return n * factorial(n-1)\n\nprint(factorial(5))", "answer":"120"},
    {"code": "def fibo(n):\n   if n <= 1:\n      return n\n   return fibo(n-1) + fibo(n-2)\n\nprint(fibo(7))", "answer":"13"},
]

current_index = 0

@app.route('/')
def index():
    global current_index
    if current_index >= len(QUESTIONS):
        current_index = 0
    question = QUESTIONS[current_index]
    return render_template('index.html', code_snippet=question["code"])

@app.route('/check', methods=['POST'])
def check_answer():
    global current_index
    user_answer = request.json.get("answer", "").strip()
    question = QUESTIONS[current_index]
    correct_output = question["answer"].strip()

    correct_answers = [ans.strip() for ans in correct_output.split("or")]

    if 'input(' in question["code"]:
        is_correct = user_answer in correct_answers
    else:
        executed_output = execute_code(question["code"]).strip()
        is_correct = user_answer == executed_output

    if is_correct:
        result = 'correct'
        current_index += 1
    else:
        result = 'wrong'

    return jsonify({
        "result": result,
        "correct_answer": correct_output
    })

def execute_code(code_str):
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            exec(code_str, {})
    except Exception as e:
        return f"Error: {e}"
    return output.getvalue().strip()

if __name__ == '__main__':
    app.run(debug=True)
