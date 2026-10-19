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

## Horizonte y superficies proyectadas

Las áreas objetivo **no se estiman en este programa**, sino que se proporcionan como datos de entrada. Los escenarios incluidos son 2024, 2029, 2034, 2039, 2044, 2049, 2054, 2059, 2064, 2069, 2074 y **2076**, con superficies respectivamente de 25,62; 23,16; 20,70; 18,24; 15,78; 13,32; 10,86; 8,40; 5,94; 3,48; 1,02 y 0,04 km².

**Horizonte temporal del estudio:** **2024–2076**. La última superficie glaciar proyectada corresponde al año **2076**, con un valor objetivo de **0,04 km²**.

## Limitaciones

- Los mapas dependen de la calidad de la delimitación glaciar de 2024, del DEM, del ajuste de áreas y de su coherencia en CRS.
- El algoritmo utiliza un supuesto de retirada preferente de hielo a menor altitud; no modela masa, espesor, exposición, orientación, dinámica ni clima futuros.
- El área final está discretizada por píxeles (156,25 m² por píxel). La rasterización y vectorización pueden variar levemente respecto del polígono original.
- Para reproducir los mapas originales es necesario usar **los mismos insumos y versiones documentadas**, y comprobar las salidas frente a los shapefiles originales.
- No se redistribuyen datos cartográficos de terceros: comprobar licencias, permisos y fuentes antes de publicarlos.

## Tesis de maestría asociada

**Título completo:** Caracterización del peligro por Drenaje Ácido de Roca y sus potenciales implicancias en la gestión hídrica de la subcuenca Quillcay en un contexto de retroceso glaciar

**Autora:** Ivana Karina Escate Gastañaga.  
**Grado académico al que se opta:** Maestra en Gestión de los Recursos Hídricos.  
**Institución:** Pontificia Universidad Católica del Perú (PUCP), Perú.  
**Año de elaboración:** 2026.

Este repositorio contiene **el código de espacialización prospectiva** que apoya esa investigación; **no constituye el texto íntegro de la tesis** ni debe citarse como si fuera la tesis publicada. Cuando la tesis esté depositada oficialmente, incorpórese aquí el enlace institucional o DOI correspondiente.

## Cómo citar

**Estilo bibliográfico recomendado.** En las referencias APA 7 de este repositorio se emplea la forma de autor **Escate, I. K. (2026)**: primer apellido, iniciales de los dos nombres y año de publicación entre paréntesis. Si utiliza, adapta o reproduce el código de este repositorio en una investigación, se recomienda citarlo siguiendo las normas de la **American Psychological Association (APA), 7.ª edición** (edición vigente en 2026), o de acuerdo con el **sistema de citación exigido por la institución, revista científica, programa académico o proyecto** en el que se desarrolla la investigación. En todos los casos deben conservarse correctamente los datos de autoría, título del recurso, versión, año y enlace permanente o DOI cuando estén disponibles.

**Para citar el código fuente:** seleccione **«Cite this repository»** en GitHub. Esta función utiliza los metadatos del archivo `CITATION.cff` y ofrece formatos **APA y BibTeX**. Verifique los metadatos de la versión consultada, especialmente la fecha de publicación, la autoría y la URL o DOI, antes de incorporar la referencia a su bibliografía. También puede adaptar esos mismos datos al estilo Vancouver, IEEE, Chicago u otro estilo exigido por su investigación.

Como **modelo orientativo de referencia en APA 7**, una vez confirmado el año de publicación y añadido el enlace público, puede utilizarse:

> Escate, I. K. (2026). *Código de espacialización prospectiva del retroceso glaciar asociado a la tesis «Caracterización del peligro por Drenaje Ácido de Roca y sus potenciales implicancias en la gestión hídrica de la subcuenca Quillcay en un contexto de retroceso glaciar»* (versión 0.1.0) [Software]. GitHub. [Agregar URL pública o DOI de la versión consultada].

**Para citar la tesis de maestría:** la tesis constituye una obra académica distinta del código y debe citarse **por separado** cuando esté disponible en el repositorio institucional de la PUCP. Con fines de identificación, sus metadatos bibliográficos son:

> Escate, I. K. (2026). *Caracterización del peligro por Drenaje Ácido de Roca y sus potenciales implicancias en la gestión hídrica de la subcuenca Quillcay en un contexto de retroceso glaciar* [Tesis de maestría, Pontificia Universidad Católica del Perú]. [Agregar URL institucional o DOI cuando exista].

**Autoría y reconocimiento:** antes de fijar una versión archivada o licencia de reutilización, confirme la autoría efectiva del código y reconozca a quienes hayan participado en su desarrollo, según corresponda. La autoría de la tesis y la del software pueden no ser idénticas.

## Alcance

El repositorio describe exclusivamente el procedimiento de **espacialización prospectiva** de coberturas glaciares. El mapeo de peligro por DAR y la regresión que determinó las áreas objetivo forman parte de otras etapas de la investigación.
