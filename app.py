import streamlit as st


def verificar_prioridade(mensagem: str) -> dict:
    """Analisa uma mensagem de atendimento e identifica se possui palavras
    negativas."""
    palavras_negativas = [
        "ruim",
        "péssimo",
        "pessimo",
        "erro",
        "falha",
        "horrível",
        "horrivel",
    ]

    # Padroniza a mensagem para minúsculas
    mensagem_minuscula = mensagem.lower()

    # Encontra as palavras negativas na mensagem
    encontradas = [
        palavra
        for palavra in palavras_negativas
        if palavra in mensagem_minuscula
    ]

    if encontradas:
        return {
            "prioridade": "ALTA",
            "status": "⚠️ ATENÇÃO: Mensagem crítica detectada!",
            "palavras_encontradas": encontradas,
        }
    else:
        return {
            "prioridade": "NORMAL",
            "status": "✅ Atendimento em fila padrão.",
            "palavras_encontradas": [],
        }


# --- INTERFACE STREAMLIT ---
def main():
    # Configuração da página
    st.set_page_config(
        page_title="Triagem de Suporte", page_icon="🎧", layout="centered"
    )

    st.title("🎧 Sistema de Priorização de Suporte")
    st.write(
        "Insira a mensagem do cliente abaixo para verificar o nível de prioridade do atendimento."
    )

    # Campo de texto para entrada da mensagem
    mensagem_input = st.text_area(
        "Mensagem do Cliente:",
        placeholder="Ex: O serviço prestado foi muito ruim e apresentou um erro na cobrança.",
    )

    # Botão para disparar a análise
    if st.button("Analisar Prioridade", type="primary"):
        if mensagem_input.strip() == "":
            st.warning("Por favor, digite uma mensagem antes de analisar.")
        else:
            resultado = verificar_prioridade(mensagem_input)

            st.divider()
            st.subheader("Resultado da Análise")

            # Exibição visual com base na prioridade
            if resultado["prioridade"] == "ALTA":
                st.error(f"**Status:** {resultado['status']}")
                st.metric(label="Prioridade", value=resultado["prioridade"])
                st.write(
                    f"**Gatilhos identificados:** {', '.join(resultado['palavras_encontradas'])}"
                )
            else:
                st.success(f"**Status:** {resultado['status']}")
                st.metric(label="Prioridade", value=resultado["prioridade"])


if __name__ == "__main__":
    main()