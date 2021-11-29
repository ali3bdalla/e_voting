#!./bin/python3
from datetime import datetime
from Crypto import Random
from blockchain import Vote, Chain
from node import Node
from user import User
import random
chain0 = Chain('Choose President', 1)
trump = chain0.add_option('Trump')
joe = chain0.add_option('JoeBiden')
for x in range(50000):
    rand = random.randint(1000,99999)
    user = User()
    if rand % 2 == 0:
        vote = Vote(user, trump)
    else:
        vote = Vote(user,joe)
    chain0.add_vote(vote);
node = Node()
start_at = datetime.now().timestamp()
node.handle(chain0);
print('tooks ' + str(datetime.now().timestamp() - start_at))
chain0.results()

