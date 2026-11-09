import pandas as pd
import streamlit as st

# Configuração inicial da página
st.set_page_config(
    page_title="Dashboard Sustenta",
    page_icon="🌱",
    layout="wide",
)

# ==========================================
# CREDENCIAIS DE ACESSO (Defina aqui!)
# ==========================================
USUARIO_CORRETO = "isabella.felipe@ufu.br"
SENHA_CORRETA = "Sustenta2026!"

# Gerenciamento de sessão de login
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# ==========================================
# TELA DE LOGIN
# ==========================================
if not st.session_state.autenticado:
    st.title("🔒 Acesso Restrito - Empresa Júnior Sustenta")
    st.markdown("Por favor, faça login para acessar o painel de demandas.")

    with st.form("form_login"):
        email_digitado = st.text_input("E-mail de acesso")
        senha_digitada = st.text_input("Senha", type="password")
        botao_entrar = st.form_submit_button("Entrar no Sistema")

        if botao_entrar:
            if (
                email_digitado == USUARIO_CORRETO
                and senha_digitada == SENHA_CORRETA
            ):
                st.session_state.autenticado = True
                st.success("Login realizado com sucesso!")
                st.rerun()
                st.rerun()
            else:
                st.error("E-mail ou senha incorretos. Tente novamente.")

    # Interrompe a execução aqui para não carregar o dashboard sem login
    st.stop()

# ==========================================
# CONTEÚDO DO DASHBOARD (Após Login)
# ==========================================

# Botão de Logout na barra lateral
with st.sidebar:
    st.write(f"Usuário: **{USUARIO_CORRETO}**")
    if st.button("Sair / Logout"):
        st.session_state.autenticado = False
        st.rerun()

# Título principal
st.title("🌱 Sustenta - Painel de Gestão e Demandas")
st.markdown(
    "Centralize o controle de entregas, pendências e novas parcerias da equipe."
)

# Inicialização dos dados simulados
if "demandas" not in st.session_state:
    st.session_state.demandas = pd.DataFrame(
        {
            "ID": [1, 2, 3],
            "Título": [
                "Relatório de Sustentabilidade - Cliente A",
                "Diagnóstico Energético",
                "Reunião com Parceiro X",
            ],
            "Tipo": ["Demanda", "Demanda", "Parceria"],
            "Status": ["Concluído", "Pendente", "Ideia"],
            "Responsável": ["Ana", "Carlos", "Beatriz"],
            "Prazo": ["2026-10-10", "2026-11-15", "2026-11-30"],
        }
    )

df = st.session_state.demandas

# Métricas no topo
col1, col2, col3 = st.columns(3)
col1.metric("Concluídas", len(df[df["Status"] == "Concluído"]))
col2.metric("Pendentes", len(df[df["Status"] == "Pendente"]))
col3.metric("Ideias / Parcerias", len(df[df["Status"] == "Ideia"]))

st.divider()

# Abas de navegação
aba1, aba2, aba3 = st.tabs(
    ["📋 Pendentes & Andamento", "✅ Concluídas", "💡 Ideias & Parcerias"]
)

with aba1:
    st.subheader("Demandas Pendentes")
    pendentes = df[df["Status"] == "Pendente"]
    st.dataframe(pendentes, use_container_width=True)

    with st.expander("➕ Adicionar Nova Demanda Pendente"):
        with st.form("form_pendente"):
            novo_titulo = st.text_input("Título da Demanda")
            novo_resp = st.text_input("Responsável")
            novo_prazo = st.date_input("Prazo de Entrega")
            submit = st.form_submit_button("Cadastrar")

            if submit and novo_titulo:
                novo_id = len(df) + 1
                nova_linha = pd.DataFrame(
                    {
                        "ID": [novo_id],
                        "Título": [novo_titulo],
                        "Tipo": ["Demanda"],
                        "Status": ["Pendente"],
                        "Responsável": [novo_resp],
                        "Prazo": [str(novo_prazo)],
                    }
                )
                st.session_state.demandas = pd.concat(
                    [df, nova_linha], ignore_index=True
                )
                st.success("Demanda adicionada com sucesso!")
                st.rerun()

with aba2:
    st.subheader("Histórico de Demandas Concluídas")
    concluidas = df[df["Status"] == "Concluído"]
    st.dataframe(concluidas, use_container_width=True)

with aba3:
    st.subheader("Banco de Ideias e Parcerias")
    ideias = df[df["Status"] == "Ideia"]
    st.dataframe(ideias, use_container_width=True)

    with st.expander("💡 Cadastrar Nova Ideia ou Parceria"):
        with st.form("form_ideia"):
            ideia_titulo = st.text_input("Descrição da Ideia / Parceria")
            ideia_resp = st.text_input("Quem propôs?")
            submit_ideia = st.form_submit_button("Salvar Ideia")

            if submit_ideia and ideia_titulo:
                novo_id = len(df) + 1
                nova_linha = pd.DataFrame(
                    {
                        "ID": [novo_id],
                        "Título": [ideia_titulo],
                        "Tipo": ["Parceria"],
                        "Status": ["Ideia"],
                        "Responsável": [ideia_resp],
                        "Prazo": ["A definir"],
                    }
                )
                st.session_state.demandas = pd.concat(
                    [df, nova_linha], ignore_index=True
                )
                st.success("Ideia registrada!")
                st.rerun()