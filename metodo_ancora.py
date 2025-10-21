import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(
    page_title="Método Âncora de Valor",
    page_icon="⚓",
    layout="centered"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
    }
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        color: #1F2937;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #6B7280;
    }
    .step-indicator {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 2rem 0;
        font-weight: bold;
    }
    .success-box {
        background: #ECFDF5;
        border: 2px solid #A7F3D0;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
    }
    .tooltip-box {
        background: #EFF6FF;
        border-left: 4px solid #3B82F6;
        padding: 0.8rem;
        margin: 0.5rem 0 1rem 0;
        border-radius: 5px;
        font-size: 0.9rem;
        color: #1E40AF;
    }
    .exemplo-box {
        background: #F0FDF4;
        border-left: 4px solid #10B981;
        padding: 0.8rem;
        margin: 0.5rem 0 1rem 0;
        border-radius: 5px;
        font-size: 0.85rem;
        color: #065F46;
    }
    .login-box {
        max-width: 450px;
        margin: 3rem auto;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Função para carregar usuários do arquivo
@st.cache_data(ttl=300)  # Cache por 5 minutos
def carregar_usuarios():
    try:
        with open('usuarios.txt', 'r', encoding='utf-8') as f:
            usuarios = {}
            for linha in f:
                linha = linha.strip()
                if linha and ',' in linha:
                    partes = linha.split(',')
                    if len(partes) >= 3:
                        email = partes[0].strip().lower()
                        codigo = partes[1].strip()
                        data_expiracao = partes[2].strip()
                        usuarios[email] = {
                            'codigo': codigo,
                            'expiracao': data_expiracao
                        }
            return usuarios
    except FileNotFoundError:
        st.error("⚠️ Arquivo de usuários não encontrado. Contate o suporte.")
        return {}

# Função para validar acesso
def validar_acesso(email, codigo):
    usuarios = carregar_usuarios()
    email = email.strip().lower()
    codigo = codigo.strip()
    
    if email not in usuarios:
        return False, "Acesso negado. Verifique seu email e código."
    
    if usuarios[email]['codigo'] != codigo:
        return False, "Acesso negado. Verifique seu email e código."
    
    # Verificar data de expiração
    try:
        data_expiracao = datetime.strptime(usuarios[email]['expiracao'], '%Y-%m-%d')
        if datetime.now() > data_expiracao:
            return False, "Seu acesso expirou. Entre em contato com o suporte para renovar."
    except:
        return False, "Erro ao verificar validade do acesso. Contate o suporte."
    
    return True, "Acesso autorizado!"

# Inicializar variáveis de sessão
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'email_usuario' not in st.session_state:
    st.session_state.email_usuario = ''
if 'etapa' not in st.session_state:
    st.session_state.etapa = 1
if 'dados' not in st.session_state:
    st.session_state.dados = {}
if 'moedas_selecionadas' not in st.session_state:
    st.session_state.moedas_selecionadas = {}
if 'imagem_gerada' not in st.session_state:
    st.session_state.imagem_gerada = None

# TELA DE LOGIN
if not st.session_state.autenticado:
    st.markdown("""
    <div class="main-header">
        <div class="main-title">⚓ Método Âncora de Valor</div>
        <div class="subtitle">Área de Acesso</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔐 Faça seu login")
    st.info("📧 O acesso será enviado pela equipe de atendimento após confirmação do pagamento")
    
    email_login = st.text_input(
        "Email cadastrado",
        placeholder="seu@email.com",
        key="email_login"
    )
    
    codigo_login = st.text_input(
        "Código de acesso",
        placeholder="Ex: ALN2847",
        type="password",
        key="codigo_login"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Acessar Ferramenta", type="primary", use_container_width=True):
            if email_login and codigo_login:
                valido, mensagem = validar_acesso(email_login, codigo_login)
                if valido:
                    st.session_state.autenticado = True
                    st.session_state.email_usuario = email_login
                    st.success(mensagem)
                    st.rerun()
                else:
                    st.error(mensagem)
            else:
                st.warning("⚠️ Preencha email e código de acesso")
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6B7280; font-size: 0.9rem;">
        <p>💡 Acesso válido por 1 ano a partir da data de ativação</p>
        <p>Problemas com o login? Entre em contato com o suporte</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()

# RESTO DO APLICATIVO (após login)

# Lista de profissões
PROFISSOES = [
    'Advogado Civil',
    'Empresa de Limpeza',
    'Profissional de Estética Avançada',
    'Escola de Idiomas',
    'Instituição de Pós-Graduação',
    'Polo EAD de Faculdade',
    'Corretor Imobiliário',
    'Corretora de Seguros',
    'Joalheria',
    'Videomaker',
    'Social Media',
    'Escola de Cursos Preparatórios',
    'Dentista',
    'Ortopedista'
]

# Exemplos por profissão
EXEMPLOS_PROFISSAO = {
    'Dentista': {
        'oferta_principal': 'Clareamento dental completo',
        'preco_principal': 'R$ 1.200,00',
        'ancora': 'Kit de manutenção (pasta, gel, moldeira)',
        'ancora_exemplo': 'Custa R$ 50 para você, mas o cliente percebe como R$ 300 de valor'
    },
    'Advogado Civil': {
        'oferta_principal': 'Consultoria jurídica completa',
        'preco_principal': 'R$ 3.500,00',
        'ancora': 'Análise prévia de documentos',
        'ancora_exemplo': '1h do seu tempo, mas evita retrabalho e gera confiança'
    },
    'Empresa de Limpeza': {
        'oferta_principal': 'Pacote mensal de limpeza',
        'preco_principal': 'R$ 800,00',
        'ancora': 'Limpeza de vidros incluída',
        'ancora_exemplo': 'Custo baixo para você, grande valor percebido'
    },
    'Profissional de Estética Avançada': {
        'oferta_principal': 'Tratamento facial completo',
        'preco_principal': 'R$ 600,00',
        'ancora': 'Sessão de limpeza de pele',
        'ancora_exemplo': 'Material de baixo custo, mas prepara a pele para o tratamento'
    },
    'Escola de Idiomas': {
        'oferta_principal': 'Curso anual de inglês',
        'preco_principal': 'R$ 4.800,00',
        'ancora': 'Material didático premium incluso',
        'ancora_exemplo': 'Custo do material é baixo, mas aumenta percepção de qualidade'
    },
    'Corretor Imobiliário': {
        'oferta_principal': 'Venda do imóvel',
        'preco_principal': '6% de comissão',
        'ancora': 'Sessão de fotos profissionais',
        'ancora_exemplo': 'Parceria com fotógrafo = custo zero, mas valoriza o anúncio'
    }
}

# Moedas de troca
MOEDAS = [
    'Bonificação',
    'Garantia Estendida',
    'Programa de Fidelidade',
    'Parcelamento Facilitado',
    'Entrega Rápida/Prioritária',
    'Personalização',
    'Recompensa por Indicação'
]

# Tooltips para cada campo
TOOLTIPS = {
    'profissao': 'Escolha sua área de atuação para receber exemplos personalizados',
    'oferta_principal': 'Seu produto ou serviço PRINCIPAL que você quer vender. Este preço NÃO sofrerá desconto.',
    'preco_principal': 'Preço cheio da sua oferta principal. Este valor permanecerá intacto na negociação.',
    'ancora': 'Um produto/serviço adicional de BAIXO CUSTO para você, mas ALTO VALOR percebido pelo cliente. Esta será sua ferramenta de negociação.',
    'preco_minimo': 'Quanto você PRECISA receber no mínimo para não ter prejuízo? Considere seus custos reais.',
    'preco_maximo': 'Preço ideal da âncora. Pode ser até 30-40% do valor da oferta principal.',
    'parcelamento': 'Quantas vezes você pode parcelar sem comprometer seu fluxo de caixa?',
    'moedas': 'Concessões que você pode oferecer SEM dar desconto. Escolha 1 a 3 opções.',
    'prioridade': 'Defina a ordem: qual concessão você oferece primeiro, segunda, terceira...'
}

# Inicializar variáveis de sessão
if 'etapa' not in st.session_state:
    st.session_state.etapa = 1
if 'dados' not in st.session_state:
    st.session_state.dados = {}
if 'moedas_selecionadas' not in st.session_state:
    st.session_state.moedas_selecionadas = {}
if 'imagem_gerada' not in st.session_state:
    st.session_state.imagem_gerada = None

# Função para mostrar tooltip
def mostrar_tooltip(texto):
    st.markdown(f'<div class="tooltip-box">💡 {texto}</div>', unsafe_allow_html=True)

# Função para mostrar exemplo
def mostrar_exemplo(texto):
    st.markdown(f'<div class="exemplo-box">✨ <strong>Exemplo:</strong> {texto}</div>', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <div class="main-title">⚓ Método Âncora de Valor</div>
    <div class="subtitle">Proteja sua oferta e negocie com inteligência</div>
</div>
""", unsafe_allow_html=True)

# Progress bar
progress = st.session_state.etapa / 4
st.progress(progress)

# Indicador de etapa
etapas_nomes = ['Identificação', 'Oferta Âncora', 'Moedas de Troca', 'Resultado']
st.markdown(f"""
<div class="step-indicator">
    Etapa {st.session_state.etapa} de 4: {etapas_nomes[st.session_state.etapa - 1]}
</div>
""", unsafe_allow_html=True)

# ETAPA 1: Identificação
if st.session_state.etapa == 1:
    st.subheader("📋 Sua Oferta Principal")
    
    # Profissão
    st.markdown("**Sua Profissão/Área**")
    mostrar_tooltip(TOOLTIPS['profissao'])
    profissao = st.selectbox(
        "Selecione sua profissão",
        ['Selecione...'] + PROFISSOES,
        key='profissao_select',
        label_visibility='collapsed'
    )
    
    # Mostrar exemplo logo após escolher profissão
    if profissao != 'Selecione...' and profissao in EXEMPLOS_PROFISSAO:
        exemplo = EXEMPLOS_PROFISSAO[profissao]
        mostrar_exemplo(f"{profissao} - {exemplo['oferta_principal']} por {exemplo['preco_principal']}")
    
    st.markdown("---")
    
    # Oferta Principal
    st.markdown("**Nome do Serviço/Produto Principal**")
    mostrar_tooltip(TOOLTIPS['oferta_principal'])
    oferta_principal = st.text_input(
        "Digite o nome da oferta",
        placeholder="Ex: Clareamento Dental",
        key='oferta_input',
        label_visibility='collapsed'
    )
    
    # Preço Principal
    st.markdown("**Preço da Oferta Principal**")
    mostrar_tooltip(TOOLTIPS['preco_principal'])
    preco_principal = st.text_input(
        "Digite o preço",
        placeholder="Ex: R$ 1.200,00",
        key='preco_input',
        label_visibility='collapsed'
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col3:
        if st.button("Avançar →", type="primary", use_container_width=True):
            if profissao != 'Selecione...' and oferta_principal and preco_principal:
                st.session_state.dados['profissao'] = profissao
                st.session_state.dados['oferta_principal'] = oferta_principal
                st.session_state.dados['preco_principal'] = preco_principal
                st.session_state.etapa = 2
                st.rerun()
            else:
                st.error("⚠️ Preencha todos os campos para continuar")

# ETAPA 2: Oferta Âncora
elif st.session_state.etapa == 2:
    st.subheader("🎯 Sua Oferta Âncora")
    
    # Nome da Âncora
    st.markdown("**Nome da Oferta Âncora**")
    mostrar_tooltip(TOOLTIPS['ancora'])
    
    # Mostrar exemplo ABAIXO do tooltip
    profissao = st.session_state.dados.get('profissao', '')
    if profissao in EXEMPLOS_PROFISSAO:
        exemplo = EXEMPLOS_PROFISSAO[profissao]
        mostrar_exemplo(f"{exemplo['ancora']} - {exemplo['ancora_exemplo']}")
    
    nome_ancora = st.text_input(
        "Digite o nome da âncora",
        placeholder="Ex: Kit de Manutenção do Clareamento",
        key='ancora_input',
        label_visibility='collapsed'
    )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Preço Mínimo da Âncora**")
        mostrar_tooltip(TOOLTIPS['preco_minimo'])
        preco_min = st.text_input(
            "Preço mínimo",
            placeholder="Ex: R$ 200,00",
            key='preco_min_input',
            label_visibility='collapsed'
        )
    with col2:
        st.markdown("**Preço Máximo da Âncora**")
        mostrar_tooltip(TOOLTIPS['preco_maximo'])
        preco_max = st.text_input(
            "Preço máximo",
            placeholder="Ex: R$ 400,00",
            key='preco_max_input',
            label_visibility='collapsed'
        )
    
    st.markdown("---")
    
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**Parcelamento Mínimo**")
        parc_min = st.text_input(
            "Ex: 2x",
            placeholder="Ex: 2x",
            key='parc_min_input',
            label_visibility='collapsed'
        )
    with col4:
        st.markdown("**Parcelamento Máximo**")
        parc_max = st.text_input(
            "Ex: 6x",
            placeholder="Ex: 6x",
            key='parc_max_input',
            label_visibility='collapsed'
        )
    
    mostrar_tooltip(TOOLTIPS['parcelamento'])
    
    col_back, col_space, col_next = st.columns([1, 1, 1])
    with col_back:
        if st.button("← Voltar", use_container_width=True):
            st.session_state.etapa = 1
            st.rerun()
    with col_next:
        if st.button("Avançar →", type="primary", use_container_width=True):
            if nome_ancora and preco_min and preco_max:
                st.session_state.dados['nome_ancora'] = nome_ancora
                st.session_state.dados['preco_min'] = preco_min
                st.session_state.dados['preco_max'] = preco_max
                st.session_state.dados['parc_min'] = parc_min
                st.session_state.dados['parc_max'] = parc_max
                st.session_state.etapa = 3
                st.rerun()
            else:
                st.error("⚠️ Preencha todos os campos para continuar")

# ETAPA 3: Moedas de Troca
elif st.session_state.etapa == 3:
    st.subheader("💰 Suas Moedas de Troca")
    
    mostrar_tooltip(TOOLTIPS['moedas'])
    st.info("📊 **Recomendação:** Escolha entre 1 a 3 moedas de troca. Mais que isso pode confundir a negociação.")
    
    mostrar_tooltip(TOOLTIPS['prioridade'])
    
    for i, moeda in enumerate(MOEDAS):
        with st.expander(f"{'✓' if moeda in st.session_state.moedas_selecionadas else '○'} {moeda}", expanded=moeda in st.session_state.moedas_selecionadas):
            usar = st.checkbox(
                f"Vou usar: {moeda}",
                key=f'check_{i}',
                value=moeda in st.session_state.moedas_selecionadas
            )
            
            if usar:
                descricao = st.text_area(
                    "Qual será sua concessão?",
                    placeholder=f"Descreva sua concessão: {moeda.lower()}",
                    key=f'desc_{i}',
                    value=st.session_state.moedas_selecionadas.get(moeda, {}).get('descricao', ''),
                    height=80
                )
                
                prioridade = st.selectbox(
                    "Prioridade (quando usar na negociação)",
                    ['1ª opção (oferecer primeiro)', '2ª opção', '3ª opção - Última opção (só se necessário)'],
                    key=f'prior_{i}',
                    index=st.session_state.moedas_selecionadas.get(moeda, {}).get('prioridade_index', 0) if moeda in st.session_state.moedas_selecionadas else 0
                )
                
                if descricao:
                    st.session_state.moedas_selecionadas[moeda] = {
                        'descricao': descricao,
                        'prioridade': prioridade,
                        'prioridade_index': ['1ª opção (oferecer primeiro)', '2ª opção', '3ª opção - Última opção (só se necessário)'].index(prioridade)
                    }
            elif moeda in st.session_state.moedas_selecionadas:
                del st.session_state.moedas_selecionadas[moeda]
    
    # Contador de moedas selecionadas
    num_moedas = len(st.session_state.moedas_selecionadas)
    if num_moedas > 0:
        cor = "green" if 1 <= num_moedas <= 3 else "orange"
        st.markdown(f"**Moedas selecionadas:** :{cor}[{num_moedas}]")
        if num_moedas > 3:
            st.warning("⚠️ Muitas opções podem confundir. Considere reduzir para 1-3 moedas.")
    
    col_back, col_space, col_next = st.columns([1, 1, 1])
    with col_back:
        if st.button("← Voltar", use_container_width=True, key='voltar_3'):
            st.session_state.etapa = 2
            st.rerun()
    with col_next:
        if st.button("Gerar Resultado →", type="primary", use_container_width=True):
            if len(st.session_state.moedas_selecionadas) > 0:
                st.session_state.etapa = 4
                st.rerun()
            else:
                st.error("⚠️ Selecione pelo menos uma moeda de troca")

# ETAPA 4: Resultado
elif st.session_state.etapa == 4:
    
    # Função para gerar imagem
    def gerar_imagem_resultado():
        # Dimensões otimizadas para celular (1080px largura)
        width = 1080
        margin = 60
        content_width = width - (margin * 2)
        
        # Criar imagem com fundo gradiente
        img = Image.new('RGB', (width, 2400), color='white')
        draw = ImageDraw.Draw(img)
        
        # Gradiente de fundo
        for i in range(width):
            for j in range(2400):
                r = int(235 + (224 - 235) * (i / width))
                g = int(244 + (231 - 244) * (i / width))
                b = int(255 + (255 - 255) * (i / width))
                draw.point((i, j), fill=(r, g, b))
        
        y_pos = 80
        
        # Cabeçalho
        try:
            font_header = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
            font_subheader = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 35)
        except:
            font_header = ImageFont.load_default()
            font_subheader = ImageFont.load_default()
        
        # Centralizar cabeçalho
        header_text = "Plano de Negociação"
        bbox = draw.textbbox((0, 0), header_text, font=font_header)
        header_width = bbox[2] - bbox[0]
        header_x = (width - header_width) // 2
        draw.text((header_x, y_pos), header_text, fill=(31, 41, 55), font=font_header)
        
        y_pos += 80
        
        # Profissão
        prof_text = st.session_state.dados['profissao']
        bbox = draw.textbbox((0, 0), prof_text, font=font_subheader)
        prof_width = bbox[2] - bbox[0]
        prof_x = (width - prof_width) // 2
        draw.text((prof_x, y_pos), prof_text, fill=(107, 114, 128), font=font_subheader)
        
        y_pos += 70
        
        # Fontes para boxes
        try:
            font_label = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
            font_oferta_nome = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
            font_preco = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 55)
            font_box_label = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
            font_box_value = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
        except:
            font_label = ImageFont.load_default()
            font_oferta_nome = ImageFont.load_default()
            font_preco = ImageFont.load_default()
            font_box_label = ImageFont.load_default()
            font_box_value = ImageFont.load_default()
        
        # Box Oferta Principal
        box_height = 220
        draw.rounded_rectangle([(margin, y_pos), (width - margin, y_pos + box_height)], radius=20, fill=(79, 70, 229))
        
        draw.text((margin + 30, y_pos + 25), "OFERTA PRINCIPAL", fill=(200, 200, 255), font=font_label)
        
        # Nome da oferta com quebra
        oferta_y = y_pos + 70
        oferta_lines = textwrap.wrap(st.session_state.dados['oferta_principal'], width=30)
        for line in oferta_lines:
            draw.text((margin + 30, oferta_y), line, fill='white', font=font_oferta_nome)
            oferta_y += 48
        
        draw.text((margin + 30, y_pos + box_height - 75), st.session_state.dados['preco_principal'], fill='white', font=font_preco)
        
        y_pos += box_height + 40
        
        # Box Oferta Âncora
        box_height = 280
        draw.rounded_rectangle([(margin, y_pos), (width - margin, y_pos + box_height)], radius=20, fill=(59, 130, 246))
        
        draw.text((margin + 30, y_pos + 25), "OFERTA ÂNCORA", fill=(200, 230, 255), font=font_label)
        
        ancora_y = y_pos + 70
        ancora_lines = textwrap.wrap(st.session_state.dados['nome_ancora'], width=30)
        for line in ancora_lines:
            draw.text((margin + 30, ancora_y), line, fill='white', font=font_oferta_nome)
            ancora_y += 48
        
        # Boxes internos
        box_interno_y = ancora_y + 20
        box_width = (content_width - 40) // 2
        
        # Box Preço
        draw.rounded_rectangle([(margin + 30, box_interno_y), (margin + 30 + box_width, box_interno_y + 95)], radius=15, fill=(150, 190, 255))
        draw.text((margin + 50, box_interno_y + 18), "Preço", fill='white', font=font_box_label)
        draw.text((margin + 50, box_interno_y + 52), f"{st.session_state.dados['preco_min']} - {st.session_state.dados['preco_max']}", fill='white', font=font_box_value)
        
        # Box Parcelamento
        draw.rounded_rectangle([(margin + 50 + box_width, box_interno_y), (width - margin - 30, box_interno_y + 95)], radius=15, fill=(150, 190, 255))
        draw.text((margin + 70 + box_width, box_interno_y + 18), "Parcelamento", fill='white', font=font_box_label)
        draw.text((margin + 70 + box_width, box_interno_y + 52), f"{st.session_state.dados['parc_min']} - {st.session_state.dados['parc_max']}", fill='white', font=font_box_value)
        
        y_pos += box_height + 40
        
        # Box Moedas (ordenadas por prioridade)
        moedas_ordenadas = sorted(st.session_state.moedas_selecionadas.items(), 
                                  key=lambda x: x[1]['prioridade_index'])
        moedas_height = 100 + len(moedas_ordenadas) * 140
        
        draw.rounded_rectangle([(margin, y_pos), (width - margin, y_pos + moedas_height)], radius=20, fill=(249, 250, 251))
        
        try:
            font_moeda_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 38)
            font_moeda_nome = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
            font_moeda_desc = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
            font_prioridade = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        except:
            font_moeda_title = ImageFont.load_default()
            font_moeda_nome = ImageFont.load_default()
            font_moeda_desc = ImageFont.load_default()
            font_prioridade = ImageFont.load_default()
        
        draw.text((margin + 30, y_pos + 30), "Concessões por Ordem de Prioridade", fill=(31, 41, 55), font=font_moeda_title)
        
        moeda_y = y_pos + 90
        for moeda_nome, moeda_info in moedas_ordenadas:
            # Box branco individual
            draw.rounded_rectangle([(margin + 30, moeda_y), (width - margin - 30, moeda_y + 120)], radius=15, fill='white')
            draw.line([(margin + 30, moeda_y), (margin + 30, moeda_y + 120)], fill=(79, 70, 229), width=8)
            
            # Prioridade badge
            draw.rounded_rectangle([(margin + 60, moeda_y + 12), (margin + 180, moeda_y + 45)], radius=8, fill=(79, 70, 229))
            draw.text((margin + 75, moeda_y + 17), moeda_info['prioridade'].split(' ')[0], fill='white', font=font_prioridade)
            
            draw.text((margin + 200, moeda_y + 12), moeda_nome, fill=(31, 41, 55), font=font_moeda_nome)
            
            # Descrição com quebra
            desc_lines = textwrap.wrap(moeda_info['descricao'], width=50)
            desc_y = moeda_y + 55
            for line in desc_lines[:2]:  # Máximo 2 linhas
                draw.text((margin + 60, desc_y), line, fill=(107, 114, 128), font=font_moeda_desc)
                desc_y += 32
            
            moeda_y += 140
        
        y_pos += moedas_height + 40
        
        # Box Roteiro
        roteiro_height = 280
        draw.rounded_rectangle([(margin, y_pos), (width - margin, y_pos + roteiro_height)], radius=20, fill=(255, 251, 235))
        
        draw.text((margin + 30, y_pos + 30), "💡 Roteiro de Negociação", fill=(31, 41, 55), font=font_moeda_title)
        
        roteiro_items = [
            "1. Apresente a Oferta Principal",
            "2. Se houver resistência, introduza a Âncora",
            "3. Use concessões pela ordem de prioridade",
            "4. Mantenha o preço principal intacto"
        ]
        
        roteiro_y = y_pos + 90
        for item in roteiro_items:
            draw.text((margin + 60, roteiro_y), item, fill=(55, 65, 81), font=font_moeda_desc)
            roteiro_y += 50
        
        # Ajustar altura final da imagem
        final_height = y_pos + roteiro_height + 80
        img_final = img.crop((0, 0, width, final_height))
        
        return img_final
    
    st.markdown("""
    <div class="success-box">
        <h3 style="color: #065F46; margin-bottom: 0.5rem;">✓ Plano Gerado com Sucesso!</h3>
        <p style="color: #047857;">Visualize abaixo e clique para gerar a imagem</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Container do resultado
    with st.container():
        st.markdown("---")
        
        # Cabeçalho
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #EBF4FF 0%, #E0E7FF 100%); border-radius: 10px; margin-bottom: 1rem;">
            <h2 style="color: #1F2937; margin-bottom: 0.3rem;">📊 Plano de Negociação</h2>
            <p style="color: #6B7280; font-size: 0.9rem;">{st.session_state.dados['profissao']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Oferta Principal
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 1rem;">
            <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Oferta Principal (Intocável)</div>
            <div style="font-size: 1.3rem; font-weight: bold; margin-bottom: 0.3rem;">{st.session_state.dados['oferta_principal']}</div>
            <div style="font-size: 2rem; font-weight: bold;">{st.session_state.dados['preco_principal']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Oferta Âncora
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #3B82F6 0%, #06B6D4 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 1rem;">
            <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Oferta Âncora (Ferramenta de Negociação)</div>
            <div style="font-size: 1.3rem; font-weight: bold; margin-bottom: 1rem;">{st.session_state.dados['nome_ancora']}</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.8rem; font-size: 0.8rem;">
                <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 8px;">
                    <div style="font-weight: 600; margin-bottom: 0.3rem;">Preço</div>
                    <div style="font-size: 0.9rem;">{st.session_state.dados['preco_min']} - {st.session_state.dados['preco_max']}</div>
                </div>
                <div style="background: rgba(255,255,255,0.2); padding: 0.8rem; border-radius: 8px;">
                    <div style="font-weight: 600; margin-bottom: 0.3rem;">Parcelamento</div>
                    <div style="font-size: 0.9rem;">{st.session_state.dados['parc_min']} - {st.session_state.dados['parc_max']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Moedas de Troca (ordenadas por prioridade)
        st.markdown("""
        <div style="background: #F9FAFB; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
            <h4 style="color: #1F2937; font-size: 1rem; margin-bottom: 1rem;">Concessões por Ordem de Prioridade</h4>
        """, unsafe_allow_html=True)
        
        moedas_ordenadas = sorted(st.session_state.moedas_selecionadas.items(), 
                                  key=lambda x: x[1]['prioridade_index'])
        
        for moeda, info in moedas_ordenadas:
            st.markdown(f"""
            <div style="background: white; padding: 0.8rem; border-radius: 8px; border-left: 3px solid #4F46E5; margin-bottom: 0.8rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.3rem;">
                    <span style="background: #4F46E5; color: white; padding: 0.2rem 0.6rem; border-radius: 5px; font-size: 0.75rem; font-weight: bold;">{info['prioridade'].split(' ')[0]}</span>
                    <span style="font-weight: 600; color: #1F2937; font-size: 0.85rem;">{moeda}</span>
                </div>
                <div style="color: #6B7280; font-size: 0.8rem;">{info['descricao']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Roteiro
        st.markdown("""
        <div style="background: #FFFBEB; border: 1px solid #FDE68A; padding: 1rem; border-radius: 10px;">
            <h4 style="color: #1F2937; font-size: 0.95rem; margin-bottom: 0.8rem;">💡 Roteiro de Negociação</h4>
            <ol style="color: #374151; font-size: 0.8rem; padding-left: 1.5rem; margin: 0;">
                <li style="margin-bottom: 0.4rem;"><strong>1.</strong> Apresente a Oferta Principal com confiança</li>
                <li style="margin-bottom: 0.4rem;"><strong>2.</strong> Se houver resistência, introduza a Oferta Âncora</li>
                <li style="margin-bottom: 0.4rem;"><strong>3.</strong> Use as concessões pela ordem de prioridade definida</li>
                <li style="margin-bottom: 0.4rem;"><strong>4.</strong> Mantenha o preço da Oferta Principal intacto</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Botões
    if st.session_state.imagem_gerada is None:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Criar Nova Estratégia", use_container_width=True):
                st.session_state.etapa = 1
                st.session_state.dados = {}
                st.session_state.moedas_selecionadas = {}
                st.session_state.imagem_gerada = None
                st.rerun()
        
        with col2:
            if st.button("📸 Gerar Imagem JPEG", type="primary", use_container_width=True):
                with st.spinner("Gerando imagem otimizada para celular..."):
                    img = gerar_imagem_resultado()
                    
                    # Converter para JPEG
                    buf = io.BytesIO()
                    img.save(buf, format='JPEG', quality=95)
                    buf.seek(0)
                    
                    st.session_state.imagem_gerada = buf.getvalue()
                    st.rerun()
    else:
        st.success("✅ Imagem gerada! Clique com botão direito e escolha 'Salvar imagem como...'")
        st.image(st.session_state.imagem_gerada, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="⬇️ Baixar Imagem",
                data=st.session_state.imagem_gerada,
                file_name=f"plano-negociacao-{st.session_state.dados['profissao'].lower().replace(' ', '-')}.jpg",
                mime="image/jpeg",
                use_container_width=True
            )
        with col2:
            if st.button("🔄 Criar Nova Estratégia", use_container_width=True):
                st.session_state.etapa = 1
                st.session_state.dados = {}
                st.session_state.moedas_selecionadas = {}
                st.session_state.imagem_gerada = None
                st.rerun()
