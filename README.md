<p align="center">
   <h1 align="center">AthenIA</h1>
   <p align="center">
      Aplicação em <b>Streamlit</b> para consulta à <b>Biblioteca Digital Brasileira de Teses e Dissertações (BDTD/IBICT)</b>, com foco em <b>preservação digital</b> e enriquecimento das informações com <b>IA generativa</b>.
   </p>
</p>

---

## 📘 Descrição

Este projeto foi desenvolvido para facilitar o acesso, preservação e valorização de conteúdos acadêmicos brasileiros. A aplicação:

- Consulta a base da BDTD via Solr
- Gera automaticamente queries otimizadas usando IA
- Analisa, contextualiza e explica resultados encontrados
- Mantém histórico de conversa para interação contínua e contextualizada

O principal objetivo é unir **acesso aberto ao conhecimento científico** com **IA aplicada à preservação digital**, promovendo usabilidade e integridade no acesso aos dados.

---

## 🎓 Contexto Acadêmico

Este projeto está sendo desenvolvido como parte de uma **tese de mestrado**, com foco em **preservação digital, acesso aberto ao conhecimento científico e aplicação de IA para recuperação e interpretação de acervos acadêmicos**.  
A pesquisa pretende propor e validar uma abordagem que auxilie pesquisadores, estudantes e instituições no acesso ético, inteligente e sustentável a repositórios acadêmicos brasileiros.

---

## ✨ Funcionalidades

- Interface estilo chat com experiência interativa
- Geração automática de consultas a partir do texto do usuário
- Pesquisa em tempo real no repositório BDTD/IBICT
- Respostas explicativas com apoio de IA
- Histórico conversacional persistente
- Cache inteligente para aumentar performance
- Links diretos para obras originais na BDTD
- Boas práticas de preservação digital e uso ético das fontes

---

## 🛠️ Tecnologias Utilizadas

- **Python**
- **Streamlit**
- **PySolr**
- **OpenAI API**
- **Apache Solr (BDTD/IBICT)**
- HTML/CSS customizado
- Sessão com cache e memória conversacional

---

## 🚀 Como rodar o projeto localmente

```bash
# Clone o repositório
git clone https://github.com/seu-repo/ProjetoIBICT.git
cd ProjetoIBICT

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate no Windows

# Instale as dependências
pip install -r requirements.txt

# Configure sua chave da OpenAI no ambiente
export OPENAI_API_KEY="sua_chave"  # Linux/macOS
setx OPENAI_API_KEY "sua_chave"    # Windows

# Rode a aplicação
streamlit run app.py
