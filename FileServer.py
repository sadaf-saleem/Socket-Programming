import socket
import threading
import os
import struct
import pyaudio

FILE_PORT = 8000
AUDIO_PORT = 8001
SAVE_DIR = 'received_files'
BUFFER_SIZE = 8192
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

file_server_running = True
audio_clients = []
audio_server_socket = None

def handle_file_transfer(conn, addr):
    try:
        print(f"[FILE] Connected by {addr}")
        file_name_size = struct.unpack("!I", conn.recv(4))[0]
        file_name = conn.recv(file_name_size).decode()
        file_size = struct.unpack("!Q", conn.recv(8))[0]
        file_name = os.path.basename(file_name)

        os.makedirs(SAVE_DIR, exist_ok=True)
        file_path = os.path.join(SAVE_DIR, file_name)

        received = 0
        with open(file_path, 'wb') as f:
            while received < file_size:
                data = conn.recv(min(BUFFER_SIZE, file_size - received))
                if not data:
                    break
                f.write(data)
                received += len(data)
                print(f"[FILE] Progress: {received}/{file_size} bytes")

        if received == file_size:
            conn.send(b"SUCCESS")
            print(f"[FILE] Received file saved to {file_path}")
        else:
            conn.send(b"FAILURE")
    except Exception as e:
        print(f"[FILE] Error: {e}")
        try:
            conn.send(b"FAILURE")
        except:
            pass
    finally:
        conn.close()


def file_transfer_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', FILE_PORT))
        s.listen()
        print(f"[FILE] File server listening on port {FILE_PORT}")
        while file_server_running:
            try:
                conn, addr = s.accept()
                threading.Thread(target=handle_file_transfer, args=(conn, addr), daemon=True).start()
            except Exception as e:
                print(f"[FILE] Server error: {e}")


def audio_broadcast_server():
    global audio_server_socket
    audio_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    audio_server_socket.bind(('', AUDIO_PORT))
    audio_server_socket.listen()
    print(f"[AUDIO] Audio server listening on port {AUDIO_PORT}")

    def accept_clients():
        while file_server_running:
            conn, addr = audio_server_socket.accept()
            print(f"[AUDIO] Client connected: {addr}")
            audio_clients.append(conn)

    threading.Thread(target=accept_clients, daemon=True).start()

    pa = pyaudio.PyAudio()
    stream = pa.open(format=AUDIO_FORMAT,
                     channels=CHANNELS,
                     rate=RATE,
                     input=True,
                     frames_per_buffer=CHUNK)

    try:
        while file_server_running:
            data = stream.read(CHUNK, exception_on_overflow=False)
            disconnected = []
            for client in audio_clients:
                try:
                    client.sendall(data)
                except:
                    disconnected.append(client)
            for dc in disconnected:
                print("[AUDIO] Client disconnected.")
                audio_clients.remove(dc)
                dc.close()
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()


def main():
    global file_server_running

    threading.Thread(target=file_transfer_server, daemon=True).start()
    threading.Thread(target=audio_broadcast_server, daemon=True).start()

    print("[SERVER] Press 1 to stop, 2 to show connected audio clients.")

    while True:
        cmd = input()
        if cmd == '1':
            file_server_running = False
            if audio_server_socket:
                audio_server_socket.close()
            print("[SERVER] Shutting down.")
            break
        elif cmd == '2':
            print(f"[AUDIO] Connected audio clients: {len(audio_clients)}")


if __name__ == "__main__":
    main()
