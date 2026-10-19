# Registro de reproducibilidad y revisión previa a publicación

## Modificaciones técnicas introducidas en la versión publicable

Para poder ejecutar el algoritmo fuera de la computadora original, se sustituyeron rutas absolutas de Windows por argumentos de línea de comandos; el comando `pip install` se trasladó a `requirements.txt`; y las áreas objetivo se almacenaron en un CSV. Se preservó la lógica principal: máscara del glaciar 2024, elección altitudinal de los píxeles más altos, número de píxeles calculado por división entera del área y exportación a polígonos.

Se añadieron comprobaciones de sistema de coordenadas, área por píxel, existencia de archivos y disponibilidad de celdas, y una máscara de valores válidos incluso cuando el DEM no define `nodata`. Además, para resolver empates de altitud, se aplica un orden determinista por fila y columna, que **puede alterar localmente píxeles de igual elevación respecto al código original**. Estas mejoras no deben confundirse con una ejecución idéntica a la original.

## Discrepancias que debe verificar la investigadora

1. **Horizonte temporal:** la tesis indica 2077; el diccionario del código recibido incluye 2076 (área objetivo 0,04 km²) y no incluye 2077. Verificar mapas, tablas y shapefiles efectivamente usados.
2. **Cobertura base:** el diccionario usa 25,62 km² para 2024. La superficie vectorial puede no coincidir exactamente con esa cifra por redondeo o rasterización.
3. **Entradas:** faltan en este paquete los archivos reales `Glaciar_2024.shp` y `Dem_quillcay.tif`; no se puede afirmar que se haya reproducido el resultado real de la tesis sin esos insumos.
4. **DEM:** el tamaño de celda de 12,5 m no implica precisión altimétrica de 12,5 m para un DEM procedente de una fuente de unos 30 m remuestreada.
5. **Autoría:** confirmar si el código fue escrito originalmente por la tesista o con colaboradores; actualizar `CITATION.cff` y reconocer contribuciones cuando corresponda.
6. **Permisos:** no añadir shapefiles, DEM ni archivos con información personal sin verificar derechos de difusión.

## Procedimiento recomendado antes del depósito definitivo

- Ejecutar esta implementación con **los mismos insumos originales**.
- Comparar los archivos `glaciar_*.shp` con los usados en la tesis (áreas y diferencias geométricas).
- Registrar versiones del entorno de Python y dependencias utilizadas en la corrida de validación.
- Resolver discrepancias entre 2076/2077 y entre la implementación original y la publicable.
- Etiquetar una liberación estable (`v1.0.0`) y conectarla con Zenodo si se desea DOI citable.
