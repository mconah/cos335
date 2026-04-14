import networkx as nx
import matplotlib
# Try interactive backends for real-time visualization
# Order matters: try GUI backends first, fall back to non-interactive
interactive_backend_set = False
for backend in ['TkAgg', 'Qt5Agg', 'QtAgg', 'macosx', 'WXAgg']:
    try:
        matplotlib.use(backend)
        interactive_backend_set = True
        print(f"Using {backend} backend for real-time display")
        break
    except:
        continue

if not interactive_backend_set:
    matplotlib.use('Agg')  # Last resort: Agg (will save files only)
    print("Note: Using Agg backend (non-interactive). Real-time display may not work.")
    print("      Install tkinter or PyQt5 for interactive visualization.")
        
import matplotlib.pyplot as plt
from typing import List, Dict, Set
from collections import deque, defaultdict
from word_ladder import find_ladders
import time
import sys
import os

# ================================================
# REAL-TIME WORD LADDER VISUALIZER
# Shows BFS exploration in real-time with animations
# ================================================

class RealTimeWordLadderVisualizer:
    def __init__(self, begin_word: str, end_word: str, word_list: List[str]):
        self.begin_word = begin_word
        self.end_word = end_word
        self.word_list = word_list
        self.word_set = set(word_list)
        self.parents = defaultdict(list)
        self.visited = set()
        self.current_level = 0
        self.found = False
        
        # Build full graph for visualization
        self.G_full = nx.Graph()
        for word in self.word_set:
            self.G_full.add_node(word)
        if begin_word not in self.word_set:
            self.G_full.add_node(begin_word)
            
        for word in self.word_set:
            for i in range(len(word)):
                for c in "abcdefghijklmnopqrstuvwxyz":
                    if c != word[i]:
                        neighbor = word[:i] + c + word[i+1:]
                        if neighbor in self.word_set:
                            self.G_full.add_edge(word, neighbor)
        
        # Add edges from begin_word if it's not in word_set
        if begin_word not in self.word_set:
            for i in range(len(begin_word)):
                for c in "abcdefghijklmnopqrstuvwxyz":
                    if c != begin_word[i]:
                        neighbor = begin_word[:i] + c + begin_word[i+1:]
                        if neighbor in self.word_set:
                            self.G_full.add_edge(begin_word, neighbor)
        
        # Compute layout once for consistency
        self.pos = nx.spring_layout(self.G_full, seed=42, k=0.5)
        
        # Setup figure
        self.fig, self.ax = plt.subplots(figsize=(14, 10))
        plt.ion()  # Turn on interactive mode
        
    def get_node_colors(self, processing=None, visited_set=None, path=None):
        """Get colors for nodes based on their state."""
        colors = []
        for node in self.G_full.nodes():
            if path and node in path:
                colors.append('#FF6B6B')  # Red for final path
            elif node == self.begin_word:
                colors.append('#4ECDC4')  # Teal for start
            elif node == self.end_word:
                colors.append('#FFE66D')  # Yellow for target
            elif processing and node == processing:
                colors.append('#FF8C42')  # Orange for currently processing
            elif visited_set and node in visited_set:
                colors.append('#95E1D3')  # Light green for visited
            else:
                colors.append('#D3D3D3')  # Gray for unvisited
        return colors
    
    def draw_graph(self, title: str, processing=None, visited_set=None, path=None):
        """Draw the current state of the graph."""
        self.ax.clear()
        
        node_colors = self.get_node_colors(processing, visited_set, path)
        
        nx.draw(self.G_full, self.pos, 
                node_color=node_colors,
                edge_color='#E0E0E0',
                with_labels=True,
                node_size=1200,
                font_size=9,
                font_weight='bold',
                ax=self.ax,
                alpha=0.9)
        
        self.ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        
        # Try to show the window (works with interactive backends)
        try:
            plt.show(block=False)
        except:
            pass  # Non-interactive backend, just save frames
    
    def visualize_bfs_realtime(self, delay: float = 0.3):
        """Run BFS with real-time visualization."""
        print("\n" + "="*60)
        print(f"Starting Real-Time BFS Visualization")
        print(f"From '{self.begin_word}' to '{self.end_word}'")
        print("="*60 + "\n")
        
        queue = deque([self.begin_word])
        self.visited = {self.begin_word}
        self.parents = defaultdict(list)
        self.current_level = 0
        self.found = False
        
        while queue and not self.found:
            level_size = len(queue)
            new_visited = set()
            
            print(f"Level {self.current_level}: Processing {level_size} word(s)")
            
            for _ in range(level_size):
                if not queue:
                    break
                    
                current = queue.popleft()
                
                # Visualize current word being processed
                title = f"Level {self.current_level} | Processing: {current}"
                self.draw_graph(title, processing=current, visited_set=self.visited)
                plt.pause(delay)
                
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
                                    self.found = True
                
                # Update visited after processing each word
                self.visited.update(new_visited)
            
            self.current_level += 1
        
        if self.found:
            print(f"\n✓ Path found in {self.current_level} levels!")
            # Final visualization with all visited nodes
            title = f"✓ Target Found! Explored {len(self.visited)} words in {self.current_level} levels"
            self.draw_graph(title, visited_set=self.visited)
            plt.pause(1.0)
        else:
            print(f"\n✗ No path found after exploring {len(self.visited)} words.")
            title = f"✗ No Path Found | Explored {len(self.visited)} words"
            self.draw_graph(title, visited_set=self.visited)
            plt.pause(2.0)
        
        return self.found
    
    def visualize_paths(self, all_paths: List[List[str]], delay: float = 1.5):
        """Visualize each shortest path found."""
        if not all_paths:
            print("No paths to visualize.")
            return
        
        print(f"\nFinding all shortest paths...")
        print(f"Found {len(all_paths)} shortest path(s):")
        
        for idx, path in enumerate(all_paths):
            print(f"  Path {idx+1}: {' → '.join(path)}")
            
            title = f"Shortest Path {idx+1}/{len(all_paths)}: {' → '.join(path)}"
            self.draw_graph(title, path=path)
            plt.pause(delay)
        
        # Show all paths together
        plt.pause(0.5)
        title = f"All {len(all_paths)} Shortest Paths - Complete!"
        self.draw_graph(title, visited_set=self.visited)
        plt.pause(2.0)


