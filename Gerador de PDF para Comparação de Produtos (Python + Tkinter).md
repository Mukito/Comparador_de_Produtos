# Gerador de PDF para Comparação de Produtos (Python + Tkinter)

Este projeto implementa um aplicativo desktop em Python, utilizando a biblioteca **Tkinter** para a interface gráfica e as bibliotecas **ReportLab** e **Matplotlib** para a geração de um PDF detalhado com tabela de pontuação e gráfico de comparação.

O código é altamente explicativo e agora permite a **adição dinâmica de critérios de comparação** na interface gráfica, atendendo ao seu novo requisito.

## Pré-requisitos

Você precisará ter o Python instalado em seu sistema (versão 3.x recomendada).

### Instalação de Dependências

Abra o terminal ou o prompt de comando (no VSCode, você pode usar o Terminal Integrado) na pasta onde você salvou o arquivo `comparador_produtos_gui.py` e execute os seguintes comandos para instalar as bibliotecas necessárias:

```bash
# Instala as bibliotecas ReportLab e Matplotlib
pip install reportlab matplotlib

# O Tkinter geralmente já vem instalado com o Python. 
# Se você tiver problemas, pode precisar instalar o pacote de desenvolvimento do Tkinter no seu sistema operacional:
# No Ubuntu/Debian:
# sudo apt-get install python3-tk
# No Windows/macOS, geralmente não é necessário.
```

## Como Usar

1.  **Execute o Script Python:**
    ```bash
    python comparador_produtos_gui.py
    ```
2.  **Interface Gráfica (GUI):**
    *   Uma janela será aberta com a estrutura de comparação.
    *   Você pode **editar os nomes dos produtos** no topo da tabela.
    *   **Adicionar Critérios Dinamicamente:**
        *   Clique no botão **"Adicionar Critério"** para inserir uma nova linha de comparação.
        *   Edite o nome do critério no campo de texto à esquerda.
        *   Para cada produto, selecione uma das opções no *dropdown* (`Excelente`, `Bom`, `Regular`, `Não possui`).
        *   Você pode remover um critério clicando no botão **"X"** ao lado da linha.
    *   **Sistema de Pontuação:**
        *   `Excelente` = 10 pontos
        *   `Bom` = 5 pontos
        *   `Regular` = 3 pontos
        *   `Não possui` = 0 pontos
3.  **Gere o PDF:**
    *   Após preencher os campos, clique no botão **"GERAR PDF DETALHADO"**.
    *   O aplicativo calculará a pontuação total de cada produto e determinará a "VENCEDORA".
    *   O arquivo **`comparativo_produtos.pdf`** será gerado na mesma pasta do script.

## Conteúdo do PDF Gerado

O PDF é elaborado e contém:

1.  **Título e Nome da Vencedora** (ou se houve empate).
2.  **Tabela Detalhada de Pontuação:** Uma planilha completa mostrando a pontuação e a opção selecionada para cada critério e produto, além da pontuação final.
3.  **Gráfico de Comparação:** Um gráfico de barras gerado pelo Matplotlib, comparando visualmente a pontuação total de cada produto.
4.  **Regras de Pontuação:** Uma seção com as regras de pontuação utilizadas.

---

**Observação:** O arquivo `comparativo_produtos.pdf` anexado foi gerado com dados de exemplo (incluindo um critério dinâmico) para que você possa ver o resultado final imediatamente. Para gerar o seu próprio PDF, basta seguir os passos acima.
