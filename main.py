from time import sleep

import kivy
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout


class HoverButton(ButtonBehavior, RelativeLayout):
    def __init__(self, text, image_source, **kwargs):
        super().__init__(**kwargs)
        self.Hovered = False
        self.sound_hover = SoundLoader.load('assets/sounds/button_hover.wav')

        Window.bind(mouse_pos=self.on_mouse_over)  # Bind the hover event

        # Add the button image
        self.button_image = Image(source=image_source, allow_stretch=True, keep_ratio=False)
        self.add_widget(self.button_image)

        # Add the button text
        self.button_text = Label(text=text, font_name="assets/fonts/PirataOne-Regular.ttf", font_size=self.height * .4, color=(0.4666666666666667, 0.2549019607843137, 0.15294117647058825))
        self.add_widget(self.button_text)

    def on_mouse_over(self, window, pos):
        # Check if the mouse is over the button
        if self.collide_point(*pos):
            if not self.Hovered:
                self.Hovered = True
                self.sound_hover.play()
        else:
            if self.Hovered:
                self.Hovered = False



class GameView(FloatLayout):
    def __init__(self):
        super(GameView, self).__init__()
        self.background_music = SoundLoader.load('assets/sounds/background_sound.mp3')
        self.background_music.loop = True
        self.background_music.play()

        # Image de fond
        self.background = Image(source='assets/images/main_menu.png',
                                allow_stretch=True,
                                keep_ratio=False)
        self.add_widget(self.background)

        # Logo
        self.logo = Image(source='assets/images/logo.png',
                          size_hint=(.20, .20),
                          pos_hint={'center_x': .5, 'center_y': .73})  # Proportionné en haut
        self.add_widget(self.logo)

        # Boutons avec espacement proportionnel
        button_positions = [0.53, 0.40, 0.27]  # Positions centrées verticalement pour les boutons
        button_texts = ["Jouer", "Options", "Quitter"]

        for pos, text in zip(button_positions, button_texts):
            self.add_widget(self.create_button(text, pos))

    def create_button(self, text, center_y):
        """Create a button with an image and centered text."""
        button_layout = HoverButton(text=text, image_source='assets/images/button.png', size_hint=(.4, .12), pos_hint={'center_x': .5, 'center_y': center_y})
        button_layout.bind(on_press=self.on_button_press)
        return button_layout

    def on_button_press(self, instance):
        sound_click = SoundLoader.load('assets/sounds/button_click.wav')
        sound_click.play()
        if instance.button_text.text == "Quitter":
            sleep(.2)
            exit()


class MainApp(App):
    def build(self):
        return GameView()


mainApp = MainApp()
mainApp.run()