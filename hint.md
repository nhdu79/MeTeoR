* Classes
Atom: A(X, mike)@[1,2] with or without temporal intervals
Terms/Entity: Const or Var

Rule: Atom + Body
Body: List of unary/binary literals
Literal: Atoms with MTL operators
    - Unary: Box, Diamond (+ -)
    - Binary: Until, Since -> Left/Right Atom


* Print Dict:
import pprint
pprint.pprint(<dict>)

* Dataset dict shape:
    - { "Predicate": {"Tuple(Term,?)": "Interval" } }

* Ground Body (method)
Generate exchanged var with const using Ground Generator until last predicate, then Apply (method) generate intervals in which head rule can be deduced

* Djsktra
* For hypergraphs, find 1 node...
