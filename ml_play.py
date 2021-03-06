"""The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop():
    """The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.

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

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information
        ball_x = scene_info.ball[0]
        ball_y = scene_info.ball[1]
        platform_C = scene_info.platform[0]+20
        #i = (platform_L - (ball_x - 14)) - ((ball_x + 14) - platform_R)
        if ball_y <= 288:
            if platform_C > 100:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            if platform_C < 100:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
        else:
            if ball_x -112 <0:
                i = -(ball_x - 112)
            elif ball_x+112 >200:
                i = 400-(ball_x + 112)
            elif ball_x < ball_ex:
                i = ball_x -112
            else:
                i = ball_x +112
            while ball_y <= 390:
                platform_L = scene_info.platform[0]
                platform_R = scene_info.platform[0]+40
                if platform_L > i:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                if platform_R < i:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                ball_y = scene_info.ball[1]
                break
        ball_ex = ball_x
        
        
