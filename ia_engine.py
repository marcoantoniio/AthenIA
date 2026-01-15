import os
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gerar_query_solr(pergunta):
    prompt = f"""
    Gere uma query Solr para buscar teses ou dissertações sobre o tema:
    "{pergunta}"

    Use os campos "title" e "author".
    A query deve buscar em ambos os campos com operador OR.
    Retorne apenas a query, no formato:
    (title:(termos) OR author:(termos))
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": prompt}]
        )
        query = response.choices[0].message.content.strip()
    except Exception as e:
        st.warning(f"Falha ao gerar query com IA: {e}. Usando busca simples.")
        query = f"(title:({pergunta}) OR author:({pergunta}))"

    if not query or ("title" not in query and "author" not in query):
        query = f"(title:({pergunta}) OR author:({pergunta}))"
    return query

def detectar_contextualidade(pergunta, ultimo_contexto):
    prompt = f"CONTEXTO: {ultimo_contexto}\nPERGUNTA: {pergunta}\nResponda apenas 'contextual' ou 'nao contextual'."
    try:
        res = client.chat.completions.create(model="gpt-5-mini-2025-08-07", messages=[{"role": "user", "content": prompt}]).choices[0].message.content.strip().lower()
        return "contextual" in res
    except: return False
