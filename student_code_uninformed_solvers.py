
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if (self.currentState.state == self.victoryCondition) or (self.currentState not in self.visited):
            self.visited[self.currentState] = True
            win_or_not = self.currentState.state == self.victoryCondition
            return win_or_not

        if not self.currentState.nextChildToVisit: 
            its = 0
            for movable in self.gm.getMovables():
                its += 1
                # time test
                # too long 
                if its == "too long":
                    return "too long"
                #make every move in movable
                self.gm.makeMove(movable)
                new = self.gm.getGameState()
                new_gs = GameState(new, self.currentState.depth+1, movable)
                
                if new_gs not in self.visited:
                    new_gs.parent = self.currentState
                    self.currentState.children.append(new_gs)
                self.gm.reverseMove(movable)            
            
        num_children = len(self.currentState.children)
        if self.currentState.nextChildToVisit < num_children:
            new = self.currentState.children[self.currentState.nextChildToVisit]
            self.currentState.nextChildToVisit = self.currentState.nextChildToVisit + 1
            self.gm.makeMove(new.requiredMovable)
            self.currentState = new
            #recurse
            return self.solveOneStep()
        else:
            self.currentState.nextChildToVisit = self.currentState.nextChildToVisit + 1
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            #recurse
            return self.solveOneStep()


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
    
    def solveOneStep_helper(self, depth):
        if self.currentState.depth > depth:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            soln = self.solveOneStep_helper(depth)
            return soln
        elif self.currentState.depth == depth:
            if self.currentState not in self.visited or (not depth) and (len(self.currentState.children) == 0):
                #make every movable move, brute force
                its = 0
                for movable in self.gm.getMovables():
                    its += 1
                    # test time
                    # too long
                    if its == "too long":
                        return "too long"
                    self.gm.makeMove(movable)
                    new = self.gm.getGameState()
                    new_gs = GameState(new, self.currentState.depth + 1, movable)  
                    if new_gs not in self.visited:
                        new_gs.parent = self.currentState
                        self.currentState.children.append(new_gs)
                    self.gm.reverseMove(movable)  

            if (self.currentState.state == self.victoryCondition) or (self.currentState not in self.visited):
                self.visited[self.currentState] = True
                win_or_not = self.currentState.state == self.victoryCondition 
                return win_or_not
            else:
                # depth is 0
                if not self.currentState.depth: 
                    return True
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
                return self.solveOneStep_helper(depth)   
        # less than or equal to depth
        else:
            num_children = len(self.currentState.children)
            if self.currentState.nextChildToVisit > num_children:
                self.currentState.nextChildToVisit = 0
            if self.currentState.nextChildToVisit < num_children:
                new = self.currentState.children[self.currentState.nextChildToVisit]
                self.currentState.nextChildToVisit += 1
                self.gm.makeMove(new.requiredMovable)
                self.currentState = new
                return self.solveOneStep_helper(depth)
            else:
                self.currentState.nextChildToVisit += 1
                # depth is 0
                if not self.currentState.depth: 
                    return True
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
                return self.solveOneStep_helper(depth)
    
    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        if (self.currentState.state == self.victoryCondition):
            self.visited[self.currentState] = True
            win_or_not = (self.currentState.state == self.victoryCondition)
            return win_or_not

        game_depth = self.currentState.depth
        continue_game = True
        test_its = 0
        while continue_game:
            test_its += 1
            # too long 
            # time test
            if test_its == "too long":
                return "too long"
            result = self.solveOneStep_helper(game_depth)
            if result:
                victory_satisfied = (self.currentState.state == self.victoryCondition)
                if victory_satisfied:
                    result_bool = True
                    return result_bool
                else:
                    game_depth = game_depth + 1
            else:
                return False