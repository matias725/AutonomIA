"""
Módulo de modelos de negocio - EcoTech Solutions
Contiene las clases Usuario, GestorUsuarios y excepciones personalizadas
Implementa 100% POO y manejo seguro de contraseñas con bcrypt
"""
import bcrypt
from db import obtener_conexion
from mysql.connector import Error


# ============================================
# EXCEPCIONES PERSONALIZADAS
# ============================================

class UsuarioException(Exception):
    """
    Excepción personalizada para errores relacionados con usuarios
    
    Hereda de Exception y permite manejar errores específicos
    del dominio de la aplicación
    """
    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class UsuarioNoEncontradoException(UsuarioException):
    """Excepción lanzada cuando no se encuentra un usuario"""
    pass


class UsuarioDuplicadoException(UsuarioException):
    """Excepción lanzada cuando se intenta crear un usuario que ya existe"""
    pass


class CredencialesInvalidasException(UsuarioException):
    """Excepción lanzada cuando las credenciales de login son incorrectas"""
    pass


# ============================================
# CLASE USUARIO (Modelo de Datos)
# ============================================

class Usuario:
    """
    Clase que representa un usuario del sistema EcoTech
    
    Atributos:
        id (int): Identificador único del usuario
        nombre_usuario (str): Nombre de usuario único
        correo (str): Correo electrónico
        rol (str): Rol del usuario (administrador, usuario, etc.)
        password_hash (str): Hash bcrypt de la contraseña
    """
    
    def __init__(self, nombre_usuario, correo, rol='usuario', password=None, id=None):
        """
        Constructor de la clase Usuario
        
        Args:
            nombre_usuario (str): Nombre de usuario
            correo (str): Email del usuario
            rol (str): Rol en el sistema
            password (str): Contraseña en texto plano (se hasheará automáticamente)
            id (int): ID del usuario (None para usuarios nuevos)
        """
        self.id = id
        self.nombre_usuario = nombre_usuario
        self.correo = correo
        self.rol = rol
        self._password_hash = None
        
        # Si se proporciona una contraseña, hashearla automáticamente
        if password:
            self.establecer_password(password)
    
    def establecer_password(self, password_plano):
        """
        Hashea y almacena la contraseña de forma segura usando bcrypt
        
        Args:
            password_plano (str): Contraseña en texto plano
            
        Seguridad: Nunca almacenamos contraseñas en texto plano.
        Bcrypt añade salt automáticamente y usa un factor de costo alto.
        """
        password_bytes = password_plano.encode('utf-8')
        salt = bcrypt.gensalt(rounds=12)  # Factor de costo 12 (muy seguro)
        self._password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    def verificar_password(self, password_plano):
        """
        Verifica si una contraseña coincide con el hash almacenado
        
        Args:
            password_plano (str): Contraseña a verificar
            
        Returns:
            bool: True si la contraseña es correcta, False en caso contrario
        """
        if not self._password_hash:
            return False
        
        password_bytes = password_plano.encode('utf-8')
        hash_bytes = self._password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hash_bytes)
    
    def obtener_password_hash(self):
        """Retorna el hash de la contraseña para almacenar en BD"""
        return self._password_hash
    
    def establecer_password_hash(self, hash_existente):
        """
        Establece un hash ya existente (para usuarios cargados de BD)
        
        Args:
            hash_existente (str): Hash bcrypt ya almacenado
        """
        self._password_hash = hash_existente
    
    def __str__(self):
        """Representación en string del usuario"""
        return f"Usuario(id={self.id}, nombre={self.nombre_usuario}, correo={self.correo}, rol={self.rol})"
    
    def __repr__(self):
        return self.__str__()


# ============================================
# CLASE GESTOR DE USUARIOS (Lógica de Negocio)
# ============================================

