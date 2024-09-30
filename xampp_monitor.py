import subprocess  # 외부 프로그램을 실행하기 위한 모듈
import time  # 시간 관련 기능을 위한 모듈
import telebot  # Telegram 봇을 만들기 위한 모듈
from telebot.types import ReplyKeyboardMarkup, KeyboardButton  # Telegram에서 사용할 키보드 타입
import psutil  # 시스템 및 프로세스 모니터링을 위한 모듈
import os  # 운영체제와 상호작용하기 위한 모듈
import sys  # 시스템 관련 기능을 위한 모듈
import mysql.connector  # MySQL 데이터베이스와 연결하기 위한 모듈
from mysql.connector import Error  # MySQL 관련 오류를 처리하기 위한 모듈
from config import token

TOKEN = token  # Telegram 봇의 토큰
bot = telebot.TeleBot(TOKEN)  # Telegram 봇 초기화

# 주어진 프로세스 이름의 상태를 확인하는 함수
def check_process_status(process_name):
    # 시스템에서 실행 중인 모든 프로세스 이름을 검사
    return process_name.lower() in (p.name().lower() for p in psutil.process_iter())

# 주어진 프로세스를 종료하는 함수
def kill_process(process_name):
    # 실행 중인 모든 프로세스를 반복하여 일치하는 프로세스를 종료
    for proc in psutil.process_iter():
        if proc.name().lower() == process_name.lower():
            proc.kill()

# XAMPP를 재시작하는 함수
def restart_xampp(chat_id):
    xampp_control = r'C:\xampp\xampp-control.exe'  # XAMPP 제어 패널 경로
    if not os.path.exists(xampp_control):
        bot.send_message(chat_id, "XAMPP 제어 패널을 찾을 수 없습니다.")  # 파일이 없을 경우 메시지 전송
        return

    # 이미 실행 중인 XAMPP 제어 패널을 종료
    kill_process('xampp-control.exe')

    try:
        # XAMPP 제어 패널을 실행
        subprocess.Popen([xampp_control])
        time.sleep(5)  # 패널이 완전히 로드될 때까지 대기
        # 각 서비스(아파치, MySQL, FileZilla)를 중지
        subprocess.run([xampp_control, 'stop', 'apache'], check=True)
        subprocess.run([xampp_control, 'stop', 'mysql'], check=True)
        subprocess.run([xampp_control, 'stop', 'filezilla'], check=True)
        time.sleep(5)  # 서비스가 종료될 때까지 대기
        # 각 서비스(아파치, MySQL, FileZilla)를 시작
        subprocess.run([xampp_control, 'start', 'apache'], check=True)
        subprocess.run([xampp_control, 'start', 'mysql'], check=True)
        subprocess.run([xampp_control, 'start', 'filezilla'], check=True)
        time.sleep(10)  # 서비스가 시작될 때까지 대기
        
        status = check_all_status()  # 모든 서비스 상태 확인
        bot.send_message(chat_id, f"XAMPP 재시작 완료:\n{status}")  # 상태 메시지 전송
    except subprocess.CalledProcessError:
        bot.send_message(chat_id, "XAMPP 재시작 중 오류가 발생했습니다.")  # 오류 발생 시 메시지 전송

# XAMPP 서비스를 리셋하는 함수
def reset_services(chat_id):
    xampp_control = r'C:\xampp\xampp-control.exe'  # XAMPP 제어 패널 경로
    if not os.path.exists(xampp_control):
        bot.send_message(chat_id, "XAMPP 제어 패널을 찾을 수 없습니다.")  # 파일이 없을 경우 메시지 전송
        return

    try:
        # 각 서비스(아파치, MySQL, FileZilla)를 중지
        subprocess.run([xampp_control, 'stop', 'apache'], check=True)
        subprocess.run([xampp_control, 'stop', 'mysql'], check=True)
        subprocess.run([xampp_control, 'stop', 'filezilla'], check=True)
        time.sleep(5)  # 서비스가 종료될 때까지 대기
        # 각 서비스(아파치, MySQL, FileZilla)를 시작
        subprocess.run([xampp_control, 'start', 'apache'], check=True)
        subprocess.run([xampp_control, 'start', 'mysql'], check=True)
        subprocess.run([xampp_control, 'start', 'filezilla'], check=True)
        time.sleep(10)  # 서비스가 시작될 때까지 대기
        
        status = check_all_status()  # 모든 서비스 상태 확인
        bot.send_message(chat_id, f"서비스 리셋 완료:\n{status}")  # 상태 메시지 전송
    except subprocess.CalledProcessError:
        bot.send_message(chat_id, "서비스 리셋 중 오류가 발생했습니다.")  # 오류 발생 시 메시지 전송

# 모든 서비스의 상태를 확인하는 함수
def check_all_status():
    # 아파치, MySQL, FileZilla의 상태를 확인
    apache_status = "정상 작동 중" if check_process_status('httpd.exe') else "작동하지 않음"
    mysql_status = "정상 작동 중" if check_process_status('mysqld.exe') else "작동하지 않음"
    filezilla_status = "정상 작동 중" if check_process_status('filezillaserver.exe') else "작동하지 않음"
    
    mysql_connection_status = "연결 성공" if check_mysql_connection() else "연결 실패"  # MySQL 연결 상태 확인

    # 상태 정보를 포맷하여 반환
    return f"Apache: {apache_status}\nMySQL: {mysql_status}\nFileZilla: {filezilla_status}\nMySQL 연결 상태: {mysql_connection_status}"

# MySQL 데이터베이스와의 연결 상태를 확인하는 함수
def check_mysql_connection():
    try:
        # MySQL 연결 시도
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        if connection.is_connected():
            connection.close()  # 연결이 성공하면 연결 종료
            return True  # 성공적으로 연결됨
    except Error:
        return False  # 연결 실패

# 봇의 시작 명령을 처리하는 핸들러
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # 사용자에게 표시할 버튼 설정
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("재시작"), KeyboardButton("리셋"), KeyboardButton("상태"), KeyboardButton("종료"))
    bot.reply_to(message, "XAMPP 모니터링 봇입니다. 원하는 작업을 선택하세요.", reply_markup=markup)

# 모든 메시지를 처리하는 핸들러
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "재시작":
        restart_xampp(message.chat.id)  # XAMPP 재시작
    elif message.text == "리셋":
        reset_services(message.chat.id)  # 서비스 리셋
    elif message.text == "상태":
        status = check_all_status()  # 상태 확인
        bot.send_message(message.chat.id, f"현재 상태:\n{status}")  # 상태 메시지 전송
    elif message.text == "종료":
        bot.send_message(message.chat.id, "모니터링 프로그램이 성공적으로 종료되었습니다.")  # 종료 메시지 전송
        # sys.exit()  # (주석 처리된 코드) 프로그램 종료
    else:
        bot.reply_to(message, "올바른 명령을 선택해주세요.")  # 올바르지 않은 명령 처리

# 메인 실행 부분
if __name__ == "__main__":
    script_path = os.path.abspath(__file__)  # 현재 스크립트의 절대 경로
    os.chdir(os.path.dirname(script_path))  # 스크립트가 있는 디렉토리로 변경
    
    print("XAMPP 모니터링 봇이 시작되었습니다.")  # 시작 메시지 출력
    bot.polling(none_stop=True)  # 봇 polling 시작
