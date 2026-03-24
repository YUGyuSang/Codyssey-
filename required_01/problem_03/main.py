import os
import csv
import pickle

uri = os.path.dirname(__file__) + '/'

def read_csv(file_name):
    try:
        with open(uri + file_name, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        print('에러: 파일을 찾을 수 없습니다.')
    except PermissionError:
        print('에러: 파일에 접근할 권한이 없습니다.')
    except Exception as e:
        print(f'에러: {e}')
    return None

def save_csv(file_name, data):
    try:
        with open(uri + file_name, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(data)
            print('csv 파일 저장 완료')
    except Exception as e:
        print(f'에러: {e}')

def save_binary(file_name, data):
    try:
        with open(uri + file_name, 'wb') as f:
            pickle.dump(data, f)
            print('이진 파일 저장 완료')
    except Exception as e:
        print(f'에러: {e}')

def load_binary(file_name):
    try:
        with open(uri + file_name, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f'에러: {e}')
    return None

if __name__ == '__main__':
    # CSV 읽기
    csv_list = read_csv('Mars_Base_Inventory_List.csv')

    # 전체 출력
    print('############ csv 데이터 ############')
    for row in csv_list:
        print(row)

    header = csv_list[0]
    data = csv_list[1:]

    # 인화성 기준 내림차순 정렬 (4번째 열)
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if float(data[i][4]) < float(data[j][4]):
                data[i], data[j] = data[j], data[i]

    sorted_list = [header] + data

    # 인화성 0.7 이상 필터링
    danger_list = [header]
    for row in data:
        if float(row[4]) >= 0.7:
            danger_list.append(row)

    # 위험 물질 출력
    print('############ 0.7 이상 Flammability ############')
    for row in danger_list:
        print(row)

    # CSV 저장
    save_csv('Mars_Base_Inventory_danger.csv', danger_list)

    # 이진 파일 저장
    save_binary('Mars_Base_Inventory_List.bin', sorted_list)

    # 이진 파일 읽기
    loaded_data = load_binary('Mars_Base_Inventory_List.bin')
    print('############ loaded binary data ############')
    for row in loaded_data:
        print(row)