document.addEventListener('DOMContentLoaded', function () {
    const checkBtn = document.getElementById('check-answer');
    const nextBtn = document.getElementById('next-question');
    const showAnswerBtn = document.getElementById('show-answer');
    const feedback = document.getElementById('feedback');
    const userOutput = document.getElementById('user-output');

    let latestCorrectAnswer = null;
    let wrongCount = 0;

    // 다음 문제 버튼 초기 비활성화
    nextBtn.disabled = true;
    nextBtn.style.opacity = 0.5;
    nextBtn.style.cursor = 'not-allowed';

    // 정답 확인
    checkBtn.addEventListener('click', function () {
        const userAnswer = userOutput.value.trim();

        fetch('/check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ answer: userAnswer })
        })
        .then(response => response.json())
        .then(data => {
            latestCorrectAnswer = data.correct_answer;

            if (data.result === 'correct') {
                feedback.textContent = '🎉 정답입니다!';
                feedback.classList.remove('wrong');

                nextBtn.disabled = false;
                nextBtn.style.opacity = 1;
                nextBtn.style.cursor = 'pointer';

                // 정답 보기 버튼 숨기기
                showAnswerBtn.style.display = 'none';
            } else {
                wrongCount += 1;
                feedback.textContent = '❌ 오답입니다.';
                feedback.classList.add('wrong');

                nextBtn.disabled = true;
                nextBtn.style.opacity = 0.5;
                nextBtn.style.cursor = 'not-allowed';

                // 오답이 3회 이상일 때 정답 보기 버튼 보이기
                if (wrongCount >= 3) {
                    showAnswerBtn.style.display = 'inline-block';
                }
            }
        })
        .catch(error => {
            feedback.textContent = '⚠️ 오류가 발생했습니다.';
            feedback.classList.add('wrong');
            console.error('Error:', error);
        });
    });

    // 정답 보기
    showAnswerBtn.addEventListener('click', function () {
        if (latestCorrectAnswer) {
            feedback.textContent = `✅ 정답: ${latestCorrectAnswer}`;
            feedback.classList.remove('wrong');
        }
    });

    // 다음 문제 이동
    nextBtn.addEventListener('click', function () {
        if (!nextBtn.disabled) {
            window.location.href = '/';
        }
    });
});
