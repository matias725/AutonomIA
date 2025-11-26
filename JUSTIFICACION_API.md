# 🌍 JUSTIFICACIÓN DE LA API - AQICN World Air Quality Index

## 📋 Información de la API

**Nombre:** AQICN - World Air Quality Index  
**URL:** https://aqicn.org/api/  
**Tipo:** REST API  
**Formato:** JSON  
**Autenticación:** Token-based  
**Costo:** Gratuito (con limitaciones)

---

## 🎯 ¿Por qué esta API?

### 1. **Relevancia para EcoTech Solutions**

EcoTech Solutions es una empresa de **gestión ambiental** que proporciona:
- Consultoría en reducción de emisiones
- Análisis de impacto ambiental
- Estrategias de sostenibilidad corporativa
- Monitoreo de calidad del aire

**La API de calidad del aire es FUNDAMENTAL** porque:
- Proporciona datos REALES de contaminación atmosférica
- Cubre más de 100 países y 12,000+ estaciones de monitoreo
- Incluye contaminantes clave: PM2.5, PM10, O3, NO2, SO2, CO
- Datos actualizados cada hora
- Información geolocalizada (coordenadas GPS)

### 2. **Aporte al Negocio**

#### 📊 **Toma de Decisiones Basada en Datos**
```python
# Ejemplo de uso en el proyecto
info = api.get_calidad_aire("Mexico")

# Retorna:
{
    'aqi': 89,                    # Índice de calidad del aire
    'clasificacion': 'Moderado',   # Bueno/Moderado/Insalubre/etc
    'contaminantes': {
        'pm25': 45,               # Partículas finas (principal indicador)
        'pm10': 78,               # Partículas gruesas
        'o3': 23,                 # Ozono
        'no2': 34,                # Dióxido de nitrógeno
        'so2': 12,                # Dióxido de azufre
        'co': 0.5                 # Monóxido de carbono
    }
}
```

Con estos datos, EcoTech puede:
1. **Evaluar riesgos de salud** para empleados en zonas industriales
2. **Recomendar medidas de mitigación** (filtros, horarios, protección)
3. **Generar reportes ambientales** para clientes corporativos
4. **Cumplir normativas** de monitoreo ambiental (ISO 14001)

#### 🏭 **Casos de Uso Reales**

**Caso 1: Empresa Manufacturera**
- Cliente pregunta: "¿Es seguro que mis trabajadores operen al aire libre hoy?"
- EcoTech consulta API → AQI = 156 (Insalubre)
- Recomendación: "Suspender actividades al aire libre, usar mascarillas N95"

**Caso 2: Proyecto de Construcción**
- Requisito regulatorio: Monitorear PM10 cerca de la obra
- EcoTech usa API → PM10 = 120 µg/m³ (excede límite de 75)
- Acción: Implementar barreras anti-polvo y riego de vías

**Caso 3: Reporte ESG (Environmental, Social, Governance)**
- Inversores solicitan métricas ambientales
- EcoTech genera dashboard con datos históricos de calidad del aire
- Demuestra impacto de iniciativas de reducción de emisiones

---

## 🔧 Implementación Técnica

### **Endpoint Utilizado**
```
GET https://api.waqi.info/feed/{ciudad}/?token={API_TOKEN}
```

### **Autenticación**
```python
# api.py
self.token = os.getenv('API_TOKEN', 'demo')  # Token protegido en .env
url = f"{self.url}/feed/{ciudad}/?token={self.token}"
```

### **Manejo de Respuesta JSON**
```python
def _procesar_datos(self, datos):
    # Deserialización de JSON anidado
    aqi = datos.get('aqi', 'N/A')
    estacion = datos.get('city', {}).get('name', 'Desconocida')
    iaqi = datos.get('iaqi', {})
    
    # Extracción de contaminantes individuales
    contaminantes = {
        'pm25': iaqi.get('pm25', {}).get('v', 'N/A'),
        'pm10': iaqi.get('pm10', {}).get('v', 'N/A'),
        'o3': iaqi.get('o3', {}).get('v', 'N/A'),
        # ... etc
    }
    
    return info
```

### **Manejo de Errores**
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    datos = response.json()
except requests.exceptions.Timeout:
    raise APIError("Timeout conectando a la API")
except requests.exceptions.ConnectionError:
    raise APIError("No se pudo conectar")
except requests.exceptions.HTTPError as e:
    raise APIError(f"HTTP error: {e}")
