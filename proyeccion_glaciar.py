#!/usr/bin/env python3
"""Espacialización altitudinal de escenarios de área glaciar para Quillcay.

Implementación publicable basada en el código proporcionado para la tesis.
Las áreas objetivo se reciben como datos de entrada: este programa NO estima
la regresión temporal ni modela dinámicamente el balance de masa glaciar.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.features import shapes
from rasterio.mask import mask
from shapely.geometry import shape


def leer_areas(ruta: Path) -> list[tuple[int, float]]:
    """Lee un CSV con columnas year y area_km2, preservando su orden."""
    salida = []
    with ruta.open("r", newline="", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo)
        if not {"year", "area_km2"}.issubset(lector.fieldnames or []):
            raise ValueError("El CSV debe tener las columnas year y area_km2.")
        vistos = set()
        for fila in lector:
            year = int(fila["year"])
            area = float(fila["area_km2"])
            if year in vistos or not np.isfinite(area) or area <= 0:
                raise ValueError(f"Año repetido o área no válida: {year}, {area}")
            vistos.add(year)
            salida.append((year, area))
    if not salida:
        raise ValueError("El CSV no contiene escenarios.")
    return salida


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--glaciar", type=Path, required=True,
                        help="Shapefile de la cobertura glaciar 2024 (.shp)")
    parser.add_argument("--dem", type=Path, required=True,
                        help="DEM recortado o de cobertura suficiente (.tif)")
    parser.add_argument("--areas", type=Path,
                        default=Path(__file__).resolve().parent / "areas_proyectadas.csv",
                        help="CSV de áreas objetivo (year,area_km2)")
    parser.add_argument("--salida", type=Path, required=True,
                        help="Carpeta para shapefiles generados y resumen CSV")
    args = parser.parse_args()

    for archivo in (args.glaciar, args.dem, args.areas):
        if not archivo.is_file():
            parser.error(f"No se encuentra el archivo: {archivo}")
    args.salida.mkdir(parents=True, exist_ok=True)
    areas = leer_areas(args.areas)

    glaciar = gpd.read_file(args.glaciar)
    if glaciar.empty or glaciar.crs is None:
        raise ValueError("El shapefile glaciar está vacío o carece de CRS.")
    if glaciar.geometry.isna().any() or not glaciar.geometry.is_valid.all():
        raise ValueError("El shapefile contiene geometrías nulas o no válidas.")

    with rasterio.open(args.dem) as src:
        if src.count < 1 or src.crs is None or not src.crs.is_projected:
            raise ValueError("El DEM debe tener al menos una banda y un CRS proyectado.")
        if src.crs.linear_units.lower() not in ("metre", "meter", "metres", "meters", "m"):
            raise ValueError("El DEM debe utilizar unidades lineales en metros (p.ej., UTM 18S).")
        glaciar = glaciar.to_crs(src.crs)
        geometrias = [g.__geo_interface__ for g in glaciar.geometry]
        # A diferencia del código original, preserva explícitamente la máscara:
        # evita tratar los píxeles exteriores como glaciar si src.nodata es None.
        imagen, transformacion = mask(src, geometrias, crop=True, filled=False)
        banda = imagen[0]
        datos = np.ma.getdata(banda)
        valido = (~np.ma.getmaskarray(banda)) & np.isfinite(datos)
        filas, columnas = np.where(valido)
        alturas = datos[filas, columnas]
        crs = src.crs

    if alturas.size == 0:
        raise ValueError("No hay elevaciones válidas dentro de la máscara glaciar 2024.")

    # Área real de celda obtenida de la transformación afín en metros².
    # El código original asumía 12,5 x 12,5 m; aquí se comprueba el tamaño.
    area_pixel_m2 = abs(transformacion.a * transformacion.e -
                        transformacion.b * transformacion.d)
    area_pixel_km2 = area_pixel_m2 / 1_000_000
    if not np.isclose(area_pixel_m2, 156.25, atol=0.001):
        raise ValueError(
            f"Se esperaba una cuadrícula de 12,5 m (156,25 m²/píxel); "
            f"el DEM tiene {area_pixel_m2:.5f} m²/píxel. "
            "Verifique el remuestreo y la resolución antes de ejecutar."
        )

    # Criterio principal del código original: conservar primero altitudes altas.
    # En empates de elevación se usa fila/columna como desempate estable.
    orden = np.lexsort((columnas, filas, -alturas))
    filas_ordenadas = filas[orden]
    columnas_ordenadas = columnas[orden]
    max_area = alturas.size * area_pixel_km2
    resumen = []

    for year, area_objetivo in areas:
        # Igual que en el algoritmo proporcionado: redondeo hacia abajo.
        n_pixeles = int(area_objetivo / area_pixel_km2)
        if n_pixeles < 1:
            raise ValueError(f"El área de {year} es menor que un píxel.")
        if n_pixeles > alturas.size:
            raise ValueError(
                f"En {year} se requieren {n_pixeles} píxeles, pero solo hay "
                f"{alturas.size} disponibles ({max_area:.5f} km²). "
                "Compruebe cobertura, resolución, CRS y áreas objetivo."
            )

        superficie = np.zeros(datos.shape, dtype=np.uint8)
        superficie[filas_ordenadas[:n_pixeles], columnas_ordenadas[:n_pixeles]] = 1
        geometrias_proyectadas = [
            shape(geometria)
            for geometria, valor in shapes(
                superficie, mask=(superficie == 1), transform=transformacion
            )
            if valor == 1
        ]
        if not geometrias_proyectadas:
            raise RuntimeError(f"La vectorización no produjo geometrías para {year}.")

        gdf = gpd.GeoDataFrame(
            {"year": [year] * len(geometrias_proyectadas)},
            geometry=geometrias_proyectadas,
            crs=crs,
        ).dissolve()
        gdf["area_km2"] = gdf.geometry.area / 1_000_000
        gdf["year"] = year
        area_final = float(gdf["area_km2"].iloc[0])
        destino = args.salida / f"glaciar_{year}.shp"
        gdf.to_file(destino)
        resumen.append({
            "year": year,
            "area_objetivo_km2": f"{area_objetivo:.5f}",
            "pixeles_seleccionados": n_pixeles,
            "area_resultante_km2": f"{area_final:.5f}",
            "diferencia_km2": f"{area_final - area_objetivo:.5f}",
        })
        print(f"{year}: objetivo {area_objetivo:.5f} km²; "
              f"resultado {area_final:.5f} km²; {destino}")

    resumen_csv = args.salida / "resumen_proyecciones.csv"
    with resumen_csv.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(resumen[0]))
        escritor.writeheader()
        escritor.writerows(resumen)
    print(f"Resumen: {resumen_csv}")


if __name__ == "__main__":
    main()
