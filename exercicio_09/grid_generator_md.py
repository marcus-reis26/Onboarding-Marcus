import argparse
import geopandas as gpd
from shapely.geometry import box
import time


def parse_args():
    parser = argparse.ArgumentParser(
        description="Gera grid de prescrição a partir de ROI e GeoJSON de daninhas"
    )

    # ===== ARGUMENTOS OBRIGATÓRIOS =====
    required = parser.add_argument_group("argumentos obrigatórios")

    required.add_argument(
        "--roi",
        required=True,
        help="Caminho para o arquivo vetorial da ROI (GeoJSON, SHP, etc.)",
    )

    required.add_argument(
        "--weeds",
        required=True,
        help="Caminho para o GeoJSON de matologia (com atributo DN)",
    )

    required.add_argument(
        "--output",
        required=True,
        help="Caminho do arquivo de saída (GeoJSON)",
    )

    # ===== ARGUMENTOS OPCIONAIS =====
    optional = parser.add_argument_group("argumentos opcionais")

    optional.add_argument(
        "--cell_size",
        type=float,
        default=1,
        help="Tamanho da célula em metros (default: 1)",
    )

    return parser.parse_args()


def create_grid(roi_df, roi_bounds, cell_size):
    xmin, ymin, xmax, ymax = roi_bounds
    cells = []
    cell_ids = []
    x = xmin
    while x < xmax:
        y = ymin
        while y < ymax:
            cells.append(box(x, y, x + cell_size, y + cell_size))
            cell_ids.append(f"{int(x)}_{int(y)}")
            y += cell_size
        x += cell_size

    return gpd.GeoDataFrame({'cell_id': cell_ids}, geometry=cells, crs=roi_df.crs)


def intersect_weeds(grid_gdf, weeds_gdf):
    # Usar overlay/intersection para detectar interseções de geometria
    intersections = gpd.overlay(grid_gdf, weeds_gdf, how='intersection')
    intersections['DN'] = intersections['DN'].astype(int)
    # Agrupar por cell_id e coletar DN únicos
    grouped = intersections.groupby('cell_id')['DN'].apply(set).reset_index()
    # Expandir para duplicar linhas por DN
    expanded = grouped.explode('DN').reset_index(drop=True)
    expanded['DN'] = expanded['DN'].astype(int)

    result = expanded.merge(grid_gdf[['cell_id', 'geometry']], on='cell_id')
    return gpd.GeoDataFrame(result, geometry='geometry', crs=grid_gdf.crs)


def generate_prescription_grid_refactored(roi_path, weed_geojson_path, cell_size):
    start_time = time.time()
    
    roi_df = gpd.read_file(roi_path)
    utm_crs = roi_df.estimate_utm_crs()
    roi_df = roi_df.to_crs(utm_crs)
    weeds = gpd.read_file(weed_geojson_path).to_crs(utm_crs)
    
    grid_gdf = create_grid(roi_df, roi_df.total_bounds, cell_size)
    out_gdf = intersect_weeds(grid_gdf, weeds)
    
    elapsed = time.time() - start_time
    print(f"Tempo total: {elapsed:.2f} s")

    return out_gdf.to_crs(4326)


if __name__ == "__main__":
    args = parse_args()

    prescription_gdf = generate_prescription_grid_refactored(
        roi_path=args.roi,
        weed_geojson_path=args.weeds,
        cell_size=args.cell_size,
    )

    prescription_gdf.to_file(args.output, driver='GeoJSON')
