from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

# Cargar el archivo KV
Builder.load_file('design.kv')

class WelcomeScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return WindowManager()

    def on_register(self):
        print("Regístrate")  # Implementa la lógica de registro aquí

    def on_login(self):
        print("Inicie sesión")  # Implementa la lógica de inicio de sesión aquí

    def on_continue_without_register(self):
        print("Continuar sin registrarse")  # Implementa la lógica aquí

    def on_skip(self):
        print("Saltar")  # Implementa la lógica de saltar aquí

if __name__ == '__main__':
    MainApp().run()
