# Comentários finais

## Cálculo da zona UTM

A zona UTM foi calculada utilizando-se a fórmula `np.floor((lons + 180) / 6) + 1`,
que é a forma usual de determinar a zona UTM a partir da longitude.

- `lons + 180` transforma as longitudes para um sistema de 0° a 360°,

- Tem-se 60 zonas de 6° cada, então divide-se por 6 e adiciona-se 1 para obter a zona correta

## Confiança no método automático

Pode-se confiar no método automático do GeoPandas quando a área de interesse é pequena 
e o CRS original é geográfico (latitude, longitude). Para áreas que se estendem a múltiplas zonas ou que possuem CRS já projetado, a fórmula manual é mais confiável.