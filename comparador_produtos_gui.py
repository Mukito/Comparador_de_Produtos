import tkinter as tk
from tkinter import ttk
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
import matplotlib.pyplot as plt
import io

# --- Configurações Fixas ---
OPCOES_PONTOS = {
    "Excelente": 10,
    "Bom": 5,
    "Regular": 3,
    "Não possui": 0
}

# --- Funções de Geração de PDF ---

def gerar_grafico_comparacao(dados_comparacao, nome_vencedora):
    """Gera um gráfico de barras comparando a pontuação total dos produtos."""
    produtos = list(dados_comparacao.keys())
    pontuacoes = [dados_comparacao[prod]["Total"] for prod in produtos]

    fig, ax = plt.subplots(figsize=(8, 4))
    barras = ax.bar(produtos, pontuacoes, color=['#4B0082', '#6A5ACD', '#9370DB']) # Cores inspiradas na imagem
    
    ax.set_ylabel('Pontuação Total')
    ax.set_title(f'Comparativo de Pontuação Total (Vencedora: {nome_vencedora})')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    # Adicionar rótulos de valor nas barras
    for barra in barras:
        yval = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2.0, yval, int(yval), ha='center', va='bottom', fontsize=10)

    # Salvar o gráfico em um buffer de memória
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf

def gerar_pdf(dados_comparacao, nome_vencedora, criterios_usados):
    """Cria o PDF detalhado com a tabela de comparação e o gráfico.
       Recebe a lista de critérios usados para garantir a ordem correta na tabela."""
    
    # 1. Configuração do Documento
    doc = SimpleDocTemplate("comparativo_produtos.pdf", pagesize=A4,
                            rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    styles.add(ParagraphStyle(name='TitleCustom', parent=styles['Title'], fontSize=20, spaceAfter=20, alignment=1))
    styles.add(ParagraphStyle(name='Heading2Custom', parent=styles['Heading2'], fontSize=14, spaceBefore=10, spaceAfter=10))
    styles.add(ParagraphStyle(name='NormalCustom', parent=styles['Normal'], fontSize=10))

    Story = []

    # 2. Título
    Story.append(Paragraph("Relatório de Comparação de Produtos", styles['TitleCustom']))
    Story.append(Paragraph(f"<b>VENCEDORA: {nome_vencedora}</b>", styles['Heading2Custom']))
    Story.append(Spacer(1, 12))

    # 3. Tabela de Detalhes
    
    # Preparar dados para a tabela
    produtos = list(dados_comparacao.keys())
    
    # Cabeçalho: CRITÉRIOS + Nomes dos Produtos + TOTAL
    data = [["CRITÉRIOS"] + produtos + ["TOTAL"]]
    
    # Linhas de Critérios
    for criterio in criterios_usados:
        row = [Paragraph(criterio, styles['NormalCustom'])]
        
        # Coletar pontuações para o critério em todos os produtos
        pontuacoes_criterio = []
        for produto in produtos:
            # Buscar dados do critério no dicionário de dados_comparacao
            criterio_data = dados_comparacao[produto]["Criterios"].get(criterio, {"Opcao": "N/A", "Pontos": 0})
            
            pontos = criterio_data["Pontos"]
            opcao = criterio_data["Opcao"]
            texto_celula = f"{pontos} pts ({opcao})"
            row.append(Paragraph(texto_celula, styles['NormalCustom']))
            pontuacoes_criterio.append(pontos)
        
        # Adicionar a pontuação total do critério (soma das colunas)
        total_criterio = sum(pontuacoes_criterio)
        row.append(Paragraph(str(total_criterio), styles['NormalCustom']))
        data.append(row)
        
    # Linha de Totais
    linha_total = [Paragraph("<b>PONTUAÇÃO FINAL</b>", styles['NormalCustom'])]
    for produto in produtos:
        linha_total.append(Paragraph(f"<b>{int(dados_comparacao[produto]['Total'])} pts</b>", styles['NormalCustom']))
    linha_total.append(Paragraph("---", styles['NormalCustom'])) # Célula vazia para o total geral
    data.append(linha_total)

    # Criar e estilizar a tabela
    table = Table(data, colWidths=[200] + [80] * len(produtos) + [80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'), # Alinhar critérios à esquerda
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
    ]))
    
    Story.append(Paragraph("<b>1. Tabela Detalhada de Pontuação</b>", styles['Heading2Custom']))
    Story.append(table)
    Story.append(Spacer(1, 24))

    # 4. Gráfico de Comparação
    
    # Gerar o gráfico
    grafico_buffer = gerar_grafico_comparacao(dados_comparacao, nome_vencedora)
    img = Image(grafico_buffer, width=400, height=200)
    
    Story.append(Paragraph("<b>2. Gráfico de Comparação de Pontuação Total</b>", styles['Heading2Custom']))
    Story.append(img)
    Story.append(Spacer(1, 12))
    
    # 5. Notas Finais
    Story.append(Paragraph("<b>3. Regras de Pontuação</b>", styles['Heading2Custom']))
    Story.append(Paragraph("As pontuações foram atribuídas com base nas seguintes regras:", styles['NormalCustom']))
    regras = [f"<b>{opcao}</b>: {pontos} pontos" for opcao, pontos in OPCOES_PONTOS.items()]
    for regra in regras:
        Story.append(Paragraph(regra, styles['NormalCustom']))
    Story.append(Spacer(1, 12))
    
    # 6. Construir o PDF
    doc.build(Story)
    return "comparativo_produtos.pdf"

