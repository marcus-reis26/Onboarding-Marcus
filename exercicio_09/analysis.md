# Analysis — Código Legado: Mapa de Prescrição (GeoDataFrame)

> Neste documento, o termo **feição** refere-se a cada geometria do GeoDataFrame,
> equivalente a uma linha com atributos espaciais.

## 1) Contrato do resultado (escreva como regras testáveis)
Defina o comportamento como regras que eu posso validar automaticamente:

- R1: o output só contém células que intersectam pelo menos uma feição de `weeds`.
- R2: cada feição do output representa um par único (`cell_id`, `DN`), sem duplicatas exatas.
- R3: se uma mesma célula intersecta múltiplos valores de `DN`, a célula aparece uma vez para cada DN distinto.

Exemplo de regra bem definida:
- “Cada feição do output representa uma entidade única (A, B)”
- “Uma feição só existe se condição C for satisfeita”
- “Se condição D ocorrer, múltiplas feições devem ser geradas”

---

## 2) Previsão antes de executar (obrigatório)
Escolha uma ROI pequena (ex.: 10×10 m) e responda:

- Quantas células o grid terá? Mostre o cálculo.

Denotando o tamanho da célula como `cs`, tem-se que para uma ROI de dimensão `m x n`, visto que a
quantidade de células em uma dimensão `d` qualquer é `int(ceil(d / cs))`, será:
`int(ceil(m / cs)) * int(ceil(n / cs))`
Para o caso `10x10 m` e considerando-se `cs = 1 m`, tem-se: `int(ceil(10 / 1))² = 10² = 100 células`

- Em quais condições uma célula é duplicada no output?

Uma célula é duplicada se:
    1. há interseção da célula com alguma geometria do vetor de matologia;
    2. a geometria cuja interseção ocorre com a célula não apresente DN único

- Qual parte do código você acredita que domina o tempo? Por quê?

Acredito que o `# loop daninhas` é o trecho do código que domina o tempo, tendo em vista que, para
cada célula do grid, ele percorre todas as geometrias do `weeds`.

**Proibição:** não rode o código antes de escrever esta seção.

---

## 3) Execução do baseline (evidências)
Rode o baseline no exemplo em anexo e cole:

- Tempo total (segundos): 

56.15

- Número total de **feições** no output: 
 
220

- Distribuição de DN (DN → número de feições): 
 
{1: 36, 2: 2, 3: 182} ({DN: número de feições})

---

## 4) Explique a duplicação por DN (mostre que entendeu)
Escolha 1 célula do output que aparece duplicada.

- cell_id escolhido:

722085_2079098

- Liste os DN dessa célula:

[1, 3]

- Explique, com suas palavras, por que ela duplicou.

A duplicação é realizada para garantir que cada valor de daninha (DN) único associado à célula
tenha uma entrada separada nos resultados finais, mesmo que geometricamente seja a mesma célula.

- Mostre onde isso acontece no código (qual trecho/loop).

A duplicação ocorre especificamente no loop 
    ```for dn in dns_unique:
        out_cells.append(cell_geom)
        out_dns.append(dn)
        out_cell_ids.append(cell_id)
    ```

---

## 5) Gargalos com justificativa técnica
Identifique **até 3 gargalos reais**.

Para cada gargalo, informe:
- Onde ocorre no fluxo (qual trecho / loop):
- Qual operação espacial ou lógica é repetida:
- Qual conjunto cresce (ex.: nº de células, nº de daninhas):
- Complexidade aproximada desse trecho:

**Gargalo 1:**
  - Nested loop do grid, entre `while x < xmax:` / `while y < ymax:` e `for i in range(len(weeds)):`
  - Teste espacial `cell_geom.intersects(weed_geom)` para cada par célula × geometria de matologia
  - Número de células do grid e número de feições de matologia (`weeds`)
  - `O(n_cells * n_weeds)`

**Gargalo 2:**
  - Dentro do loop de interseção, ao coletar DN únicos usando `if dn not in dns_unique:`
  - Varredura linear da lista `dns_unique` para cada DN encontrado
  - Número de DN associados à mesma célula (potencialmente pequeno, mas ainda repetido)
  - `O(k²)` por célula onde `k` é o número de DN encontrados naquela célula

