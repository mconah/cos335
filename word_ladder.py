import collections
from typing import List, Set, Dict

# ================================================
# WORD LADDER II - 20 FUNCTIONS (One per team member)
# Each function solves exactly ONE part of the problem
# ================================================

def create_word_set(word_list: List[str]) -> Set[str]:
    """Function 1: Convert wordList into a set for fast O(1) lookups."""
    return set(word_list)


def end_word_in_dictionary(end_word: str, word_set: Set[str]) -> bool:
    """Function 2: Check if endWord exists in the dictionary."""
    return end_word in word_set


def initialize_parents() -> Dict[str, List[str]]:
    """Function 3: Create parents dictionary to store all valid previous words."""
    return collections.defaultdict(list)


def initialize_bfs_queue(start_word: str) -> collections.deque:
    """Function 4: Initialize BFS queue with the starting word."""
    queue = collections.deque()
    queue.append(start_word)
    return queue


def initialize_visited_set(start_word: str) -> Set[str]:
    """Function 5: Initialize visited set and mark startWord as visited."""
    return {start_word}


def generate_one_letter_changes(word: str) -> List[str]:
    """Function 6: Generate all possible words by changing exactly one letter."""
    changes = []
    for i in range(len(word)):
        for ch in "abcdefghijklmnopqrstuvwxyz":
            if ch != word[i]:
                new_word = word[:i] + ch + word[i+1:]
                changes.append(new_word)
    return changes


def is_valid_neighbor(neighbor: str, word_set: Set[str], visited: Set[str]) -> bool:
    """Function 7: Check if neighbor is in dictionary and not yet visited."""
    return neighbor in word_set and neighbor not in visited


def add_parent_to_map(parents: Dict[str, List[str]], child: str, parent: str) -> None:
    """Function 8: Record that 'parent' can transform into 'child' in one step."""
    if parent not in parents[child]:
        parents[child].append(parent)


def should_enqueue_word(neighbor: str, new_visited: Set[str]) -> bool:
    """Function 9: Decide if this word should be added to the queue (first time in level)."""
    return neighbor not in new_visited


def add_to_new_visited(new_visited: Set[str], word: str) -> None:
    """Function 10: Mark word as visited in the current BFS level."""
    new_visited.add(word)


def enqueue_word(queue: collections.deque, word: str) -> None:
    """Function 11: Add word to the BFS queue."""
    queue.append(word)


def update_visited_with_level(visited: Set[str], new_visited: Set[str]) -> None:
    """Function 12: Merge current level's new words into the main visited set."""
    visited.update(new_visited)


def end_word_found_this_level(end_word: str, new_visited: Set[str]) -> bool:
    """Function 13: Check if endWord was found in the current BFS level."""
    return end_word in new_visited


def initialize_result_list() -> List[List[str]]:
    """Function 14: Create empty list to store all valid transformation sequences."""
    return []


def build_initial_path(end_word: str) -> List[str]:
    """Function 15: Start the backtracking path with the endWord."""
    return [end_word]


def is_start_word(current: str, start_word: str) -> bool:
    """Function 16: Check if we have reached the beginWord during DFS."""
    return current == start_word


def add_reversed_path_to_result(path: List[str], result: List[List[str]]) -> None:
    """Function 17: Reverse the path (to go from start → end) and add to result."""
    result.append(path[::-1])


def get_parents_of_word(parents: Dict[str, List[str]], word: str) -> List[str]:
    """Function 18: Get all immediate previous words (parents) of current word."""
    return parents.get(word, [])


def append_to_path(path: List[str], word: str) -> None:
    """Function 19: Add previous word to the current path during backtracking."""
    path.append(word)


def remove_last_from_path(path: List[str]) -> None:
    """Function 20: Remove the last word after exploring a branch (backtracking)."""
    if path:
        path.pop()


# ================================================
# MAIN FUNCTION - Brings all 20 functions together
# ================================================

def find_ladders(begin_word: str, end_word: str, word_list: List[str]) -> List[List[str]]:
    """
    Word Ladder II Solution using BFS + DFS
    Returns ALL shortest transformation sequences from beginWord to endWord.
    """
    if begin_word == end_word:
        return [[begin_word]]

    # Step 1-5: Initialization 
    word_set = create_word_set(word_list)                          # 1
    if not end_word_in_dictionary(end_word, word_set):             # 2
        return []

    parents = initialize_parents()                                 # 3
    queue = initialize_bfs_queue(begin_word)                       # 4
    visited = initialize_visited_set(begin_word)                   # 5

    # BFS Phase: Build the parent map for shortest paths
    while queue:
        new_visited = set()
        level_size = len(queue)

        for _ in range(level_size):
            current = queue.popleft()
            possible_changes = generate_one_letter_changes(current)  # 6

            for neighbor in possible_changes:
                if is_valid_neighbor(neighbor, word_set, visited):   # 7
                    add_parent_to_map(parents, neighbor, current)    # 8

                    if should_enqueue_word(neighbor, new_visited):   # 9
                        add_to_new_visited(new_visited, neighbor)    # 10
                        enqueue_word(queue, neighbor)                # 11

        update_visited_with_level(visited, new_visited)              # 12

        if end_word_found_this_level(end_word, new_visited):         # 13
            break

    # If endWord was never reached
    if end_word not in visited:
        return []

    # DFS Phase: Reconstruct all shortest paths
    result = initialize_result_list()                                # 14
    path = build_initial_path(end_word)                              # 15

    def dfs(current: str, path: List[str]):
        if is_start_word(current, begin_word):                       # 16
            add_reversed_path_to_result(path, result)                # 17
            return

        for prev in get_parents_of_word(parents, current):           # 18
            append_to_path(path, prev)                               # 19
            dfs(prev, path)
            remove_last_from_path(path)                              # 20

    dfs(end_word, path)
    return result


# ================================================
# TEST THE SOLUTION
# ================================================
if __name__ == "__main__":
    begin_word = "hit"
    end_word = "cog"
    word_list = ["hot", "dot", "dog", "lot", "log", "cog"]

    all_paths = find_ladders(begin_word, end_word, word_list)

    print(f"Found {len(all_paths)} shortest transformation sequence(s):")
    for i, path in enumerate(all_paths, 1):
        print(f"Path {i}: {' → '.join(path)}")