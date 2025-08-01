# Socket Programming Project: File Transfer and Real-Time Audio Broadcast

This project implements a Python-based socket server and client system that supports:
- File Transfer from client to server
- Real-Time Audio Broadcasting from server to clients

## Features

### File Transfer (Client → Server)
- Clients can send any file to the server.
- The server receives and saves the file under `received_files/`.
- Supports large files using chunked transfer.

### Real-Time Audio Streaming (Server → Client)
- Server captures microphone input and streams it live to connected clients.
- Clients hear the server's voice in real time.
- Multiple clients can connect and listen simultaneously.

---

## File Structure

```
project/
├── file_server.py        # Main server file
├── FileClient.py        # Client-side application
├── received_files/       # Folder where server stores uploaded files
└── README.md             # Project instructions (this file)
```

---

## Requirements

- Python 3.6+
- `pyaudio` (for audio capture/playback)

### Install Dependencies
```bash
pip install pyaudio
```

On Linux, you may also need:  
```bash
sudo apt-get install portaudio19-dev
```

---

## How to Run

### 1. Start the Server

Open one terminal and run:
```bash
python file_server.py
```

Expected output:
```
[SERVER] Press 1 to stop, 2 to show connected audio clients.
[FILE] File server listening on port 8000
[AUDIO] Audio server listening on port 8001
```

---

### 2. Start the Client

In another terminal:
```bash
python FileClient.py
```

Choose from the menu:
```
1. Send file to server
2. Start listening to audio stream
3. Exit
```

#### Sending a File
Enter the full path to the file you want to upload, for example:
```
C:/Users/USER/Documents/testfile.txt
```

#### Listening to Audio
Choose option `2` to hear live audio from the server's mic.

---

## Notes

- Files are saved in the `received_files/` directory on the server.
- Only the server's microphone is captured.
- You can run multiple clients to simulate a broadcast scenario.
- Make sure ports `8000` and `8001` are free, or edit the script to use custom ports.

---

## Troubleshooting

| Issue                                 | Solution                                                  |
|--------------------------------------|-----------------------------------------------------------|
| `[WinError 10061]` connection refused| Ensure the server is running first                        |
| `[WinError 10048]` address in use    | Kill old process or change the port numbers               |
| File not found error on client       | Use correct path with `/` or double `\\` in Windows       |
| No audio heard                       | Confirm microphone access and speaker volume              |

---

## Educational Value

Through this project, we learn:
- Python socket programming (TCP)
- Sending/receiving files over a network
- Real-time media streaming
---

## Author

Sadaf Saleem 

