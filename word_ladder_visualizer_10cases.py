import networkx as nx
import matplotlib
# Force Agg backend for server/headless environments
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from typing import List, Dict, Set
from collections import deque, defaultdict
from word_ladder import find_ladders
import time
import os

# ================================================
# WORD LADDER VISUALIZER - 10 TEST CASES
# Generates static images for each test case
# For real-time visualization, see word_ladder_realtime.py
# ================================================

class WordLadderVisualizer:
    def __init__(self, begin_word: str, end_word: str, word_list: List[str], output_dir: str = "output"):
        self.begin_word = begin_word
        self.end_word = end_word
        self.word_list = word_list
        self.word_set = set(word_list)
        self.parents = defaultdict(list)
        self.visited = set()
        self.current_level = 0
        self.found = False
        self.output_dir = output_dir
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
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
    
    def draw_and_save(self, filename: str, title: str, processing=None, visited_set=None, path=None):
        """Draw the current state and save to file."""
        fig, ax = plt.subplots(figsize=(14, 10))
        
        node_colors = self.get_node_colors(processing, visited_set, path)
        
        nx.draw(self.G_full, self.pos, 
                node_color=node_colors,
                edge_color='#E0E0E0',
                with_labels=True,
                node_size=1200,
                font_size=9,
                font_weight='bold',
                ax=ax,
                alpha=0.9)
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        return filepath
    
    def visualize_bfs(self, save_frames: bool = True):
        """Run BFS and optionally save visualization frames."""
        print(f"\nRunning BFS from '{self.begin_word}' to '{self.end_word}'...")
        
        queue = deque([self.begin_word])
        self.visited = {self.begin_word}
        self.parents = defaultdict(list)
        self.current_level = 0
        self.found = False
        
        frame_count = 0
        
        while queue and not self.found:
            level_size = len(queue)
            new_visited = set()
            
            print(f"Level {self.current_level}: Processing {level_size} word(s)")
            
            for _ in range(level_size):
                if not queue:
                    break
                    
                current = queue.popleft()
                
                # Save frame if requested
                if save_frames and frame_count < 10:  # Limit frames
                    title = f"Level {self.current_level} | Processing: {current}"
                    filepath = self.draw_and_save(
                        f"bfs_frame_{frame_count:03d}.png",
                        title, processing=current, visited_set=self.visited
                    )
                    frame_count += 1
                
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
            print(f"✓ Path found in {self.current_level} levels!")
            # Save final BFS state
            if save_frames:
                self.draw_and_save(
                    "bfs_final.png",
                    f"✓ Target Found! Explored {len(self.visited)} words in {self.current_level} levels",
                    visited_set=self.visited
                )
        else:
            print(f"✗ No path found after exploring {len(self.visited)} words.")
            if save_frames:
                self.draw_and_save(
                    "bfs_failed.png",
                    f"✗ No Path Found | Explored {len(self.visited)} words",
                    visited_set=self.visited
                )
        
        return self.found
    
    def visualize_paths(self, all_paths: List[List[str]]):
        """Visualize each shortest path found."""
        if not all_paths:
            print("No paths to visualize.")
            return []
        
        print(f"\nFound {len(all_paths)} shortest path(s):")
        saved_files = []
        
        for idx, path in enumerate(all_paths):
            print(f"  Path {idx+1}: {' → '.join(path)}")
            
            title = f"Shortest Path {idx+1}/{len(all_paths)}: {' → '.join(path)}"
            filepath = self.draw_and_save(
                f"path_{idx+1}.png",
                title, path=path
            )
            saved_files.append(filepath)
        
        # Save combined view
        self.draw_and_save(
            "all_paths_summary.png",
            f"All {len(all_paths)} Shortest Paths - Summary",
            visited_set=self.visited
        )
        
        return saved_files


def run_test_case(test_num: int, begin_word: str, end_word: str, 
                  word_list: List[str], should_succeed: bool = True,
                  output_base: str = "output"):
    """Run a single test case and save visualizations."""
    print("\n" + "#"*70)
    print(f"# TEST CASE {test_num}")
    print("#"*70)
    print(f"Start: {begin_word} → End: {end_word}")
    print(f"Word List: {word_list}")
    print(f"Expected: {'SUCCESS' if should_succeed else 'FAILURE'}")
    print("#"*70)
    
    output_dir = os.path.join(output_base, f"test_{test_num}")
    
    try:
        visualizer = WordLadderVisualizer(begin_word, end_word, word_list, output_dir)
        found = visualizer.visualize_bfs(save_frames=True)
        
        if found:
            all_paths = find_ladders(begin_word, end_word, word_list)
            if all_paths:
                visualizer.visualize_paths(all_paths)
                print(f"\n✓ Test Case {test_num} PASSED - Found {len(all_paths)} path(s)")
                print(f"  Output saved to: {output_dir}/")
            else:
                print(f"\n✗ Test Case {test_num} FAILED - BFS found path but find_ladders didn't")
        else:
            if not should_succeed:
                print(f"\n✓ Test Case {test_num} PASSED - Correctly identified no path exists")
                print(f"  Output saved to: {output_dir}/")
            else:
                print(f"\n✗ Test Case {test_num} FAILED - Expected to find a path")
        
        return found
        
    except Exception as e:
        print(f"\n✗ Test Case {test_num} ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run 10 test cases - mix of successful and failing scenarios."""
    print("="*70)
    print("WORD LADDER VISUALIZATION - 10 TEST CASES")
    print("="*70)
    print("\nThis generates static image visualizations for each test case.")
    print("For real-time animation, use: python word_ladder_realtime.py")
    print("="*70)
    
    # Test cases: (test_num, begin, end, word_list, should_succeed)
    test_cases = [
        # SUCCESSFUL CASES (7)
        (1, "hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"], True),
        (2, "cat", "dog", ["cat", "cot", "cog", "dog", "hat", "hot", "dot"], True),
        (3, "cold", "warm", ["cold", "cord", "card", "ward", "warm"], True),
        (4, "lead", "gold", ["lead", "leaf", "leap", "loop", "look", "lock", "cock", "cook", "cool", "coal", "goal", "gold"], False),  # No valid path (leap->loop diff=2)
        (5, "boy", "man", ["boy", "bay", "ban", "man"], True),
        (6, "start", "stony", ["start", "stare", "stern", "stony", "stone"], False),  # No valid path (stare->stern diff=2)
        (7, "five", "four", ["five", "fire", "fare", "fore", "four"], False),  # No valid path (fore->four diff=2)
        
        # FAILING CASES (3)
        (8, "abc", "xyz", ["def", "ghi", "jkl", "mno", "pqr", "stu", "vwx"], False),
        (9, "hit", "xyz", ["hot", "dot", "dog", "lot", "log"], False),  # end_word not in list
        (10, "aaa", "bbb", ["ccc", "ddd", "eee"], False),  # Completely disconnected
    ]
    
    results = []
    for test_num, begin, end, words, should_succeed in test_cases:
        result = run_test_case(test_num, begin, end, words, should_succeed)
        results.append((test_num, result, should_succeed))
    
    # Print summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    passed = 0
    for test_num, result, expected in results:
        success = (result == expected)
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"Test {test_num}: {status} (found={result}, expected={expected})")
        if success:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(test_cases)} tests passed")
    print(f"\nOutput directories: output/test_1/, output/test_2/, ..., output/test_10/")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
