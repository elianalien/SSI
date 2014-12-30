#!/usr/bin/kivy
from time import time
from kivy.app import App
from os.path import dirname, join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen, FadeTransition


class ShowcaseScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(ShowcaseScreen, self).add_widget(*args)


class ShowcaseApp(App):

    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    show_sourcecode = BooleanProperty(False)
    sourcecode = StringProperty()
    screen_names = ListProperty([])
    #higherarchy = ListProperty([])

    def build(self):
        self.title = 'SMART CITY SADANG SERANG'
        self.screens = {}
        self.available_screens = ['ScreenManager']
        self.screen_names = self.available_screens
        curdir = dirname(__file__)
        self.available_screens = [join(curdir, 
            '{}.kv'.format(fn)) for fn in self.available_screens]
        self.go_next_screen()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def go_previous_screen(self):
        self.index = (self.index - 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='right')
        self.current_title = screen.name
        

    def go_next_screen(self):
        self.index = (self.index + 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        #FadeTransition()
        sm.switch_to(screen, direction='left')
        self.current_title = screen.name
        

    def go_screen(self, idx):
        self.index = idx
        self.root.ids.sm.switch_to(self.load_screen(idx), direction='left')
        
    # def go_higherarchy_previous(self):
    #     ahr = self.higherarchy
    #     if len(ahr) == 1:
    #         return
    #     if ahr:
    #         ahr.pop()
    #     if ahr:
    #         idx = ahr.pop()
    #         self.go_screen(idx)

    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]
        screen = Builder.load_file(self.available_screens[index].lower())
        self.screens[index] = screen
        return screen


    def _update_clock(self, dt):
        self.time = time()

    tX = 0
    minDist = 80

    def on_touch_down(self, touch):
        self.tX = touch.x

    def on_touch_up(self, touch):
        if self.tX - touch.x > self.minDist:
            print "left"
        if self.tX - touch.x < -self.minDist:
            print "right"

if __name__ == '__main__':
    ShowcaseApp().run()
