"""
Variables
"""
old_inputs = []
banned_characters = set()

"""
Constangs
"""
CHAR_FREQ = { 
    'e': 0.11 ,
    's': 0.087, 
    'i': 0.082, 
    'a': 0.078, 
    'r': 0.073, 
    'n': 0.072,
    't': 0.067,
    'o': 0.061,
    'l': 0.053,
    'c': 0.04, 
    'd': 0.038,
    'u': 0.033,
    'g': 0.03,
    'p': 0.028,
    'm': 0.027,
    'k': 0.025,
    'h': 0.023,
    'b': 0.02,
    'y': 0.016,
    'f': 0.014,
    'v': 0.01,
    'w': 0.0091,
    'z': 0.0044,
    'x': 0.0027,
    'q': 0.0024,
    'j': 0.0021 
  }
class TrieNode:
  def __init__(self):
    self.word = None
    self.children = [None] * 26

class Trie:
  def __init__(self):
    self.parent = TrieNode()
  
  def add_word(self, word):
    curr = self.parent
    for letter in word:
      pos = ord(letter)-ord('a')
      if curr.children[pos] is None:
        curr.children[pos] = TrieNode()
      curr = curr.children[pos]
    curr.word = word

  def process_guess(self, guess):
    results = []
    def process(guess, node):
      if (len(guess) == 0): return
      if not node: return

      c = guess[0]
      if c == '*':
        for i in range(len(node.children)):
          if (chr(i+ord('a')) not in banned_characters) and node.children[i]: 
            if node.children[i].word:
              results.append(node.children[i].word)
            process(guess[1:], node.children[i])
      else:
        curr = node.children[ord(c)-ord('a')]
        if not curr: return
        if curr.word:
          results.append(curr.word)
        process(guess[1:], curr)

    process(guess, self.parent)
    return results



print("Writing words into memory...")
wordTrie =  Trie()
with open('words_list.txt') as f:
    words = f.readlines()
    for word in words:
      word = word.strip()
      wordTrie.add_word(word)


def process_guess(guess):
  return wordTrie.process_guess(guess)

def filter_misplaced(misplaced, results):
  new_results = []
  def valid(word):
    for m in misplaced:
      if word[m[0]] == m[1]: return False
      if m[1] not in word: return False

    return True

  for result in results:
    if not valid(result):
      continue
    new_results.append(result)
  return new_results

def best_candidate(candidates, misplaced):
  best_score = 0
  best_word = None

  for candidate in candidates:
    score = 1
    used = set()
    for c in candidate:
      score *= CHAR_FREQ[c]
      # Score repeated letters lower.
      if c in used:
        score /= 2
      used.add(c)
    if score > best_score:
      best_score = score
      best_word = candidate

  return best_word

"""
0 = Not in word
1 = Not in correct position
2 = Correct position

misplaced: index, character
T0E1N2O0R0
T2E2N2O2R2
T0E0N0O0R0
"""

while True:
  print("Used words:")
  print(old_inputs)
  print("\n\n")
  x = raw_input("Input word (i.e. TENOR): ")
  y = raw_input("Input states(0 = Grey, 1 = Yellow, 2 = Green) (i.e. 01200): ")
  if (len(x) != 5):
    print("Please add 5 letter word.")
    continue
  old_inputs.append(x)
  guess = ""
  misplaced = []
  for i in range(0, len(x)):
    c = x[i].lower()
    if (int(y[i]) == 2):
      guess += c
    elif (int(y[i]) == 1):
      misplaced.append((i, c))
      guess += "*"
    else:
      banned_characters.add(c)
      guess += "*"
  for c in misplaced:
    if c[1] in banned_characters:
      banned_characters.remove(c[1])

  # Win condition
  if ('*' not in guess):
    print("You win!")
    break
  print("Guess: " + guess)
  # print(banned_characters)
  # print(misplaced)
  candidates = process_guess(guess)
  candidates = filter_misplaced(misplaced, candidates)
  print(candidates)

  print("\n")
  print("Use this word: " + best_candidate(candidates, misplaced))
  print("\n")
  