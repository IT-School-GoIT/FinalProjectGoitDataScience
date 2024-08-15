import cv2
import mediapipe as mp

# Ініціалізація Mediapipe
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Захоплення відео з камери
cap = cv2.VideoCapture(0)

# Ініціалізація обробки обличчя
with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Не вдалося захопити зображення.")
            break

        # Перетворення зображення з BGR на RGB для обробки
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Виявлення облич
        results = face_detection.process(image_rgb)

        # Малювання результатів
        if results.detections:
            for detection in results.detections:
                mp_drawing.draw_detection(image, detection)

        # Відображення відеопотоку з обробленими обличчями
        cv2.imshow('Face Detection', image)

        if cv2.waitKey(5) & 0xFF == 27:  # Натисніть 'ESC' для виходу
            break

cap.release()
cv2.destroyAllWindows()
