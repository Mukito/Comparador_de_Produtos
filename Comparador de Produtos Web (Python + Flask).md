# Comparador de Produtos Web (Python + Flask)

Este projeto transforma o seu comparador de produtos em uma **aplicação web interativa**, utilizando:

*   **Python (Flask)**: Para o backend, processamento de dados e geração do PDF.
*   **HTML/CSS/JavaScript**: Para o frontend, oferecendo uma interface dinâmica e visualmente inspirada na imagem que você forneceu.
*   **ReportLab e Matplotlib**: Para gerar o PDF detalhado com a tabela de pontuação e o gráfico de comparação.

## Funcionalidades Principais

1.  **Interface Intuitiva**: Visual similar ao mockup, com campos para nomes de produtos e pontuações.
2.  **Critérios Dinâmicos**: Você pode adicionar e remover critérios de comparação livremente.
3.  **Cálculo Automático**: A pontuação total e a "VENCEDORA" são atualizadas em tempo real.
4.  **Geração de PDF Elaborado**: O botão "Baixar PDF" envia os dados para o backend, que gera um PDF profissional com tabela detalhada e gráfico de barras.

## Como Executar no VSCode

### 1. Instalação de Dependências

Abra o terminal integrado do VSCode no diretório `comparador_web/` e execute:

```bash
pip install Flask reportlab matplotlib
```

### 2. Estrutura do Projeto

O projeto é organizado da seguinte forma:

```
comparador_web/
├── app.py              # Backend Flask (lógica principal, rotas e geração de PDF)
├── templates/
│   └── index.html      # Frontend (estrutura HTML e JavaScript para interatividade)
└── static/
    └── style.css       # Estilização (CSS)
```

### 3. Execução

Execute o arquivo principal do Flask:

```bash
python app.py
```

O servidor será iniciado, e você verá uma mensagem como:

```
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

### 4. Acesso

Abra seu navegador e acesse o endereço `http://127.0.0.1:5000/` para usar o comparador.

### 5. Uso

1.  Edite os nomes dos produtos no topo da página.
2.  Use o botão **"+ Adicionar Critério"** para incluir novas linhas.
3.  Selecione a pontuação para cada critério.
4.  Clique em **"Baixar PDF"** para gerar e fazer o download do relatório.

---
**Link de Demonstração:**

Você pode acessar a aplicação rodando no ambiente de desenvolvimento neste link temporário: [https://5000-iey68dtn2qy9rectj17ld-37e623c2.manus.computer](https://5000-iey68dtn2qy9rectj17ld-37e623c2.manus.computer)
