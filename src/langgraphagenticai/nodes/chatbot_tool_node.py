from src.langgraphagenticai.state.state import State

class ChatbotWithWeb:
    """
    Basic Chat Bot with tool node
    """

    def __init__(self, model):
        self.llm = model

    # def process(self, state:State)->dict:
    #     """
    #     Process the state and regenerate the respone with tool integration
    #     """
    #     user_input=state["messages"][-1] if state["messages"] else ""
    #     llm_response=self.llm.invoke([{"role": "user", "content": user_input}])
    #
    #     #tool specific logic
    #     tools_response=f"Tool integration for:  '{user_input}'"
    #
    #     return {"messages": [llm_response, tools_response]}


    def create_chatbot(self, tools):
        """"
        Returns a chatbot node functions
        """
        llm_with_tools=self.llm.bind_tools(tools)
        def chatbot_node(state: State):
            return {"messages": [llm_with_tools.invoke(state["messages"])]}
        return chatbot_node