import os # os 라이브러리
import json # data를 json 형태로 출력하기 위해
import random # random 함수 
import datetime # 날짜 시간
import time # time.sleep(5) 대기를 사용하기 위해
import threading # 키 입력 감지

uri = os.path.dirname(__file__) + '/'


class DummySensor:
    def __init__(self): # 초기화
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0,
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 4)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    def get_env(self):
        # 보너스 과제: 로그 파일에 저장
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = (
            f'{now}, '
            f'{self.env_values["mars_base_internal_temperature"]}, '
            f'{self.env_values["mars_base_external_temperature"]}, '
            f'{self.env_values["mars_base_internal_humidity"]}, '
            f'{self.env_values["mars_base_external_illuminance"]}, '
            f'{self.env_values["mars_base_internal_co2"]}, '
            f'{self.env_values["mars_base_internal_oxygen"]}'
        )
        with open(uri + 'sensor_log.log', 'a', encoding='utf-8') as f:
            f.write(log_line + '\n')
        # 보너스 과제 끝

        return self.env_values


ds = DummySensor() # 인스턴스화


class MissionComputer:
    def __init__(self): # 초기화
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0,
        }
        self.running = True  # 반복 제어 변수 True면 계속 False면 멈춤

        # 데이터 저장 리스트
        self.history = []
        self.last_average_time = time.time()

    def get_sensor_data(self):
        input_thread = threading.Thread(target=self._wait_for_stop) # 별도의 스레드를 실행시킴 계속 키 대기 상태
        input_thread.daemon = True # True 이므로 main이 죽으면 동시에 죽음
        input_thread.start()

        while self.running:
            # 센서 값 가져와서 env_values에 담기
            ds.set_env()
            sensor_data = ds.get_env()
            for key in self.env_values:
                self.env_values[key] = sensor_data[key]

            # JSON 형태로 출력
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'\n[{now}]')
            print(json.dumps(self.env_values, indent=4))

            # 보너스 과제: 5분 평균 계산
            self.history.append(dict(self.env_values))
            if time.time() - self.last_average_time >= 300: # 300초 == 5분
                self._print_average()
                self.history = [] # 평균 출력 후 초기화
                self.last_average_time = time.time() # 시간 초기화

            time.sleep(5) # 5초 마다 출력

        print('System stopped....') # 보너스 과제

    # 보너스 과제: 키 입력 감지 함수
    def _wait_for_stop(self):
        input() # Enter Key 감지
        self.running = False

    # 보너스 과제: 5분 평균 출력 함수
    def _print_average(self):
        print('\n========== 5분 평균 값 ==========')
        for key in self.env_values:
            avg = round(sum(d[key] for d in self.history) / len(self.history), 4)
            print(f'  {key}: {avg}')
        print('==================================')


if __name__ == '__main__':
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()