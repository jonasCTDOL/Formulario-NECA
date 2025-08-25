import streamlit as st

# Centraliza todas as perguntas em um dicionário para fácil manutenção
QUESTIONS = {
    "reason": "Qual o motivo principal da sua busca por análise psicológica?",
    "anxiety_symptoms": "Descreva seus sintomas de ansiedade e quando eles costumam ocorrer.",
    "feelings": "Há mais alguma coisa que você gostaria de compartilhar sobre seus sentimentos atuais?",
    "anxiety_triggers": "Quais situações ou pensamentos costumam desencadear sua ansiedade?",
    "mood_scale": "Como você avalia seu humor geral na última semana em uma escala de 1 a 10?",
}

def get_next_question_key(current_state, answers):
    """
    Determina a CHAVE da próxima pergunta com base no estado atual e nas respostas.
    A lógica do fluxo da entrevista fica concentrada aqui.
    """
    if current_state == "start":
        return "reason"
    elif current_state == "reason":
        if "ansiedade" in answers.get("reason", "").lower():
            return "anxiety_symptoms"
        else:
            return "feelings"
    elif current_state == "anxiety_symptoms":
        return "anxiety_triggers"
    elif current_state == "anxiety_triggers":
        return "mood_scale"
    elif current_state == "feelings":
         return "mood_scale"
    else:
        return None # Indica o fim da entrevista

def app():
    st.title("Entrevista Psicológica Interativa")

    # Inicializa o estado da sessão
    if 'current_state' not in st.session_state:
        st.session_state.current_state = "start"
        st.session_state.answers = {}

    # Obtém a próxima pergunta com base no estado atual
    next_question_key = get_next_question_key(
        st.session_state.current_state,
        st.session_state.answers
    )

    # Se houver uma próxima pergunta, exibe-a
    if next_question_key:
        question_text = QUESTIONS[next_question_key]
        st.write(question_text)

        # Usa um widget diferente para a escala Likert (escala de humor)
        if next_question_key == "mood_scale":
            answer = st.slider(
                "Selecione um valor de 1 (muito baixo) a 10 (muito alto)",
                min_value=1,
                max_value=10,
                value=5, # Valor inicial
                key=f"answer_{next_question_key}"
            )
        else:
            answer = st.text_area("Sua resposta:", key=f"answer_{next_question_key}", label_visibility="collapsed")

        # Botão para submeter a resposta e avançar
        if st.button("Próxima Pergunta"):
            if answer:
                # Salva a resposta e atualiza o estado para o da pergunta que acabamos de responder
                st.session_state.answers[next_question_key] = answer
                st.session_state.current_state = next_question_key
                # Reroda o script para mostrar a próxima pergunta ou a tela final
                st.rerun()
            else:
                st.warning("Por favor, insira sua resposta antes de continuar.")
    else:
        # Tela de conclusão: exibe o resultado da entrevista
        st.success("Entrevista concluída. Obrigado por suas respostas.")
        st.header("Resumo da Análise")

        for key, answer in st.session_state.answers.items():
            # Busca o texto da pergunta no dicionário
            question_text = QUESTIONS.get(key, key.replace('_', ' ').capitalize())
            st.subheader(question_text)
            # Formata a resposta para melhor visualização
            st.markdown(f"> _{answer}_")
            st.write("---")

if __name__ == "__main__":
    app()
