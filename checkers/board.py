import pygame
from .constant import BLACK, WHITE, ROWS, COLS, RED, SQUARE_SIZE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_left = 12
        self.white_left = 12
        self.red_kings = 0
        self.white_kings = 0
        self.create_board()

    def draw_squares(self,win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2 , ROWS, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE , col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1
    
    def get_piece(self, row, col):
        return self.board[row][col]


    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))  
                    elif row > 4:

                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
    
    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1
    
    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        return None

    def get_valid(self, piece):
        moves = dict()
        coords = piece.get_pos()
        color = piece.get_color()
        if piece.get_king():
            direction = 0
        elif color == RED:
            direction = -1
        elif color == WHITE:
            direction = 1
        # if piece.color == RED or piece.king:
        #     moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
        #     moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        # if piece.color == WHITE or piece.king:
        #     moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
        #     moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
        moves.update(self._traverse(coords, color, direction))

        return moves
    
    def transform(self, start_pos, row_col):
        row = start_pos[0] + row_col[0] 
        col = start_pos[1] + row_col[1]
        return row, col

    def is_on_board(self, row, col):
        if row < 0 or row >= ROWS:
            return False
        if col < 0 or col >= COLS:
            return False 
        return True
    
    def in_skipped(self, current, skipped):
        for piece in skipped:
            if current.get_pos() == piece.get_pos():
                return True
        return False
    
    def _traverse(self, coords, color, direction, skipped = []):
        moves = {}
        transformations = []

        if direction <= 0:
            transformations += [(-1,-1),(-1,1)]
        if direction >= 0:
            transformations += [(1,-1),(1,1)]
        
        for transformation in transformations:
            row ,col = self.transform(coords, transformation)
            if not self.is_on_board(row,col):
                continue

            current = self.board[row][col]

            if current == 0:
                if skipped:
                    continue
                else:
                    moves[(row),(col)] = current
                    continue

            elif current.get_color() == color:
                continue

            elif self.in_skipped(current, skipped):
                continue

            row, col = self.transform((row,col),transformation)
            if not self.is_on_board(row,col):
                continue
            
            if self.board[row][col] == 0:
                new_skipped = skipped + [current]
                moves[(row, col)] = new_skipped
                if row == ROWS - 1 or row == 0:
                    new_direction = 0
                else:
                    new_direction = direction
                moves.update(self._traverse((row ,col), color, new_direction, new_skipped))
        return moves
    
    # def _traverse_left(self, start, stop, step, color, left, skipped=[]):
    #     moves = {}
    #     last = []
    #     for r in range(start, stop, step):
    #         if left < 0:
    #             break

    #         current = self.board[r][left]
    #         if current == 0:
    #             if skipped and not last:
    #                 break
    #             elif skipped:
    #                 moves[(r, left)] = last + skipped
    #             else:
    #                 moves[(r, left)] = last
                
    #             if last:
    #                 if step == -1:
    #                     row = max(r-3, 0)
    #                 else:
    #                     row = min(r+3, ROWS)
    #                 moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
    #                 moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
    #             break
    #         elif current.color == color:
    #             break
    #         else:
    #             last = [current]

    #         left -= 1
        
    #     return moves


    # def _traverse_right(self, start, stop, step, color, right, skipped=[]):
    #     moves = {}
    #     last = []
    #     for r in range(start,stop,step):
    #         if right >= COLS:
    #             break
                
    #         current = self.board[r][right]
    #         if current == 0 :
    #             if skipped and not last:
    #                 break
    #             elif skipped:
    #                 moves[(r,right)] = last + skipped
    #             else:
    #                 moves[(r,right)] = last
                
    #             if last:
    #                 if step == -1:
    #                     row = max(r-3, 0)
    #                 else:
    #                     row = min(r + 3, ROWS)
    #                 moves.update(self._traverse_left(r+step, row, step, color, right - 1, skipped = last))
    #                 moves.update(self._traverse_right(r+step, row, step, color, right + 1, skipped = last))
    #             break
    #         elif current.color == color:
    #             break
    #         else:
    #             last = [current]
    #         right += 1

    #     return moves
