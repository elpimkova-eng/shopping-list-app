from kivy.app import App
from ui_layouts import MainLayout
from app_logic import AppLogic

class ShoppingApp(App):
    def build(self):
        logic = AppLogic()
        return MainLayout(logic)

if __name__ == '__main__':
    ShoppingApp().run()