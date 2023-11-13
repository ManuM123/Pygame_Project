import pygame
import os       # we need to import os because we will use the operating system to specify the path of the images we use
pygame.font.init()

width, height = 900, 500
window = pygame.display.set_mode((width, height)) # Setting up the dimensions of the pygame window

pygame.display.set_caption("Pygame Ghanekar")   # This just renames the name of the window

background = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (width, height)) # Resizing the image to the height and width of the swindow itself
separation_border_colour = (255, 165, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

speed = pygame.time.Clock()         # This will help us limit the FPS at which the program will run

health_font = pygame.font.SysFont("Comicsans", 40)
winner_font = pygame.font.SysFont("Helvetica", 100)

red_spaceship_image = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
yellow_spaceship_image = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))

spaceship_width, spaceship_height = 55, 40

red_spaceship = pygame.transform.rotate(pygame.transform.scale(red_spaceship_image, (spaceship_width, spaceship_height)), 270)
yellow_spaceship = pygame.transform.rotate(pygame.transform.scale(yellow_spaceship_image, (spaceship_width, spaceship_height)), 90)

red = pygame.Rect(700, 300, spaceship_width, spaceship_height)              # We are representing the spaceships as rectangles so that it is easier to manipulate eg .x, y etc
yellow = pygame.Rect(100, 300, spaceship_width, spaceship_height)

spaceship_speed = 5     # The number of pixels the spaceships will move when either W/S or Up/Down arrows are pressed

separation_border = pygame.Rect((width / 2) - 5, 0, 10, height) # Designing the border which both players cannot cross over the (x,y) co ordinates represents the top left coordinate of the 
                                                                # rectangle, it will be drawn from here     
red_bullets =[]
yellow_bullets = []

bullet_speed = 10
max_bullets = 5

yellow_Spaceship_hit = pygame.USEREVENT + 1               # Creating our own custom events
red_Spaceship_hit = pygame.USEREVENT + 2

red_spaceship_health = 10
yellow_spaceship_health = 10


def design_window(red, yellow, red_bullets, yellow_bullets, red_spaceship_health, yellow_spaceship_health):                    
    window.blit(background, (0, 0))     # The 0,0 represents the starting coordinate of the image

    red_health_text = health_font.render("Health: " + str(red_spaceship_health), 1, (255,255,255))
    yellow_health_text = health_font.render("Health: " + str(yellow_spaceship_health), 1, (255,255,255))

    window.blit(red_health_text, (width - red_health_text.get_width() - 10, 10))
    window.blit(yellow_health_text,(10,10))

    window.blit(red_spaceship, (red.x, red.y))            # Blit function will actually add the images onto the window, we are directly "blitting" the rotated and resized images
    window.blit(yellow_spaceship, (yellow.x, yellow.y))
    pygame.draw.rect(window, separation_border_colour, separation_border)

    for bullet in red_bullets:                  # Drawing the actual bullets onto the screen
        pygame.draw.rect(window, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(window, YELLOW, bullet)


    pygame.display.update()        

def yellow_spaceship_movement():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and (yellow.y > 0):                       # Use Up/Down arrow buttons to move red spaceship up and down
            yellow.y -= spaceship_speed          
    if keys[pygame.K_s] and ((yellow.y + spaceship_height) < (height - 15)):  # The logic here is that if the y coordinate of the spaceship plus the height of the spaceship exceeds the window height, it will not let it move
            yellow.y += spaceship_speed
    if keys[pygame.K_d] and ((yellow.x + yellow.width) < separation_border.x):
                yellow.x += spaceship_speed
    if keys[pygame.K_a] and (yellow.x > 0):
            yellow.x -= spaceship_speed

def red_spaceship_movement():
    global red, yellow

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and (red.y > 0):                        # Use W/S  buttons to move yellow spaceship up and down
            red.y -= spaceship_speed
    if keys[pygame.K_DOWN] and ((red.y + spaceship_height) < height):
            red.y += spaceship_speed
    if keys[pygame.K_RIGHT] and ((red.x + spaceship_width) < width):
        red.x += spaceship_speed
    if keys[pygame.K_LEFT]  and (red.x > separation_border.right):
            red.x -= spaceship_speed   

def handle_bullets(red_bullets, yellow_bullets, red, yellow):
        for bullet in yellow_bullets:
            bullet.x += bullet_speed
            if red.colliderect(bullet):              # For when a yellow bullet hits the red spaceship
                 pygame.event.post(pygame.event.Event(red_Spaceship_hit))
                 yellow_bullets.remove(bullet)
            elif bullet.x > width:                  # For when the bullet goes off the screen
                  yellow_bullets.remove(bullet)

        for bullet in red_bullets:          # What happens when a red bullet hits the yellow spaceship
            bullet.x -= bullet_speed    # Keep in mind since the red player is on the right, the bullets must fire to the left
            if yellow.colliderect(bullet):                 
                 pygame.event.post(pygame.event.Event(yellow_Spaceship_hit))
                 red_bullets.remove(bullet)
            elif bullet.x < 0:
                  red_bullets.remove(bullet)

def draw_winner_message(text):
        winner_text = winner_font.render(text, 1, (255, 255, 255))
        window.blit(winner_text, (width // 2 - winner_text.get_width() // 2, height // 2 - winner_text.get_height() // 2))

        pygame.display.update()
        pygame.time.delay(3000)

            
    
def main():

    global red_spaceship_health, yellow_spaceship_health

    run_game = True
    while run_game:
        speed.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < max_bullets:           
                      bullet = pygame.Rect((yellow.x + yellow.width), (yellow.y + ((yellow.height // 2) - 2)), 10, 5) # Designing the bullets and adding to a list
                      yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < max_bullets:
                      bullet = pygame.Rect(red.x, red.y + ((red.height // 2) - 2), 10, 5)          # This makes sure when we shoot the bullet, it will shoot from the middle of the spaceship
                      red_bullets.append(bullet)
            
            if event.type == red_Spaceship_hit:
                  red_spaceship_health -= 1
            
            if event.type == yellow_Spaceship_hit:
                  yellow_spaceship_health -= 1
        
        win_message = ""
        if red_spaceship_health == 0:
              win_message = "Well Done Yellow Player!"
        elif yellow_spaceship_health == 0:
              win_message = "Well Done Red Player!" 
        if win_message != "":
              draw_winner_message(win_message)
              break
                          
                  
                       
        yellow_spaceship_movement()
        red_spaceship_movement()
        design_window(red, yellow, red_bullets, yellow_bullets, red_spaceship_health, yellow_spaceship_health)
        handle_bullets(red_bullets, yellow_bullets, red, yellow)

    pygame.quit()


        
        
if __name__ == "__main__":   # These 2 lines of code ensure that the main function only runs when the file is directly ran through the main program, not being imported the " if __name__ == " just means " if the name of the file is"
    main()                  
                                      
   