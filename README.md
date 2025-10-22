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

⚙️ Instalação
1. Clone o repositório:
git clone https://github.com/ErickRad/ybyscan.git
cd ybyscan

2. Crie e ative um ambiente virtual:
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

3. Instale as dependências:
pip install -r requirements.txt

📦 Estrutura do Projeto

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