```

---

## 📊 Datos Proporcionados

### **1. Índice AQI (Air Quality Index)**
- Escala 0-500 (estándar EPA)
- Clasificación automática:
  - 0-50: Bueno ✅
  - 51-100: Moderado ⚠️
  - 101-150: Insalubre para grupos sensibles 🟠
  - 151-200: Insalubre 🔴
  - 201-300: Muy Insalubre 🟣
  - 301+: Peligroso ⚫

### **2. Contaminantes Individuales**
| Contaminante | Descripción | Impacto en Salud |
|--------------|-------------|------------------|
| **PM2.5** | Partículas ≤2.5µm | Enfermedades respiratorias/cardiovasculares |
| **PM10** | Partículas ≤10µm | Irritación de vías respiratorias |
| **O3** | Ozono troposférico | Asma, reducción función pulmonar |
| **NO2** | Dióxido de nitrógeno | Inflamación de vías respiratorias |
| **SO2** | Dióxido de azufre | Broncoconstricción |
| **CO** | Monóxido de carbono | Reducción de oxígeno en sangre |

### **3. Metadata**
- Coordenadas GPS de la estación
- Timestamp de medición
- Temperatura y humedad
- Presión atmosférica

---

## 🌟 Ventajas de esta API

### ✅ **1. Cobertura Global**
- 100+ países
- 12,000+ estaciones de monitoreo
- Incluye ciudades principales de Latinoamérica

### ✅ **2. Datos en Tiempo Real**
- Actualización cada hora
- Fuentes oficiales (EPA, OMS, agencias gubernamentales)

### ✅ **3. Facilidad de Integración**
- REST API simple
- Formato JSON estándar
- Documentación clara

### ✅ **4. Gratuito para Uso Educativo**
- Token 'demo' funcional (limitado a 1000 requests/día)
- Registro gratuito para token personal

### ✅ **5. Estándares Internacionales**
- AQI según EPA (Environmental Protection Agency)
- Compatible con normativas ISO 14001

---

## 🚀 Escalabilidad Futura

Con esta API, EcoTech puede ampliar servicios:

1. **Dashboard Web**
   - Visualización de mapas de calor
   - Gráficos históricos de tendencias
   - Alertas automáticas por SMS/email

2. **API Propia**
   - Reempaquetar datos con análisis propietario
   - Ofrecer API a clientes corporativos

3. **Machine Learning**
   - Predicción de calidad del aire
   - Correlación con variables meteorológicas
   - Recomendaciones automatizadas

4. **Integración IoT**
   - Combinar con sensores propios
   - Validación cruzada de mediciones

---

## 📚 Alternativas Consideradas

| API | Ventaja | Desventaja |
|-----|---------|------------|
| **OpenWeatherMap** | Popular, fácil | Datos meteorológicos, NO especializados en contaminación |
| **IQAir** | Muy preciso | De pago (caro para estudiantes) |
| **BreezoMeter** | Predicciones ML | Requiere tarjeta de crédito |
| **AQICN** ✅ | Especializado, gratuito, educativo | Límite de requests con token demo |

---

## 🎓 Cumplimiento de Requisitos Académicos

### ✅ Correcta Integración de API
- [x] Consumo con librería `requests`
- [x] Autenticación con token
- [x] Manejo de errores (timeout, HTTP, JSON)
- [x] Deserialización de JSON anidado
- [x] Procesamiento de datos

### ✅ Justificación del Aporte
- [x] Relevancia para el negocio (gestión ambiental)
- [x] Casos de uso reales documentados
- [x] Impacto en toma de decisiones
- [x] Escalabilidad futura explicada

---

## 📖 Referencias

- [AQICN API Documentation](https://aqicn.org/json-api/doc/)
- [EPA Air Quality Index](https://www.airnow.gov/aqi/aqi-basics/)
- [WHO Air Quality Guidelines](https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health)
- [ISO 14001 Environmental Management](https://www.iso.org/iso-14001-environmental-management.html)

---

## 👨‍💻 Implementación en el Proyecto

**Archivo:** `api.py` (líneas 1-206)  
**Clase:** `ServicioAPI`  
**Métodos:**
- `get_calidad_aire(ciudad)` - Consumo de API
- `_procesar_datos(datos)` - Deserialización JSON
- `_clasificar(aqi)` - Lógica de negocio
- `mostrar_datos(ciudad)` - Presentación al usuario

**Uso en App:**
```python
# main.py
def ver_datos_api(self):
    ciudad = input("ciudad [Mexico]: ").strip() or "Mexico"
    self.api.mostrar_datos(ciudad)
```

---

**Conclusión:** La API de AQICN proporciona datos críticos de calidad del aire que son fundamentales para la misión de EcoTech Solutions de ofrecer consultoría ambiental basada en evidencia científica.
