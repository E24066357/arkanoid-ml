"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False
    finalx=100
    nowbally=0
    lastframey=0
    velocity=0
    x=0
    y=0
    NEWX=0
    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()

    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()
        

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False
            
            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information

        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)
            ball_served = True
        else:
            
            if scene_info.ball[1]>100 and (lastframey-scene_info.ball[1]<0):#往下掉
                if x==1:
                    velocity=195-scene_info.ball[0]
                    x=0
                    finalx=195-velocity*(395-nowbally)/7
                if scene_info.ball[0]==195 and x==0:
                    nowbally=scene_info.ball[1]
                    finalx=scene_info.ball[0]
                    x=1    
                if y==1:
                    velocity=scene_info.ball[0]-0
                    y=0
                    finalx=0+velocity*(395-nowbally)/7                     
                if scene_info.ball[0]==0 and y==0:
                    nowbally=scene_info.ball[1]
                    finalx=scene_info.ball[0]
                    y=1      
            else:
                x=0
                velocity=0
                y=0
                finalx=100  
            #撞左邊 
            if lastframey-scene_info.ball[1]>0:
                finalx=100
            while (finalx<0 or finalx>195) :
                if finalx>195:
                    finalx = 390-finalx
                elif finalx<0 :
                    finalx = -finalx      
            NEWX= finalx-20   
            if scene_info.platform[0]<NEWX:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)        
            if scene_info.platform[0]>NEWX:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                
               
           
            lastframey= scene_info.ball[1]
                
            
                    

                 
