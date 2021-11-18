# Class Input
#       - Correspond aux Inputs du joueur


class Input:
    def __init__(self):
        # ZQSD
        self.camera_left = False
        self.camera_right = False
        self.camera_up = False
        self.camera_down = False

        # Zoom (A / E)
        self.camera_zoom_in = False
        self.camera_zoom_out = False 

        # Arrow
        self.player_move_left = False
        self.player_move_right = False
        self.player_move_up = False
        self.player_move_down = False
