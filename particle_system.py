import pygame
import time
# Import vector2 and color class
from vector2 import *
from color import *

# Useful constants
gravityAccelation = vector2(0, 9.8 * 10)

# Individual particle class
# It has a startPosition, a startVelocity, and keeps tracks of the lifetime of the particle
# It also has some variables to make it better looking and to store the current position of the particle,
# to be used in rendering
class Particle:
    def __init__(self, startPosition, startVelocity):
        self.startPosition = startPosition
        self.startVelocity = startVelocity
        self.time = 0
        self.currentPos = self.prevPos = self.startPosition

# Particle system class
class ParticleSystem:
    def __init__(self, position, color):
        # Position of the (point) emitter
        self.position = position
        # Rate of particle emission, in particles/second
        self.rate = 0
        # Color of the particles
        self.color = color
        # Lifetime of each particle
        self.particleLifetime = 4
        # Variable to store the accumulated time since last particle spawn
        self.accumTime = 0
        # Starting speed of the particles
        self.startSpeed = (30, 50)
        # List to stores all the active particles
        self.particles = []

    # Render the particle system
    def draw(self, screen):
        c = self.color.tuple3()        
        for p in self.particles:   
            # Draws a line between the last position and the current position of the particle
            pygame.draw.line(screen, c, p.prevPos.tuple2(), p.currentPos.tuple2(), 1)
        
    # Updates the particle system
    def update(self, elapsedTime):
        # Spawn new particles according to the given rate
        self.accumTime += elapsedTime

        if (self.rate > 0):
            particles_to_spawn = (int)(math.floor(self.accumTime * self.rate))
            if (particles_to_spawn > 0):
                self.accumTime = self.accumTime - particles_to_spawn / self.rate
                self.spawn_particles(particles_to_spawn)

        # Update particle positions
        for p in self.particles:
            # Update time
            p.time += elapsedTime
            # Set previous position to the current position
            p.prevPos = p.currentPos
            # Update the current position
            p.currentPos = self.position + p.startVelocity * p.time + gravityAccelation * (p.time ** 2) * 0.5

        # Remove all particles that have exceeded their life time
        self.particles = list(filter(lambda p: p.time < self.particleLifetime, self.particles))

    # Emit new particles, using a point emitter
    def spawn_particles(self, nParticles):
        for _ in range(nParticles):
            p = Particle(self.position, vector2.random() * random.uniform(self.startSpeed[0], self.startSpeed[1]))
            self.particles.append(p)

def main():
    # Initialize pygame, with the default parameters
    pygame.init()

    # Define the size/resolution of our window
    res_x = 640
    res_y = 480

    # Create a window and a display surface
    screen = pygame.display.set_mode((res_x, res_y))

    # Timer
    delta_time = 0
    prev_time = time.time()

    # Create a particle system
    ps = ParticleSystem(vector2(320, 240), color(1,0,0,1))
    ps.rate = 120
    ps.startSpeed = (30, 50)
    ps.particleLife = 4

    # Game loop, runs forever
    while (True):
        # Process OS events
        for event in pygame.event.get():
            # Checks if the user closed the window
            if (event.type == pygame.QUIT):
                # Exits the application immediately
                return
            elif (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    return

        ps.update(delta_time)
        
        # Clears the screen with a very dark blue (0, 0, 20)
        screen.fill((0,0,0))

        ## Update the particle system
        ps.draw(screen)

        # Swaps the back and front buffer, effectively displaying what we rendered
        pygame.display.flip()

        # Updates the timer, so we we know how long has it been since the last frame
        delta_time = (time.time() - prev_time)
        prev_time = time.time()

main()