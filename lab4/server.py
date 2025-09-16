# Uses a simple gui to make it good and handles play/pause and file picker

import cv2
import socket
import pickle
import math
import threading
import time
from tkinter import Tk, Button, Label, filedialog, StringVar

CHUNK_SIZE = 60000  # Safe UDP payload size
server_ip = "127.0.0.1"
server_port = 9999

class VideoServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Streaming Server")
        self.video_path = ""
        self.running = False

        self.status = StringVar()
        self.status.set("Select a video to start...")

        # GUI layout
        Label(root, text="UDP Video Stream Server", font=("Arial", 14)).pack(pady=10)
        Button(root, text="Select Video", command=self.select_video).pack(pady=5)
        Button(root, text="Start Streaming", command=self.start_streaming).pack(pady=5)
        Button(root, text="Stop Streaming", command=self.stop_streaming).pack(pady=5)
        Label(root, textvariable=self.status, fg="blue").pack(pady=10)

    def select_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
        if self.video_path:
            self.status.set(f"Selected: {self.video_path}")

    def start_streaming(self):
        if not self.video_path:
            self.status.set("Please select a video first.")
            return

        self.running = True
        threading.Thread(target=self.stream_video, daemon=True).start()
        self.status.set("Streaming started...")

    def stop_streaming(self):
        self.running = False
        self.status.set("Streaming stopped.")

    def stream_video(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cap = cv2.VideoCapture(self.video_path)

        if not cap.isOpened():
            self.status.set("Error: Could not open video.")
            return

        frame_count = 0

        while cap.isOpened() and self.running:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (640, 360))
            _, buffer = cv2.imencode(".jpg", frame)
            data = pickle.dumps(buffer)

            total_chunks = math.ceil(len(data) / CHUNK_SIZE)

            for i in range(total_chunks):
                start = i * CHUNK_SIZE
                end = start + CHUNK_SIZE
                chunk = data[start:end]
                marker = 1 if i == total_chunks - 1 else 0
                sock.sendto(pickle.dumps((marker, chunk)), (server_ip, server_port))

            frame_count += 1
            self.status.set(f"Streaming frame {frame_count}")
            time.sleep(0.03)

        cap.release()
        sock.close()
        self.status.set("Streaming finished.")

if __name__ == "__main__":
    root = Tk()
    app = VideoServerGUI(root)
    root.mainloop()
