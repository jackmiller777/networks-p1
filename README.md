miller.john 
README.md
3700 Proj 1

Wordle Solver Client

**Approach:**
My approach to this project started with making sure I could ping the server, then connect, then send and receive. I haven't done much networking code before, so I wanted to make sure I could get it working from the python shell first. Once I was comfortable sending and receiving, I build a solver and controller class to make guesses and send the guesses to the server respectively. 

**Challenges:**
I initially had a few more ideas to rule out more words from the word list, but unfortunately I ran out of time to get them working. This involved removing words with letters that were not in the word, and removing words that didn't contain a certain letter somewhere in the word. If I get a chance, I will restart this whole process to try guessing the word from scratch without the list of word options.

**Guessing Strategy:**
The guessing strategy I implemented was very brute-force based that works by eliminating words from the given word list. All it does is take the json response from the server after a guess, and whenever a letter is in the right place, all words that do not have a letter in that place are removed. Like I said in the challenges section, I ran out of time to implement more eliminating options.

**Testing Overview:**
I tested my code by running it repeatedly with all options (-p, -s), with and without tls. I also tested my solver without any networking just by guessing words.
