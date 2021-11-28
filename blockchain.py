import binascii
import collections
from datetime import datetime

import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from user import User


class Vote:
    def __init__(self, user: User, topic_id, option_id):
        self.user = user
        self.topic_id = topic_id
        self.option_id = option_id
        self.time = datetime.now()

    def to_dict(self):
        return collections.OrderedDict(
            {'identity': self.user.identity, 'topic_id': self.topic_id, 'option_id': self.option_id, 'time': self.time})

    def sign(self):
        private_key = self.user._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')

    def display(self):
        vote_dict = self.to_dict()
        print("identity: " + vote_dict["identity"])
        print("topic_id: " + vote_dict["topic_id"])
        print("option_id: " + vote_dict["option_id"])
        print("time: ", vote_dict["time"])


class Block:
    def __init__(self):
        self.verified_votes = list()
        self.previous_block_hash = ""
        self.Nonce = ""
        self._id = RSA.generate(1024, Crypto.Random.new().read)
        self._options = list()

    @property
    def hash(self):
        return hash(self)

    @property
    def identity(self):
        return binascii.hexlify(self._id.exportKey(format='DER')).decode('ascii')


class VotingOption:
    def __init__(self, title, topic_id):
        self._title = title
        self._topic_id = topic_id
        self.votes = list()
        self._id = RSA.generate(1024, Crypto.Random.new().read)

    @property
    def title(self):
        return self._title

    @property
    def topic_id(self):
        return binascii.hexlify(self._topic_id.exportKey(format='DER')).decode('ascii')

    @property
    def identity(self):
        return binascii.hexlify(self._id.exportKey(format='DER')).decode('ascii')


class Chain:
    def __init__(self, title, creator_id):
        self._creator_id = creator_id
        self._title = title
        self._id = RSA.generate(1024, Crypto.Random.new().read)
        self._options = list()
        self._blocks = list()

    def get_block_by_index(self, index):
        return self._blocks[index]

    @property
    def options(self):
        return self._options

    @property
    def blocks_count(self):
        return len(self._blocks)

    def add_block(self, block: Block):
        self._blocks.append(block)

    def add_option(self, title):
        option = VotingOption(title, self._id)
        self._options.append(option)
        return option

    def dump(self):
        for x in range(self.blocks_count):
            block_temp = self.get_block_by_index(x)
            print("block # " + str(x))
            for vote in block_temp.verified_votes:
                vote.display()
