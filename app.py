
import cv2
from deepface import DeepFace
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np

def analyze_emotion(frame):
    try:
        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        if isinstance(results, list):
            for result in results:
                emotion = result['dominant_emotion']
                region = result['region']
                x, y, w, h = region['x'], region['y'], region['w'], region['h']
                
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                text = f"Emotion: {emotion}"
                text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)
                
                # Display text above the rectangle
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    except Exception as e:
        print(f"Error in emotion analysis: {e}")
    return frame

def open_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame = analyze_emotion(frame)
        cv2.imshow('Emotion Detection', processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def upload_image():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    try:
        img = cv2.imread(file_path)
        if img is None:
            messagebox.showerror("Error", "Could not read the image file.")
            return
            
        processed_img = analyze_emotion(img)
        cv2.imshow('Emotion Detection', processed_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def main():
    root = tk.Tk()
    root.title("Emotion Detector")

    # Set window size and position
    window_width = 400
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # Add a title label
    title_label = tk.Label(root, text="Emotion Detector", font=("Helvetica", 16))
    title_label.pack(pady=10)

    # Create a frame for the buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)

    # Style the buttons
    button_style = {'font': ('Helvetica', 12), 'bg': '#4CAF50', 'fg': 'white', 'relief': 'raised', 'borderwidth': 2, 'width': 15, 'height': 2}

    # Add buttons to the frame
    camera_btn = tk.Button(button_frame, text="Open Camera", command=open_camera, **button_style)
    camera_btn.pack(side=tk.LEFT, padx=10)

    upload_btn = tk.Button(button_frame, text="Upload Image", command=upload_image, **button_style)
    upload_btn.pack(side=tk.LEFT, padx=10)

    root.mainloop()

if __name__ == "__main__":
    main()
