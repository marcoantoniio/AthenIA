import streamlit as st
import os
import nltk

from interface_styles import aplicar_estilos, exibir_cabecalho, render_message, exibir_rodape, scroll_script
from buscas import (
    get_num_docs, buscar_no_solr, formatar_docs,
    carregar_indices_completos, buscar_trechos_relevantes,
    PASTA_PRESERVACAO, PASTA_CARDIO
)
from ia_engine import gerar_query_solr, detectar_contextualidade, client

st.set_page_config(page_title="Chatbot Acadêmico", layout="centered")
aplicar_estilos()

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


corpus_preservacao, index_preservacao, corpus_cardio, index_cardio = carregar_indices_completos()
num_docs = get_num_docs()
num_docs_formatado = f"{num_docs:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

with st.sidebar:
    st.header("Configurações de Busca")
    modo_busca = st.radio(
        "Escolha onde buscar as informações:",
        ["Banco Solr (IBICT - BDTD)", "PDFs locais"],
        index=1
    )
    st.markdown("---")
    st.markdown("*Você pode alternar o modo de busca a qualquer momento.*")
    st.image(r"BDTD.jpg", width=200)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "ultimo_contexto" not in st.session_state:
    st.session_state.ultimo_contexto = ""
if "docs_anteriores" not in st.session_state:
    st.session_state.docs_anteriores = []

exibir_cabecalho(num_docs_formatado)

for role, message in st.session_state.chat_history:
    render_message(role, message)

user_input = st.chat_input("Digite sua pergunta ou tema de pesquisa...")

if user_input:
    if any(p in user_input.lower() for p in ["quantos pdf", "quantos arquivos", "listar pdf"]):
        try:
            num_p = len([f for f in os.listdir(PASTA_PRESERVACAO) if f.lower().endswith(".pdf")])
            num_c = len([f for f in os.listdir(PASTA_CARDIO) if f.lower().endswith(".pdf")])
            total = num_p + num_c
            resposta_contagem = (
                f"Atualmente há **{total} PDFs locais** disponíveis:<br><br>"
                f"- Preservação digital: **{num_p} PDFs**<br>"
                f"- Doença cardíaca: **{num_c} PDFs**"
            )
            st.session_state.chat_history.append(("assistant", resposta_contagem))
            render_message("assistant", resposta_contagem)
            st.stop()
        except Exception:
            pass

    st.session_state.chat_history.append(("user", user_input))
    render_message("user", user_input)

    pergunta_contextual = detectar_contextualidade(user_input, st.session_state.ultimo_contexto)

    contexto_para_ia = ""
    resposta_direta = ""
    tem_contexto_anterior = bool(st.session_state.ultimo_contexto)

    if pergunta_contextual and tem_contexto_anterior:
        contexto_para_ia = st.session_state.ultimo_contexto
    else:
        with st.spinner("Buscando informações..."):
            if modo_busca == "Banco Solr (IBICT - BDTD)":
                query = gerar_query_solr(user_input)
                documentos_solr = buscar_no_solr(query)
                if documentos_solr:
                    contexto_para_ia = formatar_docs(documentos_solr)
                    st.session_state.docs_anteriores = documentos_solr
                else:
                    contexto_para_ia = "Nenhum documento encontrado."
                    resposta_direta = "Nenhum documento relevante foi encontrado no BDTD (IBICT)."

            elif modo_busca == "PDFs locais":
                trechos_p = buscar_trechos_relevantes(user_input, corpus_preservacao, index_preservacao, k=10)
                trechos_c = buscar_trechos_relevantes(user_input, corpus_cardio, index_cardio, k=10)

                partes = []
                if trechos_p: partes.append(f"PDFs Preservação:\n{trechos_p}")
                if trechos_c: partes.append(f"PDFs Cardiologia:\n{trechos_c}")

                if not partes:
                    contexto_para_ia = "Nenhum trecho encontrado."
                    resposta_direta = "Nenhum conteúdo relevante encontrado nos PDFs locais."
                else:
                    contexto_para_ia = "\n\n".join(partes)

            st.session_state.ultimo_contexto = contexto_para_ia

    if resposta_direta:
        resposta_final = resposta_direta
    else:
        mensagens = [
            {"role": "system", "content": "Você é um assistente acadêmico especializado em teses e dissertações."
                    "Use o histórico de conversa e os documentos fornecidos para responder."
                    f"Se não tiver pdf relacionado ao assunto, apenas responda com {resposta_direta}"
                    "Se não houver documentos relevantes, utilize as informações do histórico anterior. "
                    "Se ainda assim não houver base suficiente, diga claramente que não há informações disponíveis no banco de dados. "
                    "Seja direto, acadêmico e objetivo, e finalize informando o total de documentos e o titulo de cada arquivo (não fale o nome do documento)."}
        ]
        for r, m in st.session_state.chat_history:
            mensagens.append({"role": r, "content": m})

        mensagens.append({"role": "system", "content": f"Baseie-se nisto: {contexto_para_ia}"})

        with st.spinner("Gerando resposta..."):
            try:
                res = client.chat.completions.create(
                    model="gpt-5-mini-2025-08-07",
                    messages=mensagens
                )
                resposta_final = res.choices[0].message.content.strip()
            except Exception as e:
                resposta_final = f"Erro ao gerar resposta: {e}"

    st.session_state.chat_history.append(("assistant", resposta_final))
    render_message("assistant", resposta_final)
    scroll_script()

exibir_rodape()