**Gargalo 3:**
  - Atualização de dicionários `cell_to_dns` e `dn_to_cells` dentro do loop `for dn in dns_unique:`
  - Verificações `if dn not in cell_to_dns[cell_id]:` e `if cell_id not in dn_to_cells[dn]:` a cada DN
  - Número de pares célula-DN no output
  - `O(m * p)` onde `m` é o número de células com DN e `p` é o número de DN únicos por célula

---

## 6) Riscos de refatoração (com exemplos)
Liste **até 3 riscos reais** de alterar o código sem perceber.
Para cada risco:
- O que poderia mudar no resultado:
- Como você detectaria isso (qual teste/checagem):
- Um exemplo concreto de falha (1 frase já serve)

**Risco 1:**
  - A contagem de DN por célula poderia duplicar ou perder valores únicos se a lógica de `dns_unique`
  for alterada de forma incorreta
  - Comparando a lista de DN por `cell_id` antes e depois da refatoração
  - Uma célula que deveria produzir [1, 3] passa a produzir apenas [3]

**Risco 2:**
  - Inclusão de células sem interseção ou a exclusão de células válidas se a condição de interseção for alterada de forma incorreta
  - Verificando se o número total de feições e a distribuição de DN permanecem iguais nos outputs de teste
  - Uma célula que intersecta uma geometria de matologia é omitida do output

---

## 8) Plano de refatoração (decisões, não implementação)
Escreva **3 decisões técnicas** que você pretende tomar, no formato:

- Decisão 1: ______
- Motivo técnico:
- Risco associado:
- Forma de validação após a mudança:

**Decisão 1:** substituir o loop manual de interseção de cada célula com as geometrias de `weeds` por outra abordagem.
  - reduz a complexidade de `O(n_cells * n_weeds)` para uma solução mais eficiente
  - mudanças na lógica de interseção podem alterar quais células entram no output se não aplicadas corretamente
  - comparar o número total de feições, distribuição de DN e um conjunto de `cell_id` amostrados entre o baseline e a versão refatorada

**Decisão 2:** tornar explícita e eficiente a construção de DN únicos para cada célula, usando `set` ou agregação de dados em vez da verificação `if dn not in dns_unique:`.
  - resolve o gargalo 2 ao reduzir custo de `O(k²)` para `O(k)` por célula
  - se a nova agregação for implementada de forma incorreta, ela pode perder DN ou gerar duplicatas indevidas
  - validar comparando os DN únicos por `cell_id` entre o baseline e a versão refatorada

**Decisão 3:** substituir as listas e verificações manuais de presença em `cell_to_dns` e `dn_to_cells` por coleções mais apropriadas e só montar o GeoDataFrame ao final.
  - resolve o gargalo 3 ao evitar verificações repetidas `if dn not in ...`
  - risco de perder ou duplicar pares `cell_id`/`DN` se a nova estrutura não preservar corretamente a unicidade das relações
  - validar comparando os pares `cell_id`/`DN` do output final e garantindo que o GeoDataFrame resultante seja equivalente ao baseline

---

## 9) “Defesa” curta
Em 5–8 linhas:
- O que o algoritmo faz em termos geoespaciais?
- Qual é o principal motivo dele não escalar?
- Qual evidência você usará para provar que não mudou o comportamento?

O algoritmo gera um grid regular sobre a ROI e atribui a cada célula os valores de DN das geometrias de matologia que a intersectam. Ele não escala porque calcula interseções para cada célula do grid contra todas as geometrias de `weeds` e depois faz deduplicações manuais de DN, resultando em custo quadrático em relação ao número de células e/ou feições. A estrutura atual também repete verificações de presença em listas, o que aumenta ainda mais o custo e a complexidade. Para provar que o comportamento não mudou, preciso comparar o número total de feições, a distribuição de DN e os pares `cell_id`/`DN` entre o baseline e a versão refatorada.
