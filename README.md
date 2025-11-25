# 🌱 EcoTech Solutions - Sistema de Gestión Ambiental

**Proyecto Final - Programación Orientada a Objeto Seguro**

Sistema de gestión de usuarios con autenticación segura y consulta de datos ambientales en tiempo real.

---

## 📋 Descripción del Proyecto

EcoTech Solutions es una aplicación de consola desarrollada en Python que permite:

- ✅ Gestión completa de usuarios (CRUD)
- 🔐 Autenticación segura con bcrypt
- 🌍 Consulta de calidad del aire en tiempo real
- 📊 Análisis de contaminantes atmosféricos
- 🛡️ Manejo robusto de errores con excepciones personalizadas

---

## 🎯 Requisitos Técnicos

### Lenguaje
- Python 3.8 o superior

### Base de Datos
- MySQL 5.7 o superior

### Librerías Necesarias
- `mysql-connector-python` - Conexión a MySQL
- `bcrypt` - Hasheo seguro de contraseñas
- `requests` - Consumo de API REST
- `python-dotenv` - Gestión de variables de entorno

---

## 🚀 Instalación y Configuración

### Paso 1: Clonar o Descargar el Proyecto

```bash
# Si tienes el proyecto en un ZIP, descomprímelo
# Si está en Git:
git clone <url-del-repositorio>
cd programacion-3-prueba
```

### Paso 2: Instalar Dependencias

Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

Esto instalará:
- mysql-connector-python==8.2.0
- bcrypt==4.1.2
- requests==2.31.0
- python-dotenv==1.0.0

### Paso 3: Configurar MySQL

1. **Iniciar MySQL Server**
   - Si usas XAMPP: Inicia el módulo MySQL
   - Si usas MySQL Workbench: Asegúrate de que el servidor esté corriendo

