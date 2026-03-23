import os
import csv
import pickle

uri = os.path.dirname(__file__) + '/'

# 예외 처리 함수
# *args는 위치 인자(add(data1, data2) <- data1과 data2), **kwargs는 키워드 인자(add(data1 = 3, data2 = 5) <- 이런 형식)
# 위치가 중요하다 *args는 무조건 앞에 **kwargs는 무조건 뒤에
def safe_execute(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except FileNotFoundError:
        raise FileNotFoundError(f"에러: 파일을 찾을 수 없습니다. ({args[0]})")
    except PermissionError:
        raise PermissionError(f"에러: 파일에 대한 권한이 없습니다. ({args[0]})")
    except Exception as e:
        raise Exception(f"알 수 없는 에러 발생: {e}")

# csv 파일 읽어오고 list로 리턴하는 함수
def read_csv(file_name):
    return safe_execute(_read_csv, file_name)

# 언더스코어(_) 내부에서만 사용하겠다는 관례 (java의 private과 비슷한데 강제적인 것이 아님)
def _read_csv(file_name):
    with open(uri + file_name, 'r', encoding='utf-8') as c:
        csv_data = csv.reader(c)
        return list(csv_data)

# csv 파일 저장 함수
def save_to_csv_file(data, name):
    return safe_execute(_save_to_csv_file, data, name)

def _save_to_csv_file(data, name):
    with open(uri + name + '.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)
        print("csv 파일 저장 완료")
        
# 특정 행으로 정렬해주는 함수
def sort_matrix(matrix, index, reverse=False):
    return [matrix[0], 
                *sorted(matrix[1:], key=lambda x: x[index], reverse=reverse)]

# 인화성이 0.7 이상인 값만 필터링해서 리턴하는 함수
def filter_high_flammability(matrix, identifier, threshold):
    identifier_index = matrix[0].index(identifier)
    
    return [matrix[0], 
                *filter(lambda x: float(x[identifier_index])>=threshold, matrix[1:])]

# 이진 파일 저장 함수
def save_to_binary_file(data, name):
    return safe_execute(_save_to_binary_file, data, name)

def _save_to_binary_file(data, name):
    with open(uri + name + '.bin', 'wb') as f:
        pickle.dump(data, f)
        print("이진 파일 저장 완료")

# 이진 파일 읽어서 데이터 리턴하는 함수
def load_binary_file(name):
    return safe_execute(_load_binary_file, name)

def _load_binary_file(name):
    with open(uri + name + '.bin', 'rb') as f:
        return pickle.load(f)

if __name__ == '__main__':
    csv_list = read_csv('Mars_Base_Inventory_List.csv')

    print('############csv 데이터############')
    for c in csv_list:
        print(c)

    sorted_csv_list = sort_matrix(csv_list, 4, True)

    filterd_csv_list = filter_high_flammability(csv_list, 'Flammability', 0.7)

    print('############0.7 이상 Flammability############')
    for f in filterd_csv_list:
        print(f)

    save_to_csv_file(filterd_csv_list, 'Mars_Base_Inventory_danger')

    save_to_binary_file(sorted_csv_list, 'Mars_Base_Inventory_List')

    loaded_binary_data = load_binary_file('Mars_Base_Inventory_List')
    print('#############loaded binary data################')
    print(loaded_binary_data)