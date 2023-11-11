import chess

# Create a chess board with a specific FEN position
fen_position = "4k3/8/3P4/8/8/8/8/4K3 w - - 0 1"
board = chess.Board(fen_position)

# Print the initial board
print("Initial Position:"[-1])
print(board)
# niisan = board.san(chess.Move(chess.parse_square("b1"),chess.parse_square("a1"),2))
# print(niisan)
# Make a move to promote the pawn to a knight
print([str(x) for x in list(board.legal_moves)])
# board.push_san("a7a8n")

# # Print the final position
# print("\nFinal Position:")
# print(board)
# print("FEN:", board.fen())
