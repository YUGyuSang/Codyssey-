import os
import wave
import datetime

uri = os.path.dirname(__file__) + '/'
RECORDS_DIR = uri + 'records/'

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    print('경고: pyaudio가 설치되지 않았습니다.')
    print('설치 명령어: pip3 install pyaudio')

# 녹음 설정
CHUNK = 1024
FORMAT = pyaudio.paInt16 if PYAUDIO_AVAILABLE else None
CHANNELS = 1
RATE = 44100


def init_records_dir():
    if not os.path.exists(RECORDS_DIR):
        os.makedirs(RECORDS_DIR)
        print(f'records 폴더 생성: {RECORDS_DIR}')


def record_audio():
    if not PYAUDIO_AVAILABLE:
        print('에러: pyaudio가 설치되지 않아 녹음할 수 없습니다.')
        return

    init_records_dir()

    now = datetime.datetime.now()
    filename = now.strftime('%Y%m%d-%H%M%S') + '.wav'
    filepath = RECORDS_DIR + filename

    p = pyaudio.PyAudio()

    # 마이크 인식
    try:
        device_count = p.get_device_count()
        print(f'\n인식된 오디오 장치 수: {device_count}')
        for i in range(device_count):
            device = p.get_device_info_by_index(i)
            if device['maxInputChannels'] > 0:
                print(f'  [{i}] {device["name"]}')
    except Exception as e:
        print(f'에러: 마이크 인식 실패 - {e}')
        p.terminate()
        return

    print('\n녹음을 시작합니다. 멈추려면 Enter를 누르세요.')

    try:
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
    except Exception as e:
        print(f'에러: 마이크를 열 수 없습니다 - {e}')
        p.terminate()
        return

    frames = []
    recording = [True]

    import threading

    def stop_recording():
        input()
        recording[0] = False

    stop_thread = threading.Thread(target=stop_recording)
    stop_thread.daemon = True
    stop_thread.start()

    print('녹음 중...')
    while recording[0]:
        try:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
        except Exception:
            break

    print('녹음 완료!')
    stream.stop_stream()
    stream.close()
    p.terminate()

    try:
        with wave.open(filepath, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        print(f'저장 완료: {filename}')
    except Exception as e:
        print(f'에러: 파일 저장 실패 - {e}')


def show_recordings_by_date(start_date, end_date):
    init_records_dir()

    try:
        start = datetime.datetime.strptime(start_date, '%Y%m%d')
        end = datetime.datetime.strptime(end_date, '%Y%m%d')
        end = end.replace(hour=23, minute=59, second=59)
    except ValueError:
        print('에러: 날짜 형식이 올바르지 않습니다. (예: 20260101)')
        return

    try:
        files = os.listdir(RECORDS_DIR)
    except Exception as e:
        print(f'에러: records 폴더를 읽을 수 없습니다 - {e}')
        return

    wav_files = [f for f in files if f.endswith('.wav')]
    found = []

    for filename in wav_files:
        try:
            date_str = filename.replace('.wav', '')
            file_date = datetime.datetime.strptime(date_str, '%Y%m%d-%H%M%S')
            if start <= file_date <= end:
                found.append((file_date, filename))
        except ValueError:
            continue

    found.sort()

    print(f'\n====== {start_date} ~ {end_date} 녹음 파일 ======')
    if found:
        for date, filename in found:
            print(f'  {date.strftime("%Y년 %m월 %d일 %H:%M:%S")} - {filename}')
        print(f'총 {len(found)}개')
    else:
        print('  해당 날짜의 녹음 파일이 없습니다.')
    print('=' * 45)


if __name__ == '__main__':
    while True:
        print('\n====== JAVIS 녹음 시스템 ======')
        print('1. 녹음 시작')
        print('2. 날짜별 녹음 파일 보기')
        print('3. 종료')
        print('=' * 30)

        choice = input('선택: ').strip()

        if choice == '1':
            record_audio()

        elif choice == '2':
            start = input('시작 날짜 (예: 20260101): ').strip()
            end = input('종료 날짜 (예: 20261231): ').strip()
            show_recordings_by_date(start, end)

        elif choice == '3':
            print('종료합니다.')
            break

        else:
            print('1, 2, 3 중에서 선택하세요.')