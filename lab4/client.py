

import cv2
import socket
import pickle
import threading
from tkinter import Tk, Button, Label, StringVar

client_ip = "127.0.0.1"
client_port = 9999

class VideoClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Streaming Client")
        self.running = False

        self.status = StringVar()
        self.status.set("Waiting to start...")

        Label(root, text="UDP Video Stream Client", font=("Arial", 14)).pack(pady=10)
        Button(root, text="Start Receiving", command=self.start_receiving).pack(pady=5)
        Button(root, text="Stop Receiving", command=self.stop_receiving).pack(pady=5)
        Label(root, textvariable=self.status, fg="green").pack(pady=10)

    def start_receiving(self):
        self.running = True
        threading.Thread(target=self.receive_video, daemon=True).start()
        self.status.set("Receiving video stream...")

    def stop_receiving(self):
        self.running = False
        self.status.set("Receiving stopped.")

    def receive_video(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((client_ip, client_port))
        buffer = []

        while self.running:
            try:
                packet, _ = sock.recvfrom(65536)
                marker, chunk = pickle.loads(packet)
                buffer.append(chunk)

                if marker == 1:
                    data = b"".join(buffer)
                    frame_data = pickle.loads(data)
                    frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)

                    if frame is not None:
                        cv2.imshow("UDP Video Stream", frame)

                    buffer.clear()
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        self.stop_receiving()
                        break

            except Exception as e:
                self.status.set(f"Error: {e}")
                break

        sock.close()
        cv2.destroyAllWindows()
        self.status.set("Streaming ended.")

if __name__ == "__main__":
    root = Tk()
    app = VideoClientGUI(root)
    root.mainloop()
