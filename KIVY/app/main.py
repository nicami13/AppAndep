import firebase_admin
from firebase_admin import credentials, db
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
import re  # Para la validación del correo

# Configura la ventana
Window.size = (360, 640)

# Cargar el archivo .kv
Builder.load_file('design.kv')

# Inicializa Firebase
cred = credentials.Certificate('AppKivyMD/Services/test-f9337-firebase-adminsdk-a6m83-c75cf906db.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://test-f9337-default-rtdb.firebaseio.com/'
})

# Clases de pantallas
class WelcomeScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class RegisterScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return WindowManager()

    def validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email)

    def validate_password(self, password):
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"
        if not any(char.isupper() for char in password):
            return False, "La contraseña debe tener al menos una letra mayúscula"
        if not any(char.isdigit() for char in password):
            return False, "La contraseña debe tener al menos un número"
        return True, ""

    def validate_fullname(self, fullname):
        if len(fullname) < 3:
            return False, "El nombre completo debe tener al menos 3 caracteres"
        return True, ""

    def on_register(self):
        fullname = self.root.get_screen('register').ids.fullname_input.text
        username = self.root.get_screen('register').ids.username_input.text
        password = self.root.get_screen('register').ids.password_input.text
        confirm_password = self.root.get_screen('register').ids.confirm_password_input.text

        fullname_error_label = self.root.get_screen('register').ids.fullname_error
        email_error_label = self.root.get_screen('register').ids.email_error
        password_error_label = self.root.get_screen('register').ids.password_error
        confirm_password_error_label = self.root.get_screen('register').ids.confirm_password_error

        # Validar nombre completo
        valid_fullname, fullname_message = self.validate_fullname(fullname)
        if not valid_fullname:
            fullname_error_label.text = fullname_message
        else:
            fullname_error_label.text = ""

        # Validar email
        if not self.validate_email(username):
            email_error_label.text = "Correo electrónico no válido"
        else:
            email_error_label.text = ""

        # Validar contraseña
        valid_password, password_message = self.validate_password(password)
        if not valid_password:
            password_error_label.text = password_message
        else:
            password_error_label.text = ""

        # Validar confirmación de contraseña
        if password != confirm_password:
            confirm_password_error_label.text = "Las contraseñas no coinciden"
        else:
            confirm_password_error_label.text = ""

        # Si todas las validaciones son correctas
        if valid_fullname and self.validate_email(username) and valid_password and password == confirm_password:
            print("Registro exitoso")
            
            # Obtener una referencia a la base de datos
            ref = db.reference('Users')  # Ruta a 'Users'

            # Crear un nuevo registro
            user_data = {
                    'fullname': fullname,
                    'email': username,
                'password': password  # No es recomendable almacenar contraseñas en texto plano
            }

            # Actualizar la base de datos usando el método `update`
            try:
                ref.push(user_data)  # Usa `push` para crear un nuevo registro único
                print("Datos enviados a Firebase correctamente:", user_data)
            except Exception as e:
                print(f"Ocurrió un error al enviar datos a Firebase: {e}")

        else:
            print("Errores en el formulario")

    def on_login(self):
    # Obtener correo y contraseña desde la pantalla de inicio de sesión
        username = self.root.get_screen('login').ids.username_input.text
        password = self.root.get_screen('login').ids.password_input.text

        # Etiquetas para mostrar errores
        email_error_label = self.root.get_screen('login').ids.email_error
        password_error_label = self.root.get_screen('login').ids.password_error

        # Validar que los campos no estén vacíos
        if not username or not password:
            if not username:
                email_error_label.text = "Por favor ingrese su correo electrónico"
            if not password:
                password_error_label.text = "Por favor ingrese su contraseña"
            return

        # Reiniciar errores
        email_error_label.text = ""
        password_error_label.text = ""

        # Obtener referencia a la base de datos
        ref = db.reference('Users')

        # Obtener todos los usuarios
        try:
            users = ref.get()
            if users:
                # Recorrer usuarios para validar las credenciales
                for user_id, user_data in users.items():
                    if user_data.get('email') == username and user_data.get('password') == password:
                        print("Usuario logueado")
                        return
                # Si no se encontró coincidencia
                email_error_label.text = "El correo o la contraseña son incorrectos"
            else:
                email_error_label.text = "No se encontraron usuarios registrados"
        except Exception as e:
            print(f"Error al acceder a Firebase: {e}")
            email_error_label.text = "Error al conectar con la base de datos"


    # Método para continuar sin registrarse
    def on_continue_without_register(self):
        print("Continuar sin registrarse")

# Corre la aplicación
if __name__ == '__main__':
    MainApp().run()
