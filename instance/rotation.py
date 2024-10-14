from utils import Vec2

class RotationSystem():
    def __init__(self, type):
        """
        Rotation system for the game, kick tables for each piece type and rotation type
        
        args:
            type (str): The type of rotation system to use
        """
        self.type = type
        
        if self.type == 'SRS': # Super Rotation System (Guideline)
            
            # ------------------------------------------------------- 90 DEGREE KICKS -------------------------------------------------------
            self.T_KICKS = {
                '0->1': [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, +1), Vec2(0, -2), Vec2(-1, -2)],
                '1->0': [Vec2(0, 0), Vec2(+1, 0), Vec2(+1, -1), Vec2(0, +2), Vec2(+1, +2)],
                
                '1->2': [Vec2(0, 0), Vec2(+1, 0), Vec2(+1, -1), Vec2(0, +2), Vec2(+1, +2)],
                '2->1': [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, +1), Vec2(0, -2), Vec2(-1, -2)],
                
                '2->3': [Vec2(0, 0), Vec2(+1, 0), Vec2(+1, +1), Vec2(0, -2), Vec2(+1, -2)],
                '3->2': [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, -1), Vec2(0, +2), Vec2(-1, +2)],
                
                '3->0': [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, -1), Vec2(0, +2), Vec2(-1, +2)],
                '0->3': [Vec2(0, 0), Vec2(+1, 0), Vec2(+1, +1), Vec2(0, -2), Vec2(+1, -2)],
            }
            
            self.S_KICKS = {
                '0->1': [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, +1), Vec2(0, -2), Vec2(-1, -2)],
                '1->0': [Vec2(0, 0), Vec2(+1, 0), Vec2(+1, -1), Vec2(0, +2), Vec2(+1, +2)],
                
                '1->2': [Vec2(0, 0), Vec2(+1, 0), Vec2(+1, -1), Vec2(0, +2), Vec2(+1, +2)],
                '2->1': [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, +1), Vec2(0, -2), Vec2(-1, -2)],
                
                '2->3': [Vec2(0, 0), Vec2(+1, 0), Vec2(+1, +1), Vec2(0, -2), Vec2(+1, -2)],
                '3->2': [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, -1), Vec2(0, +2), Vec2(-1, +2)],
                
                '3->0': [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, -1), Vec2(0, +2), Vec2(-1, +2)],
                '0->3': [Vec2(0, 0), Vec2(+1, 0), Vec2(+1, +1), Vec2(0, -2), Vec2(+1, -2)],
            }
            
            self.Z_KICKS = {
                '0->1': [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, +1), Vec2(0, -2), Vec2(-1, -2)],
                '1->0': [Vec2(0, 0), Vec2(+1, 0), Vec2(+1, -1), Vec2(0, +2), Vec2(+1, +2)],
                
                '1->2': [Vec2(0, 0), Vec2(+1, 0), Vec2(+1, -1), Vec2(0, +2), Vec2(+1, +2)],
                '2->1': [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, +1), Vec2(0, -2), Vec2(-1, -2)],
                
                '2->3': [Vec2(0, 0), Vec2(+1, 0), Vec2(+1, +1), Vec2(0, -2), Vec2(+1, -2)],
                '3->2': [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, -1), Vec2(0, +2), Vec2(-1, +2)],
                
                '3->0': [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, -1), Vec2(0, +2), Vec2(-1, +2)],
                '0->3': [Vec2(0, 0), Vec2(+1, 0), Vec2(+1, +1), Vec2(0, -2), Vec2(+1, -2)],
            }
            
            self.L_KICKS = {
                '0->1': [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, +1), Vec2(0, -2), Vec2(-1, -2)],
                '1->0': [Vec2(0, 0), Vec2(+1, 0), Vec2(+1, -1), Vec2(0, +2), Vec2(+1, +2)],
                
                '1->2': [Vec2(0, 0), Vec2(+1, 0), Vec2(+1, -1), Vec2(0, +2), Vec2(+1, +2)],
                '2->1': [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, +1), Vec2(0, -2), Vec2(-1, -2)],
                
                '2->3': [Vec2(0, 0), Vec2(+1, 0), Vec2(+1, +1), Vec2(0, -2), Vec2(+1, -2)],
                '3->2': [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, -1), Vec2(0, +2), Vec2(-1, +2)],
                
                '3->0': [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, -1), Vec2(0, +2), Vec2(-1, +2)],
                '0->3': [Vec2(0, 0), Vec2(+1, 0), Vec2(+1, +1), Vec2(0, -2), Vec2(+1, -2)],
            }
            
            self.J_KICKS = {
                '0->1': [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, +1), Vec2(0, -2), Vec2(-1, -2)],
                '1->0': [Vec2(0, 0), Vec2(+1, 0), Vec2(+1, -1), Vec2(0, +2), Vec2(+1, +2)],
                
                '1->2': [Vec2(0, 0), Vec2(+1, 0), Vec2(+1, -1), Vec2(0, +2), Vec2(+1, +2)],
                '2->1': [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, +1), Vec2(0, -2), Vec2(-1, -2)],
                
                '2->3': [Vec2(0, 0), Vec2(+1, 0), Vec2(+1, +1), Vec2(0, -2), Vec2(+1, -2)],
                '3->2': [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, -1), Vec2(0, +2), Vec2(-1, +2)],
                
                '3->0': [Vec2(0, 0), Vec2(-1, 0), Vec2(-1, -1), Vec2(0, +2), Vec2(-1, +2)],
                '0->3': [Vec2(0, 0), Vec2(+1, 0), Vec2(+1, +1), Vec2(0, -2), Vec2(+1, -2)],
            }
                
            self.I_KICKS = {     
                '0->1': [Vec2(0, 0), Vec2(-2, 0), Vec2(+1, 0), Vec2(-2, -1), Vec2(+1, +2)],
                '1->0': [Vec2(0, 0), Vec2(+2, 0), Vec2(-1, 0), Vec2(+2, +1), Vec2(-1, -2)],
                
                '1->2': [Vec2(0, 0), Vec2(-1, 0), Vec2(+2, 0), Vec2(-1, +2), Vec2(+2, -1)],
                '2->1': [Vec2(0, 0), Vec2(+1, 0), Vec2(-2, 0), Vec2(+1, -2), Vec2(-2, +1)],
                
                '2->3': [Vec2(0, 0), Vec2(+2, 0), Vec2(-1, 0), Vec2(+2, +1), Vec2(-1, -2)],
                '3->2': [Vec2(0, 0), Vec2(-2, 0), Vec2(+1, 0), Vec2(-2, -1), Vec2(+1, +2)],
                
                '3->0': [Vec2(0, 0), Vec2(+1, 0), Vec2(-2, 0), Vec2(+1, -2), Vec2(-2, +1)],
                '0->3': [Vec2(0, 0), Vec2(-1, 0), Vec2(+2, 0), Vec2(-1, +2), Vec2(+2, -1)],
            }
            
            self.O_KICKS = {
                '0->1': [Vec2(0, 0)],
                '1->0': [Vec2(0, 0)],
        
                '1->2': [Vec2(0, 0)],
                '2->1': [Vec2(0, 0)],
        
                '2->3': [Vec2(0, 0)],
                '3->2': [Vec2(0, 0)],
        
                '3->0': [Vec2(0, 0)],
                '0->3': [Vec2(0, 0)],
            }
            
            # ------------------------------------------------------- 180 DEGREE KICKS -------------------------------------------------------
            self.T_180_KICKS = {
                '0->2': [Vec2(0, 0), Vec2(+1, 0), Vec2(+2, 0), Vec2(+1, +1), Vec2(+2, +1), Vec2(-1, 0), Vec2(-2, 0), Vec2(-1, +1), Vec2(-2, +1), Vec2(0, -1), Vec2(+3, 0), Vec2(-3, 0)],
                '2->0': [Vec2(0, 0), Vec2(-1, 0), Vec2(-2, 0), Vec2(-1, -1), Vec2(-2, -1), Vec2(+1, 0), Vec2(+2, 0), Vec2(+1, -1), Vec2(+2, -1), Vec2(0, +1), Vec2(-3, 0), Vec2(+3, 0)], 
                
                '1->3': [Vec2(0, 0), Vec2(0, +1), Vec2(0, +2), Vec2(-1, +1), Vec2(-1, +2), Vec2(0, -1), Vec2(0, -2), Vec2(-1, -1), Vec2(-1, -2), Vec2(+1, 0), Vec2(0, +3), Vec2(0, -3)],
                '3->1': [Vec2(0, 0), Vec2(0, +1), Vec2(0, +2), Vec2(+1, +1), Vec2(+1, +2), Vec2(0, -1), Vec2(0, -2), Vec2(+1, -1), Vec2(+1, -2), Vec2(-1, 0), Vec2(0, +3), Vec2(0, -3)],
            }
            
            self.S_180_KICKS = {
                '0->2': [Vec2(0, 0), Vec2(+1, 0), Vec2(+2, 0), Vec2(+1, +1), Vec2(+2, +1), Vec2(-1, 0), Vec2(-2, 0), Vec2(-1, +1), Vec2(-2, +1), Vec2(0, -1), Vec2(+3, 0), Vec2(-3, 0)],
                '2->0': [Vec2(0, 0), Vec2(-1, 0), Vec2(-2, 0), Vec2(-1, -1), Vec2(-2, -1), Vec2(+1, 0), Vec2(+2, 0), Vec2(+1, -1), Vec2(+2, -1), Vec2(0, +1), Vec2(-3, 0), Vec2(+3, 0)], 
                
                '1->3': [Vec2(0, 0), Vec2(0, +1), Vec2(0, +2), Vec2(-1, +1), Vec2(-1, +2), Vec2(0, -1), Vec2(0, -2), Vec2(-1, -1), Vec2(-1, -2), Vec2(+1, 0), Vec2(0, +3), Vec2(0, -3)],
                '3->1': [Vec2(0, 0), Vec2(0, +1), Vec2(0, +2), Vec2(+1, +1), Vec2(+1, +2), Vec2(0, -1), Vec2(0, -2), Vec2(+1, -1), Vec2(+1, -2), Vec2(-1, 0), Vec2(0, +3), Vec2(0, -3)],
            }
                
            self.Z_180_KICKS = {
                '0->2': [Vec2(0, 0), Vec2(+1, 0), Vec2(+2, 0), Vec2(+1, +1), Vec2(+2, +1), Vec2(-1, 0), Vec2(-2, 0), Vec2(-1, +1), Vec2(-2, +1), Vec2(0, -1), Vec2(+3, 0), Vec2(-3, 0)],
                '2->0': [Vec2(0, 0), Vec2(-1, 0), Vec2(-2, 0), Vec2(-1, -1), Vec2(-2, -1), Vec2(+1, 0), Vec2(+2, 0), Vec2(+1, -1), Vec2(+2, -1), Vec2(0, +1), Vec2(-3, 0), Vec2(+3, 0)], 
                
                '1->3': [Vec2(0, 0), Vec2(0, +1), Vec2(0, +2), Vec2(-1, +1), Vec2(-1, +2), Vec2(0, -1), Vec2(0, -2), Vec2(-1, -1), Vec2(-1, -2), Vec2(+1, 0), Vec2(0, +3), Vec2(0, -3)],
                '3->1': [Vec2(0, 0), Vec2(0, +1), Vec2(0, +2), Vec2(+1, +1), Vec2(+1, +2), Vec2(0, -1), Vec2(0, -2), Vec2(+1, -1), Vec2(+1, -2), Vec2(-1, 0), Vec2(0, +3), Vec2(0, -3)],
            }
            
            self.L_180_KICKS = {
                '0->2': [Vec2(0, 0), Vec2(+1, 0), Vec2(+2, 0), Vec2(+1, +1), Vec2(+2, +1), Vec2(-1, 0), Vec2(-2, 0), Vec2(-1, +1), Vec2(-2, +1), Vec2(0, -1), Vec2(+3, 0), Vec2(-3, 0)],
                '2->0': [Vec2(0, 0), Vec2(-1, 0), Vec2(-2, 0), Vec2(-1, -1), Vec2(-2, -1), Vec2(+1, 0), Vec2(+2, 0), Vec2(+1, -1), Vec2(+2, -1), Vec2(0, +1), Vec2(-3, 0), Vec2(+3, 0)], 
                
                '1->3': [Vec2(0, 0), Vec2(0, +1), Vec2(0, +2), Vec2(-1, +1), Vec2(-1, +2), Vec2(0, -1), Vec2(0, -2), Vec2(-1, -1), Vec2(-1, -2), Vec2(+1, 0), Vec2(0, +3), Vec2(0, -3)],
                '3->1': [Vec2(0, 0), Vec2(0, +1), Vec2(0, +2), Vec2(+1, +1), Vec2(+1, +2), Vec2(0, -1), Vec2(0, -2), Vec2(+1, -1), Vec2(+1, -2), Vec2(-1, 0), Vec2(0, +3), Vec2(0, -3)],
            }
            self.J_180_KICKS = {
                '0->2': [Vec2(0, 0), Vec2(+1, 0), Vec2(+2, 0), Vec2(+1, +1), Vec2(+2, +1), Vec2(-1, 0), Vec2(-2, 0), Vec2(-1, +1), Vec2(-2, +1), Vec2(0, -1), Vec2(+3, 0), Vec2(-3, 0)],
                '2->0': [Vec2(0, 0), Vec2(-1, 0), Vec2(-2, 0), Vec2(-1, -1), Vec2(-2, -1), Vec2(+1, 0), Vec2(+2, 0), Vec2(+1, -1), Vec2(+2, -1), Vec2(0, +1), Vec2(-3, 0), Vec2(+3, 0)], 
                
                '1->3': [Vec2(0, 0), Vec2(0, +1), Vec2(0, +2), Vec2(-1, +1), Vec2(-1, +2), Vec2(0, -1), Vec2(0, -2), Vec2(-1, -1), Vec2(-1, -2), Vec2(+1, 0), Vec2(0, +3), Vec2(0, -3)],
                '3->1': [Vec2(0, 0), Vec2(0, +1), Vec2(0, +2), Vec2(+1, +1), Vec2(+1, +2), Vec2(0, -1), Vec2(0, -2), Vec2(+1, -1), Vec2(+1, -2), Vec2(-1, 0), Vec2(0, +3), Vec2(0, -3)],
            }
             
            self.I_180_KICKS = {
                '0->2': [Vec2(0, 0), Vec2(-1, 0), Vec2(-2, 0), Vec2(+1, 0), Vec2(+2, 0), Vec2(0, +1)],
                '2->0': [Vec2(0, 0), Vec2(+1, 0), Vec2(+2, 0), Vec2(-1, 0), Vec2(-2, 0), Vec2(0, -1)],
                
                '1->3': [Vec2(0, 0), Vec2(0, +1), Vec2(0, +2), Vec2(0, -1), Vec2(0, -2), Vec2(-1, 0)],
                '3->1': [Vec2(0, 0), Vec2(0, +1), Vec2(0, +2), Vec2(0, -1), Vec2(0, -2), Vec2(+1, 0)],
            }
            
            self.O_180_KICKS = {
                '0->2': [Vec2(0, 0)],
                '2->0': [Vec2(0, 0)],
            
                '1->3': [Vec2(0, 0)],
                '3->1': [Vec2(0, 0)],
            }

            # ------------------------------------------------------- KICK TABLE -------------------------------------------------------
            self.kick_table = {
                '90': {'T_KICKS': self.T_KICKS, 'S_KICKS': self.S_KICKS, 'Z_KICKS': self.Z_KICKS, 'L_KICKS': self.L_KICKS, 'J_KICKS': self.J_KICKS, 'I_KICKS': self.I_KICKS, 'O_KICKS': self.O_KICKS},
                '180': {'T_KICKS': self.T_180_KICKS, 'S_KICKS': self.S_180_KICKS, 'Z_KICKS': self.Z_180_KICKS, 'L_KICKS': self.L_180_KICKS, 'J_KICKS': self.J_180_KICKS, 'I_KICKS': self.I_180_KICKS, 'O_KICKS': self.O_180_KICKS}
            }
            
    