import binascii
import collections
from datetime import datetime

import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from user import User



class VotingOption:
    def __init__(self, title, topic_id):
        self._title = title
        self._topic_id = topic_id
        self.votes_count = 0
        self._id = RSA.generate(1024, Crypto.Random.new().read)

    def voted(self):
        self.votes_count = self.votes_count + 1
    @property
    def title(self):
        return self._title

    @property
    def topic_id(self):
        return binascii.hexlify(self._topic_id.exportKey(format='DER')).decode('ascii')

    @property
    def identity(self):
        return binascii.hexlify(self._id.exportKey(format='DER')).decode('ascii')


class Vote:
    def __init__(self, user: User,  option: VotingOption):
        self.user = user
        self.chain_id = None
        self.signture = None
        self.option = option
        self.option_id = option.identity
        self.time = datetime.now()

    def to_dict(self):
        return collections.OrderedDict(
            {'identity': self.user.identity, 'chain_id': self.chain_id, 'option_id': self.option_id, 'time': self.time})

    def sign(self):
        private_key = self.user._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        self.signture =  binascii.hexlify(signer.sign(h)).decode('ascii')

    def display(self):
        vote_dict = self.to_dict()
        print("identity: " + vote_dict["identity"])
        print("option_id: " + vote_dict["option_id"])
        print("time: ", vote_dict["time"])
        print("-----------------------")

class Block:
    def __init__(self):
        self.verified_votes = list()
        self.previous_block_hash = ""
       
        self.Nonce = ""
        self._id = RSA.generate(1024, Crypto.Random.new().read)
        self._options = list()

    def vote_verified(self,vote: Vote):
        self.verified_votes.append(vote)
        vote.option.voted()
    

    @property
    def hash(self):
        return hash(self)


    @property
    def identity(self):
        return binascii.hexlify(self._id.exportKey(format='DER')).decode('ascii')



class Chain:
    def __init__(self, title, creator_id):
        self._creator_id = creator_id
        self._title = title
        self.verified_votes_count = 0
        self._id = RSA.generate(1024, Crypto.Random.new().read)
        self._options = list()
        self._blocks = list()
        self.last_block_hash = None
        self.unverified_votes = []

    def vote_verified(self,vote):
        self.verified_votes_count = self.verified_votes_count + 1

    @property
    def options_identities(self):
        for option in self._options: 
            yield option.identity

    def pickup_vote(self):
        return self.unverified_votes[0]

    def add_vote(self,vote: Vote):
        vote.chain_id = self._id
        vote.sign();
        self.unverified_votes.append(vote)

    def vote_proccessed(self,vote):
        self.unverified_votes.remove(vote)

    def get_block_by_index(self, index):
        return self._blocks[index]

    @property
    def options(self):
        return self._options

    @property
    def blocks_count(self):
        return len(self._blocks)

    def add_block(self, block: Block):
        block.previous_block_hash = self.last_block_hash
        self._blocks.append(block)
        self.last_block_hash = hash(block)


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

    @property
    def voted_users(self):
        for x in range(self.blocks_count):
            block_temp = self.get_block_by_index(x)
            for vote in block_temp.verified_votes:
                yield vote.user.identity

    def results(self):
        for option in self._options:
            percentage = round((option.votes_count / self.verified_votes_count ) * 100,2)
            print(option.title + " : " + str(percentage) + "%")