# --- Lógica da Aplicação ---

class ComparadorApp:
    def __init__(self, master):
        self.master = master
        master.title("Gerador de PDF para Comparação de Produtos")
        
        self.produtos = ["ADAPTA", "INNER AI", "TESS AI (PARETO)"]
        
        # Lista para armazenar as variáveis de controle e widgets de cada critério
        # Cada item será um dicionário: {"criterio_var": tk.StringVar, "combos": [ttk.Combobox, ...]}
        self.criterio_rows = [] 
        
        # Variáveis para armazenar os nomes dos produtos (editáveis)
        self.vars_produtos = [tk.StringVar(master, value=prod) for prod in self.produtos]
        
        self.criar_widgets()

    def criar_widgets(self):
        # Frame principal para o layout
        self.main_frame = ttk.Frame(self.master, padding="10 10 10 10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame para os cabeçalhos e critérios (para facilitar a inserção dinâmica)
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.criterios_frame = ttk.Frame(self.main_frame)
        self.criterios_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Título
        ttk.Label(self.header_frame, text="COMPARAÇÃO DE PRODUTOS", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=len(self.produtos) + 1, pady=10)
        
        # Linha dos Nomes dos Produtos (Editáveis)
        ttk.Label(self.header_frame, text="CRITÉRIOS", font=("Helvetica", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        for i, var_prod in enumerate(self.vars_produtos):
            entry_prod = ttk.Entry(self.header_frame, textvariable=var_prod, width=20)
            entry_prod.grid(row=1, column=i+1, padx=5, pady=5)
            # Configurar expansão de colunas
            self.header_frame.columnconfigure(i+1, weight=1)
        self.header_frame.columnconfigure(0, weight=1)

        # Botão para adicionar novo critério
        self.add_button = ttk.Button(self.main_frame, text="Adicionar Critério", command=self.adicionar_criterio)
        self.add_button.grid(row=2, column=0, pady=10, sticky=tk.W)
        
        # Botão para Gerar PDF
        self.pdf_button = ttk.Button(self.main_frame, text="GERAR PDF DETALHADO", command=self.processar_e_gerar_pdf)
        self.pdf_button.grid(row=3, column=0, pady=20)

        # Label de Status
        self.status_var = tk.StringVar(self.main_frame)
        self.status_label = ttk.Label(self.main_frame, textvariable=self.status_var, foreground="blue")
        self.status_label.grid(row=4, column=0)
        
        # Adicionar 3 critérios iniciais (opcional, para iniciar com a aparência da imagem)
        self.adicionar_criterio("Preço e condições")
        self.adicionar_criterio("IA para texto e funcionalidades")
        self.adicionar_criterio("Outros modelos de IA e ferramentas...")


    def adicionar_criterio(self, nome_criterio="Novo Critério"):
        """Adiciona uma nova linha de critério com entrada de texto e comboboxes."""
        
        row_index = len(self.criterio_rows)
        row_frame = ttk.Frame(self.criterios_frame)
        row_frame.grid(row=row_index, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # 1. Entrada do Nome do Critério
        criterio_var = tk.StringVar(row_frame, value=nome_criterio)
        entry_criterio = ttk.Entry(row_frame, textvariable=criterio_var, width=40)
        entry_criterio.grid(row=0, column=0, sticky=tk.W, padx=5)
        
        # 2. Comboboxes para os Produtos
        combos = []
        opcoes = list(OPCOES_PONTOS.keys())
        
        for i, produto in enumerate(self.produtos):
            var_selecao = tk.StringVar(row_frame)
            var_selecao.set("Selecione...") # Valor inicial
            
            combo = ttk.Combobox(row_frame, textvariable=var_selecao, values=opcoes, state="readonly", width=15)
            combo.grid(row=0, column=i + 1, padx=5)
            combos.append(combo)

        # 3. Botão de Remoção
        # Usamos uma função lambda para passar a referência da linha para a função de remoção
        remove_button = ttk.Button(row_frame, text="X", width=3, command=lambda rf=row_frame: self.remover_criterio(rf))
        remove_button.grid(row=0, column=len(self.produtos) + 1, padx=5)
        
        # Armazenar a linha
        self.criterio_rows.append({
            "frame": row_frame,
            "criterio_var": criterio_var,
            "combos": combos
        })
        
        # Configurar expansão de colunas
        row_frame.columnconfigure(0, weight=1)
        for i in range(len(self.produtos)):
            row_frame.columnconfigure(i+1, weight=1)
        self.criterios_frame.columnconfigure(0, weight=1)


    def remover_criterio(self, row_frame):
        """Remove a linha de critério da interface e da lista de controle."""
        # Encontrar e remover o item correspondente na lista de controle
        self.criterio_rows = [row for row in self.criterio_rows if row["frame"] is not row_frame]
        
        # Destruir o frame (e todos os seus widgets)
        row_frame.destroy()
        
        # Reorganizar as linhas restantes (opcional, mas bom para manter a ordem)
        for i, row in enumerate(self.criterio_rows):
            row["frame"].grid(row=i, column=0)


    def processar_e_gerar_pdf(self):
        """Coleta os dados dinâmicos, calcula a pontuação e chama a função de geração de PDF."""
        self.status_var.set("Processando dados e gerando PDF...")
        self.master.update()

        # 1. Coletar os nomes dos produtos atualizados
        produtos_atuais = [var.get() for var in self.vars_produtos]
        
        dados_comparacao = {prod: {"Total": 0, "Criterios": {}} for prod in produtos_atuais}
        criterios_usados = []
        
        # 2. Coletar as seleções e calcular pontuações
        pontuacoes_totais = {prod: 0 for prod in produtos_atuais}
        
        for row in self.criterio_rows:
            criterio = row["criterio_var"].get().strip()
            
            # Ignorar critérios vazios
            if not criterio:
                continue
                
            criterios_usados.append(criterio)
            
            for i, produto in enumerate(produtos_atuais):
                combo_var = row["combos"][i].cget("textvariable")
                # É necessário obter o valor da variável associada ao Combobox
                # Como o Combobox é criado com `textvariable=var_selecao`, precisamos acessar o valor
                # A maneira mais robusta é usar o `get()` do widget, mas o Tkinter retorna o nome da variável
                # Vamos assumir que o `textvariable` é uma variável de controle (tk.StringVar)
                
                # Acessar a variável de controle através do nome (mais complexo) ou
                # Acessar o valor diretamente do Combobox (mais simples, mas depende da implementação do ttk)
                
                # Solução mais simples: como criamos o `tk.StringVar` e o passamos, vamos tentar acessá-lo.
                # No entanto, o `row["combos"][i]` é o widget Combobox.
                # Acessar o valor do Combobox:
                opcao_selecionada = row["combos"][i].get()
                
                pontos = OPCOES_PONTOS.get(opcao_selecionada, 0)
                
                pontuacoes_totais[produto] += pontos
                
                dados_comparacao[produto]["Criterios"][criterio] = {
                    "Opcao": opcao_selecionada,
                    "Pontos": pontos
                }
        
        # 3. Finalizar a estrutura de dados e determinar a Vencedora
        for produto in produtos_atuais:
            dados_comparacao[produto]["Total"] = pontuacoes_totais[produto]

        if not pontuacoes_totais or not criterios_usados:
            nome_vencedora = "Nenhuma (Sem critérios ou pontuação)"
        else:
            vencedora = max(pontuacoes_totais, key=pontuacoes_totais.get)
            max_pontos = pontuacoes_totais[vencedora]
            
            # Checar por empates
            empates = [prod for prod, pontos in pontuacoes_totais.items() if pontos == max_pontos]
            
            if len(empates) > 1:
                nome_vencedora = "Empate: " + " e ".join(empates)
            else:
                nome_vencedora = vencedora

        # 4. Gerar o PDF
        try:
            nome_arquivo = gerar_pdf(dados_comparacao, nome_vencedora, criterios_usados)
            self.status_var.set(f"Sucesso! PDF gerado como: {nome_arquivo}")
            self.status_label.config(foreground="green")
        except Exception as e:
            self.status_var.set(f"Erro ao gerar PDF: {e}")
            self.status_label.config(foreground="red")


# --- SIMULAÇÃO PARA GERAÇÃO DE PDF DE EXEMPLO (PARA AMBIENTE SEM GUI) ---
def simular_dados():
    """Gera dados simulados para o PDF de exemplo."""
    produtos_simulados = ["ADAPTA", "INNER AI", "TESS AI (PARETO)"]
    criterios_simulados = [
        "Preço e condições",
        "IA para texto e funcionalidades",
        "Outros modelos de IA e ferramentas...",
        "Crédito",
        "Suporte ao Cliente" # Critério dinâmico extra
    ]
    
    # Mapeamento de Opções para Pontos
    mapa_simulado = {
        "ADAPTA": {
            "Preço e condições": "Excelente",
            "IA para texto e funcionalidades": "Bom",
            "Outros modelos de IA e ferramentas...": "Regular",
            "Crédito": "Excelente",
            "Suporte ao Cliente": "Bom"
        },
        "INNER AI": {
            "Preço e condições": "Bom",
            "IA para texto e funcionalidades": "Excelente",
            "Outros modelos de IA e ferramentas...": "Bom",
            "Crédito": "Regular",
            "Suporte ao Cliente": "Excelente"
        },
        "TESS AI (PARETO)": {
            "Preço e condições": "Regular",
            "IA para texto e funcionalidades": "Regular",
            "Outros modelos de IA e ferramentas...": "Excelente",
            "Crédito": "Bom",
            "Suporte ao Cliente": "Regular"
        }
    }
    
    dados_comparacao_simulados = {}
    pontuacoes_totais = {}
    
    for produto in produtos_simulados:
        total = 0
        criterios_data = {}
        for criterio in criterios_simulados:
            opcao = mapa_simulado[produto].get(criterio, "Não possui")
            pontos = OPCOES_PONTOS.get(opcao, 0)
            total += pontos
            criterios_data[criterio] = {"Opcao": opcao, "Pontos": pontos}
        
        dados_comparacao_simulados[produto] = {"Total": total, "Criterios": criterios_data}
        pontuacoes_totais[produto] = total

    # Determinar a Vencedora Simulada
    vencedora = max(pontuacoes_totais, key=pontuacoes_totais.get)
    max_pontos = pontuacoes_totais[vencedora]
    empates = [prod for prod, pontos in pontuacoes_totais.items() if pontos == max_pontos]
    
    if len(empates) > 1:
        nome_vencedora_simulada = "Empate: " + " e ".join(empates)
    else:
        nome_vencedora_simulada = vencedora
        
    return dados_comparacao_simulados, nome_vencedora_simulada, criterios_simulados

if __name__ == "__main__":
    # Se estiver em um ambiente que suporta GUI, executa a aplicação normalmente
    try:
        root = tk.Tk()
        app = ComparadorApp(root)
        root.mainloop()
    except Exception as e:
        # Se falhar (ambiente sem GUI, como o sandbox), gera um PDF de exemplo com dados simulados
        print("Ambiente sem suporte a GUI detectado. Gerando PDF de exemplo com dados simulados.")
        
        dados_comparacao_simulados, nome_vencedora_simulada, criterios_simulados = simular_dados()

        try:
            nome_arquivo = gerar_pdf(dados_comparacao_simulados, nome_vencedora_simulada, criterios_simulados)
            print(f"PDF de exemplo gerado com sucesso: {nome_arquivo}")
        except Exception as e:
            print(f"Erro ao gerar PDF de exemplo: {e}")
