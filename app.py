from flask import Flask, render_template, request, send_file, jsonify
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
import matplotlib
matplotlib.use('Agg')  # Usar backend não interativo para Matplotlib
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

# --- Configurações ---
OPCOES_PONTOS = {
    "Excelente": 10,
    "Bom": 5,
    "Regular": 3,
    "Não possui": 0
}

# --- Funções de Geração de PDF ---
def gerar_grafico_comparacao(dados_comparacao, nome_vencedora):
    produtos = list(dados_comparacao.keys())
    pontuacoes = [dados_comparacao[prod]["Total"] for prod in produtos]

    fig, ax = plt.subplots(figsize=(8, 4))
    barras = ax.bar(produtos, pontuacoes, color=['#1a237e', '#3f51b5', '#7986cb'])
    
    ax.set_ylabel('Pontuação Total')
    ax.set_title(f'Comparativo de Pontuação (Vencedora: {nome_vencedora})')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    for barra in barras:
        yval = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2.0, yval, int(yval), ha='center', va='bottom')

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf

def gerar_pdf(dados_comparacao, nome_vencedora, criterios_usados):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='TitleCustom', parent=styles['Title'], fontSize=20, spaceAfter=20, alignment=1))
    styles.add(ParagraphStyle(name='Heading2Custom', parent=styles['Heading2'], fontSize=14, spaceBefore=10, spaceAfter=10))
    styles.add(ParagraphStyle(name='NormalCustom', parent=styles['Normal'], fontSize=10))

    Story = []
    Story.append(Paragraph("Relatório de Comparação de Produtos", styles['TitleCustom']))
    Story.append(Paragraph(f"<b>VENCEDORA: {nome_vencedora}</b>", styles['Heading2Custom']))
    Story.append(Spacer(1, 12))

    produtos = list(dados_comparacao.keys())
    data = [["<b>CRITÉRIOS</b>"] + [f"<b>{p}</b>" for p in produtos]]

    for criterio in criterios_usados:
        row = [Paragraph(criterio, styles['NormalCustom'])]
        for produto in produtos:
            criterio_data = dados_comparacao[produto]["Criterios"].get(criterio, {"Opcao": "N/A", "Pontos": 0})
            texto_celula = f'{criterio_data["Pontos"]} pts ({criterio_data["Opcao"]})'
            row.append(Paragraph(texto_celula, styles['NormalCustom']))
        data.append(row)
        
    linha_total = [Paragraph("<b>PONTUAÇÃO FINAL</b>", styles['NormalCustom'])]
    for produto in produtos:
        linha_total.append(Paragraph(f"<b>{int(dados_comparacao[produto]['Total'])} pts</b>", styles['NormalCustom']))
    data.append(linha_total)

    table = Table(data, colWidths=[200] + [100] * len(produtos))
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor('#f0f4f8')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    Story.append(table)
    Story.append(Spacer(1, 24))

    grafico_buffer = gerar_grafico_comparacao(dados_comparacao, nome_vencedora)
    img = Image(grafico_buffer, width=450, height=225)
    Story.append(img)

    doc.build(Story)
    buffer.seek(0)
    return buffer

# --- Rotas Flask ---
@app.route('/')
def index():
    return render_template('index.html', opcoes=list(OPCOES_PONTOS.keys()))

@app.route('/gerar_pdf', methods=['POST'])
def gerar_pdf_route():
    try:
        data = request.get_json()
        produtos_atuais = data.get('produtos', [])
        criterios_data = data.get('criterios', [])
        
        if not produtos_atuais or not criterios_data:
            return jsonify({"error": "Dados insuficientes."}), 400

        dados_comparacao = {prod: {"Total": 0, "Criterios": {}} for prod in produtos_atuais}

        for criterio_item in criterios_data:
            criterio_nome = criterio_item.get('nome').strip()
            if not criterio_nome: continue

            for i, produto in enumerate(produtos_atuais):
                opcao = criterio_item['pontuacoes'][i]
                pontos = OPCOES_PONTOS.get(opcao, 0)
                dados_comparacao[produto]["Total"] += pontos
                dados_comparacao[produto]["Criterios"][criterio_nome] = {"Opcao": opcao, "Pontos": pontos}

        vencedora = max(dados_comparacao, key=lambda p: dados_comparacao[p]['Total'])
        
        pdf_buffer = gerar_pdf(dados_comparacao, vencedora, [c['nome'] for c in criterios_data if c['nome'].strip()])
        
        return send_file(pdf_buffer, mimetype='application/pdf', as_attachment=True, download_name='comparativo_produtos.pdf')

    except Exception as e:
        app.logger.error(f"Erro ao gerar PDF: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
