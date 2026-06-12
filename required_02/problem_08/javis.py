import os
import csv
import speech_recognition as sr
from datetime import timedelta

def process_audio_files():
    audio_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "course2_problem7", 'records')  # 음성 파일 폴더
    if not os.path.exists(audio_dir):
        print(f"[-] 폴더 '{audio_dir}'이(가) 존재하지 않습니다.")
        return

    recognizer = sr.Recognizer()

    for filename in os.listdir(audio_dir):
        if filename.endswith(".wav") or filename.endswith(".mp3"):
            audio_path = os.path.join(audio_dir, filename)
            print(f"[+] 음성 파일 처리 중: {filename}")

            try:
                with sr.AudioFile(audio_path) as source:
                    audio = recognizer.record(source)
                    result = recognizer.recognize_google(audio, show_all=True, language='ko-KR')

                    # CSV 저장용
                    csv_filename = os.path.splitext(filename)[0] + ".csv"
                    csv_path = os.path.join(os.path.dirname(__file__), "records_text", csv_filename)

                    with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(["Time", "Transcript"])

                        if isinstance(result, dict) and "alternative" in result:
                            transcript = result["alternative"][0]["transcript"]
                            writer.writerow(["00:00:00", transcript])  # 전체 시간 하나로 처리
                            print(f"[✓] 저장 완료: {csv_filename}")
                        else:
                            writer.writerow(["00:00:00", "(인식 실패)"])
                            print(f"[!] 인식 결과가 없습니다: {filename}")

            except Exception as e:
                print(f"[!] 오류 발생 ({filename}): {str(e)}")

if __name__ == "__main__":
    # unlock_zip()
    process_audio_files()