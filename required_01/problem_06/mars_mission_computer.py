import os
import random
import datetime

uri = os.path.dirname(__file__) + '/'

class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0,
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2) # 화성 기지 내부 온도
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2) # 화성 기지 외부 온도
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2) # 화성 기지 내부 습도
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2) # 화성 기지 외부 광량
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 4) # 화성 기지 내부 이산화탄소 농도
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2) # 화성 기지 내부 산소 농도

    def get_env(self):
        # 보너스 과제
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


if __name__ == '__main__':
    ds = DummySensor()
    ds.set_env()
    env = ds.get_env()

    print('=' * 40)
    print('       화성 기지 환경 데이터')
    print('=' * 40)
    print(f'  내부 온도       : {env["mars_base_internal_temperature"]} 도')
    print(f'  외부 온도       : {env["mars_base_external_temperature"]} 도')
    print(f'  내부 습도       : {env["mars_base_internal_humidity"]} %')
    print(f'  외부 광량       : {env["mars_base_external_illuminance"]} W/m2')
    print(f'  내부 CO2 농도   : {env["mars_base_internal_co2"]} %')
    print(f'  내부 산소 농도  : {env["mars_base_internal_oxygen"]} %')
    print('=' * 40)