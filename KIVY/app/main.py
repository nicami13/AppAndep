from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window

Window.size = (360, 640)
# Cargar el archivo KV
Builder.load_file('design.kv')

class WelcomeScreen(Screen):
    pass

class LoginScreen(Screen):
    def on_enter(self):
        self.ids.username_input.text = ''  # Limpia el campo de entrada de usuario al entrar
        self.ids.password_input.text = ''  # Limpia el campo de entrada de contraseña al entrar

class WindowManager(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return WindowManager()

    def on_register(self):
        print("Regístrate")  # Implementa la lógica de registro aquí

    def on_login(self):
        username = self.root.get_screen('login').ids.username_input.text
        password = self.root.get_screen('login').ids.password_input.text
        print(f"Nombre de usuario: {username}, Contraseña: {password}")  # Puedes implementar la lógica de autenticación aquí

    def on_continue_without_register(self):
        print("Continuar sin registrarse")  # Implementa la lógica aquí

if __name__ == '__main__':
    MainApp().run()
