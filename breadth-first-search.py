import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue

st.markdown(
    "<h1 style = 'text-align: center;'>Breadth First Search</h1>",
    unsafe_allow_html = True
)

n = st.number_input("Enter a number of vertices", min_value = 1, step = 1)

if "prev_n" not in st.session_state:
    st.session_state.prev_n = n

if "adj_list" not in st.session_state:
    st.session_state.adj_list = {i: set() for i in range(n)}

if "bfs_start" not in st.session_state:
    st.session_state.bfs_start = 0

if "bfs_end" not in st.session_state:
    st.session_state.bfs_end = 0

if "graph" not in st.session_state:
    st.session_state.graph = nx.MultiGraph()

if "bfs_tree" not in st.session_state:
    st.session_state.bfs_tree = nx.Graph()

if "parent" not in st.session_state:
    st.session_state.parent = dict.fromkeys(range(n))

if n != st.session_state.prev_n:
    st.session_state.prev_n = n
    st.session_state.adj_list = {i: set() for i in range(n)}
    st.session_state.bfs_start = 0
    st.session_state.bfs_end = 0
    st.session_state.graph = nx.MultiGraph()
    st.session_state.bfs_tree = nx.Graph()
    st.session_state.parent = dict.fromkeys(range(n))

st.write("")
st.write("Add edges:")
u = st.number_input("First endpoint", min_value = 0, max_value = n - 1, step = 1)
v = st.number_input("Second endpoint", min_value = 0, max_value = n - 1, step = 1)

if st.button("Add edge"):
    st.session_state.graph.add_edge(u, v)
    st.session_state.adj_list[u].add(v)
    st.session_state.adj_list[v].add(u)

fig, ax = plt.subplots()
graph_position = nx.circular_layout(st.session_state.graph)
nx.draw(st.session_state.graph, graph_position, with_labels = True, ax = ax)
st.pyplot(fig)

st.write("Choose a starting and ending vertex:")
s = st.number_input("Starting vertex", min_value = 0, max_value = n - 1, step = 1)
t = st.number_input("Ending vertex", min_value = 0, max_value = n - 1, step = 1)
if st.button("Run Breadth First Search"):
    st.session_state.bfs_start = s
    st.session_state.bfs_end = t
    visited = {i: False for i in range(n)}
    q = Queue()
    q.put(s)
    visited[s] = True
    while not q.empty():
        if visited[t]:
            break

        k = q.get()
        for m in st.session_state.adj_list[k]:
            if not visited[m]:
                visited[m] = True
                st.session_state.parent[m] = k
                if m == t:
                    break
                q.put(m)
    
    if visited[t]:
        st.write(f"There exists a path from {s} to {t}.")
    else:
        st.write(f"There is no path from {s} to {t}.")

    for i in list(st.session_state.parent.keys()):
        if st.session_state.parent[i] is not None:
            st.session_state.bfs_tree.add_edge(st.session_state.parent[i], i)
    
    st.write("")
    st.write("")
    st.markdown(
        "<h4 style = 'text-align: center;'>Breadth First Search Tree</h4>",
        unsafe_allow_html = True
    )
    fig_two, ax_two = plt.subplots()
    tree_position = nx.circular_layout(st.session_state.bfs_tree)
    nx.draw(st.session_state.bfs_tree, tree_position, with_labels = True, ax = ax_two)
    st.pyplot(fig_two)