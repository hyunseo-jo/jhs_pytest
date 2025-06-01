document.addEventListener('DOMContentLoaded', function () {
    const checkBtn = document.getElementById('check-answer');
    const nextBtn = document.getElementById('next-question');
    const showAnswerBtn = document.getElementById('show-answer');
    const feedback = document.getElementById('feedback');
    const userOutput = document.getElementById('user-output');
    const myScoreDisplay = document.getElementById('my-score');
    const rankingList = document.getElementById('ranking-list');

    let latestCorrectAnswer = null;
    let wrongCount = 0;

    // 초기 버튼 상태
    nextBtn.disabled = true;
    nextBtn.style.opacity = 0.5;
    nextBtn.style.cursor = 'not-allowed';
    showAnswerBtn.style.display = 'none';

    // 정답 확인 버튼 클릭
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

                showAnswerBtn.style.display = 'none';
                wrongCount = 0;

                // 점수 및 랭킹 갱신
                myScoreDisplay.textContent = data.my_score;
                updateRanking(data.ranking);
            } else {
                feedback.textContent = '❌ 오답입니다.';
                feedback.classList.add('wrong');

                nextBtn.disabled = true;
                nextBtn.style.opacity = 0.5;
                nextBtn.style.cursor = 'not-allowed';

                wrongCount += 1;
                if (wrongCount >= 3) {
                    showAnswerBtn.style.display = 'inline-block';
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            feedback.textContent = '⚠️ 오류가 발생했습니다.';
            feedback.classList.add('wrong');
        });
    });

    // 정답 보기 버튼 클릭
    showAnswerBtn.addEventListener('click', function () {
        if (latestCorrectAnswer) {
            const formatted = latestCorrectAnswer.replaceAll("\n", "\\n");
            feedback.textContent = `✅ 정답: ${formatted}`;
            feedback.classList.remove('wrong');
        }
    });

    // 다음 문제 버튼 클릭
    nextBtn.addEventListener('click', function () {
        if (!nextBtn.disabled) {
            window.location.href = '/';
        }
    });

    // 랭킹 갱신 함수
    function updateRanking(ranking) {
        rankingList.innerHTML = '';
        ranking.forEach(item => {
            const li = document.createElement('li');
            li.textContent = `${item.name} - ${item.score}점`;
            rankingList.appendChild(li);
        });
    }
});
