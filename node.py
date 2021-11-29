import hashlib

from blockchain import Block, Chain, Vote



def sha256(message):
    return hashlib.sha256(message.encode('ascii')).hexdigest()


class Node:
    def __init__(self, title=""):
        self.title = title
        self.last_transaction_index = None

    @property
    def ipv4_address(self):
        return "192.168.1.1"

    def handle(self,chain: Chain):
        while len(chain.unverified_votes) >= 3:
            self.process_chain(chain)

    def process_chain(self, chain: Chain):
        block = Block()
        
        for index in range(3):
            temp_vote = chain.pickup_vote()
            if temp_vote is not None and self.verify_vote(temp_vote,chain):
               block.vote_verified(temp_vote)
               chain.vote_verified(temp_vote)
            chain.vote_proccessed(temp_vote)
        if len(block.verified_votes) > 1:
            block.Nonce = self.mine(block,2)
            chain.add_block(block)

    def verify_vote(self,vote: Vote,chain: Chain):
        if vote.option_id not in chain.options_identities: 
            return False
        if vote.user.identity in chain.voted_users:
            return False

        return True;
                    

    def mine(self,message, difficulty=1):
        assert difficulty >= 1
        prefix = '1' * difficulty
        for i in range(1000000):
            digest = sha256(str(hash(message)) + str(i))
            if digest.startswith(prefix):
                return digest