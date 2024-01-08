import numpy as np
from typing import Set, Tuple, List

class MergeBricks:
    def __init__(self, width:int = 5, height:int =5):
        
        self.width:int = width
        self.height:int = height
        self.probabilities: dict = {
            1: [1],
            2: [.8,.2],
            3: [.7,.3,.0],
            4: [.65,.35,.0,.0],
            5: [.6,.35,.05,.0,.0],
            6: [.4,.5,.1,.0,.0,.0],
            7: [.3,.5,.1,.05,.05,.0,.0],
            8: [.2,.55,.1,.05,.05,.05,.0,.0],
            9: [.1,.55,.15,.1,.05,.05,.0,.0,.0],
            10:[0.,.4,.3,.1,.1,.05,.025,.025,0.,0.]
        }
        
        self.reset()
        self.action_list = []
        
        for y in range(height):
            for x in range(width):
                self.action_list.append((y,x))
        
        
    def reset(self):
        self.world:np.ndarray = np.zeros((self.height, self.width))
        
        self.score:int = 0
        self.visited: Set[int] = set({1.0})
        self.next = 1
        
        # Post Initilisation
        self.world[2,1] = 1
        
        self.end = False
        
        
    @property
    def valid_positions(self):
        return np.dstack(np.where(self.world==0)).reshape((-1,2))
    
    def step(self, position):
        if not self.validate_pos(position):
            return 
        
        self.world[position] = self.next
        self.score += 1
        
        self.check_merge(last_position=position)
        
        choice_list = sorted(list(self.visited))[-10:]
        # print(choice_list,len(choice_list), np.sum(self.probabilities[len(choice_list)]))
        self.next = int(np.random.choice(choice_list,p=self.probabilities[len(choice_list)]))
        
        
        self.validate_game()
    
        
        
    def check_merge(self, last_position: Tuple[int]):
        position_set:List[Tuple[int]] = [last_position]
        
        while position_set:
            current = position_set.pop(0)
            merge_value = self.world[current]
            to_merge = self.check_neighbours(current, value=merge_value)
            
            if to_merge:
                for position in to_merge:
                    self.world[position] = 0
                
                position_set.append(current)
                self.world[current] *= 2
                
                self.visited.add(self.world[current])
        
    
    def check_neighbours(self, position: Tuple[int], value:int):
        to_merge = set()
        
        check_positions = [(position[0]-1, position[1]), (position[0]+1, position[1]),(position[0], position[1]-1), (position[0], position[1]+1)]
        
        for p in check_positions:
            if (p[0]<0 or p[0]>=self.height) or (p[1]<0 or p[1]>=self.width):
                continue
            
            if self.world[p] == value:
                to_merge.add(p)
        
        return list(to_merge)
    
    def validate_pos(self,position):
        return self.world[position] == 0
    
    def validate_game(self):
        if len(self.valid_positions) == 0:
            self.end = True
        
        

        

        