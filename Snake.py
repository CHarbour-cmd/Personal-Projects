import tkinter
import random

# Constants in Python use uppercase
ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

# Create Tile class
class Tile:
  def __init__(self, x, y):
    self.x = x
    self.y = y

# Creating the game window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

# Create canvas to draw on, hover over 'Canvas' to see attributes
canvas = tkinter.Canvas(window, bg = "white", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0)
canvas.pack()
window.update()

# Centre the window on screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate (x, y) position for the window
window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

# Format "(w)x(h)+(x)+(y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# Initialise the game
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE)  # Single tile for the snakes head
food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
snake_body = []  # Multiple snake tiles
velocityX = 0
velocityY = 0
game_over = False
score = 0

# Setting up change of direction
def change_direction(e):  # e = event
  # print(e)
  # print(e.keysym)
  global velocityX, velocityY, game_over
  if (game_over):
    return

  if (e.keysym == "Up" and velocityY != 1):
    velocityX = 0
    velocityY = -1  # (0,0) starts at top left corner of window
  elif (e.keysym == "Down" and velocityY != -1):
    velocityX = 0
    velocityY = 1
  elif (e.keysym == "Left" and velocityX != 1):
    velocityX = -1
    velocityY = 0
  elif(e.keysym == "Right" and velocityX != -1):
    velocityX = 1
    velocityY = 0

# Move the snake
def move():
  global snake, food, snake_body, game_over, score
  
  # Game over conditions
  if (game_over):
    return
  
  if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
    game_over = True
    return
  
  for tile in snake_body:
    if (snake.x == tile.x and snake.y == tile.y):
      game_over = True
      return

  # Check for colision between food and the snake's head
  if (snake.x == food.x and snake.y == food.y):
    snake_body.append(Tile(food.x, food.y))
    
    # After food is eaten, update food to new random location and add to score
    food.x = random.randint(0, COLS-1) * TILE_SIZE
    food.y = random.randint(0, ROWS-1) * TILE_SIZE
    score += 1

  # Update snake body
  for i in range(len(snake_body)-1, -1, -1):
    tile = snake_body[i]
    if (i == 0):  # Checks to see if tile is at the start of the snake body, right before snake head
      tile.x = snake.x
      tile.y = snake.y
    else:
      prev_tile = snake_body[i-1]
      tile.x = prev_tile.x
      tile.y = prev_tile.y

  snake.x += velocityX * TILE_SIZE  # Have to multiply by tile size otherwise moves 1 pixel rather than 1 tile
  snake.y += velocityY * TILE_SIZE


# Draw
def draw():
  global snake, food, snake_body, game_over, score
  move()  # Calling move function within draw function means snake moves at 10FPS

  # Clear the frame
  canvas.delete("all")

  # Draw the food
  canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = "lime green")

  # Draw the snake
  canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = "blue")

  # Draw snake body after eating food
  for tile in snake_body:
    canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = "blue")

  # Score
  if(game_over):
    canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = "Arial 20", text = f"Game Over: {score}", fill = "black")
  else:
    canvas.create_text(30, 20, font = "Arial 10", text = f"Score: {score}", fill = "black")

  # Want drawing to happen in a loop
  window.after(100, draw)  # 1ms = 1/100 second, 10FPS

draw()

# Use arrowkeys to control snake with key listener
window.bind("<KeyRelease>", change_direction)

# Keep window on
window.mainloop()

