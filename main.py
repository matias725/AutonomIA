"""
Aplicación Principal - EcoTech Solutions
Sistema de gestión de usuarios con autenticación segura y consulta de datos ambientales

Asignatura: Programación Orientada a Objeto Seguro
Características:
- Login seguro con bcrypt
- Límite de 3 intentos fallidos
- Menú interactivo con CRUD de usuarios
- Consumo de API de calidad del aire
- 100% Programación Orientada a Objetos
"""
import sys
from modelos import GestorUsuarios, CredencialesInvalidasException, UsuarioException
from modelos import Usuario, UsuarioNoEncontradoException, UsuarioDuplicadoException
from api import ServicioExterno, APIException
from db import verificar_conexion


# ============================================
# CLASE APLICACIÓN PRINCIPAL
# ============================================

class AplicacionEcoTech:
    """
    Clase principal que gestiona la aplicación EcoTech Solutions
    
    Responsabilidades:
    - Gestionar el flujo de autenticación
    - Mostrar menú interactivo
    - Coordinar operaciones CRUD de usuarios
    - Integrar datos de la API externa
    """
    
    def __init__(self):
        """Inicializa los componentes de la aplicación"""
        self.gestor_usuarios = GestorUsuarios()
        self.servicio_api = ServicioExterno()
        self.usuario_actual = None
        self.intentos_login = 0
        self.max_intentos = 3
    
    def mostrar_banner(self):
        """Muestra el banner de bienvenida de la aplicación"""
        print("\n" + "=" * 70)
        print("   🌱 ECOTECH SOLUTIONS - Sistema de Gestión Ambiental 🌱")
        print("=" * 70)
        print("   Programación Orientada a Objeto Seguro")
        print("   Sistema de autenticación y análisis de calidad del aire")
        print("=" * 70 + "\n")
    
    def login(self):
        """
        Gestiona el proceso de autenticación del usuario
        
        Seguridad:
        - Valida credenciales con bcrypt
        - Limita intentos fallidos a 3
        - Cierra el programa tras 3 fallos
        
        Returns:
            bool: True si login exitoso, False si se agotaron intentos
        """
        print("🔐 INICIO DE SESIÓN\n")
        
        while self.intentos_login < self.max_intentos:
            print(f"Intento {self.intentos_login + 1} de {self.max_intentos}")
            print("-" * 40)
            
            nombre_usuario = input("Usuario: ").strip()
            password = input("Contraseña: ").strip()
            
            if not nombre_usuario or not password:
                print("⚠️  Usuario y contraseña son obligatorios\n")
                continue
            
            try:
                # Intentar autenticar con bcrypt
                self.usuario_actual = self.gestor_usuarios.autenticar_usuario(
                    nombre_usuario, password
                )
                
                print(f"\n✓ ¡Bienvenido/a {self.usuario_actual.nombre_usuario}!")
                print(f"✓ Rol: {self.usuario_actual.rol}\n")
                return True
                
            except CredencialesInvalidasException as e:
                self.intentos_login += 1
                intentos_restantes = self.max_intentos - self.intentos_login
                
                print(f"\n✗ Error: {e.mensaje}")
                
                if intentos_restantes > 0:
                    print(f"⚠️  Te quedan {intentos_restantes} intentos\n")
                else:
                    print("\n🚫 ACCESO DENEGADO: Máximo de intentos alcanzado")
                    print("   El programa se cerrará por seguridad...\n")
                    return False
                    
            except Exception as e:
                print(f"\n✗ Error inesperado: {e}\n")
                self.intentos_login += 1
        
        return False
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal de opciones"""
        print("\n" + "=" * 70)
        print("   MENÚ PRINCIPAL")
        print("=" * 70)
        print("   1. Gestionar Usuarios (CRUD)")
        print("   2. Ver Datos Ambientales (API)")
        print("   3. Salir")
        print("=" * 70)
    
    def mostrar_menu_usuarios(self):
        """Muestra el menú de gestión de usuarios"""
        print("\n" + "-" * 70)
        print("   GESTIÓN DE USUARIOS")
        print("-" * 70)
        print("   1. Crear nuevo usuario")
        print("   2. Buscar usuario")
        print("   3. Listar todos los usuarios")
        print("   4. Modificar usuario")
        print("   5. Eliminar usuario")
        print("   6. Volver al menú principal")
        print("-" * 70)
    
    def ejecutar_menu_principal(self):
        """
        Ejecuta el bucle principal del menú
        """
        while True:
            self.mostrar_menu_principal()
            opcion = input("\nSelecciona una opción: ").strip()
            
            if opcion == '1':
                self.ejecutar_menu_usuarios()
            elif opcion == '2':
                self.consultar_datos_ambientales()
            elif opcion == '3':
                self.salir()
                break
            else:
                print("⚠️  Opción no válida. Intenta de nuevo.")
    
    def ejecutar_menu_usuarios(self):
        """
        Ejecuta el bucle del menú de gestión de usuarios
        """
        while True:
            self.mostrar_menu_usuarios()
            opcion = input("\nSelecciona una opción: ").strip()
            
            if opcion == '1':
                self.crear_usuario()
            elif opcion == '2':
                self.buscar_usuario()
            elif opcion == '3':
                self.listar_usuarios()
            elif opcion == '4':
                self.modificar_usuario()
            elif opcion == '5':
                self.eliminar_usuario()
            elif opcion == '6':
                break
            else:
                print("⚠️  Opción no válida. Intenta de nuevo.")
    
    # ========== OPERACIONES CRUD ==========
    
    def crear_usuario(self):
        """Crea un nuevo usuario en el sistema"""
        print("\n--- CREAR NUEVO USUARIO ---\n")
        
        try:
            nombre_usuario = input("Nombre de usuario: ").strip()
            correo = input("Correo electrónico: ").strip()
            password = input("Contraseña: ").strip()
            password_confirm = input("Confirmar contraseña: ").strip()
            rol = input("Rol (usuario/administrador) [usuario]: ").strip() or "usuario"
            
            # Validaciones básicas
            if not all([nombre_usuario, correo, password]):
                print("⚠️  Todos los campos son obligatorios")
                return
            
            if password != password_confirm:
                print("⚠️  Las contraseñas no coinciden")
                return
            
            if len(password) < 6:
                print("⚠️  La contraseña debe tener al menos 6 caracteres")
                return
            
            # Crear objeto Usuario (se hashea automáticamente la contraseña)
            nuevo_usuario = Usuario(
                nombre_usuario=nombre_usuario,
                correo=correo,
                rol=rol,
                password=password
            )
            
            # Agregar a la base de datos
            self.gestor_usuarios.agregar_usuario(nuevo_usuario)
            
        except UsuarioDuplicadoException as e:
            print(f"✗ {e.mensaje}")
        except UsuarioException as e:
            print(f"✗ Error: {e.mensaje}")
        except Exception as e:
            print(f"✗ Error inesperado: {e}")
    
    def buscar_usuario(self):
        """Busca y muestra información de un usuario"""
        print("\n--- BUSCAR USUARIO ---\n")
        
        try:
            nombre_usuario = input("Nombre de usuario a buscar: ").strip()
            
            if not nombre_usuario:
                print("⚠️  Debes ingresar un nombre de usuario")
                return
            
            usuario = self.gestor_usuarios.buscar_usuario_por_nombre(nombre_usuario)
            
            print("\n✓ Usuario encontrado:")
            print("-" * 50)
            print(f"  ID: {usuario.id}")
            print(f"  Usuario: {usuario.nombre_usuario}")
            print(f"  Correo: {usuario.correo}")
            print(f"  Rol: {usuario.rol}")
            print("-" * 50)
            
        except UsuarioNoEncontradoException as e:
            print(f"✗ {e.mensaje}")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def listar_usuarios(self):
        """Lista todos los usuarios del sistema"""
        print("\n--- LISTADO DE USUARIOS ---\n")
        
        try:
            usuarios = self.gestor_usuarios.listar_usuarios()
            
            if not usuarios:
                print("ℹ️  No hay usuarios registrados")
                return
            
            print(f"Total de usuarios: {len(usuarios)}")
            print("-" * 70)
            print(f"{'ID':<5} {'Usuario':<20} {'Correo':<30} {'Rol':<15}")
            print("-" * 70)
            
            for usuario in usuarios:
                print(f"{usuario.id:<5} {usuario.nombre_usuario:<20} {usuario.correo:<30} {usuario.rol:<15}")
            
            print("-" * 70)
            
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def modificar_usuario(self):
        """Modifica los datos de un usuario existente"""
        print("\n--- MODIFICAR USUARIO ---\n")
        
        try:
            id_usuario = input("ID del usuario a modificar: ").strip()
            
            if not id_usuario.isdigit():
                print("⚠️  El ID debe ser un número")
                return
            
            id_usuario = int(id_usuario)
            
            # Verificar que el usuario existe
            usuario = self.gestor_usuarios.buscar_usuario_por_id(id_usuario)
            
            print(f"\nUsuario actual: {usuario.nombre_usuario}")
            print("Deja en blanco los campos que no deseas modificar\n")
            
            nuevo_correo = input(f"Nuevo correo [{usuario.correo}]: ").strip()
            nuevo_rol = input(f"Nuevo rol [{usuario.rol}]: ").strip()
            nueva_password = input("Nueva contraseña [dejar en blanco para no cambiar]: ").strip()
            
            # Solo modificar si al menos un campo fue proporcionado
            if nuevo_correo or nuevo_rol or nueva_password:
                self.gestor_usuarios.modificar_usuario(
                    id_usuario=id_usuario,
                    nuevo_correo=nuevo_correo if nuevo_correo else None,
                    nuevo_rol=nuevo_rol if nuevo_rol else None,
                    nueva_password=nueva_password if nueva_password else None
                )
            else:
                print("ℹ️  No se realizaron cambios")
                
        except UsuarioNoEncontradoException as e:
            print(f"✗ {e.mensaje}")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def eliminar_usuario(self):
        """Elimina un usuario del sistema"""
        print("\n--- ELIMINAR USUARIO ---\n")
        
        try:
            id_usuario = input("ID del usuario a eliminar: ").strip()
            
            if not id_usuario.isdigit():
                print("⚠️  El ID debe ser un número")
                return
            
            id_usuario = int(id_usuario)
            
            # Verificar que el usuario existe
            usuario = self.gestor_usuarios.buscar_usuario_por_id(id_usuario)
            
            # Prevenir auto-eliminación
            if self.usuario_actual and usuario.id == self.usuario_actual.id:
                print("⚠️  No puedes eliminar tu propia cuenta mientras estás autenticado")
                return
            
            # Confirmar eliminación
            confirmacion = input(f"¿Seguro que deseas eliminar a '{usuario.nombre_usuario}'? (s/n): ").strip().lower()
            
            if confirmacion == 's':
                self.gestor_usuarios.eliminar_usuario(id_usuario)
            else:
                print("ℹ️  Operación cancelada")
                
        except UsuarioNoEncontradoException as e:
            print(f"✗ {e.mensaje}")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    # ========== CONSULTA DE API ==========
    
    def consultar_datos_ambientales(self):
        """
        Consulta y muestra datos de calidad del aire
        
        Esta funcionalidad es clave para EcoTech Solutions ya que proporciona
        información en tiempo real sobre contaminación atmosférica, permitiendo
        tomar decisiones informadas sobre estrategias ambientales.
        """
        print("\n--- DATOS AMBIENTALES (API) ---\n")
        
        try:
            ciudad = input("Ingresa la ciudad a consultar [Mexico]: ").strip() or "Mexico"
            
            print("\n⏳ Consultando datos de calidad del aire...\n")
            self.servicio_api.mostrar_datos_aire(ciudad)
            
        except APIException as e:
            print(f"\n✗ Error al consultar API: {e.mensaje}")
        except Exception as e:
            print(f"\n✗ Error inesperado: {e}")
        
        input("\n\nPresiona Enter para continuar...")
    
    # ========== SALIDA ==========
    
    def salir(self):
        """Cierra la aplicación de forma ordenada"""
        print("\n" + "=" * 70)
        print("   Gracias por usar EcoTech Solutions")
        print("   ¡Juntos construimos un futuro más verde! 🌱")
        print("=" * 70 + "\n")
    
    def iniciar(self):
        """
        Método principal que inicia la aplicación
        
        Flujo:
        1. Mostrar banner
        2. Verificar conexión a BD
        3. Login (máximo 3 intentos)
        4. Si login exitoso, mostrar menú
        5. Si falla, cerrar programa
        """
        self.mostrar_banner()
        
        # Verificar conexión a la base de datos
        print("🔍 Verificando conexión a la base de datos...")
        if not verificar_conexion():
            print("\n✗ No se pudo conectar a la base de datos")
            print("   Verifica que MySQL esté corriendo y que las credenciales en .env sean correctas")
            sys.exit(1)
        
        print()  # Línea en blanco
        
        # Proceso de login
        if not self.login():
            sys.exit(1)
        
        # Si login exitoso, mostrar menú
        try:
            self.ejecutar_menu_principal()
        except KeyboardInterrupt:
            print("\n\n⚠️  Programa interrumpido por el usuario")
            self.salir()
        except Exception as e:
            print(f"\n✗ Error crítico: {e}")
            sys.exit(1)


# ============================================
# PUNTO DE ENTRADA DE LA APLICACIÓN
# ============================================

def main():
    """
    Función principal que crea e inicia la aplicación
    """
    app = AplicacionEcoTech()
    app.iniciar()


if __name__ == "__main__":
    main()
