import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from queue import PriorityQueue

st.markdown(
    "<h1 style = 'text-align: center;'>Kruskal's Algorithm</h1>",
    unsafe_allow_html = True
)

n = st.number_input("Enter a number of vertices", min_value = 1, step = 1)

if "prev_n" not in st.session_state:
    st.session_state.prev_n = n

if "adj_list" not in st.session_state:
    st.session_state.adj_list = {i: set() for i in range(n)}

if "edges" not in st.session_state:
    st.session_state.edges = PriorityQueue()

if "graph" not in st.session_state:
    st.session_state.graph = nx.MultiGraph()

if "mcst" not in st.session_state:
    st.session_state.mcst = nx.Graph()

if n != st.session_state.prev_n:
    st.session_state.prev_n = n
    st.session_state.adj_list = {i: set() for i in range(n)}
    st.session_state.edges = PriorityQueue()
    st.session_state.graph = nx.MultiGraph()
    st.session_state.mcst = nx.Graph()

st.write("")
st.write("Add edges:")
u = st.number_input("First endpoint", min_value = 0, max_value = n - 1, step = 1)
v = st.number_input("Second endpoint", min_value = 0, max_value = n - 1, step = 1)
w = st.number_input("Edge weight")

if st.button("Add edge"):
    st.session_state.adj_list[u].add(v)
    st.session_state.adj_list[v].add(u)
    st.session_state.edges.put((w, (u, v)))
    st.session_state.graph.add_edge(u, v, weight = w)

fig, ax = plt.subplots()
graph_position = nx.spring_layout(st.session_state.graph)
edge_weights = nx.get_edge_attributes(st.session_state.graph, "weight")
nx.draw(st.session_state.graph, graph_position, with_labels = True, ax = ax)
nx.draw_networkx_edge_labels(st.session_state.graph, graph_position, edge_labels = edge_weights, ax = ax)
st.pyplot(fig)

if st.button("Run Kruskal's Algorithm"):
    connected = {i: {j: False for j in range(n)} for i in range(n)}
    for i in range(n):
        connected[i][i] = True

    while not st.session_state.edges.empty():
        edge = st.session_state.edges.get()
        w = edge[0]
        u = edge[1][0]
        v = edge[1][1]
        if not connected[u][v]:
            st.session_state.mcst.add_edge(u, v, weight = w)
            connected[u][v] = True
            connected[v][u] = True
            for i in range(n):
                if connected[u][i] == True:
                    connected[v][i] = True
                    connected[i][v] = True

                if connected[v][i] == True:
                    connected[u][i] = True
                    connected[i][u] = True

    st.write("")
    st.write("")
    st.markdown(
        "<h4 style = 'text-align: center;'>Min-Cost Spanning Tree</h4>",
        unsafe_allow_html = True
    )
    fig_two, ax_two = plt.subplots()
    mcst_position = nx.spring_layout(st.session_state.mcst)
    mcst_edge_weights = nx.get_edge_attributes(st.session_state.mcst, "weight")
    nx.draw(st.session_state.mcst, mcst_position, with_labels = True, ax = ax_two)
    nx.draw_networkx_edge_labels(st.session_state.mcst, mcst_position, edge_labels = mcst_edge_weights, ax = ax_two)
    st.pyplot(fig_two)