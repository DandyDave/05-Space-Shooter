import arcade
import os
import math
import random
import open_color

SCALE = .5
SPRITE_SCALING = 0.35

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1080
OFFSCREEN_SPACE = 200
LEFT_LIMIT = -OFFSCREEN_SPACE
RIGHT_LIMIT = SCREEN_WIDTH + OFFSCREEN_SPACE
BOTTOM_LIMIT = -OFFSCREEN_SPACE
TOP_LIMIT = SCREEN_HEIGHT + OFFSCREEN_SPACE
SCREEN_TITLE = "WRLD SVR"

MOVEMENT_SPEED = 5
ANGLE_SPEED = 5

STARTING_ASTEROID_COUNT = 5

class TurningSprite(arcade.Sprite):
    """ Sprite that sets its angle to the direction it is traveling in. """
    def update(self):
        super().update()
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x))

class Player(arcade.Sprite):
    """ Player class """

    def __init__(self, image, scale):
        """ Set up the player """

        # Call the parent init
        super().__init__(image, scale)

        # Create a variable to hold our speed. 'angle' is created by the parent
        self.speed = 0

    def update(self):
        # Convert angle in degrees to radians.
        angle_rad = math.radians(self.angle)

        # Rotate the ship
        self.angle += self.change_angle

        # Use math to find our change based on our speed and angle
        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)  

class AsteroidSprite(arcade.Sprite):
    """ Sprite that represents an asteroid. """

    def __init__(self, image_file_name, scale):
        super().__init__(image_file_name, scale=scale)
        self.size = 0

    def update(self):
        """ Move the asteroid around. """
        super().update()
        if self.center_x < LEFT_LIMIT:
            self.center_x = RIGHT_LIMIT
        if self.center_x > RIGHT_LIMIT:
            self.center_x = LEFT_LIMIT
        if self.center_y > TOP_LIMIT:
            self.center_y = BOTTOM_LIMIT
        if self.center_y < BOTTOM_LIMIT:
            self.center_y = TOP_LIMIT

