table = ["a", "b", "c", "d","e","f", "g", "h"]

def detect_movement(m1, m2):
    moves_from = []
    moves_to = []
    for i in range(8):
        for j in range(8):
            if m1[i][j] != 0 and m2[i][j] == 0:
                moves_from.append(f"{table[j]}{8-i}")
            if m1[i][j] != m2[i][j] and m2[i][j] != 0:
                moves_to.append(f"{table[j]}{8-i}")

    size_mf = len(moves_from)
    size_mt = len(moves_to)          

    # INVALID  
    if size_mf < 1 or size_mt < 1:
        return ""
    
    # Standard movement
    if size_mf == 1 and size_mt == 1:
        return moves_from[0] + moves_to[0]

    # white castling movements
    w_left_castle_from = set(["a1", "g1"])
    w_left_castle_to = set(["d1", "c1"])
    w_right_castle_from = set(["e1", "h1"])
    w_right_castle_to = set(["g1", "f1"])

    # black castling movements
    b_left_castle_from = set(["a8", "g8"])
    b_left_castle_to = set(["d8", "c8"])
    b_right_castle_from = set(["e8", "h8"])
    b_right_castle_to = set(["g8", "f8"])

    # Castle
    if size_mf == 2 and size_mt == 2:

        # white left castling
        if set(moves_from) == w_left_castle_from and set(moves_to) == w_left_castle_to: 
            return  "e1c1"
        # white right castling
        if set(moves_from) == w_right_castle_from and set(moves_to) == w_right_castle_to: 
            return  "e1g1"
        
        # black left castling
        if set(moves_from) == b_left_castle_from and set(moves_to) == b_left_castle_to: 
            return  "e8c8"
        # black right castling
        if set(moves_from) == b_right_castle_from and set(moves_to) == b_right_castle_to: 
            return  "e8g8"

def get_square_number(square: str):
    row = int(square[1]) - 1;
    column = table.index(square[0]);
    return row * 8 + column

