print("Hello Mars")
 
try:
    with open("mission_computer_main.log", "r", encoding="utf-8") as f:
        content = f.read()
        print(content)
except FileNotFoundError:
    print("Error: 로그 파일을 찾을 수 없습니다.")
except PermissionError:
    print("Error: 파일에 접근할 권한이 없습니다.")
except UnicodeDecodeError:
    print("Error: 파일 인코딩을 읽을 수 없습니다.")
except Exception as e:
    print(f"Error: 예상치 못한 오류가 발생했습니다. {e}")
 