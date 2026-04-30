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

def generate_prescription_grid_baseline(
    roi_path:str,
    weed_geojson_path:str,
    cell_size:int,
    
):
    """
    Gera um mapa de prescrição em grid 1x1 m de forma propositalmente ineficiente.

    Args:
        roi_path (str): caminho para o arquivo vetorial da região de interesse (ROI)
        weed_geojson_path (str): caminho para o GeoJSON de matologia com atributo DN
        cell_size (int): tamanho da célula em metros

    Returns:
        GeoDataFrame: grid de prescrição
    """

    start_time = time.time()

    roi_df = gpd.read_file(roi_path)
    utm_crs = roi_df.estimate_utm_crs()

    # carrega daninhas
    weeds = gpd.read_file(weed_geojson_path)
    
    # reprojetar para utm
    roi_df = roi_df.to_crs(utm_crs)
    weeds = weeds.to_crs(utm_crs)

    # cria lista manual de células
    roi_bounds = roi_df.total_bounds
    xmin, ymin, xmax, ymax = roi_bounds

    # saída
    out_cells = []
    out_dns = []
    out_cell_ids = []

    cell_to_dns = {}
    dn_to_cells = {}

    # loop de grid
    x = xmin
    while x < xmax:
        y = ymin
        while y < ymax:
            cell_geom = box(x, y, x + cell_size, y + cell_size)

            cell_id = f"{int(x)}_{int(y)}"

            # lista temporária
            dns_found = []

            # loop daninhas
            for i in range(len(weeds)):
                weed_geom = weeds.geometry.iloc[i]

                if cell_geom.intersects(weed_geom):
                    dn_val = weeds["DN"].iloc[i]
                    dns_found.append(dn_val)

            # se achou alguma, duplica célula para cada DN único
            if len(dns_found) > 0:
                dns_unique = []
                for dn in dns_found:
                    if dn not in dns_unique:
                        dns_unique.append(dn)

                for dn in dns_unique:
                    out_cells.append(cell_geom)
                    out_dns.append(dn)
                    out_cell_ids.append(cell_id)

                    # atualiza cell_to_dns
                    if cell_id not in cell_to_dns:
                        cell_to_dns[cell_id] = []
                    if dn not in cell_to_dns[cell_id]:
                        cell_to_dns[cell_id].append(dn)

                    # atualiza dn_to_cells
                    if dn not in dn_to_cells:
                        dn_to_cells[dn] = []
                    if cell_id not in dn_to_cells[dn]:
                        dn_to_cells[dn].append(cell_id)

            y += cell_size
        x += cell_size

    # monta GeoDataFrame final
    out_gdf = gpd.GeoDataFrame(
        {"cell_id": out_cell_ids, "DN": out_dns},
        geometry=out_cells,
        crs=weeds.crs
    )

    elapsed = time.time() - start_time
    print("==== REPORT ====")
    print(f"ROI bounds: {roi_bounds}")
    print(f"cell_size: {cell_size} m")
    print(f"Número de células no output: {len(out_gdf)}")
    print(f"Tempo total: {elapsed:.2f} s")

    return out_gdf


if __name__ == "__main__":
    args = parse_args()

    prescription_gdf = generate_prescription_grid_baseline(
        roi_path=args.roi,
        weed_geojson_path=args.weeds,
        cell_size=args.cell_size,
    )

    prescription_gdf.to_crs(4326).to_file(args.output)