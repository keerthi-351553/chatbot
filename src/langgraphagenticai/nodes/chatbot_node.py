from src.langgraphagenticai.state.state import State

class BasicChatBotNode:
    """
    Basic Chat Bot Node
    """
    def __init__(self,model):
        self.llm=model

    def process(self, state:State)->dict:
        """
        Process the state and return the result
        """
        return {"messages":self.llm.invoke(state['messages'])}