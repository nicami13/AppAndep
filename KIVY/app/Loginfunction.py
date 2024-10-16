import firebase_admin
from firebase_admin import credentials, db

# Inicializa la aplicación con las credenciales de la cuenta de servicio y la base de datos
cred = credentials.Certificate('AppKivyMD/Services/test-f9337-firebase-adminsdk-a6m83-c75cf906db.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://test-f9337-default-rtdb.firebaseio.com/'
})

# Datos que deseas agregar
data = {
    'fullname': 'fullname',
    'email': 'username',
    'password': 'password',
}

# Escribir o actualizar los datos en la ruta 'Users/firs' de la base de datos
ref = db.reference('Users/')
ref.update(data)




print("Datos actualizados correctamente")


