from http.client import responses

from langchain_classic.chains.summarize.map_reduce_prompt import prompt_template

from src.langgraphagenticai.state.state import State
from tavily import TavilyClient
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate

class AINewsNode:
    def __init__(self, llm):
        self.llm = llm
        self.tavily = TavilyClient()
        self.state = {}

    def fetch_news(self, state:dict) -> dict:
        """
        Fetch AI news based on frequency
        """
        frequency=st.session_state['selected_timeframe'].lower()
        self.state['frequency'] = frequency
        time_range_map={'daily': 'd', 'weekly': 'w', 'monthly': 'm'}
        days_map={'daily':1, 'weekly':7, 'monthly':30}

        response = self.tavily.search(
            query="Top AI News in india",
            topic="news",
            include_answer="advanced",
            time_range=time_range_map[frequency],
            max_results=10,
            days=days_map[frequency]
        )

        state['news']=response.get('results', [])
        self.state['news'] = state['news']
        return self.state

    def summarize_news(self, state:dict) -> dict:
        news_items=self.state['news']
        prompt_template=ChatPromptTemplate.from_messages([
            ("system", """You are a professional news analyst.

            Summarize the following news article using clear, neutral language.
            
            Requirements:
            - Tone: factual, unbiased, easy to scan
            - Focus on: key facts, impact, and why it matters
            - Avoid: speculation, emojis, clickbait language
            
            Output format:
            Title: <concise rewritten headline>
            
            Summary:
            - Bullet point 1
            - Bullet point 2
            - Bullet point 3
            """),
            ("user","Articles:\n{articals}")
        ])

        articals_str = "\n\n".join([
            f"Content: {item.get('content', '')}\n\nDate: {item.get('published_date', '')}"
            for item in news_items
        ])
        response = self.llm.invoke(prompt_template.format(articals=articals_str))

        state['summary']=response.content
        self.state['summary'] = state['summary']
        return self.state

    def save_result(self, state):
        frequency=self.state['frequency']
        summary=self.state['summary']
        filename=f"./AINews/{frequency}.md"
        with open(filename, "w") as f:
            f.write(summary)
        self.state['filename'] = filename
        return self.state

        