2. **Ejecutar el Script SQL**

   Opción A - Línea de comandos:
   ```bash
   mysql -u root -p < database.sql
   ```

   Opción B - MySQL Workbench:
   - Abre MySQL Workbench
   - Conecta a tu servidor local
   - File → Open SQL Script → Selecciona `database.sql`
   - Ejecuta el script (⚡ icono de rayo)

   Opción C - phpMyAdmin (XAMPP):
   - Abre phpMyAdmin (http://localhost/phpmyadmin)
   - Clic en "Importar"
   - Selecciona `database.sql`
   - Clic en "Continuar"

3. **Verificar la Creación**
   
   Deberías ver:
   - Base de datos: `ecotech_db`
   - Tabla: `usuarios`
   - Usuario inicial: `admin` (contraseña: `admin123`)

### Paso 4: Configurar Variables de Entorno

1. **Copia el archivo de ejemplo:**
   ```bash
   copy .env.example .env
   ```

2. **Edita el archivo `.env`** con tus credenciales de MySQL:

   ```env
   DB_HOST=localhost
   DB_NAME=ecotech_db
   DB_USER=root
   DB_PASSWORD=        # Tu contraseña de MySQL (vacía si no tienes)
   DB_PORT=3306
   ```

   **Importante:** Si usas XAMPP y no cambiaste la configuración, la contraseña de `root` está vacía por defecto.

### Paso 5: ¡Ejecutar la Aplicación!

```bash
python main.py
```

---

## 🔑 Credenciales de Acceso

### Usuario Administrador Inicial

- **Usuario:** `admin`
- **Contraseña:** `admin123`

⚠️ **Importante:** Cambia esta contraseña después del primer inicio de sesión por seguridad.

---

## 📁 Estructura del Proyecto

```
programacion-3-prueba/
│
├── main.py              # Aplicación principal (punto de entrada)
├── db.py                # Módulo de conexión a MySQL (Singleton)
├── modelos.py           # Clases Usuario, GestorUsuarios y excepciones
├── api.py               # Servicio de API externa (calidad del aire)
├── generar_hash.py      # Utilidad para generar hashes bcrypt
│
├── database.sql         # Script SQL para crear la base de datos
├── requirements.txt     # Dependencias del proyecto
├── .env.example         # Plantilla de variables de entorno
├── .env                 # Archivo de configuración (NO subir a Git)
│
└── README.md            # Este archivo
```

---

## 🎮 Uso de la Aplicación

### 1. Login

Al ejecutar la aplicación, se solicitarán credenciales:

```
Usuario: admin
Contraseña: admin123
```

**Seguridad:** Tienes máximo 3 intentos. Después de 3 fallos, el programa se cierra automáticamente.

### 2. Menú Principal

```
═══════════════════════════════════════════════════════════════════
   MENÚ PRINCIPAL
═══════════════════════════════════════════════════════════════════
   1. Gestionar Usuarios (CRUD)
   2. Ver Datos Ambientales (API)
   3. Salir
═══════════════════════════════════════════════════════════════════
```

### 3. Gestión de Usuarios (Opción 1)

#### Crear Usuario
- Ingresa nombre de usuario, correo, contraseña y rol
- La contraseña se hashea automáticamente con bcrypt (factor 12)
- Validación de contraseñas (mínimo 6 caracteres, confirmación)

#### Buscar Usuario
- Busca por nombre de usuario
- Muestra toda la información excepto la contraseña

#### Listar Usuarios
- Muestra todos los usuarios en formato tabla
- Incluye ID, usuario, correo y rol

#### Modificar Usuario
- Modifica correo, rol o contraseña
- Deja en blanco lo que no quieras cambiar
- La nueva contraseña se hashea automáticamente

#### Eliminar Usuario
- Elimina un usuario por ID
- Solicita confirmación antes de borrar
- No puedes eliminarte a ti mismo mientras estás autenticado

### 4. Datos Ambientales (Opción 2)

Consulta datos de calidad del aire en tiempo real:

```
Ciudad: Mexico

📍 Estación de Monitoreo: Mexico City...
🔢 Índice AQI: 85
📊 Clasificación: Moderado
⚠️  Nivel de Peligro: 🟡 MEDIO

📈 CONTAMINANTES DETECTADOS:
  • PM2.5 (Partículas finas): ...
  • PM10 (Partículas suspendidas): ...
  • O₃ (Ozono): ...
  ...
```

**API Utilizada:** AQICN (Air Quality Index)
- Datos en tiempo real
- No usa OpenWeatherMap (prohibido en requisitos)
- Gratuita y sin necesidad de registro para uso básico

---

## 🛡️ Características de Seguridad

### 1. Contraseñas
- ✅ Hasheadas con bcrypt (factor de costo 12)
- ✅ Nunca se almacenan en texto plano
- ✅ Salt único para cada contraseña
- ✅ Resistente a ataques de fuerza bruta

### 2. Base de Datos
- ✅ Credenciales en archivo .env (no en código)
- ✅ Consultas preparadas (prevención de SQL Injection)
- ✅ Patrón Singleton para conexión única

### 3. Autenticación
- ✅ Límite de 3 intentos de login
- ✅ Cierre automático tras fallos
- ✅ Validación de sesión activa

### 4. Manejo de Errores
- ✅ Excepciones personalizadas
- ✅ Bloques try-except en todas las operaciones críticas
- ✅ Mensajes de error informativos sin exponer datos sensibles

---

## 🔧 Solución de Problemas

### Error: "No se pudo conectar a la base de datos"

**Causa:** MySQL no está corriendo o credenciales incorrectas

**Solución:**
1. Verifica que MySQL esté iniciado
2. Revisa las credenciales en el archivo `.env`
3. Prueba conectarte manualmente: `mysql -u root -p`

### Error: "No se ha podido resolver la importación mysql.connector"

**Causa:** La librería no está instalada

**Solución:**
```bash
pip install mysql-connector-python
```

### Error: "No module named 'bcrypt'"

**Causa:** bcrypt no está instalado

**Solución:**
```bash
pip install bcrypt
```

### Error al importar librerías después de instalar

**Causa:** Múltiples instalaciones de Python

**Solución:**
1. Verifica tu versión: `python --version`
2. Reinstala dependencias: `pip install -r requirements.txt --force-reinstall`
3. Si usas VS Code, verifica el intérprete: Ctrl+Shift+P → "Python: Select Interpreter"

### La API no devuelve datos

**Causa:** Problema de conexión o ciudad no encontrada

**Solución:**
1. Verifica tu conexión a Internet
2. Prueba con ciudades conocidas: Mexico, Beijing, London, Paris
3. El token "demo" tiene limitaciones, considera registrarte en https://aqicn.org/data-platform/token/

---

## 📊 Paradigma de Programación

Este proyecto implementa **100% Programación Orientada a Objetos**:

### Clases Principales

1. **ConexionDB** (db.py)
   - Patrón Singleton
   - Gestiona conexión única a MySQL

2. **Usuario** (modelos.py)
   - Modelo de datos
   - Encapsula lógica de contraseñas

3. **GestorUsuarios** (modelos.py)
   - Implementa CRUD completo
   - Gestiona autenticación

4. **ServicioExterno** (api.py)
   - Consume API REST
   - Procesa datos ambientales

5. **AplicacionEcoTech** (main.py)
   - Clase principal
   - Coordina flujo de la aplicación

### Excepciones Personalizadas

- `UsuarioException` - Base para errores de usuario
- `UsuarioNoEncontradoException` - Usuario no existe
- `UsuarioDuplicadoException` - Usuario/correo duplicado
- `CredencialesInvalidasException` - Login fallido
- `APIException` - Errores en API externa

---

## 🧪 Generar Hashes de Contraseñas

Si necesitas crear contraseñas hasheadas para insertar directamente en la BD:

```bash
python generar_hash.py
```

El script te permitirá:
1. Ver el hash de la contraseña del admin
2. Generar hashes personalizados
3. Copiar los hashes para usarlos en SQL

---

## 🌐 API Externa Utilizada

### AQICN (Air Quality Index)

**Endpoint:** https://api.waqi.info/feed/{ciudad}/?token={token}

**Datos Proporcionados:**
- Índice AQI (Air Quality Index)
- PM2.5, PM10 (Material particulado)
- O₃ (Ozono)
- NO₂ (Dióxido de nitrógeno)
- SO₂ (Dióxido de azufre)
- CO (Monóxido de carbono)
- Temperatura, humedad, presión

**Justificación para EcoTech:**
- Monitoreo de contaminación en tiempo real
- Base para decisiones ambientales
- Alertas de calidad del aire
- Evaluación de impacto de iniciativas ecológicas

---

## 👨‍💻 Autor

Proyecto desarrollado para la asignatura **Programación Orientada a Objeto Seguro**

---

## 📝 Licencia

Este proyecto es con fines educativos.

---

## 🤝 Contribuciones

Si encuentras un bug o tienes una sugerencia:
1. Documenta el problema
2. Propón una solución
3. Comparte tu feedback

---

## 🎓 Aprendizajes Clave

Este proyecto demuestra:

✅ Arquitectura basada en clases y objetos (POO)
✅ Seguridad en autenticación (bcrypt, intentos limitados)
✅ Gestión segura de credenciales (.env)
✅ CRUD completo en MySQL con consultas preparadas
✅ Consumo de APIs REST externas
✅ Manejo robusto de errores con excepciones personalizadas
✅ Patrón Singleton para gestión de recursos
✅ Separación de responsabilidades (módulos independientes)

---

## 📞 Soporte

Si tienes problemas durante la instalación o ejecución:

1. Verifica que cumples todos los requisitos técnicos
2. Revisa la sección "Solución de Problemas"
3. Asegúrate de haber seguido todos los pasos en orden

---

**¡Gracias por usar EcoTech Solutions! 🌱**

*Juntos construimos un futuro más verde* 🌍
