import asyncio
from core.core import Core
from instance.four import Four

#TODO:

# - check if when prefSD is true if the order of preform actions and gravity needs to be swapped in game loop. 90% sure i dont have to worry about this but lmao icba to check

#  === game logic ===
# - PERFECT CLEAR DETECTION 
# - COMBO DETECTION
# - SCORING
# - LEVELS
# - GAME OVER CONDITIONS

# TODO: implement das cut delay

# === rendering ===
# - make blocks use textures
# - animations
# -  lignment helper funcs:
#            -  horizontal align (define line)
#            -  vertical align (define line)
#            -  center align (uses surface)
#            -  left align (uses surface)
#            -  right align (uses surface)
#            -  top align (uses surface)
#            -  bottom align (uses surface)
#            -  center align (uses surface)
#            -  corner align (uses surface)

async def main():
    game_instance = Core()
    four = Four(game_instance, matrix_width = 10, matrix_height = 20, rotation_system = 'SRS', randomiser = '7BAG', queue_previews = 5,  seed = 292168102)
    await game_instance.run(four)

if __name__ == "__main__":
    asyncio.run(main())
