import streamlit as st
from src.langgraphagenticai.ui.streamlit.loadui import LoadUI
from src.langgraphagenticai.LLMs.groqllm import GroqLLM
from src.langgraphagenticai.graph.grapb_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlit.display import DisplayMessage

def load_ui():
    """
    Loads and runs the Langgraph agentic ui application with Steamlit UI.
    """

    ui = LoadUI()
    user_input=ui.load_ui()

    if not user_input:
        st.error("Please load a user input")
        return

    user_message = st.chat_input("Enter your message:")

    if user_message:
        try:
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model=obj_llm_config.get_llm_model()

            if not model:
                st.error("LLM Model not found")

            usecase=user_input.get("selected_usecase")

            if not usecase:
                st.error("Please enter a valid user case")
                return

            graph_builder=GraphBuilder(model)

            try:
                graph=graph_builder.setup_graph(usecase)
                DisplayMessage(usecase, graph, user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error in graph setup - {e}")
                return
        except Exception as e:
            st.error(f"Error - {e}")
            return