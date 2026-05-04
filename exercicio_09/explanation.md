# Breve explicação da refatoração

- **Decisão 1** (substituir o loop manual de interseção de cada célula com as geometrias de `weeds` por outra abordagem):

Utilizado `intersect_weeds()` com `gpd.overlay(..., how='intersection')` para detectar as interseções entre células e geometrias de `weeds`, evitando o loop célula×daninha do baseline.

- **Decisão 2** (tornar explícita e eficiente a construção de DN únicos para cada célula, usando `set` ou agregação de dados em vez da verificação `if dn not in dns_unique:`):
  
Agrupando por `cell_id` e convertendo `DN` em `set` antes do `explode()`, gerando valores únicos sem a verificação repetida `if dn not in ...`.

- **Decisão 3** (substituir as listas e verificações manuais de presença em `cell_to_dns` e `dn_to_cells` por coleções mais apropriadas e só montar o GeoDataFrame ao final):

Separada a geração do grid em `create_grid()` e GeoDataFrame final montado só depois da agregação, deixando a lógica mais limpa e sem atualizações manuais de listas.
