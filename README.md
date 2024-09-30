
# XAMPP Monitoring Bot

이 봇은 Telegram을 통해 XAMPP의 상태를 모니터링하고 제어할 수 있는 기능을 제공합니다. 이 봇은 Apache, MySQL, FileZilla와 같은 XAMPP 서비스를 재시작하고 리셋하며, 현재 상태를 확인할 수 있습니다.

## 필요 모듈
- `subprocess`: 외부 프로그램을 실행하기 위한 모듈
- `time`: 시간 관련 기능을 위한 모듈
- `telebot`: Telegram 봇을 만들기 위한 모듈
- `psutil`: 시스템 및 프로세스 모니터링을 위한 모듈
- `os`: 운영체제와 상호작용하기 위한 모듈
- `mysql.connector`: MySQL 데이터베이스와 연결하기 위한 모듈

## 설치 방법
1. 필요한 모듈을 설치합니다:
   ```bash
   pip install pyTelegramBotAPI psutil mysql-connector-python
   ```

2. `config.py` 파일을 생성하여 봇의 토큰을 추가합니다:
   ```python
   # config.py
   token = 'YOUR_TELEGRAM_BOT_TOKEN'  # 여기에 자신의 Telegram 봇 토큰을 입력하세요
   ```

## 사용법
- `/start`: 봇을 시작하고 명령어 버튼을 표시합니다.
- "재시작": XAMPP 서비스를 재시작합니다.
- "리셋": XAMPP 서비스를 리셋합니다.
- "상태": 현재 XAMPP 서비스 상태를 확인합니다.
- "종료": 모니터링 프로그램을 종료합니다.

## 주의사항
- XAMPP가 설치된 경로가 `C:\xampp\xampp-control.exe`여야 합니다. 경로가 다를 경우, 코드에서 경로를 수정해야 합니다.
