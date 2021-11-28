from blockchain import Vote, Block, Chain
from node import Node, mine
from user import User

last_block_hash = None

chain0 = Chain('Choose President', 1)
trump = chain0.add_option('Trump')
joe = chain0.add_option('JoeBiden')

block0 = Block()
block0.previous_block_hash = None
Ramesh = User()
Dinesh = User()
Seema = User()
Vijay = User()
vote0 = Vote(Ramesh, block0.identity, joe.identity)
vote0.sign()
block0.verified_votes.append(vote0)
last_block_hash = block0.hash

print(last_block_hash)
vote1 = Vote(Ramesh, block0.identity, joe.identity)
vote1.sign()

vote2 = Vote(Dinesh, block0.identity, trump.identity)
vote2.sign()

vote3 = Vote(Seema, block0.identity, joe.identity)
vote3.sign()

vote4 = Vote(Vijay, block0.identity, joe.identity)
vote4.sign()

chain0.add_block(block0)
chain0.dump()

node = Node()

print(node.ipv4_address)
# for vote in block0.verified_votes:
#     vote.display()
#     print('--------------')
#
#

print(mine('hello', 3))
