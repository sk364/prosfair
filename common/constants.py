import json

DEPTH = 4
PIECE_VALUE = json.load(open("common/chess_piece_priority.json"))

OPPOSITE = { "white" : "black" , "black" : "white" }

SIZE = 800
IMAGE_DIR = "./res/basic_chess_pieces/"
BACKGROUND_FILE_PATH = "res/Background/background_chess_set.jpg"

# colors
GRAY = (150, 150, 150)
WHITE = (255, 255, 255)
BLUE = ( 0 , 0 , 150)
