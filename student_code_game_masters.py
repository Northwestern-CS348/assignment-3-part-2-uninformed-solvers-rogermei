from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        states = [list(),list(),list()]
        on_str = 'fact: (on ?disk ?peg)'
        bindings = self.kb.kb_ask(parse_input(on_str)) 
        
        test_cnt = 0
        for b in bindings:
            smaller = int(b['?peg'][3])-1
            bigger = int(b['?disk'][4])
            states[smaller].append(bigger)
            test_cnt += 1
        
        test_cnt = 0
        sorted_states = []
        for state in states:
            tup = tuple(sorted(state))
            sorted_states.append(tup)
            test_cnt += 1
        tup_sorted = tuple(sorted_states)
        
        return tup_sorted

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        term_list = []
        for term in movable_statement.terms:
            term_list.append(str(term))
        
        end_paren = ')'
        asserts = parse_input('fact: (onTopOf ' + term_list[0] + ' ' + term_list[2] + end_paren)
        a = [asserts]
        rets = parse_input('fact: (onTopOf ' + term_list[0] + ' ' + term_list[1] + end_paren)
        r = [rets]
        
        ans_str = 'fact: (onTopOf ?disk ' + term_list[2] + end_paren
        binding = self.kb.kb_ask(parse_input(ans_str))
        if binding == False: 
            a_str = 'fact: (onPeg ' + term_list[0] + ' ' + term_list[2] + end_paren
            a.append(parse_input(a_str))
            r_str = 'fact: (empty ' + term_list[2] + end_paren
            r.append(parse_input(r_str))
        else:
            a_str = 'fact: (onDisk ' + term_list[0] + ' ' + binding[0]['?disk'] + end_paren
            a.append(parse_input(a_str))
            r_str = 'fact: (onTopOf ' + binding[0]['?disk'] + ' '+ term_list[2] + end_paren
            r.append(parse_input(r_str))
            

        ans_str2 = 'fact: (onDisk ' + term_list[0] + ' ?disk)'
        binding = self.kb.kb_ask(parse_input(ans_str2))
        if binding: 
            a.append(parse_input('fact: (onTopOf ' + binding[0]['?disk'] + ' ' + term_list[1] + end_paren))
            r.append(parse_input('fact: (onDisk ' + term_list[0] + ' ' + binding[0]['?disk'] + end_paren))
        else:
            a.append(parse_input('fact: (empty ' + term_list[1] + end_paren))
            r.append(parse_input('fact: (onPeg ' + term_list[0] + ' ' + term_list[1] + end_paren))
            
        for f in r:
            self.kb.kb_retract(f)
        for f in a:
            self.kb.kb_assert(f)
        

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        states = [[-1 for i in range(3)] for j in range(3)] 
        
        at_str ='fact: '
        at_str += '(at ?tile ?posx ?posy)'
        bindings = self.kb.kb_ask(parse_input(at_str))
        
        for b in bindings:
            i1 = int(b['?posy'][3])-1
            i2 = int(b['?posx'][3])-1
            states[i1][i2] = int(b['?tile'][4])
            
        result = []
        for state in states:
            result.append(tuple(state))
        return tuple(result)


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        term_list = []
        for term in movable_statement.terms:
            term_list.append(str(term))
        
        end_paren = ')'
        str_assert = 'fact: (at ' 
        str_assert += term_list[0] + ' ' + term_list[3] + ' ' + term_list[4] + end_paren
        str_ret = 'fact: (at ' 
        str_ret += term_list[0] + ' ' + term_list[1] + ' ' + term_list[2] + end_paren
        
        s1 = 'fact: (empty ' 
        s1 += term_list[1] + ' ' + term_list[2] + end_paren
        s2 = 'fact: (empty ' 
        s2 += term_list[3] + ' ' + term_list[4] + end_paren
        assert_list = [parse_input(str_assert), parse_input(s1)]
        ret_list = [parse_input(str_ret), parse_input(s2)]

        for f in assert_list:
            self.kb.kb_assert(f)
        for f in ret_list:
            self.kb.kb_retract(f)
        

        
    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
