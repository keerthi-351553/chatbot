import streamlit as st
import os

from src.langgraphagenticai.ui.uiconfig import Config

class LoadUI:
    def __init__(self):
        self.config = Config()
        self.user_controls={}

    def load_ui(self):
        st.set_page_config(page_title=self.config.get_page_title(), layout="wide")
        st.header(self.config.get_page_title())

        with st.sidebar:
            #get options
            llm_options=self.config.get_llm_options()
            usecase_options=self.config.get_usecase_options()

            #LLM selections
            self.user_controls["selected_llm"]=st.selectbox("Select LLM",llm_options)

            if self.user_controls["selected_llm"]== 'Groq':
                #Model selection
                model_options=self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"]=st.selectbox("Select Groq Model",model_options)
                self.user_controls["GROQ_API_KEY"]=st.session_state["GROQ_API_KEY"]=st.text_input("GROQ API KEY",type="password")

                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("Please enter a valid Groq API KEY")

            # use case selection
            self.user_controls["selected_usecase"] = st.selectbox("Select Usecase", usecase_options)

            if self.user_controls["selected_usecase"] == 'Chatbot with Web':
                os.environ["TAVILY_API_KEY"]=self.user_controls["TAVILY_API_KEY "]=st.session_state["TAVILY_API_KEY "]=st.text_input("Tavily API KEY",type="password")

                if not self.user_controls["TAVILY_API_KEY "]:
                    st.warning("Please enter a valid Tavily API KEY")

        return self.user_controls