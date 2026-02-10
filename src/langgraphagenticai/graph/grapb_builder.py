from langgraph.graph import StateGraph
from src.langgraphagenticai.state.state import State
from langgraph.graph import START, END
from src.langgraphagenticai.nodes.chatbot_node import BasicChatBotNode
from src.langgraphagenticai.tools.search_tool import get_tools, create_tool_node
from langgraph.prebuilt import tools_condition, ToolNode
from src.langgraphagenticai.nodes.chatbot_tool_node import ChatbotWithWeb
from src.langgraphagenticai.nodes.ai_news_node import AINewsNode

class GraphBuilder:
    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(State)

    def basic_chatbot_graph(self):
        """
        Build a chtbot using Langgraph.
        """
        self.basic_chatbot_node=BasicChatBotNode(self.llm)

        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def chatbot_with_web(self):
        """
        Build a advanced chatbot using Langgraph and Tavily.
        Make tavily api call to fetch the recent news.
        """
        ## Define the tool and tool node
        tools=get_tools()
        tool_node=create_tool_node(tools)

        ## Define llm
        llm=self.llm

        ## Define the chatbot node

        obj_chatbot_node=ChatbotWithWeb(llm)

        chatbot_node=obj_chatbot_node.create_chatbot(tools)

        ## Add nodes
        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)

        ## Define Edges
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def ai_news_builder(self):

        ai_news_node=AINewsNode(self.llm)

        #Define nodes
        self.graph_builder.add_node("fetch_news", ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news", ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result", ai_news_node.save_result)

        #Define edges
        self.graph_builder.add_edge(START, "fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_result")
        self.graph_builder.add_edge("save_result", END)

    def setup_graph(self, usecase: str):
        if usecase == "Basic Chatbot":
            self.basic_chatbot_graph()
        if usecase == "Chatbot with Web":
            self.chatbot_with_web()
        if usecase == "AI News":
            self.ai_news_builder()

        return self.graph_builder.compile()


