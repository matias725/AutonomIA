# Sistema de Gestión de Empleados — EcoTech Solutions

Proyecto de evaluación (Evaluación Sumativa 4).

Descripción:
- Aplicación de escritorio en Python para gestionar empleados, departamentos, proyectos y registros de tiempo (timesheets).

Requisitos técnicos implementados:
- Programación orientada a objetos (herencia y polimorfismo): `Persona` -> `Empleado`.
- Seguridad: contraseñas almacenadas como hash SHA-256.
- Base de datos: SQLite (`ecotech.db`).
- Validación de emails y campos no vacíos.
- Reglas de negocio: cada empleado pertenece a 1 departamento; empleado puede estar en varios proyectos; registro de horas.

Archivos principales:
- `models.py` — clases POO.
- `db.py` — inicialización de BD y operaciones CRUD.
- `validaciones.py` — funciones de validación.
- `gui.py` — interfaz con `tkinter` (crear/editar/eliminar empleados, crear/eliminar departamentos y proyectos, asignar gerente, registrar horas).
- `main.py` — punto de entrada.
- `datos_ejemplo.py` — script para poblar datos de ejemplo.
- `tests/` — pruebas unitarias para `db` y `validaciones`.

Cómo ejecutar (Windows PowerShell):

1) Crear/activar entorno virtual (opcional):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Inicializar la base de datos y ejecutar la GUI:

```powershell
python main.py
```

3) (Opcional) Poblar datos de ejemplo:

```powershell
python datos_ejemplo.py
```

Ejecutar pruebas unitarias (recomendado antes de entregar):

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Características implementadas (resumen técnico):

- Herencia y polimorfismo: `Persona` -> `Empleado` (método `obtener_descripcion` sobrescrito).
- Seguridad: contraseñas almacenadas como hash SHA-256 usando `db.hash_contrasena`.
- Base de datos: SQLite con tablas `empleados`, `departamentos`, `proyectos`, `proyectos_empleados`, `registros_tiempo`.
- Validaciones: `validaciones.py` valida email, campos no vacíos, fecha ISO y rango de horas.
- Reglas de negocio aplicadas: empleado pertenece a un solo departamento; empleado puede estar en varios proyectos; se registran horas por proyecto y fecha.
- GUI: creación, edición y eliminación de empleados; creación y eliminación de departamentos y proyectos; asignación de gerente a departamento; registro de horas (timesheets).

Notas y recomendaciones:

- `tkinter` suele venir con Python en Windows. Si la interfaz no aparece, verifique la instalación de Python.
- Para pruebas aisladas de la base de datos, las pruebas usan una base temporal.
- Todos los archivos contienen comentarios en español para la evaluación.

Si quieres, puedo:
- Empaquetar el proyecto en un archivo ZIP listo para entregar.
- Mejorar la GUI usando `ttk.Treeview` para tablas con columnas y filtros.
- Añadir más pruebas unitarias (GUI o casos de borde).


Notas:
- `tkinter` suele incluirse en la instalación estándar de Python en Windows.
- Todos los comentarios están en español para la evaluación.
