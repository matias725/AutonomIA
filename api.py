"""
Módulo de API Externa - EcoTech Solutions
Consume datos de calidad del aire de la API pública AQICN (Air Quality Index China)
Esta API NO requiere clave y proporciona datos de contaminación del aire en tiempo real

PROHIBICIÓN: No usar OpenWeatherMap según requisitos del proyecto

Justificación empresarial para EcoTech Solutions:
- Los datos de calidad del aire son críticos para decisiones ambientales
- Permite evaluar niveles de contaminación en tiempo real
- Ayuda a planificar estrategias de reducción de emisiones
- Facilita recomendaciones basadas en datos científicos actualizados
"""
import requests
import json
from datetime import datetime


# ============================================
# EXCEPCIÓN PERSONALIZADA PARA API
# ============================================

class APIException(Exception):
    """
    Excepción personalizada para errores relacionados con la API externa
    """
    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


# ============================================
# CLASE SERVICIO EXTERNO
# ============================================

class ServicioExterno:
    """
    Clase que gestiona el consumo de la API de calidad del aire
    
    Usa la API pública AQICN para obtener datos de contaminación atmosférica
    Esta información es vital para EcoTech Solutions en la toma de decisiones
    sobre estrategias ambientales.
    
    API Utilizada: AQICN (Air Quality Open Data Platform)
    Endpoints: https://api.waqi.info/
    """
    
    def __init__(self):
        """
        Inicializa el servicio con la URL base de la API
        
        Nota: Esta API pública no requiere autenticación para endpoints básicos
        En producción, se usaría un token almacenado en .env
        """
        self.base_url = "https://api.waqi.info"
        # Para uso completo de la API, registrarse en: https://aqicn.org/data-platform/token/
        self.token = "demo"  # Token demo para testing (limitado)
    
    def obtener_calidad_aire_ciudad(self, ciudad="Mexico"):
        """
        Obtiene datos de calidad del aire para una ciudad específica
        
        Args:
            ciudad (str): Nombre de la ciudad (por defecto Mexico)
            
        Returns:
            dict: Diccionario con datos de calidad del aire
            
        Raises:
            APIException: Si hay error en la consulta a la API
            
        Impacto para EcoTech:
        - Monitorear contaminación en zonas de interés
        - Evaluar eficacia de iniciativas de reducción de emisiones
        - Generar alertas cuando la calidad del aire es peligrosa
        """
        try:
            # Construir URL del endpoint
            url = f"{self.base_url}/feed/{ciudad}/?token={self.token}"
            
            # Realizar petición GET
            print(f"🌍 Consultando calidad del aire en {ciudad}...")
            response = requests.get(url, timeout=10)
            
            # Verificar que la respuesta sea exitosa
            response.raise_for_status()
            
            # Parsear JSON
            datos = response.json()
            
            # Verificar que la respuesta sea válida
            if datos.get('status') != 'ok':
                raise APIException(f"Error en API: {datos.get('data', 'Respuesta inválida')}")
            
            # Extraer información relevante
            info_aire = self._procesar_datos_aire(datos['data'])
            return info_aire
            
        except requests.exceptions.Timeout:
            raise APIException("Tiempo de espera agotado al conectar con la API")
        except requests.exceptions.ConnectionError:
            raise APIException("No se pudo conectar con el servicio de calidad del aire")
        except requests.exceptions.HTTPError as e:
            raise APIException(f"Error HTTP: {e}")
        except json.JSONDecodeError:
            raise APIException("Error al procesar la respuesta JSON de la API")
        except Exception as e:
            raise APIException(f"Error inesperado: {e}")
    
    def _procesar_datos_aire(self, datos):
        """
        Procesa y estructura los datos recibidos de la API
        
        Args:
            datos (dict): Datos crudos de la API
            
        Returns:
            dict: Datos procesados y estructurados
        """
        # Extraer índice AQI (Air Quality Index)
        aqi = datos.get('aqi', 'N/A')
        
        # Extraer estación de monitoreo
        estacion = datos.get('city', {}).get('name', 'Desconocida')
        
        # Extraer coordenadas
        coordenadas = datos.get('city', {}).get('geo', [])
        
        # Extraer información de contaminantes
        iaqi = datos.get('iaqi', {})
        
        # Extraer fecha/hora de medición
        tiempo = datos.get('time', {}).get('s', 'N/A')
        
        # Construir diccionario estructurado
        info_procesada = {
            'aqi': aqi,
            'estacion': estacion,
            'coordenadas': coordenadas,
            'clasificacion': self._clasificar_aqi(aqi),
            'nivel_peligro': self._nivel_peligro_aqi(aqi),
            'contaminantes': {
                'pm25': iaqi.get('pm25', {}).get('v', 'N/A'),  # Material particulado 2.5
                'pm10': iaqi.get('pm10', {}).get('v', 'N/A'),  # Material particulado 10
                'o3': iaqi.get('o3', {}).get('v', 'N/A'),      # Ozono
                'no2': iaqi.get('no2', {}).get('v', 'N/A'),    # Dióxido de nitrógeno
                'so2': iaqi.get('so2', {}).get('v', 'N/A'),    # Dióxido de azufre
                'co': iaqi.get('co', {}).get('v', 'N/A')       # Monóxido de carbono
            },
            'temperatura': iaqi.get('t', {}).get('v', 'N/A'),
            'humedad': iaqi.get('h', {}).get('v', 'N/A'),
            'presion': iaqi.get('p', {}).get('v', 'N/A'),
            'tiempo_medicion': tiempo
        }
        
        return info_procesada
    
    def _clasificar_aqi(self, aqi):
        """
        Clasifica el índice AQI según estándares internacionales
        
        Args:
            aqi (int): Índice de calidad del aire
            
        Returns:
            str: Clasificación textual
        """
        if aqi == 'N/A':
            return 'Desconocido'
        
        try:
            aqi = int(aqi)
            if aqi <= 50:
                return 'Bueno'
            elif aqi <= 100:
                return 'Moderado'
            elif aqi <= 150:
                return 'Dañino para grupos sensibles'
            elif aqi <= 200:
                return 'Dañino'
            elif aqi <= 300:
                return 'Muy dañino'
            else:
                return 'Peligroso'
        except (ValueError, TypeError):
            return 'Desconocido'
    
    def _nivel_peligro_aqi(self, aqi):
        """
        Determina el nivel de peligro basado en el AQI
        
        Args:
            aqi (int): Índice de calidad del aire
            
        Returns:
            str: Nivel de peligro (BAJO, MEDIO, ALTO, CRÍTICO)
        """
        if aqi == 'N/A':
            return 'DESCONOCIDO'
        
        try:
            aqi = int(aqi)
            if aqi <= 50:
                return '🟢 BAJO'
            elif aqi <= 100:
                return '🟡 MEDIO'
            elif aqi <= 200:
                return '🟠 ALTO'
            else:
                return '🔴 CRÍTICO'
        except (ValueError, TypeError):
            return 'DESCONOCIDO'
    
    def mostrar_datos_aire(self, ciudad="Mexico"):
        """
        Obtiene y muestra de forma amigable los datos de calidad del aire
        
        Args:
            ciudad (str): Ciudad a consultar
            
        Esta función presenta los datos de manera clara para que EcoTech Solutions
        pueda tomar decisiones informadas sobre estrategias ambientales.
        """
        try:
            datos = self.obtener_calidad_aire_ciudad(ciudad)
            
            print("\n" + "=" * 70)
            print(" 🌍 INFORME DE CALIDAD DEL AIRE - EcoTech Solutions")
            print("=" * 70)
            
            print(f"\n📍 Estación de Monitoreo: {datos['estacion']}")
            print(f"📅 Fecha/Hora: {datos['tiempo_medicion']}")
            
            if datos['coordenadas']:
                print(f"🗺️  Coordenadas: {datos['coordenadas']}")
            
            print(f"\n🔢 Índice AQI: {datos['aqi']}")
            print(f"📊 Clasificación: {datos['clasificacion']}")
            print(f"⚠️  Nivel de Peligro: {datos['nivel_peligro']}")
            
            print("\n📈 CONTAMINANTES DETECTADOS:")
            print("-" * 70)
            
            contaminantes = datos['contaminantes']
            print(f"  • PM2.5 (Partículas finas):        {contaminantes['pm25']}")
            print(f"  • PM10 (Partículas suspendidas):   {contaminantes['pm10']}")
            print(f"  • O₃ (Ozono):                      {contaminantes['o3']}")
            print(f"  • NO₂ (Dióxido de nitrógeno):      {contaminantes['no2']}")
            print(f"  • SO₂ (Dióxido de azufre):         {contaminantes['so2']}")
            print(f"  • CO (Monóxido de carbono):        {contaminantes['co']}")
            
            print("\n🌡️  CONDICIONES METEOROLÓGICAS:")
            print("-" * 70)
            print(f"  • Temperatura: {datos['temperatura']}°C")
            print(f"  • Humedad: {datos['humedad']}%")
            print(f"  • Presión: {datos['presion']} hPa")
            
            print("\n💡 ANÁLISIS PARA ECOTECH SOLUTIONS:")
            print("-" * 70)
            self._generar_recomendaciones(datos['aqi'])
            
            print("\n" + "=" * 70)
            
        except APIException as e:
            print(f"\n✗ Error al obtener datos: {e.mensaje}")
    
    def _generar_recomendaciones(self, aqi):
        """
        Genera recomendaciones empresariales basadas en el AQI
        
        Args:
            aqi (int/str): Índice de calidad del aire
        """
        try:
            aqi_val = int(aqi) if aqi != 'N/A' else 0
            
            if aqi_val <= 50:
                print("  ✓ Calidad del aire óptima para actividades al aire libre")
                print("  ✓ Condiciones favorables para iniciativas de energía solar")
                print("  ✓ Momento ideal para campañas de concientización ambiental")
            elif aqi_val <= 100:
                print("  ⚠ Calidad del aire aceptable, monitorear tendencias")
                print("  ⚠ Considerar estrategias preventivas de reducción de emisiones")
            elif aqi_val <= 200:
                print("  ⚠ Alerta: Implementar medidas de mitigación inmediatas")
                print("  ⚠ Limitar actividades que generen más contaminación")
                print("  ⚠ Activar protocolos de protección para grupos vulnerables")
            else:
                print("  🚨 CRÍTICO: Activar plan de emergencia ambiental")
                print("  🚨 Suspender actividades contaminantes no esenciales")
                print("  🚨 Coordinar con autoridades para acciones correctivas")
                
        except (ValueError, TypeError):
            print("  ℹ️  No hay suficientes datos para generar recomendaciones")
    
    def obtener_datos_json(self, ciudad="Mexico"):
        """
        Retorna los datos en formato JSON para integración con otros sistemas
        
        Args:
            ciudad (str): Ciudad a consultar
            
        Returns:
            str: Datos en formato JSON
        """
        try:
            datos = self.obtener_calidad_aire_ciudad(ciudad)
            return json.dumps(datos, indent=2, ensure_ascii=False)
        except APIException as e:
            return json.dumps({'error': str(e.mensaje)}, indent=2)


# ============================================
# FUNCIÓN AUXILIAR PARA TESTING
# ============================================

def probar_api():
    """
    Función de prueba para verificar el funcionamiento de la API
    """
    print("Iniciando prueba del servicio de API...\n")
    
    servicio = ServicioExterno()
    
    # Probar con diferentes ciudades
    ciudades = ["Mexico", "Beijing", "London"]
    
    for ciudad in ciudades:
        print(f"\n--- Probando: {ciudad} ---")
        try:
            servicio.mostrar_datos_aire(ciudad)
        except Exception as e:
            print(f"Error: {e}")
        
        input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    # Ejecutar pruebas si se ejecuta directamente
    probar_api()
