import pygame
from Agent import Agent
from Player import Player
from Ball import Ball
from Helper import plot
import time
import Constants
import Graphic


class Game:
    def __init__(self):
        self.width = Constants.WIDTH
        self.height = Constants.HEIGHT

    @staticmethod
    def text_objects(text, color, size):
        if size == "small":
            text_surface = Graphic.smallfont.render(text, True, color)
        elif size == "medium":
            text_surface = Graphic.medfont.render(text, True, color)
        elif size == "large":
            text_surface = Graphic.largefont.render(text, True, color)
        return text_surface, text_surface.get_rect()

    def message_to_screen(self, msg, color, y_displace=0, x_displace=0, size="small"):
        text_surf, text_rect = self.text_objects(msg, color, size)
        text_rect.center = (Graphic.win.get_width() / 2 + x_displace), ((Graphic.win.get_height() / 2) + y_displace)
        Graphic.win.blit(text_surf, text_rect)

    def draw_window(self, p1, p2, b, elapsed_time):
        Graphic.win.fill(Graphic.white)
        Graphic.win.blit(Graphic.pitch, (0, 0))
        Graphic.win.blit(Graphic.ball, (b.x, b.y))
        Graphic.win.blit(Graphic.poland, (p1.x, p1.y))
        Graphic.win.blit(Graphic.germany, (p2.x, p2.y))
        pygame.draw.rect(Graphic.win, Graphic.grey, pygame.Rect(370, 0, 280, 90))
        pygame.draw.line(Graphic.win, Graphic.white, (370, 0), (370, 90), width=5)
        pygame.draw.line(Graphic.win, Graphic.white, (370, 90), (650, 90), width=5)
        pygame.draw.line(Graphic.win, Graphic.white, (650, 90), (650, 0), width=5)
        pygame.draw.line(Graphic.win, Graphic.white, (370, 0), (650, 0), width=5)
        self.message_to_screen("Pol", Graphic.white, -270, -100, "small")
        self.message_to_screen(str(p1.score), Graphic.white, -270, -50, "small")
        self.message_to_screen("Ger", Graphic.white, -270, 100, "small")
        self.message_to_screen(str(p2.score), Graphic.white, -270, 50, "small")
        self.message_to_screen(str(int(elapsed_time)), Graphic.white, -250, 0, "small")
        pygame.display.update()

    @staticmethod
    def game_over(p1, p2, b):
        p1.reset_score()
        p2.reset_score()
        b.itr = 0
        p1.x = Constants.WIDTH / 4 - Constants.PLAYER_WIDTH / 2
        p1.y = Constants.HEIGHT / 2 - Constants.PLAYER_HEIGHT / 2
        p2.x = 3 / 4 * Constants.WIDTH - Constants.PLAYER_WIDTH / 2
        p2.y = Constants.HEIGHT / 2 - Constants.PLAYER_HEIGHT / 2
        p1.reward = 0
        p2.reward = 0
        b.after_goal(1)

    @staticmethod
    def check_goal(b, p1, p2):
        if Constants.HEIGHT / 2 - Constants.GOAL_HEIGHT / 2 - Constants.BALL_HEIGHT < b.y < Constants.HEIGHT / 2 + Constants.GOAL_HEIGHT / 2 + Constants.BALL_HEIGHT:
            if 0 <= b.x <= Constants.GOAL_WIDTH - Constants.BALL_WIDTH:
                p2.score += 1
                b.after_goal(1)
                if b.last_player_touch == 2:
                    p2.reward = 1
                p1.reward = - 1.5
            elif Constants.WIDTH - Constants.GOAL_WIDTH - Constants.BALL_WIDTH <= b.x <= Constants.WIDTH:
                p1.score += 1
                b.after_goal(2)
                if b.last_player_touch == 1:
                    p1.reward = 1
                p2.reward = - 1.5
        else:
            return

    def game_loop(self):
        total_score = 0
        plot_score = []
        plot_mean_score = []
        # Creating a ball
        b = Ball()
        # Creating players for Team 1
        p1 = Player(1, Constants.WIDTH / 4 - Constants.PLAYER_WIDTH / 2,
                    Constants.HEIGHT / 2 - Constants.PLAYER_HEIGHT / 2, 0, 0, Constants.WIDTH / 2, Constants.HEIGHT)
        # Creating players for Team 2
        p2 = Player(2, 3 / 4 * Constants.WIDTH - Constants.PLAYER_WIDTH / 2,
                    Constants.HEIGHT / 2 - Constants.PLAYER_HEIGHT / 2, Constants.WIDTH / 2, 0, Constants.WIDTH,
                    Constants.HEIGHT)
        clock = pygame.time.Clock()
        # Creating Agents
        agent_p1 = Agent()
        agent_p2 = Agent()
        # Loading Model
        # file_model1 = './model/model1.pth'
        # file_model2 = "./model/model2.pth"
        # agent_p1.load_model(file_model1)
        # agent_p2.load_model(file_model2)
        done = False
        time_limit = Constants.TIME_MATCH
        start_time = time.time()
        run = True
        while run:
            elapsed_time = time.time() - start_time
            clock.tick(Constants.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            # Get the state of the game for all players
            state_p1 = agent_p1.get_state(p1, b, p2)
            state_p2 = agent_p2.get_state(p2, b, p1)

            # Let the agents choose actions based on the current states
            action_p1 = agent_p1.get_action(state_p1)
            action_p2 = agent_p2.get_action(state_p2)

            # Update the players' positions based on the chosen actions
            p1.handle_movement(action_p1)
            p2.handle_movement(action_p2)

            # Update ball's position
            b.copy_cordinates()
            b.handle_movement()
            b.handle_collision(p1)
            b.handle_collision(p2)

            # Check if a goal has been scored
            self.check_goal(b, p1, p2)

            # Check if the game is over
            done = elapsed_time > time_limit

            # Draw the game window
            self.draw_window(p1, p2, b, elapsed_time)

            # Get the next states of the game for all players
            next_state_p1 = agent_p1.get_state(p1, b, p2)
            next_state_p2 = agent_p2.get_state(p2, b, p1)
            # Calculate the rewards based on the game states
            reward_p1 = p1.reward
            reward_p2 = p2.reward

            # Update the agents' memories with the current experiences
            agent_p1.remember(state_p1, action_p1, reward_p1, next_state_p1, done)
            agent_p2.remember(state_p2, action_p2, reward_p2, next_state_p2, done)

            # Train the agents using the short-term memories
            agent_p1.train_short_memory(state_p1, action_p1, reward_p1, next_state_p1, done)
            agent_p2.train_short_memory(state_p2, action_p2, reward_p2, next_state_p2, done)

            if done:
                agent_p1.n_games += 1
                if agent_p1.n_games == 100:
                    agent_p1.model.save('model1.pth')
                    agent_p2.model.save('model2.pth')
                agent_p1.train_long_memory()
                agent_p2.train_long_memory()
                time_limit = Constants.TIME_MATCH
                start_time = time.time()
                plot_score.append(b.itr)
                total_score += b.itr
                mean_score = total_score / agent_p1.n_games
                plot_mean_score.append(mean_score)
                plot(plot_score, plot_mean_score)
                self.game_over(p1, p2, b)
                done = False

        pygame.quit()
