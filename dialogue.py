import pygame

class DialogueBox:
    def __init__(self, game, width=400, height=100):
        self.game = game
        self.width = width
        self.height = height
        self.visible = False
        self.text = ""
        self.font = pygame.font.SysFont("arial", 18)
        self.box_color = (190, 196, 162)
        self.text_color = (0, 0, 0)
        self.padding = 10

    def show(self, text):
        self.text = text
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self):
        if self.visible:
            x = (self.game.screen.get_width() - self.width) // 2
            y = self.game.screen.get_height() - self.height - 20

            pygame.draw.rect(self.game.screen, self.box_color, (x, y, self.width, self.height))
            pygame.draw.rect(self.game.screen, (0, 0, 0), (x, y, self.width, self.height), 2)  # border

            wrapped_lines = self.wrap_text(self.text, self.font, self.width - 2 * self.padding)

            for i, line in enumerate(wrapped_lines):
                text_surface = self.font.render(line, True, self.text_color)
                self.game.screen.blit(text_surface, (x + self.padding, y + self.padding + i * 20))

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        lines.append(current_line.strip())
        return lines