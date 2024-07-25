import speech_recognition as sr
from fuzzywuzzy import process

# 音声入力をテキストに変換する関数
def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    try:
        response["transcription"] = recognizer.recognize_google(audio, language="ja-JP")
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"
    return response

# 誤変換の修正候補を生成する関数
def generate_candidates(input_text, dictionary):
    candidates = process.extract(input_text, dictionary, limit=10)
    return [candidate[0] for candidate in candidates]

# メイン関数
def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("音声入力を開始します。話してください...")
    response = recognize_speech_from_mic(recognizer, microphone)

    if response["success"]:
        print(f"認識されたテキスト: {response['transcription']}")
        dictionary = ["正しい単語1", "正しい単語2", "正しい単語3"]  # 辞書データ
        candidates = generate_candidates(response["transcription"], dictionary)
        print("修正候補:")
        for i, candidate in enumerate(candidates):
            print(f"{i+1}: {candidate}")

        choice = int(input("正しい候補の番号を選んでください（1-10）: "))
        if 1 <= choice <= 10:
            correct_text = candidates[choice - 1]
            print(f"選択されたテキスト: {correct_text}")
        else:
            print("無効な選択です。")
    else:
        print(f"エラー: {response['error']}")

if __name__ == "__main__":
    main()