import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from queue import LifoQueue, PriorityQueue

st.markdown(
    "<h1 style = 'text-align: center;'>Bellman-Ford Algorithm</h1>",
    unsafe_allow_html = True
)

n = st.number_input("Enter a number of vertices", min_value = 1, step = 1)

if "prev_n" not in st.session_state:
    st.session_state.prev_n = n

if "adj_list" not in st.session_state:
    st.session_state.adj_list = {i: set() for i in range(n)}

if "predecessor" not in st.session_state:
    st.session_state.predecessor = dict.fromkeys(range(n))

if "path_cost" not in st.session_state:
    st.session_state.path_cost = {i: float('inf') for i in range(n)}

if "graph" not in st.session_state:
    st.session_state.graph = nx.MultiGraph()

if "shortest_path_tree" not in st.session_state:
    st.session_state.shortest_path_tree = nx.Graph()

if n != st.session_state.prev_n:
    st.session_state.prev_n = n
    st.session_state.adj_list = {i: set() for i in range(n)}
    st.session_state.predecessor = dict.fromkeys(range(n))
    st.session_state.path_cost = {i: float('inf') for i in range(n)}
    st.session_state.graph = nx.MultiGraph()
    st.session_state.shortest_path_tree = nx.Graph()

st.write("")
st.write("Add edges:")
u = st.number_input("First endpoint", min_value = 0, max_value = n - 1, step = 1)
v = st.number_input("Second endpoint", min_value = 0, max_value = n - 1, step = 1)
w = st.number_input("Edge weight")

if st.button("Add edge"):
    st.session_state.graph.add_edge(u, v, weight = w)
    st.session_state.adj_list[u].add((v, w))
    st.session_state.adj_list[v].add((u, w))

fig, ax = plt.subplots()
graph_position = nx.circular_layout(st.session_state.graph)
edge_weights = nx.get_edge_attributes(st.session_state.graph, "weight")
nx.draw(st.session_state.graph, graph_position, with_labels = True, ax = ax)
nx.draw_networkx_edge_labels(st.session_state.graph, graph_position, edge_labels = edge_weights, ax = ax)
st.pyplot(fig)

st.write("Choose a starting and ending vertex:")
s = st.number_input("Starting vertex", min_value = 0, max_value = n - 1, step = 1)
t = st.number_input("Ending vertex", min_value = 0, max_value = n - 1, step = 1)
if st.button("Run Bellman-Ford Algorithm"):
    st.session_state.predecessor[s] = None
    st.session_state.path_cost[s] = 0
    for i in range(1, n):
        next_array = {v: 0 for v in range(n)}
        for j in range(n):
            pq = PriorityQueue()
            pq.put((st.session_state.path_cost[j], (-1, -1)))
            for v, w in st.session_state.adj_list[j]:
                pq.put((st.session_state.path_cost[v] + w, (v, w)))
            
            pair = pq.get()
            next_array[j] = pair[0]
            if pair[1] != (-1, -1):
                st.session_state.predecessor[j] = pair[1][0]
        
        st.session_state.path_cost = next_array

    for i in range(n):
        pq = PriorityQueue()
        pq.put((st.session_state.path_cost[j], (-1, -1)))
        for v, w in st.session_state.adj_list[j]:
            pq.put((st.session_state.path_cost[v] + w, (v, w)))
            
        pair = pq.get()
        if pair[0] != st.session_state.path_cost[i]:
            st.session_state.path_cost[i] = float('-inf')


    for i in range(n):
        if i != s:
            w = sorted(edge["weight"] for edge in st.session_state.graph.get_edge_data(i, st.session_state.predecessor[i]).values())[0]
            st.session_state.shortest_path_tree.add_edge(i, st.session_state.predecessor[i], weight = w)

    if st.session_state.path_cost[t] != float('-inf'):
        st.write(f"The shortest path from {s} to {t} is of length {st.session_state.path_cost[t]}.")
        stack = LifoQueue()
        stack.put(t)
        v = st.session_state.predecessor[t]
        while v is not None:
            stack.put(v)
            v = st.session_state.predecessor[v]
    
        path = f"The path is {stack.get()}"
        while not stack.empty():
            path += f" -> {stack.get()}"

        path += f"."
        st.write(path)

    else:
        st.write(f"There is no shortest path from {s} to {t}.")
    
    st.write("")
    st.write("")
    st.markdown(
        "<h4 style = 'text-align: center;'>Shortest Path Tree</h4>",
        unsafe_allow_html = True
    )
    fig_two, ax_two = plt.subplots()
    shortest_path_tree_position = nx.circular_layout(st.session_state.shortest_path_tree)
    shortest_path_tree_edge_weights = nx.get_edge_attributes(st.session_state.shortest_path_tree, "weight")
    nx.draw(st.session_state.shortest_path_tree, shortest_path_tree_position, with_labels = True, ax = ax_two)
    nx.draw_networkx_edge_labels(st.session_state.shortest_path_tree, shortest_path_tree_position, edge_labels = shortest_path_tree_edge_weights, ax = ax_two)
    st.pyplot(fig_two)