class BulletSprite(TurningSprite):
    """
    Class that represents a bullet.

    Derives from arcade.TurningSprite which is just a Sprite
    that aligns to its direction.
    """

    def update(self):
        super().update()
        if self.center_x < -100 or self.center_x > 1500 or \
                self.center_y > 1100 or self.center_y < -100:
            self.kill()

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.frame_count = 0

        

        # Variables that will hold sprite lists
        self.player_list = None

        # Set up the player info
        self.player_sprite = None

        # Stores Background Image as Variable
        self.background = None

        self.all_sprites_list = None
        self.asteroid_list = None
        self.bullet_list = None
        self.ship_life_list = None

        self.score = 0
        self.lives = 5

    def setup(self):
        """ Set up the game and initialize the variables. """
        
        self.frame_count = 0
        self.game_over = False

        #Background Image
        self.background = arcade.load_texture("assets/nebula.jpg")

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.all_sprites_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.ship_life_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player("assets/starshippixelart_rotate_transparant_2.png", SPRITE_SCALING)
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = SCREEN_HEIGHT / 2
        self.player_list.append(self.player_sprite)
        self.score = 0
        self.lives = 5

        cur_pos = 10
        for i in range(self.lives):
            life = arcade.Sprite("assets/starshippixelart_rotate_transparant_small.png", SCALE/3)
            life.center_x = cur_pos + life.width-20
            life.center_y = life.height*2+20
            cur_pos += life.width
            self.all_sprites_list.append(life)
            self.ship_life_list.append(life)

            # Make the asteroids
        image_list = ("assets/spaceMeteors_001.png",
                      "assets/spaceMeteors_002.png",
                      "assets/spaceMeteors_003.png",
                      "assets/spaceMeteors_004.png")
        for i in range(STARTING_ASTEROID_COUNT):
            image_no = random.randrange(4)
            enemy_sprite = AsteroidSprite(image_list[image_no], SCALE)
            enemy_sprite.guid = "Asteroid"

            enemy_sprite.center_y = random.randrange(BOTTOM_LIMIT, TOP_LIMIT)
            enemy_sprite.center_x = random.randrange(LEFT_LIMIT, RIGHT_LIMIT)

            enemy_sprite.change_x = random.random() * 2 - 1
            enemy_sprite.change_y = random.random() * 2 - 1

            enemy_sprite.change_angle = (random.random() - 0.5) * 2
            enemy_sprite.size = 4
            self.all_sprites_list.append(enemy_sprite)
            self.asteroid_list.append(enemy_sprite)
 
    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        #Draw Background
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Draw all the sprites.
        self.player_list.draw()
        self.all_sprites_list.draw()

         # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 15, 57, arcade.color.WHITE, 20)

        output = f"Asteroid Count: {len(self.asteroid_list)}"
        arcade.draw_text(output, 15, 25, arcade.color.WHITE, 20)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """


         # Shoot if the player hit the space bar
        if key == arcade.key.SPACE:
            bullet_sprite = BulletSprite("assets/bullet.png", SCALE)
            bullet_sprite.guid = "Bullet"

            bullet_speed = 10
            bullet_sprite.change_y = \
                math.cos(math.radians(self.player_sprite.angle))* bullet_speed
            bullet_sprite.change_x = \
                -math.sin(math.radians(self.player_sprite.angle)) \
                * bullet_speed 

            bullet_sprite.center_x = self.player_sprite.center_x
            bullet_sprite.center_y = self.player_sprite.center_y
            bullet_sprite.update()

            self.all_sprites_list.append(bullet_sprite)
            self.bullet_list.append(bullet_sprite)

        # Rotate left/right
        if key == arcade.key.LEFT:
            self.player_sprite.change_angle = 3
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_angle = -3

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_angle = 0

    def split_asteroid(self, asteroid: AsteroidSprite):
        """ Split an asteroid into chunks. """
        x = asteroid.center_x
        y = asteroid.center_y
        self.score += 1

        if asteroid.size == 4:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = ["assets/spaceMeteors_small_001.png",
                              "assets/spaceMeteors_small_002.png"]

                enemy_sprite = AsteroidSprite(image_list[image_no],
                                              SCALE * 1.5)

                enemy_sprite.center_y = y
                enemy_sprite.center_x = x

                enemy_sprite.change_x = random.random() * 2.5 - 1.25
                enemy_sprite.change_y = random.random() * 2.5 - 1.25

                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 3

                self.all_sprites_list.append(enemy_sprite)
                self.asteroid_list.append(enemy_sprite)
        elif asteroid.size == 3:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = ["assets/spaceMeteors_smaller_003.png",
                              "assets/spaceMeteors_smaller_004.png"]

                enemy_sprite = AsteroidSprite(image_list[image_no],
                                              SCALE * 1.5)

                enemy_sprite.center_y = y
                enemy_sprite.center_x = x

                enemy_sprite.change_x = random.random() * 3 - 1.5
                enemy_sprite.change_y = random.random() * 3 - 1.5

                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 2

                self.all_sprites_list.append(enemy_sprite)
                self.asteroid_list.append(enemy_sprite)
        elif asteroid.size == 2:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = ["assets/spaceMeteors_tiny_003.png",
                              "assets/spaceMeteors_tiny_004.png"]

                enemy_sprite = AsteroidSprite(image_list[image_no],
                                              SCALE * 1.5)

                enemy_sprite.center_y = y
                enemy_sprite.center_x = x

                enemy_sprite.change_x = random.random() * 3.5 - 1.75
                enemy_sprite.change_y = random.random() * 3.5 - 1.75

                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 1

                self.all_sprites_list.append(enemy_sprite)
                self.asteroid_list.append(enemy_sprite)

    def update(self, delta_time):
        """ Movement and game logic """
        self.frame_count += 1

        if not self.game_over:
            self.all_sprites_list.update()

            for bullet in self.bullet_list:
                asteroids_plain = arcade.check_for_collision_with_list(bullet, self.asteroid_list)
                asteroids_spatial = arcade.check_for_collision_with_list(bullet, self.asteroid_list)
                if len(asteroids_plain) != len(asteroids_spatial):
                    print("ERROR")

                asteroids = asteroids_spatial

                for asteroid in asteroids:
                    self.split_asteroid(asteroid)
                    asteroid.kill()
                    bullet.kill()

            asteroids = arcade.check_for_collision_with_list(self.player_sprite, self.asteroid_list)
            if len(asteroids) > 0:
                if self.lives > 0:
                    self.lives -= 1
                    self.split_asteroid(asteroids[0])
                    asteroids[0].kill()
                    self.ship_life_list.pop().kill()
                    print("Crash")
                else:
                    self.game_over = True
                    print("Game over")

        # Call update on all sprites 
        self.player_list.update()

def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()