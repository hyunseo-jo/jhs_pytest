from flask import Flask, render_template, request, jsonify
import io
import contextlib

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # 세션 사용 시 필요

# 문제 리스트
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
    {"code": "다음 프로그램에서 3을 입력한 후 실행 결과를쓰시오.\na=int(input())\nfor i in range(2+a):\n   print(i)", "answer": "0\n1\n2\n3\n4\n5"},
    {"code": "semester = ['정보','수학','과학']\nfor subject in semester:\n   print(subject)", "answer": "정보\n수학\n과학"},
    {"code": "name = 'Hong Gil Dong'\nfor i in name\n   print(i)", "answer": "H\no\nn\ng\n \nG\ni\nl\n \nD\no\nn\ng"},
    {"code": "17을 입력했을 때 출력 결과는? \n age = int(input())]\n if age < 13:\n   print("전체 관람가")\nelse:\n   if age < 18:\n      print("12세 이상 관람가")\n   else:\n      print("성인 관람가")", "answer": "12세 이상 관람가"},
    {"code": "28을 입력했을 때 출력 결과는? \n tem = int(input())]\n if tem < 0:\n   print("두꺼운 코트")\nelse:\n   if tem < 20:\n      print("가벼운 자켓")\n   else:\n      print("반팔 티셔츠")", "answer": "반팔 티셔츠"},
    {"code": "rows = 5\ni = 1\nwhile i <= rows:\n   j = 1\n   while j<=i\n      print("*", end=" ")\n      j=j+1\n   print()\n   i=i+1", "answer": "*\n**\n***\n****\n*****"},
    {"code": "a = [1,2,3,4]\nprint(a)", "answer" : "[1,2,3,4]"},
    {"code": "b = ['딸기',12,7,'복숭아']\nprint(b)", "answer" : "['딸기',12,7,'복숭아']"},
    {"code": "c = 'Hello Python'\nprint(c)", "answer" : "Hello Python"},
    {"code": "과일 = ['딸기','바나나','사과']", "answer" : "딸기"},
    {"code": "출력 결과가 8일 때, 밑줄에 알맞은 숫자를 쓰시오.\nnum = [1,2,_,4,5]\nprint(num[-1]+num[2])","answer":"3"},    # ... 필요시 계속 추가]
    {"code": "출력 결과가 P일 때, 밑줄에 알맞은 명령어를 쓰시오.\nchar = 'Hello! Python'\nprint(_____)","answer":"char[7] or char[-6]"},    # ... 필요시 계속 추가]
    {"code": "def hello():\n   print('hi')\n   print("hello")\n\nhello()","answer":"hi\nhello"},    # ... 필요시 계속 추가]
    {"code": "def even(number):\n   return number % 2 == 0\n\nprint(even(4)\nprint(even(7)))","answer":"True\nFalse"},    # ... 필요시 계속 추가]
    {"code": "def factorial(n):\n   if n == 1:\n      return 1\n   return n * factorial(n-1)\n\nprint(factorial(5))","answer":"120"},    # ... 필요시 계속 추가]
    {"code": "def fibo(n):\n   if n <= 1:\n      return n\n   return fibo(n-1) + fibo(n-2)\n\nprint(fibo(7))","answer":"13"}]    # ... 필요시 계속 추가]








# 문제 번호를 저장하는 전역 변수
current_index = 0

@app.route('/')
def index():
    global current_index
    if current_index >= len(QUESTIONS):
        current_index = 0  # 마지막 문제까지 푼 경우 처음으로

    question = QUESTIONS[current_index]
    return render_template('index.html', code_snippet=question["code"])

@app.route('/check', methods=['POST'])
def check_answer():
    global current_index
    user_answer = request.json.get("answer", "").strip()
    question = QUESTIONS[current_index]

    correct_output = execute_code(question["code"]).strip()

    if user_answer == correct_output:
        result = 'correct'
        current_index += 1  # 다음 문제로 넘어감
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
