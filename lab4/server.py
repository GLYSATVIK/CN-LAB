#Satvik lab assement

import cv2
import socket
import pickle
import math
import time

# Server settings
server_ip = "127.0.0.1"
server_port = 9999

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Open video file (NO fallback)
video_path = r"C:\Users\Satvik\Downloads\1MB.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    raise FileNotFoundError(f"Error: Could not open {video_path}")

# Max UDP payload (safe size)
CHUNK_SIZE = 60000  
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("[SERVER] End of video reached.")
        break

    # Resize (optional: smaller frames = smaller packets)
    frame = cv2.resize(frame, (640, 360))

    # Encode frame
    _, buffer = cv2.imencode(".jpg", frame)
    data = pickle.dumps(buffer)

    # Split into chunks
    total_chunks = math.ceil(len(data) / CHUNK_SIZE)

    for i in range(total_chunks):
        start = i * CHUNK_SIZE
        end = start + CHUNK_SIZE
        chunk = data[start:end]

        # Marker = 1 if last chunk, else 0
        marker = 1 if i == total_chunks - 1 else 0

        # Send (marker, chunk)
        sock.sendto(pickle.dumps((marker, chunk)), (server_ip, server_port))

    frame_count += 1
    print(f"[SERVER] Video frame {frame_count} uploaded")

    time.sleep(0.03)  # ~30 FPS

cap.release()
sock.close()
print("[SERVER] Streaming finished")
