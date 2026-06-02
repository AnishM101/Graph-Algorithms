import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.markdown(
    "<h1 style = 'text-align: center;'>Depth First Search</h1>",
    unsafe_allow_html = True
)

n = st.number_input("Enter a number of vertices", min_value = 1, step = 1)

if "prev_n" not in st.session_state:
    st.session_state.prev_n = n

if "adj_list" not in st.session_state:
    st.session_state.adj_list = {i: set() for i in range(n)}

if "dfs_start" not in st.session_state:
    st.session_state.dfs_start = 0

if "dfs_end" not in st.session_state:
    st.session_state.dfs_end = 0

if "graph" not in st.session_state:
    st.session_state.graph = nx.MultiGraph()

if "dfs_tree" not in st.session_state:
    st.session_state.dfs_tree = nx.Graph()

if "parent" not in st.session_state:
    st.session_state.parent = dict.fromkeys(range(n))

if n != st.session_state.prev_n:
    st.session_state.prev_n = n
    st.session_state.adj_list = {i: set() for i in range(n)}
    st.session_state.dfs_start = 0
    st.session_state.dfs_end = 0
    st.session_state.graph = nx.MultiGraph()
    st.session_state.dfs_tree = nx.Graph()
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

def explore(p):
    for i in st.session_state.adj_list[p]:
        if not visited[i]:
            visited[i] = True
            st.session_state.parent[i] = p
            explore(i)

st.write("Choose a starting and ending vertex:")
s = st.number_input("Starting vertex", min_value = 0, max_value = n - 1, step = 1)
t = st.number_input("Ending vertex", min_value = 0, max_value = n - 1, step = 1)
if st.button("Run Depth First Search"):
    st.session_state.dfs_start = s
    st.session_state.dfs_end = t
    visited = {i: False for i in range(n)}
    visited[s] = True
    explore(s)
    
    if visited[t]:
        st.write(f"There exists a path from {s} to {t}.")
    else:
        st.write(f"There is no path from {s} to {t}.")

    for i in list(st.session_state.parent.keys()):
        if st.session_state.parent[i] is not None:
            st.session_state.dfs_tree.add_edge(st.session_state.parent[i], i)
    
    st.write("")
    st.write("")
    st.markdown(
        "<h4 style = 'text-align: center;'>Depth First Search Tree</h4>",
        unsafe_allow_html = True
    )
    fig_two, ax_two = plt.subplots()
    tree_position = nx.circular_layout(st.session_state.dfs_tree)
    nx.draw(st.session_state.dfs_tree, tree_position, with_labels = True, ax = ax_two)
    st.pyplot(fig_two)