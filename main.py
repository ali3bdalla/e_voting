#!/usr/bin/python3
from blockchain import Vote, Chain
from node import Node
from user import User

last_block_hash = None

chain0 = Chain('Choose President', 1)
trump = chain0.add_option('Trump')
joe = chain0.add_option('JoeBiden')

Ramesh = User()
Dinesh = User()
Seema = User()
Vijay = User()
Khalid = User()
Hussam = User()

vote0 = Vote(Khalid, joe)
chain0.add_vote(vote0);

vote1 = Vote(Ramesh, joe)
chain0.add_vote(vote1);

vote2 = Vote(Dinesh, trump)
chain0.add_vote(vote2);

vote3 = Vote(Seema, joe)
chain0.add_vote(vote3);

vote4 = Vote(Vijay, joe)
chain0.add_vote(vote4);



vote5 = Vote(Hussam, joe)
chain0.add_vote(vote5);

node = Node()
node.handle(chain0);

chain0.results()
chain0.dump()
