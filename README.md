# 3D Cube Pygame

![Gif de demonstração da implementação](https://user-images.githubusercontent.com/104772038/230260304-5060c771-c0dd-49b9-be35-dc098d56afab.gif)

## Descrição
Programa em pygame que utiliza algoritmo de pinhole fotográfico para projetar um cubo 3D sofrendo rotações sobre a tela 2D. 

## Como utilizar
- É possível instalar a aplicação de duas formas:
    - Clonagem do repositório utilizando o seguinte comando no terminal: `git clone https://github.com/PedroPertusi/3d-Cube-Pygame-APS`.
    - Ou baixar o arquivo zip desse repositório em `Code > Download Zip`. E descompactá-lo onde preferir.
- Em seguida, execute o comando: `pip install -r requirements.txt` no diretório principal do projeto clonado.
- Execute o programa com o seguinte comando: `python demo.py`

## Modelo Matemático
O desafio desse projeto foi transformar um cubo com posições em 3D numa projeção em duas dimensões, que mantivesse sua forma mesmo com diversas transformações de rotação e expansão.
A projeção do Cubo ocorreu por meio de Pinhole Fotográfico, técnica que consiste em posicionar uma pequena passagem de luz para gerar uma imagem no destino final, o anteparo. 
Na implementação, a projeção resultante do pinhole pode ser representada por uma matriz de transformação, gerada a partir da seguinte dedução matemática:

![Pinhole e Anteparo](img/IMG_2974.jpg)

* (X0Z0 e XpZp): Posição objeto e projeção;
* Pinhole: Origem do plano;
* d: Distância entre pinhole e anteparo.

De acordo com a figura, é possível concluir que `Zp = -d`;
O objeto e sua projeção geram o mesmo ângulo theta, em relação ao eixo vertical, e opostos pelo vértice. Assim, foi feita uma semelhança de triângulos para encontrar o valor de Xp.

$$
Tg\theta = \frac{X_0}{Z_0} = \frac{X_p}{Z_p} 
$$
$$
Xp = \frac{X_0 * Z_p}{Z_0}
$$

Para evitar que houvesse divisão na matriz, substituiu-se a matriz por uma nova variável Wp.

$$
Wp = \frac{Z_0}{Z_p} = -\frac{Z_0}{d}
$$

$$
X_0 = X_p * W_p
$$

Podemos fazer esse mesmo processo, mas agora para Y em função de Z. Para encontrar: 

$$
Y_0 = Y_p * W_p
$$

Em seguida, podemos montar a matriz de projeção: `T = Projeção @ X`, sabendo:

$$
X = \begin{bmatrix}
X_0 \\
Y_0 \\
Z_0 \\
1
\end{bmatrix}
T = \begin{bmatrix}
X_pW_p \\
Y_pW_p \\
Z_p \\
W_p
\end{bmatrix}
$$

Como vimos que `X0 = Xp * Wp`, e `Y0 = Yp * Wp`a primeira e segunda linha da matriz projeção serão: `[1,0,0,0]` e `[0,1,0,0]`, respectivamente.
Sabemos que `Y0 = -d`, portanto, a terceira linha será: `[0,0,-d,0]`. Por fim, `Wp = Y0/-d = -1/d` a quarta linha será: `[0,-1/d, 0]`.

$$
\begin{bmatrix}
1 & 0 & 0 & 0\\
0 & 1 & 0 & 0\\
0 & 0 & -d & 0\\
0 & -1/d & 0 & 0\\
\end{bmatrix}*
\begin{bmatrix}
X_0 \\
Y_0 \\
Z_0 \\
1
\end{bmatrix}=
\begin{bmatrix}
X_pW_p \\
Y_pW_p \\
Z_p \\
W_p
\end{bmatrix}
$$

Concluindo, para finalmente encontrar os valores de Xp e Yp, basta divide-se as linhas 1 e 2 do vetor T por sua quarta linha: `Xp*Wp/Wp = T[0]/T[2]` e `Yp*Wp/Wp = T[1]/T[2]`.

## Implementação
- Inicialmente, foi feita a modelagem do cubo de aresta 1u por meio de uma matriz 4x8. Quando transposta, as linhas guardam as posições dos 8 vértices do Cubo, já as colunas 1,2,3 são as posições X,Y,Z, e a coluna restante é composta apenas de uns para auxiliar nas transformações futuras;
- Em seguida, foram aplicadas as transformações `Rotação_X, Rotação_Y e Rotação_Z` sobre o objeto, por meio de multiplicações matriciais: `proj = rz @ ry @ rx @ objeto`;
- Após isso, aplicou-se a matriz de projeção P: `proj = P @ proj`;
- Dividiu-se toda a matriz pela linha Wp, para encontrar os reais valores de destino da projeção. Lembrando, a dimensão Z pode agora ser descartada, pois essa será a dimensão perdida no processo de projeção 3D -> 2D.
- Por fim, houve uma etapa para acertar o posicionamento do cubo: Aumento de suas arestas em 200x e translação para o centro da tela.

Para criar o efeito de rotação do cubo, para cada frame, incrementa-se o ângulo theta para X, Y ou Z, de acordo com o input do usuário. Consequentemente, apresenta na tela a nova posição atualizada, assim, gerando movimento para o cubo.

#### Matrizes de Rotação:
$$
R_x = \begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & \cos(\theta) & -\sin(\theta) & 0 \\
0 & \sin(\theta) & \cos(\theta) & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
\hspace{0.5in}
R_y = \begin{bmatrix}
\cos(\theta) & 0 & \sin(\theta) & 0 \\
0 & 1 & 0 & 0 \\
-\sin(\theta) & 0 & \cos(\theta) & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
\hspace{0.5in}
R_z = \begin{bmatrix}
\cos(\theta) & - \sin(\theta) & 0 & 0 \\
\sin(\theta) & \cos(\theta) & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

## Funcionalidades
| Ação | Input | 
| --- | --- |
| Zoom IN & OUT | Scroll |
| Rotacionar Eixo X | A, D |
| Rotacionar Eixo Y | W, S |
| Rotacionar Eixo Z | Z, X |
| Resetar Ângulo de Rotação | R |


