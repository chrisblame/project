import pygame
import sys

pygame.init()
pygame.display.set_caption('Крестики-нолики')
cross_image = pygame.image.load('крестик.png')
circle_image = pygame.image.load('нолик.png')
cross_image = pygame.transform.scale(cross_image, (80, 80))
circle_image = pygame.transform.scale(circle_image, (80, 80))
screen = pygame.display.set_mode((300, 300))
board = [[' ' for i in range(3)] for j in range(3)]
current_player = 'X'
game_over = False
winner = None
winning_line = None


def draw_board():
    screen.fill('white')
    for x in range(1, 3):
        pygame.draw.line(screen, ('black'), (x * 100, 0), (x * 100, 300), 5)
        pygame.draw.line(screen, ('black'), (0, x * 100), (300, x * 100), 5)
    for row in range(3):
        for col in range(3):
            if board[row][col] == 'X':
                screen.blit(cross_image, (col * 100 + 10, row * 100 + 10))
            elif board[row][col] == 'O':
                screen.blit(circle_image, (col * 100 + 10, row * 100 + 10))
    if winning_line and winner is not None:
        draw_winning_line(winning_line)
    pygame.display.flip()


def draw_winning_line(winning_combination):
    start_pos, end_pos = winning_combination
    if start_pos[1] > end_pos[1]:
        start_x = 300
        start_y = 0
        end_x = 0
        end_y = 300
    else:
        start_x = start_pos[1] * 100
        start_y = start_pos[0] * 100
        end_x = (end_pos[1] + 1) * 100
        end_y = (end_pos[0] + 1) * 100
        if start_pos[0] == end_pos[0]:
            start_y += 100 // 2
            end_y = start_y
        elif start_pos[1] == end_pos[1]:
            start_x += 100 // 2
            end_x = start_x
    pygame.draw.line(screen, ('red'), (start_x, start_y), (end_x, end_y), 10)


def get_clicked_cell(mouse_position):
    x, y = mouse_position
    row = y // 100
    col = x // 100
    return row, col


def check_draw():
    for row in board:
        if ' ' in row:
            return False
    return True


def check_winner():
    global winner
    for row in range(3):
        if (board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None):
            winner = board[row][0]
            return True
    for col in range(3):
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


pygame.font.init()
font = pygame.font.Font(None, 36)


def show_winner(winner):
    if winner:
        winner_text = f'Выиграл игрок {winner}'
    else:
        winner_text = 'Ничья'
    text = font.render(winner_text, True, ('white'))
    text_rect = text.get_rect(center=(150, 150))
    background_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 10,
                                  text_rect.width + 20, text_rect.height + 20)
    pygame.draw.rect(screen, ('blue'), background_rect)
    screen.blit(text, text_rect)
    pygame.display.flip()


draw_board()
timer_set = False
while True:
    for event in pygame.event.get():
        handle_event(event)
    if game_over and not timer_set:
        show_winner(winner)
        pygame.time.set_timer(pygame.USEREVENT, 2000)
        timer_set = True