class GestorUsuarios:
    """
    Clase que gestiona todas las operaciones CRUD de usuarios
    
    Implementa:
    - Create: Agregar nuevos usuarios
    - Read: Buscar y listar usuarios
    - Update: Modificar datos de usuarios
    - Delete: Eliminar usuarios
    
    Además maneja la autenticación con validación de contraseñas hasheadas
    """
    
    def __init__(self):
        """Constructor que inicializa la conexión a BD"""
        self.db = obtener_conexion()
    
    # ========== CREATE ==========
    
    def agregar_usuario(self, usuario):
        """
        Agrega un nuevo usuario a la base de datos
        
        Args:
            usuario (Usuario): Objeto Usuario con los datos
            
        Returns:
            int: ID del usuario creado
            
        Raises:
            UsuarioDuplicadoException: Si el nombre de usuario o correo ya existen
            UsuarioException: Si hay un error al crear el usuario
        """
        try:
            # Verificar que el usuario no exista
            if self._usuario_existe(usuario.nombre_usuario, usuario.correo):
                raise UsuarioDuplicadoException(
                    f"El usuario '{usuario.nombre_usuario}' o el correo '{usuario.correo}' ya existen"
                )
            
            # Preparar query con parámetros (previene SQL Injection)
            query = """
                INSERT INTO usuarios (nombre_usuario, password, correo, rol)
                VALUES (%s, %s, %s, %s)
            """
            parametros = (
                usuario.nombre_usuario,
                usuario.obtener_password_hash(),
                usuario.correo,
                usuario.rol
            )
            
            # Ejecutar y obtener el ID generado
            id_generado = self.db.ejecutar_query(query, parametros, commit=True)
            usuario.id = id_generado
            
            print(f"✓ Usuario '{usuario.nombre_usuario}' creado exitosamente (ID: {id_generado})")
            return id_generado
            
        except UsuarioDuplicadoException:
            raise
        except Error as e:
            raise UsuarioException(f"Error al agregar usuario: {e}")
    
    def _usuario_existe(self, nombre_usuario, correo):
        """
        Verifica si un usuario o correo ya existen en la BD
        
        Args:
            nombre_usuario (str): Nombre de usuario a verificar
            correo (str): Correo a verificar
            
        Returns:
            bool: True si existe, False en caso contrario
        """
        query = """
            SELECT id FROM usuarios 
            WHERE nombre_usuario = %s OR correo = %s
        """
        resultados = self.db.ejecutar_query(query, (nombre_usuario, correo))
        return len(resultados) > 0
    
    # ========== READ ==========
    
    def buscar_usuario_por_nombre(self, nombre_usuario):
        """
        Busca un usuario por su nombre de usuario
        
        Args:
            nombre_usuario (str): Nombre del usuario a buscar
            
        Returns:
            Usuario: Objeto Usuario encontrado
            
        Raises:
            UsuarioNoEncontradoException: Si el usuario no existe
        """
        try:
            query = "SELECT * FROM usuarios WHERE nombre_usuario = %s"
            resultados = self.db.ejecutar_query(query, (nombre_usuario,))
            
            if not resultados:
                raise UsuarioNoEncontradoException(
                    f"Usuario '{nombre_usuario}' no encontrado"
                )
            
            # Convertir el resultado en objeto Usuario
            datos = resultados[0]
            usuario = Usuario(
                nombre_usuario=datos['nombre_usuario'],
                correo=datos['correo'],
                rol=datos['rol'],
                id=datos['id']
            )
            usuario.establecer_password_hash(datos['password'])
            
            return usuario
            
        except UsuarioNoEncontradoException:
            raise
        except Error as e:
            raise UsuarioException(f"Error al buscar usuario: {e}")
    
    def buscar_usuario_por_id(self, id_usuario):
        """
        Busca un usuario por su ID
        
        Args:
            id_usuario (int): ID del usuario
            
        Returns:
            Usuario: Objeto Usuario encontrado
            
        Raises:
            UsuarioNoEncontradoException: Si el usuario no existe
        """
        try:
            query = "SELECT * FROM usuarios WHERE id = %s"
            resultados = self.db.ejecutar_query(query, (id_usuario,))
            
            if not resultados:
                raise UsuarioNoEncontradoException(
                    f"Usuario con ID {id_usuario} no encontrado"
                )
            
            datos = resultados[0]
            usuario = Usuario(
                nombre_usuario=datos['nombre_usuario'],
                correo=datos['correo'],
                rol=datos['rol'],
                id=datos['id']
            )
            usuario.establecer_password_hash(datos['password'])
            
            return usuario
            
        except UsuarioNoEncontradoException:
            raise
        except Error as e:
            raise UsuarioException(f"Error al buscar usuario: {e}")
    
    def listar_usuarios(self):
        """
        Lista todos los usuarios del sistema
        
        Returns:
            list: Lista de objetos Usuario
        """
        try:
            query = "SELECT * FROM usuarios ORDER BY id"
            resultados = self.db.ejecutar_query(query)
            
            usuarios = []
            for datos in resultados:
                usuario = Usuario(
                    nombre_usuario=datos['nombre_usuario'],
                    correo=datos['correo'],
                    rol=datos['rol'],
                    id=datos['id']
                )
                usuario.establecer_password_hash(datos['password'])
                usuarios.append(usuario)
            
            return usuarios
            
        except Error as e:
            raise UsuarioException(f"Error al listar usuarios: {e}")
    
    # ========== UPDATE ==========
    
    def modificar_usuario(self, id_usuario, nuevo_correo=None, nuevo_rol=None, nueva_password=None):
        """
        Modifica los datos de un usuario existente
        
        Args:
            id_usuario (int): ID del usuario a modificar
            nuevo_correo (str): Nuevo correo (opcional)
            nuevo_rol (str): Nuevo rol (opcional)
            nueva_password (str): Nueva contraseña (opcional)
            
        Returns:
            bool: True si se modificó correctamente
            
        Raises:
            UsuarioNoEncontradoException: Si el usuario no existe
        """
        try:
            # Verificar que el usuario existe
            usuario = self.buscar_usuario_por_id(id_usuario)
            
            # Construir query dinámicamente según campos a modificar
            campos_actualizar = []
            parametros = []
            
            if nuevo_correo:
                campos_actualizar.append("correo = %s")
                parametros.append(nuevo_correo)
            
            if nuevo_rol:
                campos_actualizar.append("rol = %s")
                parametros.append(nuevo_rol)
            
            if nueva_password:
                # Hashear la nueva contraseña
                usuario_temp = Usuario('temp', 'temp@temp.com', password=nueva_password)
                campos_actualizar.append("password = %s")
                parametros.append(usuario_temp.obtener_password_hash())
            
            if not campos_actualizar:
                print("⚠ No se especificaron campos para modificar")
                return False
            
            # Agregar ID al final de los parámetros
            parametros.append(id_usuario)
            
            query = f"UPDATE usuarios SET {', '.join(campos_actualizar)} WHERE id = %s"
            filas_afectadas = self.db.ejecutar_query(query, tuple(parametros), commit=True)
            
            if filas_afectadas > 0:
                print(f"✓ Usuario ID {id_usuario} modificado exitosamente")
                return True
            return False
            
        except UsuarioNoEncontradoException:
            raise
        except Error as e:
            raise UsuarioException(f"Error al modificar usuario: {e}")
    
    # ========== DELETE ==========
    
    def eliminar_usuario(self, id_usuario):
        """
        Elimina un usuario de la base de datos
        
        Args:
            id_usuario (int): ID del usuario a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
            
        Raises:
            UsuarioNoEncontradoException: Si el usuario no existe
        """
        try:
            # Verificar que el usuario existe
            usuario = self.buscar_usuario_por_id(id_usuario)
            
            query = "DELETE FROM usuarios WHERE id = %s"
            filas_afectadas = self.db.ejecutar_query(query, (id_usuario,), commit=True)
            
            if filas_afectadas > 0:
                print(f"✓ Usuario '{usuario.nombre_usuario}' eliminado exitosamente")
                return True
            return False
            
        except UsuarioNoEncontradoException:
            raise
        except Error as e:
            raise UsuarioException(f"Error al eliminar usuario: {e}")
    
    # ========== AUTENTICACIÓN ==========
    
    def autenticar_usuario(self, nombre_usuario, password):
        """
        Autentica un usuario validando su contraseña
        
        Args:
            nombre_usuario (str): Nombre de usuario
            password (str): Contraseña en texto plano
            
        Returns:
            Usuario: Objeto Usuario si las credenciales son válidas
            
        Raises:
            CredencialesInvalidasException: Si las credenciales son incorrectas
        """
        try:
            # Buscar el usuario
            usuario = self.buscar_usuario_por_nombre(nombre_usuario)
            
            # Verificar la contraseña con bcrypt
            if usuario.verificar_password(password):
                print(f"✓ Usuario '{nombre_usuario}' autenticado correctamente")
                return usuario
            else:
                raise CredencialesInvalidasException(
                    "Contraseña incorrecta"
                )
                
        except UsuarioNoEncontradoException:
            raise CredencialesInvalidasException(
                f"Usuario '{nombre_usuario}' no encontrado"
            )
        except CredencialesInvalidasException:
            raise
        except Exception as e:
            raise UsuarioException(f"Error en autenticación: {e}")
