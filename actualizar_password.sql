-- Script para actualizar la contraseña del usuario admin
-- Ejecuta este script en MySQL Workbench, phpMyAdmin o línea de comandos

USE pepe123;

-- Actualizar el hash de la contraseña del usuario admin
UPDATE usuarios 
SET password = '$2b$12$Rab1Q7PyXEsHVG2O.8gY1.GMNXKGuri277DhY8Y.7Dt2k.q2tTAVm' 
WHERE nombre_usuario = 'admin';

-- Verificar que se actualizó correctamente
SELECT nombre_usuario, correo, rol, 'Contraseña actualizada' AS status 
FROM usuarios 
WHERE nombre_usuario = 'admin';
