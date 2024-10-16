import firebase_admin
import json
from kivy.uix.label import Label
from firebase_admin import credentials, db
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
import random
import re  
import requests
from kivy.properties import StringProperty
import kivy 
from kivy.uix.label import Label
from kivy.uix.button import Button

# Configura la ventana
Window.size = (360, 640)

# Cargar el archivo .kv
Builder.load_file('design.kv')

# Inicializa Firebase
cred = credentials.Certificate('AppKivyMD/Services/test-f9337-firebase-adminsdk-a6m83-9c3e250c65.json')
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
class ChatScreen(Screen):
    pass
class BubbleLabel(Label):
    pass

class UserMessage(BubbleLabel):
    def __init__(self, **kwargs):
        super(UserMessage, self).__init__(**kwargs)
        self.bg_color = (0.9, 0.9, 0.9, 1)  # Color del fondo del mensaje
        self.color = (0, 0, 0, 1)  # Color del texto
        self.halign= 'left'
        self.color= 0, 0, 0, 1
        self.text_size= self.size
        self.size_hint= (1, None)

class BotMessage(BubbleLabel):
    def __init__(self, **kwargs):
        super(BotMessage, self).__init__(**kwargs)
        self.bg_color = (0.1, 0.6, 0.1, 1)  # Color del fondo del mensaje
        self.color = (0, 0, 0, 1)  # Color del texto
        self.halign= 'left'
        self.font_size = 20
        self.width = 300
        self.text_size= self.size
        self.size_hint= (1, None)

class WindowManager(ScreenManager):
    pass

