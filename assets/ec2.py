"""
Simple EC2 icon generator for the Gomoku game
"""
import pygame

def create_ec2_icon(size=40, color=(255, 153, 0)):
    """Create an EC2 icon surface"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Draw the EC2 icon (simplified orange square with "EC2" text)
    pygame.draw.rect(surface, color, (0, 0, size, size), border_radius=5)
    
    # Add text
    font = pygame.font.SysFont('Arial', int(size * 0.5))
    text = font.render("EC2", True, (255, 255, 255))
    text_rect = text.get_rect(center=(size/2, size/2))
    surface.blit(text, text_rect)
    
    return surface
