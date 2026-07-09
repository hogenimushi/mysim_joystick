# -*- coding: utf-8 -*-
"""
Inspect pygame axis/button/hat indices for a joystick connected to Windows.

Based on the pygame joystick documentation:
https://www.pygame.org/docs/ref/joystick.html

Usage:
  1. Connect the joystick (for F710: plug the USB dongle, wait for recognition,
     then press the Logicool button to activate).
  2. Run: python check_key_binding.py
  3. Operate sticks/buttons/D-pad and note axis/button/hat indices.
  4. Close the window to exit.

Notes:
  - Prefer a single joystick device while mapping.
  - F710 D-mode and X-mode use different mappings (use X-mode for this project).
"""
import pygame


BLACK = pygame.Color('black')
WHITE = pygame.Color('white')


class TextPrint(object):
    """Helper to print text lines onto the pygame window."""

    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def tprint(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


try:
    pygame.init()
except Exception:
    raise

screen = pygame.display.set_mode((500, 700))
pygame.display.set_caption("Joystick Key Binding Check")

done = False
clock = pygame.time.Clock()
pygame.joystick.init()
textPrint = TextPrint()

while not done:
    for event in pygame.event.get():
        try:
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
            elif event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")
        except Exception:
            raise

    screen.fill(WHITE)
    textPrint.reset()

    joystick_count = pygame.joystick.get_count()
    textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()

    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        textPrint.tprint(screen, "Joystick {}".format(i))
        textPrint.indent()

        name = joystick.get_name()
        textPrint.tprint(screen, "Joystick name: {}".format(name))

        axes = joystick.get_numaxes()
        textPrint.tprint(screen, "Number of axes: {}".format(axes))
        textPrint.indent()
        for axis_i in range(axes):
            axis = joystick.get_axis(axis_i)
            textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(axis_i, axis))
        textPrint.unindent()

        buttons = joystick.get_numbuttons()
        textPrint.tprint(screen, "Number of buttons: {}".format(buttons))
        textPrint.indent()
        for button_i in range(buttons):
            button = joystick.get_button(button_i)
            textPrint.tprint(screen, "Button {:>2} value: {}".format(button_i, button))
        textPrint.unindent()

        hats = joystick.get_numhats()
        textPrint.tprint(screen, "Number of hats: {}".format(hats))
        textPrint.indent()
        for hat_i in range(hats):
            hat = joystick.get_hat(hat_i)
            textPrint.tprint(screen, "Hat {} value: {}".format(hat_i, str(hat)))
        textPrint.unindent()

        textPrint.unindent()

    pygame.display.flip()
    clock.tick(20)

try:
    pygame.quit()
except Exception:
    raise
