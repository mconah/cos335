"""
Word Ladder Real-Time Visualizer with 10 Test Cases
=====================================================

This module provides real-time visualization of the Word Ladder problem using:
1. Matplotlib interactive mode for step-by-step BFS visualization
2. NetworkX for graph representation
3. Multiple test cases including successful and failing scenarios

REAL-TIME VISUALIZATION IMPLEMENTATION GUIDE:
=============================================

Option 1: Matplotlib Interactive Mode (plt.ion())
-------------------------------------------------
- Uses plt.ion() to enable interactive mode
- plt.pause(0.5) creates animation-like updates
- Updates the same figure window in real-time
- Best for: Simple animations, terminal-based visualization

Option 2: FuncAnimation from matplotlib.animation
-------------------------------------------------
- More control over frame timing
- Can save as GIF or video
- Better for complex animations

Option 3: Tkinter GUI Integration
---------------------------------
- Embed matplotlib in Tkinter canvas
- Use after() method for timed updates
- Best for: Full GUI applications with controls

Option 4: PyQt5/PySide2 with matplotlib
---------------------------------------
- Professional GUI with full control
- Can add buttons, sliders, speed control
- Best for: Production applications

Option 5: Browser-based with Plotly/Dash
----------------------------------------
- Web-based real-time visualization
- Interactive graphs with hover info
- Best for: Remote access, sharing

Current Implementation: Option 1 (Matplotlib Interactive Mode)
"""

import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import List, Dict, Set, Tuple
from collections import deque, defaultdict
import time
import sys

# Import word ladder functions
from word_ladder import find_ladders


