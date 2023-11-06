from modules.motor import MotorModule

##tabuleiro:

#     8
#     7
#     6
#     5
#     4
#     3
#     2
#     1
#       w x   a b c d e f g h   y z



class PathModule:
    def __init__(self):
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

        

        leters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'w', 'x', 'y', 'z']

        for x in range(1, 9):
            for y in range(1, 9):
                self.board_positions[leters[x] + str(y)] = (self.BOARD_CORNER_X + 4*self.HALF_SQUARE + self.CEMITERY_GAP + 2*self.HALF_SQUARE*x,
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
        
            
