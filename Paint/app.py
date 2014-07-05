from kivy.app import App
from kivy.uix.widget import Widget


class CanvasWidget(Widget):
    pass


class PaintApp(App):
    def build(self):
        return CanvasWidget()

if __name__ == '__main__':
    PaintApp().run()
