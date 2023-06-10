import Constants


class Ball:
    def __init__(self):
        self.x = Constants.WIDTH / 2 - Constants.PLAYER_WIDTH / 2
        self.y = Constants.HEIGHT / 2 - Constants.PLAYER_HEIGHT / 2
        self.direction_x = Constants.BALL_DIRECTION
        self.direction_y = Constants.BALL_DIRECTION
        self.v_x = Constants.BALL_VELOCITY
        self.v_y = Constants.BALL_VELOCITY
        self.w = Constants.BALL_WIDTH
        self.h = Constants.BALL_HEIGHT
        self.prev_x = 0
        self.prev_y = 0
        self.itr = 0
        self.last_player_touch = 0

    def handle_movement(self):
        if self.x + self.v_x + self.w <= Constants.WIDTH and self.x + self.v_x - self.w / 2 >= 0:
            self.x += self.v_x
        else:
            self.v_x = -self.v_x  # Reflect horizontally

            if self.x + self.v_x + self.w > Constants.WIDTH:
                overlap = abs((self.x + self.v_x + self.w) - Constants.WIDTH)
                self.x = Constants.WIDTH - self.w - overlap  # Adjust position to prevent sliding

        if self.y + self.v_y + self.h <= Constants.HEIGHT and self.y + self.v_y - self.h / 2 >= 0:
            self.y += self.v_y
        else:
            self.v_y = -self.v_y  # Reflect vertically

            if self.y + self.v_y + self.h > Constants.HEIGHT:
                overlap = abs((self.y + self.v_y + self.h) - Constants.HEIGHT)
                self.y = Constants.HEIGHT - self.h - overlap  # Adjust position to prevent sliding

    def handle_collision(self, player):
        if (self.x + self.w >= player.x and self.x <= player.x + player.width) and (
                self.y + self.h >= player.y and self.y <= player.y + player.height):
            # Calculate the distance between the centers of the objects
            dx = (self.x + self.w / 2) - (player.x + player.width / 2)
            dy = (self.y + self.h / 2) - (player.y + player.height / 2)

            combined_width = self.w + player.width
            combined_height = self.h + player.height

            # Check the direction of collision
            if abs(dx) <= combined_width / 2:
                if self.v_x != 0:
                    self.x -= self.v_x  # Move the ball back to its previous position
                    self.v_x *= -1  # Reverse the velocity component in y-direction
                else:
                    self.v_x = Constants.BALL_VELOCITY
            if abs(dy) <= combined_height / 2:
                # Colliding vertically
                if self.v_y != 0:
                    self.y -= self.v_y  # Move the ball back to its previous position
                    self.v_y *= -1  # Reverse the velocity component in y-direction
                else:
                    self.v_y = Constants.BALL_VELOCITY

            if self.itr >= 100:
                player.reward = -0.5
            else:
                player.reward = 0.5
            player.itr = 0
            self.itr += 1
            self.last_player_touch = player.player_nr

    def after_goal(self, team):
        self.x = Constants.WIDTH / 2 - self.w / 2
        self.y = Constants.HEIGHT / 2 - self.h / 2
        self.last_player_touch = 0
        if team == 1:
            self.v_x *= 1
            self.v_y *= 1
        elif team == 2:
            self.v_x *= -1
            self.v_y *= -1

    def copy_cordinates(self):
        self.prev_x = self.x
        self.prev_y = self.y
