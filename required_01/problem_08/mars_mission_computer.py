import os # 경로 잡을 때 사용
import json # json 출력
import platform # OS, Version, cpu Type 
import psutil # cpu 코어 수, 메모리 크기, cpu/메모리 실시간 사용량

uri = os.path.dirname(__file__) + '/' #현재 실행 중 위치 경로

class MissionComputer:
    def __init__(self):

        # 보너스 과제: setting.txt에서 출력할 항목 읽기
        # __init__ 함수안에 넣은 이유는 클래스가 생성될 때 Setting.txt 한번만 읽으면 되기 때문
        self.info_settings = self._load_settings('info_settings')
        self.load_settings = self._load_settings('load_settings')

    # 보너스 과제: setting.txt 읽기
    def _load_settings(self, section):
        settings = [] # 항목을 담을 빈 리스트 세팅
        try:
            with open(uri + 'setting.txt', 'r', encoding='utf-8') as f: # r 읽기 모드 
                current_section = None
                for line in f:
                    line = line.strip()  # 앞 뒤 공백 제거 함수
                    if line.startswith('[') and line.endswith(']'): # line을 읽을 때 처음 '[' 끝']' 확인
                        current_section = line[1:-1] # 그 후 첫번 째 문자 제외 및 마지막 문자 제외 파싱 작업
                    elif line and current_section == section: # 줄이 비어있지 않고 섹션이 일치하면
                        settings.append(line) # 해당 항목을 리스트에 추가
        except FileNotFoundError: # 예외처리
            pass
        return settings

    def get_mission_computer_info(self):
        try:
            all_info = {
                'os': platform.system(),
                'os_version': platform.version(),
                'cpu_type': platform.processor(),
                'cpu_core': psutil.cpu_count(logical=False), #False: 물리 코어 True: 논리적코어 수 *Mac M시리즈는 하이퍼스레딩이 없어서 상관 없음
                'memory_size': f'{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB', #total함수는 바이트 단위로 나오기 때문에 1KB = 1024 바이트이기 때문에
                                                                                              #GB 바꺼주기위해서 3으로 거듭제곱 후 round 처리
            }

            # setting.txt에 항목이 있으면 해당 항목만 출력
            if self.info_settings:
                info = {key: v for key, v in all_info.items() if key in self.info_settings} # setting.txt에 있는 항목만 골라서 딕셔너리 생성
            else: # setting.txt가 없거나 비어있으면 전체 출력
                info = all_info

            print(json.dumps(info, indent=4, ensure_ascii=False)) #indent=4는 4칸 들여쓰기
        except Exception as e:
            print(f'에러: 시스템 정보를 가져올 수 없습니다. {e}')

    def get_mission_computer_load(self):
        try:
            all_load = {
                'cpu_usage': f'{psutil.cpu_percent(interval=1)} %', # CPU 1초 동안 측정 후 값 출력
                'memory_usage': f'{psutil.virtual_memory().percent} %',
            }

            # setting.txt에 항목이 있으면 해당 항목만 출력
            if self.load_settings:
                load = {key: v for key, v in all_load.items() if key in self.load_settings}
            else:
                load = all_load

            print(json.dumps(load, indent=4, ensure_ascii=False))
        except Exception as e:
            print(f'에러: 부하 정보를 가져올 수 없습니다. {e}')


if __name__ == '__main__':
    runComputer = MissionComputer() # MissionComputer 클래스를 runComputer로 인스턴스화
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()