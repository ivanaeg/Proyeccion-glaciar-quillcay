# Espacialización prospectiva del retroceso glaciar — subcuenca Quillcay

**Código de apoyo a una tesis de maestría sobre el peligro por drenaje ácido de roca (DAR) en la subcuenca Quillcay, Áncash, Perú.**

Este repositorio publica una **versión adaptada para distribución y ejecución en otros equipos**, basada en el código original utilizado para distribuir espacialmente superficies glaciares prospectivas. El script **no calcula la regresión lineal**, **no pronostica la dinámica física de un glaciar** y **no genera el mapa final de peligro por DAR**: recibe áreas objetivo que fueron calculadas previamente y las representa espacialmente.

## Qué hace el algoritmo

1. Lee el polígono de cobertura glaciar de **2024** y un modelo digital de elevación (DEM) en un sistema de coordenadas proyectadas en metros.
2. Recorta el DEM al polígono y selecciona los píxeles interiores con datos de elevación válidos.
3. Ordena los píxeles **de mayor a menor altitud**, manteniendo preferentemente las cotas altas y retirando primero las bajas.
4. Para cada horizonte temporal del archivo `areas_proyectadas.csv`, conserva el número de píxeles equivalente al área objetivo; convierte la máscara a polígonos y disuelve geometrías.
5. Exporta un **shapefile por horizonte** y un CSV con áreas objetivo y obtenidas.

El algoritmo representa una **espacialización altitudinal simplificada**, no un modelo de balance de masa, espesor, flujo glaciar o evolución hidrogeoquímica.

## Archivos

| Archivo | Descripción |
|---|---|
| `proyeccion_glaciar.py` | Implementación publicable y parametrizada del algoritmo. |
| `areas_proyectadas.csv` | Valores de superficie objetivo transcritos del código proporcionado. |
| `requirements.txt` | Dependencias de Python. |
| `CITATION.cff` | Metadatos de citación del software (revisar autoría antes de publicar). |
| `NOTAS_REPRODUCIBILIDAD.md` | Supuestos, diferencias frente al código fuente y asuntos que deben revisarse. |

## Requisitos e instalación

- Python 3.10 o posterior, recomendado en entorno virtual.
- Paquetes: `numpy`, `geopandas`, `rasterio`, `shapely`.
- **Insumos no incluidos:** un shapefile glaciar de 2024 (`.shp`, `.shx`, `.dbf`, `.prj`) y el DEM (`.tif`) empleado en el estudio.
- El código presupone una cuadrícula de **12,5 × 12,5 m** y un CRS proyectado con unidades en **metros** (por ejemplo, UTM 18S). La resolución de celda de 12,5 m **no implica** una resolución altimétrica efectiva de 12,5 m si el DEM original era de unos 30 m y fue remuestreado.

Instalación:

```bash
python -m pip install -r requirements.txt
```

Ejemplo de ejecución (sustituya rutas por las de sus archivos):

```bash
python proyeccion_glaciar.py \
  --glaciar "datos/Glaciar_2024.shp" \
  --dem "datos/Dem_quillcay.tif" \
  --areas "areas_proyectadas.csv" \
  --salida "salidas"
```

En Windows (PowerShell) puede escribirse el comando en una sola línea o usar el carácter de continuación propio de PowerShell.

## Horizontes y superficies del código recibido

Las áreas objetivo **no se estiman en este programa**, sino que provienen del código facilitado. Los escenarios incluidos son 2024, 2029, 2034, 2039, 2044, 2049, 2054, 2059, 2064, 2069, 2074 y **2076**, con superficies respectivamente de 25,62; 23,16; 20,70; 18,24; 15,78; 13,32; 10,86; 8,40; 5,94; 3,48; 1,02 y 0,04 km².

**ATENCIÓN: diferencia documental por resolver.** La tesis menciona un horizonte **2024–2077**, mientras que el código compartido termina en **2076**. No se ha añadido artificialmente una cobertura para 2077. Esta diferencia debe reconciliarse con la versión del procesamiento que produjo las figuras, capas y resultados finales antes de utilizar el repositorio como evidencia de reproducción exacta.

## Limitaciones

- Los mapas dependen de la calidad de la delimitación glaciar de 2024, del DEM, del ajuste de áreas y de su coherencia en CRS.
- El algoritmo utiliza un supuesto de retirada preferente de hielo a menor altitud; no modela masa, espesor, exposición, orientación, dinámica ni clima futuros.
- El área final está discretizada por píxeles (156,25 m² por píxel). La rasterización y vectorización pueden variar levemente respecto del polígono original.
- Para reproducir los mapas originales es necesario usar **los mismos insumos y versiones documentadas**, y comprobar las salidas frente a los shapefiles originales.
- No se redistribuyen datos cartográficos de terceros: comprobar licencias, permisos y fuentes antes de publicarlos.

## Reconocimiento y cita

Consulte `CITATION.cff`. **Antes de publicar, confirme la autoría efectiva del algoritmo**, incluya coautores o colaboradores que corresponda y establezca una licencia únicamente si posee derechos para otorgarla. Cuando exista una versión estable, puede archivarse una liberación (*release*) en **Zenodo** para obtener un **DOI** permanente. Actualice entonces los metadatos de citación.

## Alcance

El repositorio describe exclusivamente el procedimiento de **espacialización prospectiva** de coberturas glaciares. El mapeo de peligro por DAR y la regresión que determinó las áreas objetivo forman parte de otras etapas de la investigación.
