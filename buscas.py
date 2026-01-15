import os
import pysolr
import fitz
import streamlit as st
from nltk.tokenize import word_tokenize
from rank_bm25 import BM25Okapi
from dotenv import load_dotenv

PASTA_PRESERVACAO = r"pdfs/Preservação_Digital"
PASTA_CARDIO = r"pdfs/Doenca_Cardiaca"

load_dotenv()
URL = os.getenv("SOLR_URL")
try:
    solr = pysolr.Solr(URL, always_commit=True, timeout=30)
except Exception:
    class MockSolr:
        def search(self, *args, **kwargs): return type('obj', (object,), {'hits': 0, 'docs': []})
    solr = MockSolr()

@st.cache_data(ttl=43200)
def get_num_docs():
    try: return solr.search("*:*", rows=0).hits
    except: return 0

def buscar_no_solr(query, max_resultados=10):
    try:
        results = solr.search(query, **{'fl': 'title,author,description,publishDate,url','rows': max_resultados})
        return results.docs if results.hits > 0 else []
    except: return []

def formatar_docs(docs):
    blocos = []
    for i, doc in enumerate(docs[:10], start=1):
        blocos.append(f"**{i}. {doc.get('title', 'Sem título')}**\n- Autor: {doc.get('author', 'Não informado')}\n- [Acessar]({doc.get('url', '#')})")
    return "\n".join(blocos)

@st.cache_data(ttl=86400)
def carregar_e_indexar_pdfs(pasta, chunk_size=1200):
    corpus_chunks = []
    if not os.path.isdir(pasta): return corpus_chunks, None
    for arquivo in sorted(os.listdir(pasta)):
        if arquivo.lower().endswith(".pdf"):
            try:
                doc = fitz.open(os.path.join(pasta, arquivo))
                texto = "".join([pag.get_text() for pag in doc])
                doc.close()
                for i in range(0, len(texto), chunk_size):
                    parte = texto[i:i+chunk_size]
                    tokens = word_tokenize(parte.lower())
                    corpus_chunks.append({"arquivo": arquivo, "texto": parte, "tokens": tokens})
            except: continue
    bm25 = BM25Okapi([c["tokens"] for c in corpus_chunks]) if corpus_chunks else None
    return corpus_chunks, bm25

@st.cache_data(ttl=60*60*24)
def carregar_indices_completos():
    corpus_preservacao, index_preservacao = carregar_e_indexar_pdfs(PASTA_PRESERVACAO)
    corpus_cardio, index_cardio = carregar_e_indexar_pdfs(PASTA_CARDIO)
    return corpus_preservacao, index_preservacao, corpus_cardio, index_cardio

def buscar_trechos_relevantes(query, corpus_chunks, bm25, k=10):
    if not corpus_chunks or bm25 is None: return ""
    tokens_query = word_tokenize(query.lower())
    scores = bm25.get_scores(tokens_query)
    melhores_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
    return "\n\n".join([f"Arquivo: {corpus_chunks[i]['arquivo']}\n{corpus_chunks[i]['texto']}" for i in melhores_idx])