class MainApp(App):
    logged_in_user = StringProperty()
    Email_in_user = StringProperty()
    mealt_in_user=StringProperty()
    hobbie_in_user=StringProperty()
    age_in_user=StringProperty()
    song_in_user=StringProperty()
    user_id=StringProperty("")
    
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        # Cargar el archivo JSON con los intents
        with open("app/intents_massive.json", "r", encoding='utf-8') as file:
            self.intents = json.load(file)
    
    def build(self):
        Builder.load_file('design.kv')
        return WindowManager()
    

    def email_exists(self, email):
        ref = db.reference('Users')
        users = ref.get()  # Obtener todos los usuarios de Firebase

        if users:  # Si existen usuarios en la base de datos
            for user_id, user_data in users.items():
                if user_data.get('email') == email:
                    return True  # El correo ya está en uso
        return False  # El correo no está en uso
    

    
    def edit_field(self, field):
        user_screen = self.root.get_screen('UserScreen')
        
        app = App.get_running_app()  
        user_id = app.user_id  # El user_id del usuario autenticado o seleccionado
        
        if not user_id:
            print("Error: No se encontró el ID del usuario.")
            return  # Asegúrate de que user_id esté definido
        
        # Referencia a la base de datos con el ID del usuario correcto
        user_ref = db.reference(f'Users/{user_id}')
        
        # Validar que el campo sea uno de los permitidos para modificar
        if field == 'nombre':
            if user_screen.ids.nombre_input.disabled:  # Si está en modo Label
                user_screen.ids.nombre_input.opacity = 1  # Mostrar TextInput
                user_screen.ids.nombre_input.disabled = False  # Habilitar edición
                user_screen.ids.nombre_button.text = "Guardar"
            else:  # Si está en modo edición (TextInput visible)
                nuevo_nombre = user_screen.ids.nombre_input.text.strip()
                user_screen.ids.nombre_label.text = nuevo_nombre  # Actualizar el texto del Label
                user_screen.ids.nombre_input.opacity = 0  # Ocultar TextInput
                user_screen.ids.nombre_input.disabled = True
                user_screen.ids.nombre_button.text = "Editar"
                
                # Validar que el campo no esté vacío
                if nuevo_nombre:
                    user_ref.update({"fullname": nuevo_nombre})
                    print(f"Nombre actualizado a {nuevo_nombre} en la base de datos")
                else:
                    print("Error: El nombre no puede estar vacío")
                    user_screen.ids.nombre_label.text = "Nombre no ingresado"

        elif field == 'edad':
            if user_screen.ids.edad_input.disabled:
                user_screen.ids.edad_input.opacity = 1
                user_screen.ids.edad_input.disabled = False
                user_screen.ids.edad_button.text = "Guardar"
                user_screen.ids.edad_label.opacity = 0
            else:
                nueva_edad = user_screen.ids.edad_input.text.strip()
                user_screen.ids.edad_label.text = nueva_edad
                user_screen.ids.edad_input.opacity = 0
                user_screen.ids.edad_input.disabled = True
                user_screen.ids.edad_label.opacity = 1
                user_screen.ids.edad_button.text = "Editar"
                
                # Validar que el campo no esté vacío
                if nueva_edad:
                    user_ref.update({"edad": nueva_edad})
                    print(f"Edad actualizada a {nueva_edad} en la base de datos")
                else:
                    print("Error: La edad no puede estar vacía")
                    user_screen.ids.edad_label.text = "Edad no ingresada"

        elif field == 'cancion':
            if user_screen.ids.cancion_input.disabled:
                user_screen.ids.cancion_input.opacity = 1
                user_screen.ids.cancion_input.disabled = False
                user_screen.ids.cancion_button.text = "Guardar"
            else:
                nueva_cancion = user_screen.ids.cancion_input.text.strip()
                user_screen.ids.cancion_label.text = nueva_cancion
                user_screen.ids.cancion_input.opacity = 0
                user_screen.ids.cancion_input.disabled = True
                user_screen.ids.cancion_button.text = "Editar"
                
                # Validar que el campo no esté vacío
                if nueva_cancion:
                    user_ref.update({"song": nueva_cancion})
                    print(f"Canción favorita actualizada a {nueva_cancion} en la base de datos")
                else:
                    print("Error: La canción no puede estar vacía")
                    user_screen.ids.cancion_label.text = "Canción no ingresada"

        elif field == 'comida':
            if user_screen.ids.comida_input.disabled:
                user_screen.ids.comida_input.opacity = 1
                user_screen.ids.comida_input.disabled = False
                user_screen.ids.comida_button.text = "Guardar"
            else:
                nueva_comida = user_screen.ids.comida_input.text.strip()

                # Si el campo está vacío, se asigna un valor predeterminado
                if not nueva_comida:
                    nueva_comida = "No comida favorita"

                user_screen.ids.comida_label.text = nueva_comida
                user_screen.ids.comida_input.opacity = 0
                user_screen.ids.comida_input.disabled = True
                user_screen.ids.comida_button.text = "Editar"
                
                # Actualizar en la base de datos
                user_ref.update({"Favorite mealt": nueva_comida})  # Corregir el nombre de la clave en la base de datos
                print(f"Comida favorita actualizada a {nueva_comida} en la base de datos")

        elif field == 'actividad':
            if user_screen.ids.actividad_input.disabled:
                user_screen.ids.actividad_input.opacity = 1
                user_screen.ids.actividad_input.disabled = False
                user_screen.ids.actividad_button.text = "Guardar"
            else:
                nueva_actividad = user_screen.ids.actividad_input.text.strip()
                user_screen.ids.actividad_label.text = nueva_actividad
                user_screen.ids.actividad_input.opacity = 0
                user_screen.ids.actividad_input.disabled = True
                user_screen.ids.actividad_button.text = "Editar"
                
                # Validar que el campo no esté vacío
                if nueva_actividad:
                    user_ref.update({"hobbie": nueva_actividad})
                    print(f"Actividad favorita actualizada a {nueva_actividad} en la base de datos")
                else:
                    print("Error: La actividad no puede estar vacía")
                    user_screen.ids.actividad_label.text = "Actividad no ingresada"





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

    def on_register(self, screen):
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

            try:
                if hasattr(self, 'user_id') and self.user_id:
                    # Actualizar los datos del usuario anónimo existente
                    user_ref = db.reference(f'Users/{self.user_id}')
                    updated_user_data = {
                        'fullname': fullname,
                        'email': username,
                        'password': password,  # Nuevamente, no es recomendable guardar contraseñas en texto plano
                        'edad': 'No edad',
                        'song': 'No Canción',
                        'hobbie': 'No hobbie',
                        'Favorite mealt': 'No Comida Favorita'
                    }
                    user_ref.update(updated_user_data)
                    print(f"Usuario {self.user_id} actualizado con los datos: {updated_user_data}")

                else:
                    # Crear un nuevo usuario si no existe uno anónimo
                    new_user_ref = db.reference('Users').push()  # Genera un nuevo ID único
                    new_user_data = {
                        'fullname': fullname,
                        'email': username,
                        'password': password,  # Nuevamente, no es recomendable guardar contraseñas en texto plano
                        'edad': 'No edad',
                        'song': 'No Canción',
                        'hobbie': 'No hobbie',
                        'Favorite mealt': 'No Comida Favorita'
                    }
                    new_user_ref.set(new_user_data)  # Guardar los datos del nuevo usuario

                    # Obtener la clave generada por Firebase
                    self.user_id = new_user_ref.key  # Guardar el ID en self.user_id
                    print(f"Nuevo usuario creado con ID: {self.user_id} y datos: {new_user_data}")

                # Habilitar el botón de inicio de sesión
                login_button.disabled = False

            except Exception as e:
                print(f"Ocurrió un error al actualizar o crear el usuario: {e}")
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
                        app.Email_in_user = user_data.get('email')
                        app.mealt_in_user = user_data.get('Favorite mealt')
                        app.hobbie_in_user = user_data.get('hobbie')
                        app.age_in_user = user_data.get('edad')
                        app.song_in_user = user_data.get('song')
                        app.user_id=user_id
                        print(f"Usuario logueado:{user_id}")
                        
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
        
        if not self.user_id:  # Verifica si user_id es una cadena vacía
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
        self.user_id = ""  # Usa una cadena vacía en lugar de None
        print("El usuario y sus respuestas han sido eliminados.")
        
    def send_message(self):
        # Obtienes la referencia a la pantalla 'ChatScreen'
        screen = self.root.get_screen('ChatScreen')
        user_message = screen.ids.user_input.text.strip()

        # Si el mensaje del usuario está vacío, no hacemos nada
        if not user_message:
            return

        # Eliminar el mensaje anterior del usuario
        if screen.ids.chat_messages.children:
            screen.ids.chat_messages.remove_widget(screen.ids.chat_messages.children[0])

        # Mostrar el nuevo mensaje del usuario
        screen.ids.chat_messages.add_widget(UserMessage(text=f'Tu: {user_message}'))

        # Limpiar el campo de texto
        screen.ids.user_input.text = ""

        # Obtener la respuesta del bot
        response = self.get_response_from_intents(user_message)

        # Eliminar el mensaje anterior del bot
        if screen.ids.chat_messages.children:
            screen.ids.chat_messages.remove_widget(screen.ids.chat_messages.children[0])

        # Mostrar la nueva respuesta del bot
        screen.ids.chat_messages.add_widget(BotMessage(text=f'Bot: {response}'))


    def get_response_from_intents(self, user_message):
        # Aquí la lógica para obtener la respuesta
        for intent in self.intents["intents"]:
            for pattern in intent["patterns"]:
                if pattern.lower() in user_message.lower():
                    return random.choice(intent["responses"])
        return "Lo siento, no entendí eso. ¿Podrías reformular la pregunta?"


# Corre la aplicación
if __name__ == '__main__':
    MainApp().run()
