from graphics import *     # Import the graphics library for drawing
import time               # Import time for delays and timing control
import random             # Import random for generating food positions

# Set the game window dimensions and block size
width, height = 600, 400
block_size = 20

# Function to generate a random position for the food
def random_food_position():
    fx = random.randint(0, (width - block_size) // block_size) * block_size  # Random x-position
    fy = random.randint(0, (height - block_size) // block_size) * block_size # Random y-position
    return fx, fy

# Main game loop function
def game_loop():
    win = GraphWin("🐍 Snake Game", width, height)  # Create game window
    win.setBackground('black')                     # Set background color to black

    # Define colors
    green = color_rgb(0, 255, 0)   # Snake color
    red = color_rgb(255, 0, 0)     # Food color
    white = color_rgb(255, 255, 255) # Text color

    # Draw the initial score text
    score_text = Text(Point(50, 10), "Score: 0")
    score_text.setTextColor(white)
    score_text.setSize(12)
    score_text.draw(win)

    snake = []           # List to hold snake body blocks
    length = 1           # Initial length of the snake

    # Start position (center of the window)
    x = width // 2
    y = height // 2

    dx = 0  # Movement in x-direction
    dy = 0  # Movement in y-direction

    # Draw the initial snake head
    head = Rectangle(Point(x, y), Point(x + block_size, y + block_size))
    head.setFill(green)
    head.draw(win)
    snake.append(head)

    # Generate and draw the first food
    food_x, food_y = random_food_position()
    food = Rectangle(Point(food_x, food_y), Point(food_x + block_size, food_y + block_size))
    food.setFill(red)
    food.draw(win)

    score = 0             # Initial score
    game_over = False     # Game over flag
    last_key = None       # Last direction key pressed

    snake_speed = 0.15    # Initial delay between movements (speed control)

    # Function to move the snake one step
    def move_snake(dx, dy):
        nonlocal x, y, snake, length  # Use variables from outer scope

        x += dx  # Update x-position
        y += dy  # Update y-position

        # Check wall collision
        if x < 0 or x >= width or y < 0 or y >= height:
            return False

        # Remove tail if snake isn't growing
        if len(snake) == length:
            tail = snake.pop(0)
            tail.undraw()

        # Create new head block
        new_head = Rectangle(Point(x, y), Point(x + block_size, y + block_size))
        new_head.setFill(green)
        new_head.draw(win)
        snake.append(new_head)

        # Check collision with self
        for segment in snake[:-1]:  # Exclude the head
            seg_p1 = segment.getP1()
            if seg_p1.getX() == x and seg_p1.getY() == y:
                return False  # Collision with body

        return True  # No collision

    # Function to update score display
    def update_score(new_score):
        score_text.setText(f"Score: {new_score}")

    # Game loop (runs while not game over)
    while not game_over:
        key = win.checkKey()  # Check for key press
        if key != "":
            last_key = key    # Store last key for continuous movement

        # Change direction only if not reversing
        if last_key == "Left" and dx == 0:
            dx, dy = -block_size, 0
        elif last_key == "Right" and dx == 0:
            dx, dy = block_size, 0
        elif last_key == "Up" and dy == 0:
            dx, dy = 0, -block_size
        elif last_key == "Down" and dy == 0:
            dx, dy = 0, block_size

        # If the snake is moving
        if dx != 0 or dy != 0:
            if not move_snake(dx, dy):  # If collision happens
                game_over = True
                break  # Exit game loop

            # Check if food is eaten
            if x == food_x and y == food_y:
                length += 1        # Increase snake length
                score += 1         # Increase score
                update_score(score)

                # Generate new food
                food.undraw()
                food_x, food_y = random_food_position()
                food = Rectangle(Point(food_x, food_y), Point(food_x + block_size, food_y + block_size))
                food.setFill(red)
                food.draw(win)

        # Control snake speed (minimum delay = 0.05 seconds)
        time.sleep(max(0.05, snake_speed - score * 0.005))

    # Show "Game Over" message
    game_over_text = Text(Point(width / 2, height / 2 - 30), "Game Over!")
    game_over_text.setTextColor(red)
    game_over_text.setSize(20)
    game_over_text.draw(win)

    # Show restart/quit instructions
    prompt_text = Text(Point(width / 2, height / 2 + 10), "Press R to Restart or Q to Quit")
    prompt_text.setTextColor(white)
    prompt_text.setSize(15)
    prompt_text.draw(win)

    # Wait for player input to restart or quit
    while True:
        key = win.getKey().upper()
        if key == 'Q':
            break               # Quit the game
        elif key == 'R':
            win.close()         # Close current window
            game_loop()         # Restart game
            break

    win.close()  # Close the window after quitting

# Start the game
game_loop()
