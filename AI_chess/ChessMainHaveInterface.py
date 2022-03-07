"""
Main driver file.
Handling user input.
Displaying current GameStatus object.
"""
from os import truncate
import pygame as p
from pygame.image import load
import ChessEngine, ChessAI
import sys
from multiprocessing import Process, Queue

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    """
    Initialize a global directory of images.
    This will be called exactly once in the main.
    """
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


def main():
    """
    The main driver for our code.
    This will handle user input and updating the graphics.
    """
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("black"))
    game_state = ChessEngine.GameState()
    valid_moves = game_state.getValidMoves()
    move_made = False  # flag variable for when a move is made
    animate = False  # flag variable for when we should animate a move
    loadImages()  # do this only once before while loop
    running = True
    square_selected = ()  # no square is selected initially, this will keep track of the last click of the user (tuple(row,col))
    player_clicks = []  # this will keep track of player clicks (two tuples)
    game_over = False
    ai_thinking = False
    move_undone = False
    move_finder_process = None
    move_log_font = p.font.SysFont("Arial", 14, False, False)
    player_one = True # if a human is playing white, then this will be True, else False
    player_two = False  # if a human is playing black, then this will be True, else False
    gd1 = p.transform.scale(p.image.load("images/gd1.png"), (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    gd2 = p.transform.scale(p.image.load("images/gd2.png"), (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    gd3 = p.transform.scale(p.image.load("images/gd3.png"), (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    global yn, qt, resume
    yn = p.transform.scale(p.image.load("images/yn.png"), (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    qt = p.transform.scale(p.image.load("images/log.png"), (MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    resume = p.transform.scale(p.image.load("images/resume.png"), (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    help = p.transform.scale(p.image.load("images/help.png"), (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    aboutUs = p.transform.scale(p.image.load("images/aboutUs.png"), (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    draw = p.transform.scale(p.image.load("images/draw.png"), (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    bw = p.transform.scale(p.image.load("images/bw.png"), (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    ww = p.transform.scale(p.image.load("images/ww.png"), (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    difficult = 0
    
    play = 1
    tmpPlay = 0
    quitFlag = 0
    reFlag = 0
    goFlag = 0

    while running:
        if play == 1:  
            screen.blit(gd1, p.Rect(0, 0, BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))          
            for e in p.event.get():
                if e.type == p.QUIT:
                    play = 13
                    reFlag = 1
                if e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()  # (x, y) location of the mouse
                    if (125 < location[1] < 180):
                        if 120 < location[0] < 360:
                            play = 2
                            player_one = True
                            player_two = False
                        elif 390 < location[0] < 630:
                            play = 3
                            player_one = True
                            player_two = True
                    elif 260 < location[0] < 500 and location[1] > 180:
                        if 220 < location[1] < 280:
                            play = 11
                            #help
                        if 325 < location[1] < 380:
                            play = 12#about us
                        if 415 < location[1] < 470:
                            play = 13
                            reFlag = 1
        if play == 11:
            screen.blit(help, p.Rect(0, 0, BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
            '''
                add help content 
            '''
            for e in p.event.get():
                if e.type == p.QUIT:
                    play = 13
                    reFlag = 11
                if e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()
                    if 730 < location[0] < 740:
                        if 20 < location[1] < 32:
                            play = 1
        if play == 12:
            screen.blit(aboutUs, p.Rect(0, 0, BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
            '''
            add about us content
            '''
            for e in p.event.get():
                if e.type == p.QUIT:
                    play = 13
                    reFlag = 12
                if e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()
                    if 730 < location[0] < 740:
                        if 20 < location[1] < 32:
                            play = 1
        if play == 13:
            screen.blit(yn, p.Rect(0, 0, BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
            for e in p.event.get():
                if e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()
                    if 240 < location[1] < 280:
                        if 195 < location[0] < 365:
                            p.quit()
                            sys.exit()
                        elif 400 < location[0] < 570:
                            play = reFlag  

        if play == 2:
            screen.blit(gd2, p.Rect(0, 0, BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
            for e in p.event.get():
                if e.type == p.QUIT:
                    play = 13
                    reFlag = 2
                if e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()
                    if 260 < location[0] < 500:
                        if 80 < location[1] < 136:
                            difficult = 1
                            play = 3
                        elif 180 < location[1] < 240:
                            difficult = 2
                            play = 3
                        elif 285 < location[1] < 345:
                            difficult = 3
                            play = 3
                        elif 390 < location[1] < 450:
                            play = 1
        if play == 3:
            if e.type == p.QUIT:
                play = 13
                reFlag = 3
            screen.blit(gd3, p.Rect(0, 0, BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
            for e in p.event.get():
                if e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()
                    if 260 < location[0] < 500:
                        if 180 < location[1] < 240:
                            play = 4
                        elif 275 < location[1] < 335:
                            if player_two == False:
                                play = 2
                            else: 
                                play = 1
        
        if play == 41:
            screen.blit(bw, p.Rect(0, 0, BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
        if play == 42:
            screen.blit(ww, p.Rect(0, 0, BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
        if play == 43:
            screen.blit(draw, p.Rect(0, 0, BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))

        if play == 41 or play == 42 or play == 43:
                for e in p.event.get():
                    if e.type == p.QUIT:
                        reFlag = 4
                        play = 13

                    if e.type == p.MOUSEBUTTONDOWN:
                            play = 1
                            tmpPlay = 0
                            quitFlag = 0
                            game_state = ChessEngine.GameState()
                            valid_moves = game_state.getValidMoves()
                            square_selected = ()
                            player_clicks = []
                            move_made = False
                            animate = False
                            game_over = False
                            if ai_thinking: 
                                move_finder_process.terminate()
                                ai_thinking = False
                            move_undone = True
                            break
        if play == 4:
            human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two) 

            screen.blit(qt, p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
            drawMoveLog(screen, game_state, move_log_font)
            if tmpPlay == 1:
                screen.blit(yn, p.Rect(0, 0, BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))

            if tmpPlay == 2:
                screen.blit(resume, p.Rect(0, 0, BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))

            for e in p.event.get():
                if e.type == p.QUIT:
                    tmpPlay = 1
                    quitFlag = 1
                    goFlag = 2
                    
                # mouse handler
                elif e.type == p.MOUSEBUTTONDOWN:
                    if not game_over:
                        location = p.mouse.get_pos() 
                        if 470 < location[1] < 500 and tmpPlay == 0:
                            if 520 < location[0] < 630:
                                tmpPlay = 1
                            elif 645 < location[0] < 755:
                                tmpPlay = 2
                        if quitFlag == 1:
                            if 195 < location[0] < 365:
                                p.quit()
                                sys.exit()
                            elif 400 < location[0] < 570:
                                tmpPlay = 0
                                quitFlag = 0
                        if tmpPlay == 1  and 240 < location[1] < 280 :
                            if 195 < location[0] < 365:
                                play = 1
                                tmpPlay = 0
                                game_state = ChessEngine.GameState()
                                valid_moves = game_state.getValidMoves()
                                square_selected = ()
                                player_clicks = []
                                move_made = False
                                animate = False
                                game_over = False
                                if ai_thinking:
                                    move_finder_process.terminate()
                                    ai_thinking = False
                                move_undone = True

                            elif 400 < location[0] < 570:
                                tmpPlay = 0

                        if tmpPlay == 2:
                            if 260 < location[0] < 505 and 235 < location[1] < 295:
                                tmpPlay = 0

                        if tmpPlay == 0:
                            col = location[0] // SQUARE_SIZE
                            row = location[1] // SQUARE_SIZE
                            if square_selected == (row, col) or col >= 8:  # user clicked the same square twice
                                square_selected = ()  # deselect
                                player_clicks = []  # clear clicks
                            else:
                                square_selected = (row, col)
                                player_clicks.append(square_selected)  # append for both 1st and 2nd click
                            if len(player_clicks) == 2 and human_turn:  # after 2nd click --> check and make move
                                move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                                for i in range(len(valid_moves)):
                                    if move == valid_moves[i]:
                                        game_state.makeMove(valid_moves[i])
                                        move_made = True
                                        animate = True
                                        square_selected = ()  # reset user clicks
                                        player_clicks = []
                                if not move_made:
                                    player_clicks = [square_selected]

                    # key handler
                elif e.type == p.KEYDOWN and tmpPlay == 0:
                    if e.key == p.K_z:  # undo when 'z' is pressed
                        game_state.undoMove()
                        move_made = True
                        animate = False
                        game_over = False
                        if ai_thinking:
                            move_finder_process.terminate()
                            ai_thinking = False
                        move_undone = True
                    if e.key == p.K_r:  # reset the game when 'r' is pressed
                        game_state = ChessEngine.GameState()
                        valid_moves = game_state.getValidMoves()
                        square_selected = ()
                        player_clicks = []
                        move_made = False
                        animate = False
                        game_over = False
                        if ai_thinking:
                            move_finder_process.terminate()
                            ai_thinking = False
                        move_undone = True

            # AI move finder
            if not game_over and not human_turn and not move_undone: # machine turn
                if not ai_thinking:
                    ai_thinking = True
                    return_queue = Queue()  # used to pass data between threads, to print the move
                    # find good move
                    move_finder_process = Process(target=ChessAI.findBestMove, args=(game_state, valid_moves, return_queue, difficult)) 
                    move_finder_process.start()

                if not move_finder_process.is_alive():
                    ai_move = return_queue.get()
                    if ai_move is None:
                        ai_move = ChessAI.findRandomMove(valid_moves)
                    game_state.makeMove(ai_move)
                    move_made = True
                    animate = True
                    ai_thinking = False

            # after each AI move: reset all status
            if move_made:
                if animate:
                    animateMove(game_state.move_log[-1], screen, game_state.board, clock)
                valid_moves = game_state.getValidMoves()
                move_made = False
                animate = False
                move_undone = False

            if tmpPlay == 0:
                drawGameState(screen, game_state, valid_moves, square_selected)

            if not game_over and tmpPlay == 0:
                drawMoveLog(screen, game_state, move_log_font)

            if game_state.checkmate or game_state.stalemate and play < 40:
                game_over = True
                if game_state.white_to_move:
                    play = 41

                else:
                    play = 42

            if game_state.count_move >= game_state.count_limit and play < 40:
                game_over = True
                play = 43
                    
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, game_state, valid_moves, square_selected):
    """
    Responsible for all the graphics within current game state.
    """
    drawBoard(screen)  # draw squares on the board
    highlightSquares(screen, game_state, valid_moves, square_selected)
    drawPieces(screen, game_state.board)  # draw pieces on top of those squares


def drawBoard(screen):
    """
    Draw the squares on the board.
    The top left square is always light.
    """
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def highlightSquares(screen, game_state, valid_moves, square_selected):
    """
    Highlight square selected and moves for piece selected.
    """
    if (len(game_state.move_log)) > 0:
        last_move = game_state.move_log[-1]
        s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(p.Color('green'))
        screen.blit(s, (last_move.end_col * SQUARE_SIZE, last_move.end_row * SQUARE_SIZE))
    if square_selected != ():
        row, col = square_selected
        if game_state.board[row][col][0] == (
                'w' if game_state.white_to_move else 'b'):  # square_selected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)  # transparency value 0 -> transparent, 255 -> opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE))


def drawPieces(screen, board):
    """
    Draw the pieces on the board using the current game_state.board
    """
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawMoveLog(screen, game_state, font):
    """
    Draws the move log.

    """
    move_log_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)

    move_log = game_state.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = str(i // 2 + 1) + '. ' + str(move_log[i]) + " "
        if i + 1 < len(move_log):
            move_string += str(move_log[i + 1]) + "  "
        move_texts.append(move_string)

    moves_per_row = 3
    padding = 5
    line_spacing = 2 # khoảng cách hai dòng
    text_y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]

        text_object = font.render(text, True, p.Color('white'))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing

def animateMove(move, screen, board, clock):
    """
    Animating a move
    """
    global colors
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 10  # frames to move one square
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.piece_captured != '--':
            if move.is_enpassant_move:
                enpassant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = p.Rect(move.end_col * SQUARE_SIZE, enpassant_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            screen.blit(IMAGES[move.piece_captured], end_square)
        # draw moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()