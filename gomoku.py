"""
AWS Gomoku Game - Five in a Row using EC2 and S3 icons
"""
import pygame
import sys
import numpy as np
import os
import traceback

# Initialize pygame
pygame.init()

# Game constants
BOARD_SIZE = 15  # 15x15 board
CELL_SIZE = 40   # Size of each cell in pixels
MARGIN = 50      # Margin around the board
GRID_COLOR = (0, 0, 0)  # Black for the grid lines
BACKGROUND_COLOR = (255, 255, 255)  # White background
LINE_WIDTH = 2

# Calculate window size
WINDOW_WIDTH = BOARD_SIZE * CELL_SIZE + 2 * MARGIN
WINDOW_HEIGHT = BOARD_SIZE * CELL_SIZE + 2 * MARGIN

# Create the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("AWS Gomoku - EC2 vs S3")

# Game state
# 0: empty, 1: EC2 (player 1), 2: S3 (player 2)
board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
current_player = 1  # Start with player 1 (EC2)
game_over = False
winner = None

# Load AWS icons
try:
    # Get the absolute path to the image files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ec2_path = os.path.join(current_dir, 'assets', 'images', 'Res_Amazon-EC2_Instances_48.png')
    s3_path = os.path.join(current_dir, 'assets', 'images', 'Res_Amazon-Simple-Storage-Service_S3-Standard_48.png')
    
    print(f"Loading EC2 icon from: {ec2_path}")
    print(f"Loading S3 icon from: {s3_path}")
    
    # Check if files exist
    if not os.path.exists(ec2_path) or not os.path.exists(s3_path):
        raise FileNotFoundError(f"Icon files not found: EC2 exists: {os.path.exists(ec2_path)}, S3 exists: {os.path.exists(s3_path)}")
    
    # Load official AWS icons
    ec2_original = pygame.image.load(ec2_path)
    s3_original = pygame.image.load(s3_path)
    
    # Scale icons to fit the board cells
    icon_size = int(CELL_SIZE * 0.8)
    ec2_icon = pygame.transform.scale(ec2_original, (icon_size, icon_size))
    s3_icon = pygame.transform.scale(s3_original, (icon_size, icon_size))
    print("Successfully loaded AWS icons")
except Exception as e:
    # Fallback to colored squares if images can't be loaded
    print(f"Warning: Could not load AWS icons: {e}")
    print(traceback.format_exc())
    ec2_icon = pygame.Surface((int(CELL_SIZE * 0.8), int(CELL_SIZE * 0.8)))
    ec2_icon.fill((255, 153, 0))  # EC2 orange
    
    s3_icon = pygame.Surface((int(CELL_SIZE * 0.8), int(CELL_SIZE * 0.8)))
    s3_icon.fill((66, 133, 244))  # S3 blue

def draw_board():
    """Draw the game board"""
    screen.fill(BACKGROUND_COLOR)
    
    # Draw grid lines
    for i in range(BOARD_SIZE):
        # Horizontal lines
        pygame.draw.line(
            screen, 
            GRID_COLOR, 
            (MARGIN, MARGIN + i * CELL_SIZE), 
            (MARGIN + (BOARD_SIZE - 1) * CELL_SIZE, MARGIN + i * CELL_SIZE), 
            LINE_WIDTH
        )
        # Vertical lines
        pygame.draw.line(
            screen, 
            GRID_COLOR, 
            (MARGIN + i * CELL_SIZE, MARGIN), 
            (MARGIN + i * CELL_SIZE, MARGIN + (BOARD_SIZE - 1) * CELL_SIZE), 
            LINE_WIDTH
        )
    
    # Draw stones (EC2 and S3 icons)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 1:  # EC2
                icon_rect = ec2_icon.get_rect(
                    center=(MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE)
                )
                screen.blit(ec2_icon, icon_rect)
            elif board[row][col] == 2:  # S3
                icon_rect = s3_icon.get_rect(
                    center=(MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE)
                )
                screen.blit(s3_icon, icon_rect)
    
    # Display current player and game status
    font = pygame.font.SysFont('Arial', 24)
    if game_over:
        if winner == 1:
            status_text = "EC2 wins!"
        elif winner == 2:
            status_text = "S3 wins!"
        else:
            status_text = "Game Over - Draw"
    else:
        status_text = f"Current Player: {'EC2' if current_player == 1 else 'S3'}"
    
    text = font.render(status_text, True, (0, 0, 0))
    screen.blit(text, (MARGIN, 20))

def check_winner(row, col):
    """Check if the current move results in a win"""
    player = board[row][col]
    
    # Check all 8 directions
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # Count the current stone
        
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
            count += 1
            r += dr
            c += dc
        
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc
        
        # If 5 or more in a row, we have a winner
        if count >= 5:
            return True
    
    return False

def main():
    global current_player, game_over, winner, board
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reset game with 'R' key
                    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
                    current_player = 1
                    game_over = False
                    winner = None
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                # Get mouse position and convert to board coordinates
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Calculate the row and column
                col = round((mouse_x - MARGIN) / CELL_SIZE)
                row = round((mouse_y - MARGIN) / CELL_SIZE)
                
                # Check if the click is within the board and the cell is empty
                if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == 0:
                    # Place the stone
                    board[row][col] = current_player
                    
                    # Check for a winner
                    if check_winner(row, col):
                        game_over = True
                        winner = current_player
                    # Check for a draw
                    elif np.count_nonzero(board) == BOARD_SIZE * BOARD_SIZE:
                        game_over = True
                    else:
                        # Switch players
                        current_player = 3 - current_player  # Toggle between 1 and 2
        
        # Draw the board
        draw_board()
        
        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()
