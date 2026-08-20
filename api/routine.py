from http.server import BaseHTTPRequestHandler
import json
import os
from anthropic import Anthropic

# 파일명이 곧 API 경로가 된다: api/routine.py -> /api/routine
# 클래스 이름은 반드시 'handler'여야 Vercel이 이 파일을 함수로 인식한다
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 요청 본문(JSON)을 읽어온다
            content_length = int(self.headers['Content-Length'])
            body = json.loads(self.rfile.read(content_length))

            goal = body.get('goal', '')
            level = body.get('level', '')
            time = body.get('time', '')
            injury = body.get('injury', '')

            # 실패 처리: 필수값 누락
            if not goal or not time:
                self._send_json(400, {'error': '목표와 가능 시간을 선택해주세요.'})
                return

            # 코드에 키를 직접 쓰지 않고, 환경 변수에서 읽어온다
            client = Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

            prompt = (
                f"운동 목표: {goal}\n"
                f"운동 경험: {level}\n"
                f"부상/제약 부위: {injury if injury else '없음'}\n"
                f"하루 가용 시간: {time}분\n\n"
                "위 조건에 맞는 홈트레이닝 루틴을 한국어로 만들어줘. "
                "운동명, 세트/횟수 또는 시간, 순서를 포함하고, 예상 소요시간과 주의사항도 알려줘."
            )

            message = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            result_text = message.content[0].text
            self._send_json(200, {'result': result_text})


        except Exception as e:
            # 실패 처리: 무슨 에러인지 서버 로그에 출력 (디버깅용)
            import traceback
            traceback.print_exc()
            self._send_json(500, {'error': '일시적인 오류입니다. 잠시 후 다시 시도해주세요.'})


    # 응답을 JSON으로 보내는 반복 코드를 함수로 분리
    def _send_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
