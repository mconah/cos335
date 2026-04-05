import networkx as nx
import matplotlib.pyplot as plt
import time
from typing import List, Dict
from word_ladder import find_ladders  

# ================================================
# WORD LADDER VISUALIZER
# Save this as word_ladder_visualizer.py
# Run it together with your main file that has the 20 functions
# ================================================

def create_word_ladder_graph(begin_word: str, word_set: set, parents: Dict[str, List[str]]) -> nx.DiGraph:
    """Build a directed graph from the parents map (BFS result)."""
    G = nx.DiGraph()
    
    # Add all words that appeared in the search
    for child, prev_list in parents.items():
        for parent in prev_list:
            G.add_edge(parent, child)  # arrow: parent → child
    
    # Add begin_word if not present
    if begin_word not in G:
        G.add_node(begin_word)
    
    return G


def visualize_bfs_exploration(begin_word: str, end_word: str, word_list: List[str]):
    """Run the full algorithm and show animated visualization of BFS + paths."""
    # Import your main functions (assume they are in the same folder or same file)
    # If your 20 functions + find_ladders are in a file called word_ladder.py, do:
    # from word_ladder import find_ladders, create_word_set, ... (or just paste them here)
    
    # For simplicity, we'll re-use the logic but add pauses for visualization
    from collections import deque, defaultdict
    
    word_set = set(word_list)
    if end_word not in word_set:
        print("End word not in dictionary!")
        return
    
    # Build the graph for full view
    G_full = nx.Graph()
    for word in word_set:
        G_full.add_node(word)
    for word in word_set:
        for i in range(len(word)):
            for c in "abcdefghijklmnopqrstuvwxyz":
                if c != word[i]:
                    neighbor = word[:i] + c + word[i+1:]
                    if neighbor in word_set:
                        G_full.add_edge(word, neighbor)
    
    # --- BFS Visualization ---
    print("Starting BFS visualization...")
    parents = defaultdict(list)
    queue = deque([begin_word])
    visited = {begin_word}
    level = 0
    found = False
    
    plt.figure(figsize=(12, 8))
    
    while queue and not found:
        level_size = len(queue)
        new_visited = set()
        
        for _ in range(level_size):
            current = queue.popleft()
            
            # Highlight current word being processed
            pos = nx.spring_layout(G_full, seed=42)
            node_colors = ['lightblue' if n != current else 'orange' for n in G_full.nodes()]
            edge_colors = ['gray'] * len(G_full.edges())
            
            nx.draw(G_full, pos, node_color=node_colors, edge_color=edge_colors,
                    with_labels=True, node_size=800, font_size=10, alpha=0.8)
            plt.title(f"BFS Level {level} - Processing: {current}")
            plt.pause(0.8)  # Real-time pause so you can see it
            
            for i in range(len(current)):
                for ch in "abcdefghijklmnopqrstuvwxyz":
                    if ch != current[i]:
                        neighbor = current[:i] + ch + current[i+1:]
                        if neighbor in word_set and neighbor not in visited:
                            parents[neighbor].append(current)
                            if neighbor not in new_visited:
                                new_visited.add(neighbor)
                                queue.append(neighbor)
                            if neighbor == end_word:
                                found = True
        
        visited.update(new_visited)
        level += 1
        plt.pause(0.5)
    
    plt.close()
    
    if not found:
        print("No path found!")
        return
    
    # --- Final Graph with Parents (Shortest Path DAG) ---
    G = create_word_ladder_graph(begin_word, word_set, parents)
    pos = nx.spring_layout(G, seed=42)
    
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightgreen', 
            node_size=900, font_size=9, arrows=True, arrowstyle='->')
    plt.title("Shortest Path DAG (Parents Map) - Arrows show possible previous words")
    plt.show()
    
    # --- Highlight All Shortest Paths One by One ---
    all_paths = find_ladders(begin_word, end_word, word_list)  # Use your main function
    
    print(f"\nFound {len(all_paths)} shortest path(s). Visualizing them one by one...\n")
    
    for idx, path in enumerate(all_paths):
        print(f"Path {idx+1}: {' → '.join(path)}")
        
        plt.figure(figsize=(12, 8))
        nx.draw(G_full, pos, with_labels=True, node_color='lightgray', 
                edge_color='lightgray', node_size=800, font_size=10)
        
        # Highlight the current path
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_nodes(G_full, pos, nodelist=path, node_color='red', node_size=1200)
        nx.draw_networkx_edges(G_full, pos, edgelist=path_edges, edge_color='red', width=3)
        
        plt.title(f"Shortest Path {idx+1} of {len(all_paths)}: {' → '.join(path)}")
        plt.pause(2.0)   # Show each path for 2 seconds
        plt.show()       # Keep the window open until closed manually


# ================================================
# EXAMPLE USAGE
# ================================================
if __name__ == "__main__":
    begin_word = "hit"
    end_word = "cog"
    word_list = ["hot", "dot", "dog", "lot", "log", "cog"]
    
    visualize_bfs_exploration(begin_word, end_word, word_list)