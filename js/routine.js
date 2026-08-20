// routine.html의 폼과, 결과를 표시할 영역들을 찾아둔다
const form = document.getElementById('routine-form');
const statusMessage = document.getElementById('status-message');
const resultBox = document.getElementById('routine-result');

form.addEventListener('submit', async function (event) {
  event.preventDefault();

  const goal = document.getElementById('goal').value;
  const level = document.getElementById('level').value;
  const time = document.getElementById('time').value;
  const injury = document.getElementById('injury').value;

  if (!goal || !time) {
    statusMessage.textContent = '목표와 가능 시간을 선택해주세요.';
    return;
  }

  resultBox.textContent = '';
  statusMessage.textContent = '루틴을 만드는 중입니다...';

  try {
    const response = await fetch('/api/routine', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ goal, level, time, injury })
    });

    const data = await response.json();

    if (!response.ok) {
      statusMessage.textContent = data.error || '오류가 발생했습니다. 잠시 후 다시 시도해주세요.';
      return;
    }

    statusMessage.textContent = '';
    resultBox.textContent = data.result;

  } catch (error) {
    statusMessage.textContent = '네트워크 오류가 발생했습니다. 연결을 확인해주세요.';
  }
});
