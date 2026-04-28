import geopandas as gpd
import os
import json
from vectors_inspect import load_vector


def inspect_attribute(gdf, attribute):
    
    # Tipo do atributo
    attr_type = gdf[attribute].dtype
    
    # Valores únicos
    unique_values = gdf[attribute].nunique()
    
    # Distribuição
    distribution = gdf[attribute].value_counts().sort_index()
    
    # Documentação por classe
    docs = {
        'tipo': str(attr_type),
        'valores_unicos': int(unique_values),
        'distribuicao': distribution.to_dict()
    }
    for class_value, count in distribution.items():
        docs[class_value] = {
            'valor': class_value,
            'quantidade': int(count),
            'percentual': round((count / len(gdf)) * 100, 2)
        }
    
    return docs


def filter_by_attribute(gdf, attribute, value):
    
    # Filtro usando máscara booleana
    mask = gdf[attribute] == value
    filtered_gdf = gdf[mask].copy()
    
    return filtered_gdf


if __name__ == "__main__":

    # Carregando arquivo
    input_path = 'exercicio_04/MATOLOGIA_Orthomosaico.geojson'
    gdf = load_vector(input_path)
    
    # Inspecionando atributo DN
    dn_info = inspect_attribute(gdf, 'DN')

    json_path = os.path.join('exercicio_04', 'DN_inspection.json')
    with open(json_path, 'w') as f:
        json.dump(dn_info, f, indent=4)
    
    # Filtrando apenas DN=2
    gdf_dn2 = filter_by_attribute(gdf, 'DN', 2)
    
    # Salvando arquivo derivado
    output_dir = 'exercicio_04/filtered_vectors'
    output_path = os.path.join(output_dir, 'MATOLOGIA_DN2.geojson')
    gdf_dn2.to_file(output_path, driver='GeoJSON')
