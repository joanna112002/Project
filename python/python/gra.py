import pygame
import sys
import random
import os

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.fps = 60
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Gra zgadywanka")
        self.clock = pygame.time.Clock()
        self.current_state = MenuScreen(self)

    def run(self):
        running = True
        while running:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.current_state.handle_event(event)
            self.current_state.update()
            self.current_state.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
        sys.exit()

class GameState:
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2

class MenuScreen(GameState):
    def __init__(self, game):
        self.game = game

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.current_state = DifficultySelectionScreen(self.game, 1)
            elif event.key == pygame.K_1:
                self.game.current_state = DifficultySelectionScreen(self.game, 1)
            elif event.key == pygame.K_2:
                self.game.current_state = DifficultySelectionScreen(self.game, 2)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(self.game.black)
        font = pygame.font.Font(None, 48)
        title_text = font.render("Gra zgadywanka", True, self.game.white)
        start_text = font.render("Naciśnij SPACJĘ, aby rozpocząć", True, self.game.white)
        difficulty_text = font.render("Wybierz poziom trudności:", True, self.game.white)
        easy_text = font.render("1 - Łatwy", True, self.game.white)
        hard_text = font.render("2 - Trudny", True, self.game.white)
        screen.blit(title_text, (self.game.screen_width // 2 - title_text.get_width() // 2, 200))
        screen.blit(start_text, (self.game.screen_width // 2 - start_text.get_width() // 2, 300))
        screen.blit(difficulty_text, (self.game.screen_width // 2 - difficulty_text.get_width() // 2, 400))
        screen.blit(easy_text, (self.game.screen_width // 2 - easy_text.get_width() // 2, 450))
        screen.blit(hard_text, (self.game.screen_width // 2 - hard_text.get_width() // 2, 500))

class DifficultySelectionScreen(GameState):
    def __init__(self, game, difficulty):
        self.game = game
        self.difficulty = difficulty

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            word_file = ""
            if self.difficulty == 1:
                word_file = "words_list/kotek.txt"
            elif self.difficulty == 2:
                word_file = "words_list/trawa.txt"
            if os.path.isfile(word_file):
                self.game.current_state = PlayingScreen(self.game, word_file)
            else:
                print("Brak pliku z listą słów dla wybranego poziomu trudności.")

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(self.game.black)
        font = pygame.font.Font(None, 48)
        title_text = font.render("Gra zgadywanka", True, self.game.white)
        difficulty_text = font.render("Wybrano poziom trudności:", True, self.game.white)
        level_text = font.render(str(self.difficulty), True, self.game.white)
        start_text = font.render("Naciśnij SPACJĘ, aby rozpocząć", True, self.game.white)
        screen.blit(title_text, (self.game.screen_width // 2 - title_text.get_width() // 2, 200))
        screen.blit(difficulty_text, (self.game.screen_width // 2 - difficulty_text.get_width() // 2, 300))
        screen.blit(level_text, (self.game.screen_width // 2 - level_text.get_width() // 2, 350))
        screen.blit(start_text, (self.game.screen_width // 2 - start_text.get_width() // 2, 400))

class PlayingScreen(GameState):
    def __init__(self, game, word_file):
        self.game = game
        self.word_list = self.load_word_list(word_file)
        self.word = random.choice(self.word_list)
        self.player_guess = ""
        self.remaining_attempts = 6
        self.entered_words = []

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.player_guess = self.player_guess[:-1]
            elif event.key == pygame.K_RETURN:
                if len(self.player_guess) == len(self.word):
                    self.remaining_attempts -= 1
                    self.entered_words.append(self.player_guess)
                    if self.player_guess == self.word:
                        self.game.current_state = GameOverScreen(self.game, True, self.word)
                    else:
                        if self.remaining_attempts == 0:
                            self.game.current_state = GameOverScreen(self.game, False, self.word)
                        else:
                            self.player_guess = ""
                else:
                    self.player_guess = ""
            else:
                if len(self.player_guess) < len(self.word):
                    self.player_guess += event.unicode

    def update(self):
        pass

    def draw(self, screen):
        tlo = pygame.image.load('tło.jpg')
        screen.blit(tlo, (0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render("Odgadnij słowo: " + self.player_guess, True, self.game.white)
        screen.blit(text, (self.game.screen_width // 2 - text.get_width() // 2, 50))

        text = font.render("Pozostałe próby: " + str(self.remaining_attempts), True, self.game.white)
        screen.blit(text, (self.game.screen_width // 2 - text.get_width() // 2, 100))

        # Podpowiedzi
        correct_letters = set()
        misplaced_letters = set()

        for i, letter in enumerate(self.player_guess):
            if i < len(self.word) and letter == self.word[i]:
                correct_letters.add(i)
            elif letter in self.word:
                misplaced_letters.add(i)

        for i, letter in enumerate(self.player_guess):
            if i in correct_letters:
                letter_color = (0, 255, 0)  # Zielony kolor dla poprawnej litery
            elif i in misplaced_letters:
                letter_color = (0, 0, 255)  # Niebieski kolor dla litery na niewłaściwym miejscu
            else:
                letter_color = self.game.white



        # Przygotowanie tekstu do sekcji "Podane słowa"
        entered_words_text = "Podane słowa: "

        # Pozycja początkowa dla słów w sekcji "Podane słowa"
        entered_words_x = self.game.screen_width  // 2 - 200

        # Renderowanie wszystkich słów w sekcji "Podane słowa" z uwzględnieniem kolorów liter
        for word in self.entered_words:
            word_color = self.game.white
            word_text = ""
            for i, letter in enumerate(word):
                if i < len(self.word) and letter == self.word[i]:
                    letter_color = (0, 255, 0)  # Zielony kolor dla poprawnej litery
                elif letter in self.word:
                    letter_color = (0, 0, 255)  # Niebieski kolor dla litery na niewłaściwym miejscu
                else:
                    letter_color = self.game.white

                letter_text = font.render(letter, True, letter_color)
                screen.blit(letter_text, (entered_words_x, 200))

                word_text += letter
                entered_words_x += letter_text.get_width()   + 5  # Dodatkowy odstęp między literami

            entered_words_text += word_text + " , "

        entered_words_text = font.render(entered_words_text, True, self.game.white)
        screen.blit(entered_words_text, (self.game.screen_width // 2 - entered_words_text.get_width() // 2, 250))

    def load_word_list(self, word_file):
        with open(word_file, "r") as file:
            word_list = file.read().splitlines()
        return word_list

class GameOverScreen(GameState):
    def __init__(self, game, is_won, correct_word):
        self.game = game
        self.is_won = is_won
        self.correct_word = correct_word

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game.current_state = MenuScreen(self.game)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(self.game.black)
        font = pygame.font.Font(None, 48)
        title_text = font.render("Koniec gry", True, self.game.white)
        result_text = font.render("Wygrałeś!" if self.is_won else "Przegrałeś!", True, self.game.white)
        word_text = font.render("Zgadywane słowo: " + self.correct_word, True, self.game.white)
        restart_text = font.render("Naciśnij SPACJĘ, aby zagrać ponownie", True, self.game.white)
        screen.blit(title_text, (self.game.screen_width // 2 - title_text.get_width() // 2, 200))
        screen.blit(result_text, (self.game.screen_width // 2 - result_text.get_width() // 2, 300))
        screen.blit(word_text, (self.game.screen_width // 2 - word_text.get_width() // 2, 350))
        screen.blit(restart_text, (self.game.screen_width // 2 - restart_text.get_width() // 2, 400))

# Uruchomienie gry
if __name__ == "__main__":
    game = Game()
    game.run()