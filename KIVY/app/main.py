import firebase_admin
from firebase_admin import credentials, db
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
import random
import re  # Para la validación del correo
from kivy.properties import StringProperty

# Configura la ventana
Window.size = (360, 640)

# Cargar el archivo .kv
Builder.load_file('design.kv')

# Inicializa Firebase
cred = credentials.Certificate('AppKivyMD/Services/test-f9337-firebase-adminsdk-a6m83-4e39d48233.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://test-f9337-default-rtdb.firebaseio.com/'
})
class RutinasScreen(Screen):
    pass
class EstrategiasScreen(Screen):
    pass
class InformacionScreen(Screen):
    pass
class HomeScreen(Screen):
    pass

class ChatScreen(Screen):
    pass
class UserScreen(Screen): 
    pass
class WelcomeScreen(Screen):
    pass
class LoginScreen(Screen):
    pass
class RegisterScreen_1(Screen):
    pass
class RegisterScreen_2(Screen):
    pass
class QuestionScreen_1(Screen):
    pass
class QuestionScreen_3(Screen):
    pass
class QuestionScreen_2(Screen):
    pass
class QuestionScreen_4(Screen):
    pass
class QuestionScreen_5(Screen):
    pass
class QuestionScreen_6(Screen):
    pass
class QuestionScreen_7(Screen):
    pass
class WindowManager(ScreenManager):
    pass

class MainApp(App):
    logged_in_user = StringProperty()
    def build(self):
        return WindowManager()
    
    def email_exists(self, email):
        ref = db.reference('Users')
        users = ref.get()  # Obtener todos los usuarios de Firebase

        if users:  # Si existen usuarios en la base de datos
            for user_id, user_data in users.items():
                if user_data.get('email') == email:
                    return True  # El correo ya está en uso
        return False  # El correo no está en uso

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

    def validate_fullname(self, fullname,):
        if len(fullname) < 3:
            return False, "El nombre completo debe tener al menos 3 caracteres"
        return True, ""

    def on_register(self,screen):
        # Obtener los datos del registro
        fullname = self.root.get_screen(screen).ids.fullname_input.text
        username = self.root.get_screen(screen).ids.username_input.text
        password = self.root.get_screen(screen).ids.password_input.text
        confirm_password = self.root.get_screen(screen).ids.confirm_password_input.text

        fullname_error_label = self.root.get_screen(screen).ids.fullname_error
        email_error_label = self.root.get_screen(screen).ids.email_error
        password_error_label = self.root.get_screen(screen).ids.password_error
        confirm_password_error_label = self.root.get_screen(screen).ids.confirm_password_error
        login_button = self.root.get_screen(screen).ids.login_button

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

        # Verificar si el correo ya existe en la base de datos
        if self.email_exists(username):
            email_error_label.text = "El correo ya está en uso"
            return  # No continuar si el correo ya existe

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

            # Aquí actualizamos los datos del usuario anónimo
            if hasattr(self, 'user_id'):
                try:
                    # Obtener una referencia a la base de datos para el usuario actual
                    user_ref = db.reference(f'Users/{self.user_id}')
                    
                    # Actualizar los datos del usuario
                    updated_user_data = {
                        'fullname': fullname,
                        'email': username,
                        'password': password  # Nuevamente, no es recomendable guardar contraseñas en texto plano
                    }
                    user_ref.update(updated_user_data)
                    print(f"Usuario {self.user_id} actualizado con los datos: {updated_user_data}")

                    # Habilitar el botón de inicio de sesión
                    login_button.disabled = False
                except Exception as e:
                    print(f"Ocurrió un error al actualizar el usuario: {e}")
            else:
                print("No se encontró un usuario anónimo para actualizar.")
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
                        app = App.get_running_app()  # Obtener la instancia de la aplicación
                        app.root.current = 'HomeScreen'  # Cambiar la pantalla
                        app.logged_in_user = user_data.get('fullname') 
                        print("Usuario logueado")
                        
                        return
                # Si no se encontró coincidencia
                email_error_label.text = "El correo o la contraseña son incorrectos"
            else:
                email_error_label.text = "No se encontraron usuarios registrados"
        except Exception as e:
            print(f"Error al acceder a Firebase: {e}")
            email_error_label.text = "Error al conectar con la base de datos"



    def on_continue_without_register(self):
    # Generar identificador único para usuario anónimo
        anonymous_email = f"No email{random.randint(1000, 9999)}"
        
        ref = db.reference('Users')
        users = ref.get()
        
        # Buscar si ya existe un usuario anónimo similar
        existing_user = None
        if users:
            for user_id, user_data in users.items():
                if user_data.get('email') == anonymous_email:
                    existing_user = user_id
                    break

        if existing_user:
            # Si el usuario ya existe, usamos su ID
            self.user_id = existing_user
            print(f"Usuario anónimo existente encontrado: {self.user_id}")
        else:
            # Si no existe, creamos un nuevo usuario anónimo
            user_data = {
                'fullname': f"No nombre{random.randint(1000, 9999)}",
                'email': anonymous_email,
                'password': f"No contraseña{random.randint(1000, 9999)}"
            }
            new_user_ref = ref.push(user_data)
            self.user_id = new_user_ref.key
            print(f"Nuevo usuario anónimo registrado: {self.user_id}")

    def on_star_selected(self, rating, screen):
        self.rating = rating
        print(f"Calificación seleccionada: {rating}")
        
        # Habilitar el botón "Siguiente"
        next_button = self.root.get_screen(screen).ids.next_button
        next_button.disabled = False

    def go_to_next_question(self, screen, QNumber):
        print(f"ID de usuario: {self.user_id}")
        print(f"Rating seleccionado: {self.rating}")
        
        # Enviar la calificación a Firebase bajo el user_id único
        ref = db.reference(f'Responses/{self.user_id}')
        
        response_data = {
            'question': f'Pregunta {QNumber}',  # Podrías cambiar esto dinámicamente
            'rating': self.rating
        }

        try:
            ref.push(response_data)
            print("Respuesta enviada a Firebase correctamente:", response_data)
        except Exception as e:
            print(f"Ocurrió un error al enviar la respuesta a Firebase: {e}")

        # Desactivar el botón después de responder
        next_button = self.root.get_screen(screen).ids.next_button
        next_button.disabled = True
    def delete_user_and_responses(self):
    # Asegurarse de que `self.user_id` esté asignado
        if not hasattr(self, 'user_id'):
            print("No hay usuario para eliminar.")
            return

        # Eliminar respuestas del usuario en Firebase
        try:
            responses_ref = db.reference(f'Responses/{self.user_id}')
            responses_ref.delete()
            print(f"Respuestas del usuario {self.user_id} eliminadas.")
        except Exception as e:
            print(f"Ocurrió un error al eliminar las respuestas: {e}")

        # Eliminar usuario en Firebase
        try:
            user_ref = db.reference(f'Users/{self.user_id}')
            user_ref.delete()
            print(f"Usuario {self.user_id} eliminado.")
        except Exception as e:
            print(f"Ocurrió un error al eliminar el usuario: {e}")

        # Reiniciar el user_id después de eliminar el usuario y sus respuestas
        self.user_id = None
        print("El usuario y sus respuestas han sido eliminados.")



# Corre la aplicación
if __name__ == '__main__':
    MainApp().run()
