"""
Punto de entrada de la aplicación.
Inicializa la base de datos y lanza la interfaz gráfica.
"""
import db
from gui import iniciar_aplicacion


def main():
    # Inicializar la base de datos (archivo ecotech.db en el mismo directorio)
    db.inicializar_bd()
    iniciar_aplicacion()


if __name__ == "__main__":
    main()
