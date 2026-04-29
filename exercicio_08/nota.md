# Nota curta acerca da implementação da Subtask PO2-515

### Como CRS em metros foi garantido

O CRS do raster de entrada é garantido pelo trecho de verificação em "# Garantindo CRS em metros". O 
CRS do grid, por sua vez, é comparado com o do raster de entrada e, caso haja divergência, reprojeta-se
para que tenham o mesmo.

### Como tile com size 10x10 m foi garantido

O tile size é passado como parâmetro para a função `create_grid`, que irá usar esse valor para calcular
o número de células em x e y. Utilizando-se a função `ceil` do numpy garante-se que as células cobrirão
toda a extensão da área de interesse. Com limites definidos sendo múltiplos de 10, garante-se, por fim,
que os tiles tenham size 10x10 m.

### Regra de tiles vazios/nodata

Os tiles vazios são salvos.