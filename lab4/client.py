# Satvik- lab assesment

import cv2
import socket
import pickle

client_ip = "127.0.0.1"
client_port = 9999

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((client_ip, client_port))

buffer = []

print("[CLIENT] Waiting for video stream...")

while True:
    try:
        packet, _ = sock.recvfrom(65536)  # receive packet
        marker, chunk = pickle.loads(packet)  # receive (marker, chunk)

        buffer.append(chunk)

        if marker == 1:  # last chunk of frame
            # Reconstruct frame
            data = b"".join(buffer)
            frame_data = pickle.loads(data)
            frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)

            # Display video frame
            cv2.imshow("UDP Video Stream", frame)

            buffer.clear()

            # Stop when user presses "q"
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        break

sock.close()
cv2.destroyAllWindows()
print("[CLIENT] Streaming finished")
