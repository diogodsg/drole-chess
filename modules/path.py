from modules.motor import MotorModule

##tabuleiro se WHITE:

#     8
#     7
#     6
#     5
#     4
#     3
#     2
#     1
#       w x   a b c d e f g h   y z


##tabuleiro se BLACK:

#     8      1                 8
#     7      2                 7
#     6      3                 6
#     5      4                 5
#     4      5                 4
#     3      6                 3
#     2      7                 2
#     1      8                 1
#       w x   h g f e d c b a   y z



class PathModule:
    def __init__(self, player_color):
        self.motors = MotorModule()

        self.BOARD_CORNER_X = 0
        self.BOARD_CORNER_Y = 0 
        self.HALF_SQUARE = 1.5
        self.CEMITERY_GAP = 1

        self.motors.return_home()
        self.current_pos = (36, -3)##(self.BOARD_CORNER_X + 16*self.HALF_SQUARE + self.CEMITERY_GAP + , 0)

        self.board_positions = {}
        self.white_cemitery_positions = {}
        self.black_cemitery_positions = {}

        #types: 1-pawn 2-knight 3-bishop 4-rook 5-queen 6-king
        self.white_cemitery_typemap = [None,
                                        ["w8", "x8", "w7", "x7", "w6", "x6", "w5", "x5",], #pawn
                                        ["w4", "x4"], #knight
                                        ["w3", "x3"], #bishop
                                        ["w2", "x2"], #rook
                                        ["x1"]        #queen
                                    ]
        self.black_cemitery_typemap = [None,
                                        ["y1", "z1", "y2", "z2", "y3", "z3", "y4", "z4",], #pawn
                                        ["y5", "z5"], #knight
                                        ["y6", "z6"], #bishop
                                        ["y7", "z7"], #rook
                                        ["z8"]        #queen
                                    ]

        

        leters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'w', 'x', 'y', 'z']

        if player_color == "WHITE":
            for x in range(0, 8):
                for y in range(1, 9):
                    self.board_positions[leters[x] + str(y)] = (self.BOARD_CORNER_X + 4*self.HALF_SQUARE + self.CEMITERY_GAP + 2*self.HALF_SQUARE*x,
                                                                self.BOARD_CORNER_Y + 2*self.HALF_SQUARE*(y-1))
        else:
            for x in range(1, 9):
                for y in range(1, 9):
                    self.board_positions[leters[7-x] + str(9-y)] = (self.BOARD_CORNER_X + 4*self.HALF_SQUARE + self.CEMITERY_GAP + 2*self.HALF_SQUARE*x,
                                                                self.BOARD_CORNER_Y + 2*self.HALF_SQUARE*(y-1))

        
        for x in range(0, 2):
            for y in range (0, 8):
                self.white_cemitery_positions[leters[8+x] + str(y+1)] = (self.BOARD_CORNER_X + 2*self.HALF_SQUARE*x, self.BOARD_CORNER_Y + 2*self.HALF_SQUARE*x)
                self.black_cemitery_positions[leters[10+x] + str(y+1)] = ()


        

    def calculate_path(self, destination):

        path = []
        
        if self.current_pos == self.board_positions[destination]:
            return path

        #move piece to the bottom left corner of origin square
        path.append((-self.HALF_SQUARE, 0))
        path.append((0, -self.HALF_SQUARE))

        #move piece to the bottom left corner of destination square
        path.append((self.board_positions[destination][0]-self.current_pos[0], 0)) # x axis
        path.append((0, self.board_positions[destination][1]-self.current_pos[1])) # y axis

        #move piece to the center of the destination square
        path.append((self.HALF_SQUARE, 0))
        path.append((0, self.HALF_SQUARE))

        self.current_pos = self.board_positions[destination]

        return path

    def calculate_path_no_offset(self, destination):

        path = []

        if self.current_pos == self.board_positions[destination]:
            return path

        #move piece to the bottom left corner of origin square
        #path.append((-self.HALF_SQUARE, 0))
        #path.append((0, -self.HALF_SQUARE))
        print(f"pos of {destination} is {self.board_positions[destination]}, current pos is {self.current_pos}")
        #move piece to the bottom left corner of destination square
        path.append((self.board_positions[destination][0]-self.current_pos[0], 0)) # x axis
        path.append((0, self.board_positions[destination][1]-self.current_pos[1])) # y axis

        #move piece to the center of the destination square
        #path.append((self.HALF_SQUARE, 0))
        #path.append((0, self.HALF_SQUARE))

        self.current_pos = self.board_positions[destination]

        return path



    def move_piece(self, movement: str):
        if len(movement) != 4:
            return
        print(f"mov is {movement}")
        path = self.calculate_path_no_offset(movement[:2]) #go to piece
        print("motor path origin")
        print(path)
        self.motors.follow_path(path)
        print("mov org done")
        self.motors.set_magnet(True)
         
        path = self.calculate_path(movement[2:4]) #go to target
        print("motor path dst")
        print(path)
        self.motors.follow_path(path)
        print("mov dst done")
        self.motors.set_magnet(False)

    def move_to_cemitery(self, square, piece_type, color):
        cemitery_pos = ""
        if color: #color is true when white
            cemitery_pos = self.white_cemitery_typemap[piece_type].pop()
        else:
            cemitery_pos = self.black_cemitery_typemap[piece_type].pop()

        if cemitery_pos:
            self.move_piece(square+cemitery_pos)    
