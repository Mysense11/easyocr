import cv2
import easyocr
import pyttsx3

# List of input files
input_files = [
    "ex1.png",
    "ex2.png",
    "ex3.png",
    "ex4.png",
    "morse.mp4",
]  # Add more file paths as needed
output_text_file = "extracted_text.txt"

# Initialize the TTS engine
engine = pyttsx3.init()

while True:
    # Display the list of input files for selection
    print("Available input files:")
    for i, file_name in enumerate(input_files):
        print(f"{i + 1}. {file_name}")

    # Prompt the user to select a file
    selected_file_index = (
        int(input(f"Select a file (1 to {len(input_files)}), or enter 0 to exit: ")) - 1
    )

    if selected_file_index == -1:
        print("Exiting.")
        break
    elif selected_file_index < 0 or selected_file_index >= len(input_files):
        print("Invalid selection. Please select a valid file or enter 0 to exit.")
        continue

    selected_file = input_files[selected_file_index]

    # 동영상에서 이미지 프레임 추출 (동영상 파일의 경우)
    if selected_file.lower().endswith((".mp4", ".avi", ".mov")):
        cap = cv2.VideoCapture(selected_file)
        success, frame = cap.read()
        if not success:
            raise ValueError("동영상에서 이미지 프레임을 읽을 수 없습니다.")
        cv2.imwrite("temp_image.png", frame)
        selected_file = "temp_image.png"

    # Select a voice
    voices = engine.getProperty("voices")
    print("Available voices:")
    for i, voice in enumerate(voices):
        print(f"{i + 1}. ID: {voice.id}, Name: {voice.name}")

    selected_voice_index = int(input("Select a voice (1 to {len(voices)}): ")) - 1
    if selected_voice_index < 0 or selected_voice_index >= len(voices):
        print("Invalid voice selection. Using the default voice.")
    else:
        selected_voice_id = voices[selected_voice_index].id
        engine.setProperty("voice", selected_voice_id)

    # 이미지에서 텍스트 추출
    reader = easyocr.Reader(lang_list=["ko", "en"])

    image = cv2.imread(selected_file)
    results = reader.readtext(image)

    # 추출된 텍스트 파일에 저장
    extracted_text = ""
    for bbox, text, prob in results:
        extracted_text += text + "\n"

    with open(
        output_text_file, "a", encoding="utf-8"
    ) as f:  # Append to the file instead of overwriting
        f.write(f"File: {selected_file}\n")
        f.write(extracted_text)

    # 추출된 텍스트가 비어 있는지 확인하고, 비어 있지 않으면 음성으로 출력
    if extracted_text.strip():
        # 텍스트를 음성으로 변환 및 출력
        engine.say(extracted_text)
        engine.runAndWait()

        # 추출된 텍스트를 터미널에 출력
        print(f"Extracted text from {selected_file}:\n{extracted_text}")
    else:
        print(f"No text extracted from {selected_file}")

    print("Processing of the selected file completed.")
