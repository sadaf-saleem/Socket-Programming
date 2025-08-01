import socket
import os
import struct
import pyaudio
import threading

SERVER_ADDRESS = 'localhost'
FILE_PORT = 8000
AUDIO_PORT = 8001
BUFFER_SIZE = 8192

def send_file(file_path):
    if not os.path.isfile(file_path):
        print("[ERROR] File not found.")
        return

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_ADDRESS, FILE_PORT))

            # Send file name length, then name
            s.sendall(struct.pack("!I", len(file_name)))
            s.sendall(file_name.encode())

            # Send file size
            s.sendall(struct.pack("!Q", file_size))

            # Send file data
            with open(file_path, 'rb') as f:
                sent = 0
                while sent < file_size:
                    data = f.read(BUFFER_SIZE)
                    if not data:
                        break
                    s.sendall(data)
                    sent += len(data)
                    print(f"[FILE] Progress: {sent}/{file_size} bytes")

            # Get confirmation
            response = s.recv(1024).decode()
            if response == "SUCCESS":
                print("[FILE] File sent successfully.")
            else:
                print("[FILE] File transfer failed.")

    except Exception as e:
        print(f"[ERROR] {e}")


def start_audio_client():
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    output=True,
                    frames_per_buffer=1024)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_ADDRESS, AUDIO_PORT))
            print("[AUDIO] Connected to audio stream. Listening...")

            while True:
                data = s.recv(1024)
                if not data:
                    break
                stream.write(data)

    except Exception as e:
        print(f"[AUDIO ERROR] {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


def main():
    while True:
        print("\n--- Menu ---")
        print("1. Send file to server")
        print("2. Start listening to audio stream")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            path = input("Enter full path to the file: ").strip()
            send_file(path)
        elif choice == '2':
            threading.Thread(target=start_audio_client, daemon=True).start()
        elif choice == '3':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
