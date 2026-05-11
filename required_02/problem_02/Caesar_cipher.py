import os

uri = os.path.dirname(__file__) + '/'


def caesar_cipher_decode(target_text):
    # 텍스트 사전 (보너스 과제: 사전에 있는 단어 발견 시 자동 중단)
    dictionary = ['the', 'is', 'are', 'was', 'and', 'or', 'in', 'on', 'at',
                  'to', 'for', 'of', 'with', 'this', 'that', 'it', 'be',
                  'have', 'do', 'say', 'go', 'get', 'make', 'know', 'think']

    print('=' * 60)
    print('           카이사르 암호 해독 시작')
    print('=' * 60)
    print(f'원문: {target_text}')
    print('-' * 60)

    auto_found = None
    
    # 알파벳 수(26)만큼 반복
    for shift in range(1, 27):
        decoded = ''
        for char in target_text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                decoded += chr((ord(char) - base - shift) % 26 + base)
            else:
                decoded += char

        print(f'[{shift:2d}자리] {decoded}')

        # 보너스 과제: 사전 단어 발견 시 자동 감지
        words = decoded.lower().split()
        matches = [w for w in words if w in dictionary]
        if len(matches) >= 2 and auto_found is None:
            auto_found = (shift, decoded)
            print(f'       ↑ 사전 단어 발견: {matches} → 자동 감지!')

    print('-' * 60)

    # 보너스 과제: 자동 감지된 결과 있으면 먼저 출력
    if auto_found:
        print(f'자동 감지된 자리수: {auto_found[0]}자리')
        print(f'자동 감지된 결과: {auto_found[1]}')
        save = input('자동 감지 결과를 result.txt로 저장할까요? (y/n): ')
        if save.lower() == 'y':
            with open(uri + 'result.txt', 'w', encoding='utf-8') as f:
                f.write(auto_found[1])
            print('result.txt 저장 완료')
            return auto_found[1]

    # 눈으로 확인 후 자리수 입력
    try:
        shift_num = int(input('해독된 자리수를 입력하세요 (1~26): '))
        if 1 <= shift_num <= 26:
            decoded = ''
            for char in target_text:
                if char.isalpha():
                    base = ord('A') if char.isupper() else ord('a')
                    decoded += chr((ord(char) - base - shift_num) % 26 + base)
                else:
                    decoded += char

            print(f'\n최종 해독 결과: {decoded}')

            with open(uri + 'result.txt', 'w', encoding='utf-8') as f:
                f.write(decoded)
            print('result.txt 저장 완료')
            return decoded
        else:
            print('1~26 사이의 숫자를 입력하세요.')
    except ValueError:
        print('올바른 숫자를 입력하세요.')

    return None


if __name__ == '__main__':
    try:
        with open(uri + 'password.txt', 'r', encoding='utf-8') as f:
            password = f.read().strip()
        print(f'password.txt 읽기 완료: {password}')
        caesar_cipher_decode(password)
    except FileNotFoundError:
        print('에러: password.txt 파일을 찾을 수 없습니다.')
    except Exception as e:
        print(f'에러: {e}')