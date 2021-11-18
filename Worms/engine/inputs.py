# Class Input
#       - Correspond aux Inputs du joueur


class Input:
    def __init__(self):
        # Arrow keys
        self.left = False
        self.right = False
        self.up = False
        self.down = False

        # Zoom (a / e)
        self.zoom_in = False
        self.zoom_out = False 
