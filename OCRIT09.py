import cv2
import pytesseract
from PIL import Image
import numpy as np
import os
import time
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def capture_image(cap):
    ret, frame = cap.read()
    if not ret:
        raise Exception("Failed to capture image")
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_path = f'captured_image_{timestamp}.jpg'
    cv2.imwrite(image_path, frame)
    return image_path, timestamp

def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Image file not found at {image_path}")
    
    _, img_bin = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    img_inv = cv2.bitwise_not(img_bin)
    img_blur = cv2.medianBlur(img_inv, 3)
    img_contrast = cv2.convertScaleAbs(img_blur, alpha=1.5, beta=0)
    cv2.imwrite('preprocessed_image.jpg', img_contrast)
    
    return img_contrast

def extract_text(image_path):
    preprocessed_img = preprocess_image(image_path)
    pil_img = Image.fromarray(preprocessed_img)
    
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(pil_img, config=custom_config)
    return text

def save_to_text_file(text, timestamp, filename):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"{timestamp}: {text}\n")

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Could not open video device")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            cv2.imshow('Camera Feed', frame)
            
            if int(time.time()) % 10 == 0:
                image_path, timestamp = capture_image(cap)
                text = extract_text(image_path)
                print(f"Extracted Text at {timestamp}: {text}")
                save_to_text_file(text, timestamp, 'extracted_text.txt')
                time.sleep(1)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("Program manually stopped.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Camera closed.")

if __name__ == "__main__":
    try:
        if os.system(r'"C:\Program Files\Tesseract-OCR\tesseract.exe" --version') != 0:
            raise pytesseract.TesseractNotFoundError()
        main()
    except pytesseract.TesseractNotFoundError:
        print("Tesseract not found. Make sure Tesseract is installed and the PATH is properly configured.")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(e)
