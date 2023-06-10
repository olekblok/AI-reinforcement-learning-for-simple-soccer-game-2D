import Constants


class Player:
    def __init__(self, nr, ix, iy, bx1, by1, bx2, by2):
        self.player_nr = nr
        self.width = Constants.PLAYER_WIDTH
        self.height = Constants.PLAYER_HEIGHT
        self.x = ix
        self.y = iy
        self.bx1 = bx1
        self.by1 = by1
        self.bx2 = bx2
        self.by2 = by2
        self.score = 0
        self.reward = 0
        self.v = Constants.PLAYER_VELOCITY
        self.itr = 0

    def handle_movement(self, action):
        if action == [1, 0, 0, 0] and self.x - self.v - self.width > self.bx1:  # LEFT
            self.x -= self.v
        if action == [1, 0, 0, 0] and self.x - self.v - self.width <= self.bx1:
            self.reward -= 0.1
        if action == [0, 1, 0, 0] and self.x + self.width + self.v < self.bx2 - 50:  # RIGHT
            self.x += self.v
        if action == [0, 1, 0, 0] and self.x + self.width + self.v >= self.bx2:  # RIGHT
            self.reward -= 0.1
        if action == [0, 0, 1, 0] and self.y - self.height - self.v > self.by1:  # UP
            self.y -= self.v
        if action == [0, 0, 1, 0] and self.y - self.height - self.v <= self.by1:  # UP
            self.reward -= 0.1
        if action == [0, 0, 0, 1] and self.y + self.height + self.v < self.by2:  # DOWN
            self.y += self.v
        if action == [0, 0, 0, 1] and self.y + self.height + self.v >= self.by2:  # DOWN
            self.reward -= 0.1

    def reset_score(self):
        self.score = 0
