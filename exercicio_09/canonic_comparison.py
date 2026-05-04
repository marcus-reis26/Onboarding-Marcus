import argparse
import sys

import geopandas as gpd


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compare dois outputs de prescrição e decide se são semanticamente equivalentes"
    )

    # ===== ARGUMENTOS OBRIGATÓRIOS =====
    required = parser.add_argument_group("argumentos obrigatórios")

    required.add_argument(
        "--baseline",
        required=True,
        help="Caminho para o arquivo baseline (output original)",
    )
    required.add_argument(
        "--optimized",
        required=True,
        help="Caminho para o arquivo otimizado (output refatorado)",
    )

    return parser.parse_args()


def read_output(path: str) -> gpd.GeoDataFrame:
    gdf = gpd.read_file(path)
    if "cell_id" not in gdf.columns or "DN" not in gdf.columns:
        raise ValueError(
            f"Arquivo {path} deve conter as colunas 'cell_id' e 'DN'."
        )
    return gdf


def build_pair_set(gdf: gpd.GeoDataFrame) -> set[tuple[str, int | str]]:
    trimmed = gdf[["cell_id", "DN"]].drop_duplicates()
    return set(trimmed.itertuples(index=False, name=None))


def compare_outputs(baseline_path: str, optimized_path: str) -> bool:
    baseline_gdf = read_output(baseline_path)
    optimized_gdf = read_output(optimized_path)

    baseline_set = build_pair_set(baseline_gdf)
    optimized_set = build_pair_set(optimized_gdf)

    only_in_baseline = baseline_set - optimized_set
    only_in_optimized = optimized_set - baseline_set

    equivalent = len(only_in_baseline) == 0 and len(only_in_optimized) == 0

    print("=== Comparação de outputs ===")
    print(f"Baseline: {baseline_path}")
    print(f"Otimizado: {optimized_path}")
    print(f"Pares únicos (cell_id, DN) baseline: {len(baseline_set)}")
    print(f"Pares únicos (cell_id, DN) otimizado: {len(optimized_set)}")

    if equivalent:
        print("Resultado: EQUIVALENTE")
    else:
        print("Resultado: NÃO EQUIVALENTE")
        print(f"Pares presentes apenas no baseline: {len(only_in_baseline)}")
        print(f"Pares presentes apenas no otimizado: {len(only_in_optimized)}")

    duplicate_count_baseline = len(read_output(baseline_path)) - len(baseline_set)
    duplicate_count_optimized = len(read_output(optimized_path)) - len(optimized_set)
    if duplicate_count_baseline > 0 or duplicate_count_optimized > 0:
        print("\nAviso: foram encontradas entradas duplicadas de (cell_id, DN) nos dados originais:")
        print(f"  baseline: {duplicate_count_baseline} duplicatas")
        print(f"  otimizado: {duplicate_count_optimized} duplicatas")

    return equivalent


if __name__ == "__main__":
    args = parse_args()
    equivalent = compare_outputs(args.baseline, args.optimized)
    sys.exit(0 if equivalent else 1)