class WordLadderRealTimeVisualizer:
    """Real-time visualizer for Word Ladder problem using matplotlib interactive mode."""
    
    def __init__(self, begin_word: str, end_word: str, word_list: List[str]):
        self.begin_word = begin_word
        self.end_word = end_word
        self.word_list = word_list
        self.word_set = set(word_list)
        self.parents = defaultdict(list)
        self.visited = set()
        self.current_level = 0
        self.found_path = False
        self.all_paths = []
        
        # Create the full graph of all possible connections
        self.G_full = self._create_full_graph()
        
        # Setup figure and axis
        self.fig, self.ax = plt.subplots(figsize=(14, 10))
        self.pos = nx.spring_layout(self.G_full, seed=42, k=0.5)
        
    def _create_full_graph(self) -> nx.Graph:
        """Create a graph with all possible word connections."""
        G = nx.Graph()
        for word in self.word_set:
            G.add_node(word)
        
        # Add edges between words that differ by one letter
        for word in self.word_set:
            for i in range(len(word)):
                for c in "abcdefghijklmnopqrstuvwxyz":
                    if c != word[i]:
                        neighbor = word[:i] + c + word[i+1:]
                        if neighbor in self.word_set:
                            G.add_edge(word, neighbor)
        
        # Add begin_word if not in word_set
        if self.begin_word not in G:
            G.add_node(self.begin_word)
            
        return G
    
    def _get_node_colors(self, current_word: str = None, visited_words: Set[str] = None,
                         path_words: List[str] = None) -> List[str]:
        """Get colors for nodes based on their state."""
        colors = []
        for node in self.G_full.nodes():
            if path_words and node in path_words:
                colors.append('#FF6B6B')  # Red for path
            elif node == current_word:
                colors.append('#FFE66D')  # Yellow for current
            elif visited_words and node in visited_words:
                colors.append('#4ECDC4')  # Teal for visited
            elif node == self.begin_word:
                colors.append('#95E1D3')  # Light green for start
            elif node == self.end_word:
                colors.append('#F38181')  # Pink for target
            else:
                colors.append('#E0E0E0')  # Gray for unvisited
        return colors
    
    def _draw_graph(self, title: str, current_word: str = None, 
                    visited_words: Set[str] = None, path_words: List[str] = None):
        """Draw the current state of the graph."""
        self.ax.clear()
        
        node_colors = self._get_node_colors(current_word, visited_words, path_words)
        
        # Draw nodes
        nx.draw_networkx_nodes(self.G_full, self.pos, 
                              node_color=node_colors,
                              node_size=700, 
                              alpha=0.8, 
                              ax=self.ax)
        
        # Draw edges
        nx.draw_networkx_edges(self.G_full, self.pos, 
                              edge_color='#CCCCCC', 
                              width=1, 
                              alpha=0.6, 
                              ax=self.ax)
        
        # Draw labels
        nx.draw_networkx_labels(self.G_full, self.pos, 
                               font_size=9, 
                               font_weight='bold',
                               ax=self.ax)
        
        # Set title
        self.ax.set_title(title, fontsize=14, fontweight='bold')
        self.ax.axis('off')
        
        # Add info text
        info_text = f"Start: {self.begin_word} | Target: {self.end_word}\n"
        info_text += f"Visited: {len(visited_words) if visited_words else 0} | "
        info_text += f"Level: {self.current_level}"
        if path_words:
            info_text += f" | Path Length: {len(path_words)}"
        
        self.fig.text(0.5, 0.02, info_text, ha='center', fontsize=10,
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
    
    def visualize_bfs_realtime(self, delay: float = 0.3):
        """
        Run BFS with real-time visualization.
        
        Args:
            delay: Time in seconds between each step (default: 0.3s)
        
        Returns:
            bool: True if path found, False otherwise
        """
        print(f"\n{'='*60}")
        print(f"Starting Real-Time BFS Visualization")
        print(f"From '{self.begin_word}' to '{self.end_word}'")
        print(f"{'='*60}\n")
        
        # Enable interactive mode
        plt.ion()
        plt.show()
        
        queue = deque([self.begin_word])
        self.visited = {self.begin_word}
        self.current_level = 0
        self.found_path = False
        
        initial_visited = set()
        
        while queue and not self.found_path:
            level_size = len(queue)
            new_visited = set()
            
            for _ in range(level_size):
                current = queue.popleft()
                
                # Update visualization
                title = f"BFS Exploration - Level {self.current_level} | Processing: {current}"
                self._draw_graph(title, current, self.visited.union(new_visited))
                
                plt.pause(delay)  # This creates the real-time effect
                plt.gcf().canvas.draw()
                plt.gcf().canvas.flush_events()
                
                # Generate neighbors
                for i in range(len(current)):
                    for ch in "abcdefghijklmnopqrstuvwxyz":
                        if ch != current[i]:
                            neighbor = current[:i] + ch + current[i+1:]
                            if neighbor in self.word_set and neighbor not in self.visited:
                                self.parents[neighbor].append(current)
                                if neighbor not in new_visited:
                                    new_visited.add(neighbor)
                                    queue.append(neighbor)
                                
                                if neighbor == self.end_word:
                                    self.found_path = True
            
            self.visited.update(new_visited)
            self.current_level += 1
        
        plt.ioff()
        
        if self.found_path:
            print(f"\n✓ Path found in {self.current_level} levels!")
            self._show_final_results()
            return True
        else:
            print(f"\n✗ No path found from '{self.begin_word}' to '{self.end_word}'")
            self._show_no_path_result()
            return False
    
    def _show_final_results(self):
        """Display final results with all shortest paths."""
        print("\nFinding all shortest paths...")
        self.all_paths = find_ladders(self.begin_word, self.end_word, self.word_list)
        
        print(f"\nFound {len(self.all_paths)} shortest path(s):")
        for i, path in enumerate(self.all_paths, 1):
            print(f"  Path {i}: {' → '.join(path)}")
        
        # Visualize each path
        plt.ion()
        fig2, axes = plt.subplots(2, 2, figsize=(14, 12))
        axes = axes.flatten()
        
        # Show DAG of parent relationships
        ax = axes[0]
        G_dag = nx.DiGraph()
        for child, parents_list in self.parents.items():
            for parent in parents_list:
                G_dag.add_edge(parent, child)
        
        pos_dag = nx.spring_layout(G_dag, seed=42)
        nx.draw(G_dag, pos_dag, with_labels=True, node_color='lightgreen',
               node_size=600, font_size=8, arrows=True, ax=ax)
        ax.set_title("Parent Relationship DAG", fontweight='bold')
        
        # Show up to 3 paths
        for idx, path in enumerate(self.all_paths[:3]):
            ax = axes[idx + 1]
            
            # Create subgraph for this path
            path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
            
            nx.draw_networkx_nodes(self.G_full, self.pos, nodelist=path,
                                  node_color='#FF6B6B', node_size=800, ax=ax)
            nx.draw_networkx_edges(self.G_full, self.pos, edgelist=path_edges,
                                  edge_color='#FF6B6B', width=3, ax=ax)
            nx.draw_networkx_labels(self.G_full, self.pos, font_size=9, ax=ax)
            
            # Fade other nodes
            other_nodes = [n for n in self.G_full.nodes() if n not in path]
            nx.draw_networkx_nodes(self.G_full, self.pos, nodelist=other_nodes,
                                  node_color='#E0E0E0', node_size=400, alpha=0.5, ax=ax)
            
            ax.set_title(f"Path {idx+1}: {' → '.join(path)}", fontweight='bold')
            ax.axis('off')
        
        plt.suptitle(f"Word Ladder Results: {self.begin_word} → {self.end_word}", 
                    fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.ioff()
        plt.show()
    
    def _show_no_path_result(self):
        """Display result when no path exists."""
        plt.ion()
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.text(0.5, 0.6, f"✗ No Path Found!", 
               ha='center', va='center', fontsize=24, fontweight='bold', color='red')
        ax.text(0.5, 0.4, f"From '{self.begin_word}' to '{self.end_word}'", 
               ha='center', va='center', fontsize=16)
        ax.text(0.5, 0.2, f"Words explored: {len(self.visited)}", 
               ha='center', va='center', fontsize=14)
        
        ax.axis('off')
        plt.tight_layout()
        plt.ioff()
        plt.show()


def run_test_case(case_num: int, begin: str, end: str, words: List[str], 
                  realtime: bool = True, delay: float = 0.3):
    """Run a single test case with optional real-time visualization."""
    print(f"\n{'#'*70}")
    print(f"# TEST CASE {case_num}")
    print(f"{'#'*70}")
    print(f"Start: {begin} → End: {end}")
    print(f"Word List: {words}")
    print(f"{'#'*70}\n")
    
    visualizer = WordLadderRealTimeVisualizer(begin, end, words)
    
    if realtime:
        success = visualizer.visualize_bfs_realtime(delay=delay)
    else:
        # Just compute without visualization
        paths = find_ladders(begin, end, words)
        if paths:
            print(f"✓ Found {len(paths)} path(s):")
            for i, path in enumerate(paths, 1):
                print(f"  Path {i}: {' → '.join(path)}")
            success = True
        else:
            print("✗ No path found")
            success = False
    
    return success


def main():
    """Run all 10 test cases with real-time visualization."""
    
    # 10 Test Cases: Mix of successful and failing scenarios
    test_cases = [
        # Case 1: Classic example (SUCCESS)
        {
            "begin": "hit",
            "end": "cog",
            "words": ["hot", "dot", "dog", "lot", "log", "cog"]
        },
        
        # Case 2: Short path (SUCCESS)
        {
            "begin": "cat",
            "end": "dog",
            "words": ["cat", "cot", "cog", "dog", "hat", "hot", "dot"]
        },
        
        # Case 3: No path exists - missing connection (FAIL)
        {
            "begin": "hit",
            "end": "cog",
            "words": ["hot", "dot", "dog", "lot", "log"]  # Missing "cog"
        },
        
        # Case 4: Multiple paths (SUCCESS)
        {
            "begin": "start",
            "end": "end",
            "words": ["stare", "state", "slate", "plate", "place", "plage", "elage", "ends"]
        },
        
        # Case 5: Direct one-step transformation (SUCCESS)
        {
            "begin": "cat",
            "end": "bat",
            "words": ["cat", "bat", "rat", "mat", "hat"]
        },
        
        # Case 6: No path - disconnected components (FAIL)
        {
            "begin": "aaa",
            "end": "bbb",
            "words": ["aaa", "aab", "aac", "bbb", "bba", "bbc"]  # No bridge between aaa* and bbb*
        },
        
        # Case 7: Long chain required (SUCCESS)
        {
            "begin": "cold",
            "end": "warm",
            "words": ["cold", "cord", "card", "ward", "warm", "hold", "hard", "warp"]
        },
        
        # Case 8: End word not in dictionary (FAIL)
        {
            "begin": "lead",
            "end": "gold",
            "words": ["lead", "load", "goad", "goal"]  # Missing "gold"
        },
        
        # Case 9: Complex with multiple solutions (SUCCESS)
        {
            "begin": "five",
            "end": "four",
            "words": ["five", "fire", "fare", "fore", "four", "fine", "line", "lore", "more"]
        },
        
        # Case 10: Same start and end (EDGE CASE - SUCCESS)
        {
            "begin": "test",
            "end": "test",
            "words": ["test", "best", "rest", "west"]
        }
    ]
    
    print("="*70)
    print("WORD LADDER REAL-TIME VISUALIZATION - 10 TEST CASES")
    print("="*70)
    print("\nThis demonstration shows real-time BFS exploration of the word ladder problem.")
    print("Watch as the algorithm explores words level by level!")
    print("\nClose each visualization window to proceed to the next test case.")
    print("="*70)
    
    input("\nPress Enter to start the visualizations...")
    
    results = []
    for i, case in enumerate(test_cases, 1):
        try:
            success = run_test_case(
                case_num=i,
                begin=case["begin"],
                end=case["end"],
                words=case["words"],
                realtime=True,
                delay=0.4  # Adjust speed here (lower = faster)
            )
            results.append((i, success))
            
            if i < len(test_cases):
                print(f"\n{'-'*70}")
                print(f"Test Case {i} completed. Press Enter for next case...")
                input()
                
        except KeyboardInterrupt:
            print(f"\n\nVisualization interrupted at test case {i}")
            break
        except Exception as e:
            print(f"\nError in test case {i}: {e}")
            results.append((i, False))
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY OF ALL TEST CASES")
    print("="*70)
    
    successful = sum(1 for _, success in results if success)
    failed = len(results) - successful
    
    for case_num, success in results:
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"Case {case_num:2d}: {status}")
    
    print(f"\nTotal: {successful} successful, {failed} failed out of {len(results)} cases")
    print("="*70)
    
    plt.show()  # Keep windows open until closed


if __name__ == "__main__":
    main()
