# -*- coding: utf-8 -*-
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
kivy.require('1.9.1')
import project


class Controller(BoxLayout):
    def __init__(self):
        super(Controller, self).__init__()

    def btn_clk(self):
        self.lbl.text = "Tunneling activated"
        project.tunnel()


class guiApp(App):

    def build(self):
        return Controller()


myApp = guiApp()

myApp.run()