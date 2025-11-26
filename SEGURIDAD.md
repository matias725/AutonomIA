# 🛡️ SEGURIDAD Y PROTECCIÓN DE DATOS SENSIBLES

## 📋 Resumen

Este documento explica cómo EcoTech Solutions protege datos sensibles y credenciales en el proyecto.

---

## 🔐 Datos Sensibles Protegidos

### 1. **Credenciales de Base de Datos**
- ❌ **NO hardcodeadas** en el código fuente
- ✅ **Almacenadas en** `.env` (archivo local)
- ✅ **Excluidas de Git** mediante `.gitignore`

**Ubicación:** `.env`
```env
DB_HOST=localhost
DB_NAME=pepe123
DB_USER=root
DB_PASSWORD=tu_password
DB_PORT=3306
```

**Carga segura en código:**
```python
# db.py
import os
from dotenv import load_dotenv

load_dotenv()

self.host = os.getenv('DB_HOST', 'localhost')
self.database = os.getenv('DB_NAME', 'pepe123')
self.user = os.getenv('DB_USER', 'root')
self.password = os.getenv('DB_PASSWORD', '')
```

### 2. **Token de API Externa**
- ❌ **NO expuesto** en el código
- ✅ **Almacenado en** `.env`
- ✅ **Valor por defecto 'demo'** solo para pruebas

**Ubicación:** `.env`
```env
API_TOKEN=tu_token_real_aqui
```

**Uso en código:**
```python
# api.py
self.token = os.getenv('API_TOKEN', 'demo')
url = f"{self.url}/feed/{ciudad}/?token={self.token}"
```

### 3. **Contraseñas de Usuarios**
- ❌ **NUNCA en texto plano**
- ✅ **Hasheadas con bcrypt** (factor de costo 12)
- ✅ **Almacenadas como hash** en base de datos (VARCHAR 255)

**Implementación:**
```python
# modelos.py
import bcrypt

def set_password(self, password):
    pw_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)  # Factor de costo 12
    self._pass_hash = bcrypt.hashpw(pw_bytes, salt).decode('utf-8')

def check_password(self, password):
    pw_bytes = password.encode('utf-8')
    hash_bytes = self._pass_hash.encode('utf-8')
    return bcrypt.checkpw(pw_bytes, hash_bytes)
```

**Ejemplo de hash en BD:**
```
$2b$12$96a8CGK7RivIM6IkB8i78.YaTr3NCQ96M3PzxP7x.I2cO.pkpEsWO
```

---

## 🚫 Archivo .gitignore

El archivo `.gitignore` previene que datos sensibles se suban a Git:

```gitignore
# Variables de entorno (DATOS SENSIBLES)
.env

# Archivos de Python
__pycache__/
*.pyc
*.pyo
*.pyd

# Entorno virtual
.venv/
venv/
env/
```

---

## 📚 Librerías de Seguridad Utilizadas

### 1. **bcrypt** (Hashing de Contraseñas)
```bash
pip install bcrypt==4.1.2
```

**Características:**
- Algoritmo Blowfish adaptativo
- Salt automático por cada hash
- Protección contra ataques de fuerza bruta
- Factor de costo configurable (12 en este proyecto)

### 2. **python-dotenv** (Gestión de Variables de Entorno)
```bash
pip install python-dotenv==1.0.0
```

**Características:**
- Carga variables desde archivo `.env`
- Separación de configuración y código
- Valores por defecto con `os.getenv('VAR', 'default')`
- Compatible con diferentes entornos (dev, prod)

### 3. **mysql-connector-python** (Prevención SQL Injection)
```bash
pip install mysql-connector-python==8.2.0
```

**Características:**
- Prepared statements automáticos
- Parámetros escapados: `cursor.execute(query, (param1, param2))`
- Protección contra inyección SQL

---

## 🔒 Buenas Prácticas Implementadas

### ✅ 1. Separación de Configuración y Código
- Credenciales en `.env`, NO en archivos `.py`
- Archivo `.env.example` como plantilla (sin valores reales)

### ✅ 2. Principio de Mínimo Privilegio
- Usuario de BD con permisos específicos (no usar root en producción)
- Validación de roles en la aplicación (usuario/administrador)

### ✅ 3. Encriptación de Datos Sensibles
- Contraseñas hasheadas con bcrypt (irreversible)
- Factor de costo 12 (balance seguridad/rendimiento)

### ✅ 4. Validación de Entrada
- Verificación de campos obligatorios
- Sanitización de inputs para prevenir SQL injection
- Manejo de errores con excepciones personalizadas

### ✅ 5. Autenticación Segura
- Límite de 3 intentos de login
- Mensajes de error genéricos (no revelar si usuario existe)
- Session management con usuario actual

### ✅ 6. Protección de API
- Token en variable de entorno
- Timeout de 10 segundos en requests
- Manejo de errores de conexión y HTTP

---

## 📝 Checklist de Seguridad

- [x] Contraseñas hasheadas con bcrypt (factor 12)
- [x] Credenciales en archivo .env
- [x] .env incluido en .gitignore
- [x] Prepared statements para SQL
- [x] Token de API protegido
- [x] Validación de inputs
- [x] Manejo de excepciones
- [x] Límite de intentos de login
- [x] Dependencias actualizadas en requirements.txt
- [x] Documentación de seguridad

---

## 🎓 Cumplimiento de Requisitos Académicos

### ✅ Ocultamiento de Datos Sensibles
1. **Credenciales DB:** `.env` + `python-dotenv`
2. **Token API:** `.env` + `os.getenv()`
3. **Passwords:** bcrypt hashing (irreversible)
4. **.gitignore:** Excluye `.env` de repositorio

### ✅ Uso de Entorno Virtual
```bash
# Crear entorno virtual
python -m venv .venv

# Activar (Windows)
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### ✅ Archivo de Dependencias
**requirements.txt:**
```
bcrypt==4.1.2
mysql-connector-python==8.2.0
python-dotenv==1.0.0
requests==2.31.0
```

---

## 📖 Referencias

- [bcrypt Documentation](https://github.com/pyca/bcrypt/)
- [python-dotenv Guide](https://github.com/theskumar/python-dotenv)
- [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

---

## 👨‍💻 Autor

**Matias**  
Programación Orientada a Objeto Seguro  
Fecha: Noviembre 2025
