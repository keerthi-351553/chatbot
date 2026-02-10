import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

class DisplayMessage:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message
        if usecase == "Basic Chatbot":
            for event in graph.stream({'messages': ("user", user_message)}):
                for value in event.values():
                    with st.chat_message("user"):
                        st.write(user_message)
                    with st.chat_message("assistant"):
                        st.write(value["messages"].content)

        elif usecase == "Chatbot with Web":
            initial_state = {"messages": [("user", user_message)]}
            res=graph.invoke(initial_state)
            for message in res["messages"]:
                if type(message) is HumanMessage:
                    with st.chat_message("user"):
                        st.write(message.content)
                elif type(message) is ToolMessage:
                    with st.chat_message("ai"):
                        st.write("Tool Message start")
                        st.write(message.content)
                        st.write("Tool Message end")
                elif type(message) is AIMessage:
                    with st.chat_message("assistant"):
                        st.write("AI Message start")
                        st.write(message.content)
                        st.write("AI Message end")