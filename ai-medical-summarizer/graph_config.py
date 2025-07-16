from typing import TypedDict, List
from langgraph.graph import StateGraph, END

from agents.retriever import retriever_node
from agents.classifier import classifier_node
from agents.summarizer import summarizer_node
from agents.citation import citation_node
from agents.assembler import assembler_node

class GraphState(TypedDict):
    query: str
    docs: List[dict]
    final_output: str

graph = StateGraph(GraphState)

graph.add_node("retriever", retriever_node)
graph.add_node("classifier", classifier_node)
graph.add_node("summarizer", summarizer_node)
graph.add_node("citation", citation_node)
graph.add_node("assembler", assembler_node)

graph.set_entry_point("retriever")
graph.add_edge("retriever", "classifier")
graph.add_edge("classifier", "summarizer")
graph.add_edge("summarizer", "citation")
graph.add_edge("citation", "assembler")
graph.add_edge("assembler", END)

compiled = graph.compile()
