"""
Script auxiliar para generar hashes de contraseñas con bcrypt
Útil para crear usuarios iniciales o resetear contraseñas
"""
import bcrypt

def generar_hash(password):
    """
    Genera un hash bcrypt para la contraseña proporcionada
    
    Args:
        password (str): Contraseña en texto plano
        
    Returns:
        str: Hash bcrypt de la contraseña
    """
    # Convertir la contraseña a bytes
    password_bytes = password.encode('utf-8')
    
    # Generar salt y hash (factor de costo 12 para seguridad óptima)
    salt = bcrypt.gensalt(rounds=12)
    hash_generado = bcrypt.hashpw(password_bytes, salt)
    
    # Retornar como string
    return hash_generado.decode('utf-8')

if __name__ == "__main__":
    print("=" * 60)
    print("Generador de Hashes Bcrypt - EcoTech Solutions")
    print("=" * 60)
    
    # Generar hash para el admin inicial
    password_admin = "admin123"
    hash_admin = generar_hash(password_admin)
    
    print(f"\nContraseña: {password_admin}")
    print(f"Hash generado: {hash_admin}")
    print("\n" + "=" * 60)
    
    # Permitir generar hashes personalizados
    print("\n¿Deseas generar otro hash? (s/n): ", end="")
    respuesta = input().strip().lower()
    
    while respuesta == 's':
        nueva_password = input("Ingresa la contraseña: ").strip()
        if nueva_password:
            nuevo_hash = generar_hash(nueva_password)
            print(f"\nHash generado: {nuevo_hash}\n")
        
        print("¿Generar otro? (s/n): ", end="")
        respuesta = input().strip().lower()
    
    print("\n¡Listo! Puedes usar estos hashes en tu base de datos.")
