import pygame
import sys

pygame.init()
CELL_SIZE = 100
CELL_COUNT = 3
WIDTH = CELL_SIZE * CELL_COUNT
HEIGHT = CELL_SIZE * CELL_COUNT
LINE_WIDTH = 5
WIN_LINE_WIDTH = 10
RED = (255, 0, 0)
BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
cross_image = pygame.image.load('крестик.png')
circle_image = pygame.image.load('нолик.png')
cross_image = pygame.transform.scale(cross_image, (CELL_SIZE - 20, CELL_SIZE - 20))
circle_image = pygame.transform.scale(circle_image, (CELL_SIZE - 20, CELL_SIZE - 20))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Крестики-нолики')
board = [[' ' for _ in range(CELL_COUNT)] for _ in range(CELL_COUNT)]
current_player = 'X'
game_over = False
winner = None
winning_line = None


def draw_board():
    screen.fill(BG_COLOR)
    for x in range(1, CELL_COUNT):
        pygame.draw.line(screen, LINE_COLOR, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, x * CELL_SIZE), (WIDTH, x * CELL_SIZE), LINE_WIDTH)
    for row in range(CELL_COUNT):
        for col in range(CELL_COUNT):
            if board[row][col] == 'X':
                screen.blit(cross_image, (col * CELL_SIZE + 10, row * CELL_SIZE + 10))
            elif board[row][col] == 'O':
                screen.blit(circle_image, (col * CELL_SIZE + 10, row * CELL_SIZE + 10))
    if winning_line and winner is not None:
        draw_winning_line(winning_line)
    pygame.display.flip()


def draw_winning_line(winning_combination):
    start_pos, end_pos = winning_combination
    if start_pos[1] > end_pos[1]:
        start_x = WIDTH
        start_y = 0
        end_x = 0
        end_y = HEIGHT
    else:
        start_x = start_pos[1] * CELL_SIZE
        start_y = start_pos[0] * CELL_SIZE
        end_x = (end_pos[1] + 1) * CELL_SIZE
        end_y = (end_pos[0] + 1) * CELL_SIZE
        if start_pos[0] == end_pos[0]:
            start_y += CELL_SIZE // 2
            end_y = start_y
        elif start_pos[1] == end_pos[1]:
            start_x += CELL_SIZE // 2
            end_x = start_x
    pygame.draw.line(screen, RED, (start_x, start_y), (end_x, end_y), WIN_LINE_WIDTH)


def get_clicked_cell(mouse_position):
    x, y = mouse_position
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return row, col


def check_draw():
    for row in board:
        if ' ' in row:
            return False
    return True


def check_winner():
    global winner
    for row in range(CELL_COUNT):
        if (board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None):
            winner = board[row][0]
            return True
    for col in range(CELL_COUNT):
        if (board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None):
            winner = board[0][col]
            return True
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        winner = board[0][0]
        return True
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        winner = board[0][0]
        return True
    return False


def get_winning_line(row, col):
    if board[row][0] == board[row][1] == board[row][2] != ' ':
        return (row, 0), (row, 2)
    if board[0][col] == board[1][col] == board[2][col] != ' ':
        return (0, col), (2, col)
    if row == col and board[0][0] == board[1][1] == board[2][2] != ' ':
        return (0, 0), (2, 2)
    if row + col == 2 and board[0][2] == board[1][1] == board[2][0] != ' ':
        return (0, 2), (2, 0)
    return None


def handle_event(event):
    global current_player, game_over, winner, winning_line
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
        mouse_position = pygame.mouse.get_pos()
        row, col = get_clicked_cell(mouse_position)
        if board[row][col] == ' ':
            board[row][col] = current_player
            winning_line = get_winning_line(row, col)
            if winning_line:
                winner = current_player
                game_over = True
            elif check_draw():
                game_over = True
            else:
                current_player = 'O' if current_player == 'X' else 'X'
            draw_board()
    elif event.type == pygame.USEREVENT:
        pygame.quit()
        sys.exit()


draw_board()
timer_set = False
while True:
    for event in pygame.event.get():
        handle_event(event)
    if game_over and not timer_set:
        pygame.time.set_timer(pygame.USEREVENT, 2000)
        timer_set = True
