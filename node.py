import hashlib


def mine(message, difficulty=1):
    assert difficulty >= 1
    prefix = '1' * difficulty
    for i in range(1000000):
        digest = sha256(str(hash(message)) + str(i))
        if digest.startswith(prefix):
            print("after " + str(i) + " iterations found nonce: "
                  + digest)
            return digest


def sha256(message):
    return hashlib.sha256(message.encode('ascii')).hexdigest()


class Node:
    def __init__(self, title=""):
        self.title = title
        self.last_transaction_index = None

    @property
    def ipv4_address(self):
        return "192.168.1.1"
