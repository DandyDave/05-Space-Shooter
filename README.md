I made a an astroids like space shooter for my Game Technology class at Indiana Univversity. There are many parts of the code that were built 
out python arcade demonstrations. I still need to figure out how to get the bullets to spawn out the end of the sprite and not the center. 

Still haveing two problems one major the other minor. The major problem is that there is a chance that asteroids can spawn in 
the player's hitbox which will immediately take all of the player's lives because there are no invincibility frames implemented.
The smaller problem is that I cannot figure out the right way to have the bullets come out the end of the player sprite. The bullets
will go in the correct direction but are currently spawning from the center of the world (since that is the middle of the player sprite).

If you want to change the "difficulty".
Change self.lives in line 125 and 149 which will add more player lives/health
And changing STARTING_ASTEROID_COUNT in line 22 will change the amount of starting asteroids. 