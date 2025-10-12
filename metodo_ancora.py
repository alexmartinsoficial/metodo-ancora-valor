import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

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
</style>
""", unsafe_allow_html=True)

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

# Inicializar variáveis de sessão
if 'etapa' not in st.session_state:
    st.session_state.etapa = 1
if 'dados' not in st.session_state:
    st.session_state.dados = {}
if 'moedas_selecionadas' not in st.session_state:
    st.session_state.moedas_selecionadas = {}

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
    
    profissao = st.selectbox(
        "Sua Profissão/Área",
        ['Selecione...'] + PROFISSOES,
        key='profissao_select'
    )
    
    oferta_principal = st.text_input(
        "Nome do Serviço/Produto Principal",
        placeholder="Ex: Clareamento Dental",
        key='oferta_input'
    )
    
    preco_principal = st.text_input(
        "Preço da Oferta Principal",
        placeholder="Ex: R$ 1.200,00",
        key='preco_input'
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
    
    nome_ancora = st.text_input(
        "Nome da Oferta Âncora",
        placeholder="Ex: Kit de Manutenção do Clareamento",
        key='ancora_input'
    )
    
    col1, col2 = st.columns(2)
    with col1:
        preco_min = st.text_input(
            "Preço Mínimo",
            placeholder="Ex: R$ 200",
            key='preco_min_input'
        )
    with col2:
        preco_max = st.text_input(
            "Preço Máximo",
            placeholder="Ex: R$ 400",
            key='preco_max_input'
        )
    
    col3, col4 = st.columns(2)
    with col3:
        parc_min = st.text_input(
            "Parcelamento Mínimo",
            placeholder="Ex: 2x",
            key='parc_min_input'
        )
    with col4:
        parc_max = st.text_input(
            "Parcelamento Máximo",
            placeholder="Ex: 6x",
            key='parc_max_input'
        )
    
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
    st.info("Marque as concessões que você pode oferecer e descreva como aplicará cada uma")
    
    for i, moeda in enumerate(MOEDAS):
        with st.expander(f"{'✓' if moeda in st.session_state.moedas_selecionadas else '○'} {moeda}", expanded=moeda in st.session_state.moedas_selecionadas):
            usar = st.checkbox(
                f"Vou usar: {moeda}",
                key=f'check_{i}',
                value=moeda in st.session_state.moedas_selecionadas
            )
            
            if usar:
                descricao = st.text_area(
                    "Como você vai aplicar essa concessão?",
                    placeholder=f"Descreva como você aplicará: {moeda.lower()}",
                    key=f'desc_{i}',
                    value=st.session_state.moedas_selecionadas.get(moeda, ''),
                    height=80
                )
                if descricao:
                    st.session_state.moedas_selecionadas[moeda] = descricao
            elif moeda in st.session_state.moedas_selecionadas:
                del st.session_state.moedas_selecionadas[moeda]
    
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
    st.markdown("""
    <div class="success-box">
        <h3 style="color: #065F46; margin-bottom: 0.5rem;">✓ Plano Gerado com Sucesso!</h3>
        <p style="color: #047857;">Tire um print da tela ou salve a imagem abaixo</p>
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
            <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Oferta Principal</div>
            <div style="font-size: 1.3rem; font-weight: bold; margin-bottom: 0.3rem;">{st.session_state.dados['oferta_principal']}</div>
            <div style="font-size: 2rem; font-weight: bold;">{st.session_state.dados['preco_principal']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Oferta Âncora
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #3B82F6 0%, #06B6D4 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 1rem;">
            <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Oferta Âncora</div>
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
        
        # Moedas de Troca
        st.markdown("""
        <div style="background: #F9FAFB; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
            <h4 style="color: #1F2937; font-size: 1rem; margin-bottom: 1rem;">Concessões Disponíveis</h4>
        """, unsafe_allow_html=True)
        
        for moeda, descricao in st.session_state.moedas_selecionadas.items():
            st.markdown(f"""
            <div style="background: white; padding: 0.8rem; border-radius: 8px; border-left: 3px solid #4F46E5; margin-bottom: 0.8rem;">
                <div style="font-weight: 600; color: #1F2937; font-size: 0.85rem; margin-bottom: 0.3rem;">{moeda}</div>
                <div style="color: #6B7280; font-size: 0.8rem;">{descricao}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Roteiro
        st.markdown("""
        <div style="background: #FFFBEB; border: 1px solid #FDE68A; padding: 1rem; border-radius: 10px;">
            <h4 style="color: #1F2937; font-size: 0.95rem; margin-bottom: 0.8rem;">💡 Roteiro de Negociação</h4>
            <ol style="color: #374151; font-size: 0.8rem; padding-left: 1.5rem; margin: 0;">
                <li style="margin-bottom: 0.4rem;"><strong>1.</strong> Apresente a Oferta Principal</li>
                <li style="margin-bottom: 0.4rem;"><strong>2.</strong> Se houver resistência, introduza a Âncora</li>
                <li style="margin-bottom: 0.4rem;"><strong>3.</strong> Use concessões, nunca desconto</li>
                <li style="margin-bottom: 0.4rem;"><strong>4.</strong> Mantenha o preço principal intacto</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Botões
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Criar Nova Estratégia", use_container_width=True):
            st.session_state.etapa = 1
            st.session_state.dados = {}
            st.session_state.moedas_selecionadas = {}
            st.rerun()
    
    with col2:
        st.info("💡 Dica: Tire um print dessa tela para salvar seu plano!")
