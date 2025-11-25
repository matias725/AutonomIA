"""
Módulo de conexión a la base de datos MySQL
Implementa el patrón Singleton para garantizar una única instancia de conexión
Usa python-dotenv para cargar credenciales de forma segura
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env
load_dotenv()


class ConexionDB:
    """
    Clase Singleton para gestionar la conexión a MySQL
    
    Esta clase garantiza que solo exista una instancia de conexión
    a la base de datos durante toda la ejecución del programa.
    
    Principio de Seguridad: Las credenciales se cargan desde variables
    de entorno (.env) y nunca se almacenan directamente en el código.
    """
    
    _instancia = None  # Variable de clase para almacenar la única instancia
    
    def __new__(cls):
        """
        Implementación del patrón Singleton
        
        Si no existe una instancia, la crea.
        Si ya existe, retorna la existente.
        """
        if cls._instancia is None:
            cls._instancia = super(ConexionDB, cls).__new__(cls)
            cls._instancia._inicializar_conexion()
        return cls._instancia
    
    def _inicializar_conexion(self):
        """
        Inicializa la conexión con MySQL usando credenciales del .env
        """
        self.host = os.getenv('DB_HOST', 'localhost')
        self.database = os.getenv('DB_NAME', 'ecotech_db')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.port = os.getenv('DB_PORT', '3306')
        self.conexion = None
    
    def conectar(self):
        """
        Establece la conexión con la base de datos
        
        Returns:
            mysql.connector.connection: Objeto de conexión activa
            
        Raises:
            Error: Si no se puede establecer la conexión
        """
        try:
            if self.conexion is None or not self.conexion.is_connected():
                self.conexion = mysql.connector.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    port=self.port
                )
                
                if self.conexion.is_connected():
                    print("✓ Conexión exitosa a la base de datos MySQL")
                    return self.conexion
            else:
                return self.conexion
                
        except Error as e:
            print(f"✗ Error al conectar con MySQL: {e}")
            raise
    
    def desconectar(self):
        """
        Cierra la conexión con la base de datos de forma segura
        """
        try:
            if self.conexion is not None and self.conexion.is_connected():
                self.conexion.close()
                print("✓ Conexión cerrada correctamente")
        except Error as e:
            print(f"✗ Error al cerrar la conexión: {e}")
    
    def obtener_cursor(self):
        """
        Obtiene un cursor para ejecutar consultas SQL
        
        Returns:
            mysql.connector.cursor: Cursor para ejecutar queries
        """
        try:
            conexion = self.conectar()
            return conexion.cursor(dictionary=True)  # dictionary=True devuelve resultados como diccionarios
        except Error as e:
            print(f"✗ Error al obtener cursor: {e}")
            raise
    
    def ejecutar_query(self, query, parametros=None, commit=False):
        """
        Ejecuta una consulta SQL de forma segura
        
        Args:
            query (str): Consulta SQL con placeholders (%s)
            parametros (tuple): Parámetros para la consulta preparada
            commit (bool): Si True, hace commit de la transacción
            
        Returns:
            list: Resultados de la consulta (para SELECT)
            int: ID del último registro insertado (para INSERT)
            int: Número de filas afectadas (para UPDATE/DELETE)
        """
        cursor = None
        try:
            cursor = self.obtener_cursor()
            cursor.execute(query, parametros or ())
            
            if commit:
                self.conexion.commit()
                # Para INSERT, retornar el ID generado
                if query.strip().upper().startswith('INSERT'):
                    return cursor.lastrowid
                # Para UPDATE/DELETE, retornar filas afectadas
                return cursor.rowcount
            else:
                # Para SELECT, retornar todos los resultados
                return cursor.fetchall()
                
        except Error as e:
            if commit and self.conexion:
                self.conexion.rollback()
            print(f"✗ Error ejecutando query: {e}")
            raise
        finally:
            if cursor:
                cursor.close()


# ============================================
# Funciones de utilidad para usar en otros módulos
# ============================================

def obtener_conexion():
    """
    Función helper para obtener la instancia de conexión
    
    Returns:
        ConexionDB: Instancia única de la conexión
    """
    return ConexionDB()


def verificar_conexion():
    """
    Verifica que la conexión a la base de datos funcione correctamente
    
    Returns:
        bool: True si la conexión es exitosa, False en caso contrario
    """
    try:
        db = ConexionDB()
        db.conectar()
        return True
    except Exception as e:
        print(f"Error en la verificación: {e}")
        return False
