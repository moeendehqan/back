from cryptography.fernet import Fernet


key = 'GXCs1b_Ki2q5XR6M038drJTsjjgdlBozbFN4irI0iHo='
f = Fernet(key)

def encrypt(msg):
    msg = str(msg).encode()
    msg = f.encrypt(msg)
    return msg

def decrypt(msg):
    msg = f.decrypt(msg)
    msg = msg.decode()
    return msg