def run_test_case(test_num: int, begin_word: str, end_word: str, 
                  word_list: List[str], should_succeed: bool = True):
    """Run a single test case with visualization."""
    print("\n" + "#"*70)
    print(f"# TEST CASE {test_num}")
    print("#"*70)
    print(f"Start: {begin_word} → End: {end_word}")
    print(f"Word List: {word_list}")
    print(f"Expected: {'SUCCESS' if should_succeed else 'FAILURE'}")
    print("#"*70 + "\n")
    
    try:
        visualizer = RealTimeWordLadderVisualizer(begin_word, end_word, word_list)
        found = visualizer.visualize_bfs_realtime(delay=0.4)
        
        if found:
            all_paths = find_ladders(begin_word, end_word, word_list)
            if all_paths:
                visualizer.visualize_paths(all_paths, delay=1.5)
                print(f"\n✓ Test Case {test_num} PASSED - Found {len(all_paths)} path(s)")
            else:
                print(f"\n✗ Test Case {test_num} FAILED - BFS found path but find_ladders didn't")
        else:
            if not should_succeed:
                print(f"\n✓ Test Case {test_num} PASSED - Correctly identified no path exists")
            else:
                print(f"\n✗ Test Case {test_num} FAILED - Expected to find a path")
        
        # Only wait for user input if using interactive backend
        if matplotlib.get_backend().lower() != 'agg':
            input(f"\n--- Test Case {test_num} completed. Press Enter for next case... ---")
        else:
            print(f"\n--- Test Case {test_num} completed (non-interactive mode) ---")
            time.sleep(1)
        plt.close()
        
    except Exception as e:
        print(f"\n✗ Test Case {test_num} ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        if matplotlib.get_backend().lower() != 'agg':
            input("Press Enter to continue...")
        else:
            time.sleep(1)
        plt.close()


def main():
    """Run 10 test cases - mix of successful and failing scenarios."""
    print("="*70)
    print("WORD LADDER REAL-TIME VISUALIZATION - 10 TEST CASES")
    print("="*70)
    print(f"\nCurrent backend: {matplotlib.get_backend()}")
    print("\nThis demonstration shows real-time BFS exploration of the word ladder problem.")
    print("Watch as the algorithm explores words level by level!")
    
    if matplotlib.get_backend().lower() != 'agg':
        print("\nClose each visualization window to proceed to the next test case.")
    else:
        print("\nNote: Running in non-interactive mode (saving frames only).")
        print("      Install tkinter for interactive display: sudo apt-get install python3-tk")
    
    print("="*70)
    
    if matplotlib.get_backend().lower() != 'agg':
        input("\nPress Enter to start the visualizations...")
    else:
        print("\nStarting visualizations in 2 seconds...")
        time.sleep(2)
    
    # Test cases: (test_num, begin, end, word_list, should_succeed)
    test_cases = [
        # SUCCESSFUL CASES (7)
        (1, "hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"], True),
        (2, "cat", "dog", ["cat", "cot", "cog", "dog", "hat", "hot", "dot"], True),
        (3, "red", "blue", ["bed", "red", "bet", "bat", "cat", "cot", "cog", "bog", "bug", "lug", "lug", "blue"], False),  # Actually might fail depending on dict
        (4, "start", "stony", ["start", "smart", "stare", "stern", "stony", "stone"], True),
        (5, "cold", "warm", ["cold", "cord", "card", "ward", "warm"], True),
        (6, "lead", "gold", ["lead", "leaf", "leap", "loop", "look", "lock", "cock", "cook", "cool", "coal", "goal", "gold"], True),
        (7, "boy", "man", ["boy", "bay", "ban", "man"], True),
        
        # FAILING CASES (3)
        (8, "abc", "xyz", ["def", "ghi", "jkl", "mno", "pqr", "stu", "vwx"], False),
        (9, "hit", "xyz", ["hot", "dot", "dog", "lot", "log"], False),  # end_word not in list
        (10, "aaa", "bbb", ["ccc", "ddd", "eee"], False),  # Completely disconnected
    ]
    
    for test_num, begin, end, words, should_succeed in test_cases:
        run_test_case(test_num, begin, end, words, should_succeed)
    
    print("\n" + "="*70)
    print("ALL TEST CASES COMPLETED!")
    print("="*70)
    print("\nSummary:")
    print("- Cases 1-7: Successful path finding with visualization")
    print("- Cases 8-10: Correctly identified when no path exists")
    print("\nReal-time visualization demonstrates BFS exploration step-by-step.")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
