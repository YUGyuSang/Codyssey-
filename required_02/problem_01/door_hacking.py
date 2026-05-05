import zipfile
import itertools
import string
import time
import multiprocessing
import os

uri = os.path.dirname(__file__) + '/'

CHARS = string.digits + string.ascii_lowercase
PASSWORD_LENGTH = 6
ZIP_FILE = uri + 'emergency_storage_key.zip'
PASSWORD_FILE = uri + 'password.txt'


def unlock_zip():
    if not os.path.exists(ZIP_FILE):
        print(f'에러: {ZIP_FILE} 파일을 찾을 수 없습니다.')
        return

    print('=' * 50)
    print('        ZIP 파일 암호 해제 시작')
    print('=' * 50)

    start_time = time.time()
    print(f'시작 시간: {time.strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'총 경우의 수: {len(CHARS) ** PASSWORD_LENGTH:,} 가지')
    print('-' * 50)

    count = 0

    try:
        with zipfile.ZipFile(ZIP_FILE) as zf:
            for combo in itertools.product(CHARS, repeat=PASSWORD_LENGTH):
                password = ''.join(combo)
                count += 1

                if count % 100000 == 0:
                    elapsed = time.time() - start_time
                    print(f'시도 횟수: {count:,} | 진행 시간: {elapsed:.1f}초 | 현재: {password}')

                try:
                    zf.extractall(pwd=password.encode('utf-8'))
                    elapsed = time.time() - start_time
                    print('-' * 50)
                    print(f'암호 해제 성공! 암호: {password}')
                    print(f'총 시도 횟수: {count:,} | 총 소요 시간: {elapsed:.2f}초')
                    print('=' * 50)
                    with open(PASSWORD_FILE, 'w', encoding='utf-8') as f:
                        f.write(password)
                    print('password.txt 저장 완료')
                    return password
                except Exception:
                    continue

    except zipfile.BadZipFile:
        print(f'에러: 유효한 ZIP 파일이 아닙니다.')
        return

    print('암호 해제 실패')
    return None


# 보너스 과제: 멀티프로세싱 - 첫 글자 기준으로 나눠서 병렬 처리
def try_range(args):
    zip_file, first_char = args
    try:
        with zipfile.ZipFile(zip_file) as zf:
            for combo in itertools.product(CHARS, repeat=PASSWORD_LENGTH - 1):
                password = first_char + ''.join(combo)
                try:
                    zf.extractall(pwd=password.encode('utf-8'))
                    return password
                except Exception:
                    continue
    except Exception:
        pass
    return None


def unlock_zip_fast():
    if not os.path.exists(ZIP_FILE):
        print(f'에러: {ZIP_FILE} 파일을 찾을 수 없습니다.')
        return

    print('=' * 50)
    print('    ZIP 파일 암호 해제 시작 (멀티프로세싱)')
    print('=' * 50)

    start_time = time.time()
    cpu_count = multiprocessing.cpu_count()
    print(f'시작 시간: {time.strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'사용 CPU 코어 수: {cpu_count}')
    print('-' * 50)

    # 첫 글자 36개 기준으로 나눠서 병렬 처리
    args = [(ZIP_FILE, c) for c in CHARS]

    with multiprocessing.Pool(cpu_count) as pool:
        for i, result in enumerate(pool.imap(try_range, args)):
            elapsed = time.time() - start_time
            print(f'진행: {i + 1}/{len(CHARS)} | 진행 시간: {elapsed:.1f}초')
            if result:
                elapsed = time.time() - start_time
                print('-' * 50)
                print(f'암호 해제 성공! 암호: {result}')
                print(f'총 소요 시간: {elapsed:.2f}초')
                print('=' * 50)
                with open(PASSWORD_FILE, 'w', encoding='utf-8') as f:
                    f.write(result)
                print('password.txt 저장 완료')
                pool.terminate()
                return result

    print('암호 해제 실패')
    return None


if __name__ == '__main__':
    # 기본 브루트포스
    # unlock_zip()

    # 보너스 과제: 멀티프로세싱 버전
    unlock_zip_fast()