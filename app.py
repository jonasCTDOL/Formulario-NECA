
import streamlit as st

def get_next_question(current_state, answers):
    """
    Determina a próxima pergunta com base no estado atual e nas respostas.
    Esta é uma lógica simplificada para demonstração.
    Em uma aplicação real, isso seria mais complexo.
    """
    if current_state == "start":
        return "Qual o motivo principal da sua busca por análise psicológica?", "reason"
    elif current_state == "reason":
        # Exemplo de lógica simples: se o motivo for "ansiedade", faça perguntas sobre ansiedade.
        # Caso contrário, faça uma pergunta geral.
        if "ansiedade" in answers.get("reason", "").lower():
            return "Descreva seus sintomas de ansiedade e quando eles costumam ocorrer.", "anxiety_symptoms"
        else:
            return "Há mais alguma coisa que você gostaria de compartilhar sobre seus sentimentos atuais?", "feelings"
    elif current_state == "anxiety_symptoms":
        return "Quais situações ou pensamentos costumam desencadear sua ansiedade?", "anxiety_triggers"
    elif current_state == "anxiety_triggers":
        return "Como você avalia seu humor geral na última semana em uma escala de 1 a 10?", "mood_scale"
    elif current_state == "feelings":
         return "Como você avalia seu humor geral na última semana em uma escala de 1 a 10?", "mood_scale"
    # Adicione mais estados e lógica condicional aqui
    else:
        return None, "end" # Indica que não há mais perguntas


def app():
    st.title("Formulário de Análise Psicológica")

    # Inicializa o estado da sessão
    if 'current_state' not in st.session_state:
        st.session_state.current_state = "start"
        st.session_state.answers = {}

    # Obtém a próxima pergunta com base no estado atual
    question_text, question_key = get_next_question(
        st.session_state.current_state,
        st.session_state.answers
    )

    # Se houver uma próxima pergunta, exibe-a
    if question_text:
        st.write(question_text)

        # Campo de entrada para a resposta. A chave do widget é única para cada pergunta.
        answer = st.text_area("Sua resposta:", key=f"answer_{question_key}")

        # Botão para submeter a resposta e avançar
        if st.button("Próxima Pergunta"):
            if answer:
                # Salva a resposta e atualiza o estado para o da pergunta que acabamos de responder
                st.session_state.answers[question_key] = answer
                st.session_state.current_state = question_key
                # Reroda o script para mostrar a próxima pergunta ou a tela final
                st.rerun()
            else:
                st.warning("Por favor, insira sua resposta antes de continuar.")
    else:
        st.success("Análise concluída. Obrigado por suas respostas.")
        st.write("Respostas Coletadas:")
        st.json(st.session_state.answers) # Exibe as respostas coletadas

if __name__ == "__main__":
    app()
