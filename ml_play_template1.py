"""
The template of the script for the machine learning process in game pingpong
"""

class MLPlay:
    def __init__(self, side):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.ball_served = False
        self.side = side
        

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            return "SERVE_TO_LEFT"
        else:
            return "MOVE_LEFT"
            
       
        if '1P'==self.side:
            if scene_info["ball_speed"][1] > 0 : # 球正在向下 # ball goes down
                x = ( scene_info["platform_1P"][1]-scene_info["ball"][1] ) // scene_info["ball_speed"][1] # 幾個frame以後會需要接  # x means how many frames before catch the ball
                pred = scene_info["ball"][0]+(scene_info["ball_speed"][0]*x)  # 預測最終位置 # pred means predict ball landing site 
                bound = pred // 200 # Determine if it is beyond the boundary
                #print("1P predict " +str(pred))
                #print("1P bound " +str(bound))
                if (bound > 0): # pred > 200 # fix landing position
                    if (bound%2 == 0) : 
                        pred = pred - bound*200                    
                    else :
                        pred = 200 - (pred - 200*bound)
                elif (bound < 0) : # pred < 0
                    if (bound%2 ==1) :
                        pred = abs(pred - (bound+1) *200)
                    else :
                        pred = pred + (abs(bound)*200)
                #print("result " + str(pred))
                return self.move_to(player = '1P',pred = pred)
            else : # 球正在向上 # ball goes up
                return self.move_to(player = '1P',pred = 100)
        
        elif '2P'==self.side:
            if scene_info["ball_speed"][1] > 0 : 
                return move_to(player = '2P',pred = 100)
            else : 
                x = ( scene_info["platform_2P"][1]+30-scene_info["ball"][1] ) // scene_info["ball_speed"][1] 
                pred = scene_info["ball"][0]+(scene_info["ball_speed"][0]*x) 
                bound = pred // 200 
                if (bound > 0):
                    if (bound%2 == 0):
                        pred = pred - bound*200 
                    else :
                        pred = 200 - (pred - 200*bound)
                elif (bound < 0) :
                    if bound%2 ==1:
                        pred = abs(pred - (bound+1) *200)
                    else :
                        pred = pred + (abs(bound)*200)
                return self.move_to(player = '2P',pred = pred)        

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
    def move_to(self, player, pred) : #move platform to predicted position to catch ball 
        if player == '1P':
            if scene_info["platform_1P"][0]+20  > (pred-10) and scene_info["platform_1P"][0]+20 < (pred+10): return 0 # NONE
            elif scene_info["platform_1P"][0]+20 <= (pred-10) : return 1 # goes right
            else : return 2 # goes left
        else :
            if scene_info["platform_2P"][0]+20  > (pred-10) and scene_info["platform_2P"][0]+20 < (pred+10): return 0 # NONE
            elif scene_info["platform_2P"][0]+20 <= (pred-10) : return 1 # goes right
            else : return 2 # goes left    
