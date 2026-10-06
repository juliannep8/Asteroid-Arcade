import math
import random
import pygame
import asyncio

async def main():
  pygame.init()
  
  # Game Constants
  WIDTH = 800
  HEIGHT = 600
  NUM_ASTEROIDS = 5
  MISSILE_SPEED = 7
  
  # Colors
  BLACK = (10, 10, 20)
  WHITE = (255, 255, 255)
  GRAY = (170, 170, 170)
  YELLOW = (255, 230, 80)
  RED = (255, 80, 80)
  
  # Pygame Setup
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption("Asteroids Arcade")
  clock = pygame.time.Clock()
  font = pygame.font.Font(None, 28)
  
  
  class Asteroid:
      def __init__(self):
          self.radius = random.randint(18, 35)
          self.position = pygame.Vector2(
              random.randint(self.radius, WIDTH - self.radius),
              random.randint(self.radius, HEIGHT - self.radius),
          )
          angle = random.uniform(0, 2 * math.pi)
          speed = random.uniform(1.0, 2.5)
          self.velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
  
      def update(self):
          self.position += self.velocity
  
          # Screen wrapping
          if self.position.x > WIDTH + self.radius:
              self.position.x = -self.radius
          elif self.position.x < -self.radius:
              self.position.x = WIDTH + self.radius
  
          if self.position.y > HEIGHT + self.radius:
              self.position.y = -self.radius
          elif self.position.y < -self.radius:
              self.position.y = HEIGHT + self.radius
  
      def draw(self):
          pygame.draw.circle(
              screen,
              GRAY,
              (int(self.position.x), int(self.position.y)),
              self.radius,
              2,
          )
  
  
  class Missile:
      def __init__(self, start_position, target_position):
          self.position = pygame.Vector2(start_position)
          self.radius = 5
          direction = target_position - self.position
          if direction.length() != 0:
              direction = direction.normalize()
          self.velocity = direction * MISSILE_SPEED
  
      def update(self):
          self.position += self.velocity
  
      def draw(self):
          pygame.draw.circle(
              screen,
              YELLOW,
              (int(self.position.x), int(self.position.y)),
              self.radius,
          )
  
      def is_off_screen(self):
          return (
              self.position.x < 0
              or self.position.x > WIDTH
              or self.position.y < 0
              or self.position.y > HEIGHT
          )
  
  
  class Ship:
      def __init__(self):
          self.position = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
          self.velocity = pygame.Vector2(0, 0)  # Part 1: Stationary start
          self.acceleration = pygame.Vector2(0, 0)  # Part 2: Acceleration vector
          self.angle = 90
          self.rotation_speed = 3
  
          self.THRUST = 0.15  # Part 5
          self.DRAG = 0.99  # Part 7
          self.MAX_SPEED = 6.0  # Part 8
          self.is_thrusting = False  # Part 11
  
      def update(self, keys):
          # Handle Rotation
          if keys[pygame.K_LEFT]:
              self.angle += self.rotation_speed
          if keys[pygame.K_RIGHT]:
              self.angle -= self.rotation_speed
  
          # Part 3
          radians = math.radians(self.angle)
          forward = pygame.Vector2(math.cos(radians), -math.sin(radians))
  
          # Part 4
          self.acceleration = pygame.Vector2(0, 0)
          self.is_thrusting = False
  
          # Part 5
          if keys[pygame.K_UP]:
              self.acceleration = forward * self.THRUST
              self.is_thrusting = True  # Part 11
  
          # Part 6
          self.velocity += self.acceleration
  
          # Part 7
          self.velocity *= self.DRAG
  
          # Part 8
          if self.velocity.length() > self.MAX_SPEED:
              self.velocity.scale_to_length(self.MAX_SPEED)
  
          # Part 9
          self.position += self.velocity
  
          # Part 10
          if self.position.x > WIDTH:
              self.position.x = 0
          elif self.position.x < 0:
              self.position.x = WIDTH
  
          if self.position.y > HEIGHT:
              self.position.y = 0
          elif self.position.y < 0:
              self.position.y = HEIGHT
  
      def draw(self):
          radians = math.radians(self.angle)
          forward = pygame.Vector2(math.cos(radians), -math.sin(radians))
  
          p1 = self.position + forward * 18
          p2 = self.position + forward.rotate(135) * 14
          p3 = self.position + forward.rotate(-135) * 14
  
          # Draw Ship
          pygame.draw.polygon(screen, RED, [p1, p2, p3], 2)
          pygame.draw.circle(
              screen, RED, (int(self.position.x), int(self.position.y)), 3
          )
  
          # Part 11
          if self.is_thrusting:
              back = self.position - forward * 18
              pygame.draw.circle(screen, YELLOW, (int(back.x), int(back.y)), 5)
  class EnemyShip:
      def __init__(self):
          self.position = pygame.Vector2(WIDTH / 4, HEIGHT / 2)
          self.velocity = pygame.Vector2(0, 0)  # Part 1
          self.acceleration = pygame.Vector2(0, 0)  # Part 2
          self.angle = 180
          self.rotation_speed = 3
  
          self.THRUST = 0.15  # Part 5
          self.DRAG = 0.99  # Part 7
          self.MAX_SPEED = 6.0  # Part 8
          self.is_thrusting = False  # Part 11
          
          radians = math.radians(self.angle)
          self.forward = pygame.Vector2(math.cos(radians), -math.sin(radians))
  
      def update(self):
          # Part 3
          radians = math.radians(self.angle)
          self.forward = pygame.Vector2(math.cos(radians), -math.sin(radians))
  
          # Part 7
          self.velocity *= self.DRAG
  
          # Part 8
          if self.velocity.length() > self.MAX_SPEED:
              self.velocity.scale_to_length(self.MAX_SPEED)
  
          # Part 9
          self.position += self.velocity
  
          # Part 10
          if self.position.x > WIDTH:
              self.position.x = 0
          elif self.position.x < 0:
              self.position.x = WIDTH
  
          if self.position.y > HEIGHT:
              self.position.y = 0
          elif self.position.y < 0:
              self.position.y = HEIGHT
  
      def draw(self, detected):
          radians = math.radians(self.angle)
          self.forward = pygame.Vector2(math.cos(radians), -math.sin(radians))
  
          p1 = self.position + self.forward * 18
          p2 = self.position + self.forward.rotate(135) * 14
          p3 = self.position + self.forward.rotate(-135) * 14
  
          # Draw Ship
          if not detected:
              pygame.draw.polygon(screen, WHITE, [p1, p2, p3], 2)
              pygame.draw.circle(
                  screen, WHITE, (int(self.position.x), int(self.position.y)), 3
              )
          else:
              pygame.draw.polygon(screen, RED, [p1, p2, p3], 2)
              pygame.draw.circle(
                  screen, RED, (int(self.position.x), int(self.position.y)), 3
              )
  
          # Part 11
          if self.is_thrusting:
              back = self.position - self.forward * 18
              pygame.draw.circle(screen, YELLOW, (int(back.x), int(back.y)), 5)
  
  def missile_hits_asteroid(missile, asteroid):
      distance = missile.position.distance_to(asteroid.position)
      return distance < missile.radius + asteroid.radius
  
  # Game setup
  player_ship = Ship()
  
  enemy_ship = EnemyShip()
  DETECTION_RANGE = 300
  FOV_THRESHOLD = 0.7
  
  asteroids = [Asteroid() for _ in range(NUM_ASTEROIDS)]
  missiles = []
  
  score = 0
  running = True
  
  # Main Game Loop
  while running:
      clock.tick(60)
  
      # 1. Event Handling
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              running = False
          if event.type == pygame.MOUSEBUTTONDOWN:
              target_position = pygame.Vector2(event.pos)
              # Create missile originating from current ship position
              new_missile = Missile(player_ship.position, target_position)
              missiles.append(new_missile)
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_SPACE:
                  radians = math.radians(player_ship.angle)
                  front_direction = pygame.Vector2(math.cos(radians), -math.sin(radians))
                  target_position = player_ship.position + front_direction * 100
                  missiles.append(Missile(player_ship.position, target_position))
  
  
      # 2. Input Handling & Physics Updates
      keys = pygame.key.get_pressed()
      player_ship.update(keys)
      enemy_ship.update()
      
      to_player = (
      player_ship.position - enemy_ship.position
      )
      if to_player.length() > 0:
          to_player = to_player.normalize()
          distance = enemy_ship.position.distance_to(
          player_ship.position
          )
      if distance > 0:
              to_player_normalized = to_player.normalize()
              dot = enemy_ship.forward.dot(to_player_normalized)
              
              if distance < DETECTION_RANGE and dot > FOV_THRESHOLD:
                  detected = True
      if (distance < DETECTION_RANGE and dot > FOV_THRESHOLD):
          detected = True
      else:
          detected = False
  
      for asteroid in asteroids:
          asteroid.update()
  
      for missile in missiles:
          missile.update()
  
      missiles = [m for m in missiles if not m.is_off_screen()]
  
      # 3. Collision Detection
      for missile in missiles[:]:
          for asteroid in asteroids[:]:
              if missile_hits_asteroid(missile, asteroid):
                  if missile in missiles:
                      missiles.remove(missile)
                  if asteroid in asteroids:
                      asteroids.remove(asteroid)
                      asteroids.append(Asteroid())
                  score += 1
                  break
  
      screen.fill(BLACK)
      player_ship.draw()
      enemy_ship.draw(detected)
  
      for asteroid in asteroids:
          asteroid.draw()
  
      for missile in missiles:
          missile.draw()
  
      # UI Display
      instruction = font.render("Click to fire, Arrows to drive", True, WHITE)
      screen.blit(instruction, (20, 20))
  
      score_text = font.render("Points: " + str(score), True, WHITE)
      screen.blit(score_text, (20, 50))
  
      pygame.display.flip()
      await asyncio.sleep(0)
      pygame.quit()
asyncio.run(main())
