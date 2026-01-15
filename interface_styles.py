import streamlit as st

def aplicar_estilos():
    st.markdown("""
        <style>
            .stChatMessage { padding: 1rem; border-radius: 10px; margin-bottom: 1rem; font-size: 16px; line-height: 1.5; }
            .user-message { background-color: #e9e9e9; border-left: 5px solid #0f5132; }
            .assistant-message { background-color: #e9e9e9; border-left: 5px solid #191970; }
            .title { font-size: 30px; margin-bottom: 10px; font-weight: bold; }
            .subtitle { font-size: 16px; color: #555; }
            .block-container { padding-bottom: 150px !important; }
            [data-testid="stChatInputContainer"] { margin-bottom: 80px !important; }
            .footer { position: fixed; bottom: 0; left: 0; width: 100%; background-color: #f9f9f9; color: #555; text-align: center; font-size: 14px; padding: 10px 0; border-top: 1px solid #ddd; z-index: 9999; }
        </style>
    """, unsafe_allow_html=True)

def exibir_cabecalho(num_docs_formatado):
    col1, col2 = st.columns([1, 8])
    with col1:
        try:
            st.image(r"IESB.jpg", width=200)
            st.image(r"Athenia.png", width=200)
        except:
            st.caption("Logo IESB")
            st.caption("Logo Athenia")
    with col2:
        st.markdown(f"""
            <div class="title">Protótipo IA - Dissertação de Mestrado </div>
            <div class="subtitle">
            As informações são extraídas do banco de dados BDTD do IBICT, que atualmente possui <b>{num_docs_formatado}</b> documentos. 
            Esses dados podem ser complementados com informações geradas por uma inteligência artificial, com o objetivo de enriquecer e contextualizar os resultados apresentados. 
            Além disso, todo o processo considera práticas de preservação digital, garantindo que os dados sejam armazenados de forma segura, acessível e íntegra ao longo do tempo, 
            protegendo contra perdas, obsolescência tecnológica e degradação das informações.
            </div>
        """, unsafe_allow_html=True)

def render_message(role, message):
    if role == "user":
        st.markdown(f'<div class="stChatMessage user-message"><strong>Você:</strong><br>{message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="stChatMessage assistant-message"><strong>Assistente:</strong><br>{message}</div>', unsafe_allow_html=True)

def exibir_rodape():
    st.markdown('<div class="footer">Dados provenientes do repositório <strong>IBICT - BDTD</strong></div>', unsafe_allow_html=True)

def scroll_script():
    st.markdown('''
        <input type="text" id="scrollTarget" style="opacity:0; height:0; border:0; padding:0; margin:0">
        <script>
            const el = document.getElementById("scrollTarget");
            if (el) { setTimeout(() => { el.focus(); }, 500); }
        </script>
    ''', unsafe_allow_html=True)
