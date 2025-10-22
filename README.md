# 🌱 Ybyscan — Segmentação Inteligente de Imagens Agrícolas

**Ybyscan** é um miniaplicativo de linha de comando (CLI) criado para a  
**Ybysys Agricultura Inteligente e Acessível**, com foco em **visão computacional agrícola**.  
Ele realiza **segmentação de imagens** de plantações usando dois métodos clássicos:  
**HSV (por cor)** e **K-Means (por agrupamento)**.

---

## 🚀 Funcionalidades

- 📸 Carrega imagens locais (ou stream de webcam, opcional)
- 🏞 Segmenta regiões 🟢**verdes** ou 🔵**azuis**
- 🔁 Alterna métodos `HSV` ↔ `K-Means`
- 🎚️ Ajuste fino de limiares HSV via flags
- 💾 Gera:
  - `*_mask.png` — Máscara binária (0/255)
  - `*_overlay.png` — Máscara sobre a imagem original
- 📊 Log informativo:
  - Tempo de execução
  - Percentual de pixels segmentados

---

## 🧠 Métodos Implementados

### Segmentação por Cor (HSV):

Converte a imagem para o espaço **HSV** e aplica filtros por intervalo de cor (`H`, `S`, `V`).  
Ideal para identificar áreas verdes de cultivo ou superfícies azuis como lonas e marcações.

```bash
python segment.py --input samples/soja.jpg --method hsv --target green
```

Ajuste fino (verde intenso):

```bash
python segment.py --input samples/soja.jpg --method hsv --target green \
--hmin 35 --hmax 85 --smin 60 --smax 255 --vmin 40 --vmax 255
```

### Segmentação por Agrupamento (K-Means):

Aplica K-Means clustering nos pixels (em RGB ou HSV) para separar regiões por similaridade de cor.
O cluster mais próximo da cor-alvo é considerado área segmentada.

```bash
python segment.py --input samples/soja.jpg --method kmeans --k 3 --target green
```

## ⚠️ Limitações

Embora o **Ybyscan** entregue bons resultados em condições controladas, alguns fatores reais de campo podem impactar a precisão da segmentação:

### 🌤️ 1. Iluminação irregular
- Mudanças bruscas de luminosidade (como sol e sombra) afetam o valor **V (Value)** no espaço HSV.  
- Em imagens com brilho intenso, a cor tende a “estourar” para branco, confundindo o filtro.

### 🍂 2. Baixa saturação
- Folhas amareladas, secas ou com baixo vigor apresentam saturação muito baixa, dificultando a segmentação baseada em cor.  
- O algoritmo pode confundir essas áreas com o solo.

### 🪵 3. Presença de ruído visual
- Objetos com cores próximas (como troncos, mourões, ou plástico degradado) podem ser detectados como verde/azul.  
- Uma filtragem morfológica extra (ex: `cv2.morphologyEx`) poderia reduzir falsos positivos.

### 🔁 4. Dependência de parâmetros
- O método HSV exige **ajuste manual dos limiares** conforme a câmera, o horário e o tipo de cultura.  
- Pequenas variações de `Hmin/Hmax` podem alterar drasticamente o resultado.

### 🧮 5. Variabilidade do K-Means
- O K-Means inicia com centróides aleatórios — isso faz com que resultados possam variar levemente a cada execução.  
- Para reprodutibilidade total, é necessário fixar a semente (`np.random.seed()`).

### 🌾 6. Contexto agrícola real
- Sombras das folhas, variações de solo e mistura de espécies no mesmo quadro reduzem a pureza da segmentação.  
- O algoritmo não distingue *tipo de planta*, apenas separa cores dominantes.

---

🔧 **Sugestões futuras**:
- Aplicar equalização de histograma (`cv2.equalizeHist`) para corrigir iluminação.
- Implementar um pós-processamento com morfologia (erosão/dilatação).
- Incorporar aprendizado de máquina leve (CNN ou U-Net compacta) para reconhecimento semântico.


## ⚙️ Instalação

1. Clone o repositório:

 - git clone https://github.com/ErickRad/ybyscan.git
   cd ybyscan

2. Crie e ative um ambiente virtual:

 - python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate      # Windows
 
3. Instale as dependências:

 - pip install -r requirements.txt

## 📦 Estrutura do Projeto

ybyscan/

├── segment.py

├── segmentation/

│   ├── base_segmenter.py

│   ├── hsv_segmenter.py

│   └── kmeans_segmenter.py

├── outputs/

├── samples/

│   └── soja.jpg

├── requirements.txt

└── README.md
