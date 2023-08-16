#!/usr/bin/env python3

from socket import *
import ssl
import json
import sys        
from random import randint

#./client -p 27993 proj1.3700.network miller.john

class Client:
    
    def __init__(self, port : 27993, tls : False, hostname, username):
        self.port = int(port)
        self.tls = tls
        self.hostname = hostname
        self.username = username
        
        self.session_id = None
        self.client_socket = None

    # Sends a message to the server encoded with a newline
    def send(self, message):
        msg_encoded = (message + '\n').encode()
        self.client_socket.send(msg_encoded)
    
    # Recieves from the server until newline is received
    def receive(self):
        message_from_server = ''
        while True:
            message_from_server += self.client_socket.recv(1024).decode()
            if '\n' in message_from_server:
                return message_from_server

    
    # Create and connect client socket.
    def start(self):
        
        # Close socket if open
        try:
            self.client_socket.close()
        except:
            pass
        
        identifier = (self.hostname, self.port)
        
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(identifier)
        
        if self.tls:
            context = ssl.create_default_context()
            self.client_socket = context.wrap_socket(self.client_socket, server_hostname=self.hostname)

        # The introductory message
        hello = '{"type": "hello", "northeastern_username": "' + self.username + '"}'

        # Send message to server.
        self.send(hello)

        # Convert message to output string.
        output_message = self.receive()

        output_dict = json.loads(output_message)

        # Get session id for guessing
        self.session_id = output_dict['id']
#        print(self.session_id)

    # Sends a guess to the server and returns the json result as a dict
    def guess(self, guess):
        if self.session_id == None:
            self.start()
            return

        guess_dict = {}
        guess_dict['type'] = 'guess'
        guess_dict['id'] = self.session_id
        guess_dict['word'] = guess
        guess_msg = json.dumps(guess_dict)
        
        self.send(guess_msg)

        output_message = self.receive()
        output_dict = json.loads(output_message)
        
        msg_type = output_dict['type']
        
        
        if output_dict['type'] == 'bye':
            self.close()

        return output_dict


    def close(self):
        self.client_socket.close()

    # Solver - Attempts to solve the wordle puzzle given the last guess and a list of words that is slowly wittled down
class Solver:
    def __init__(self):
        self.words = get_words()
#        print(len(self.words))
        
    # Makes a guess by eliminating words that do not have any correct letters (brute force)
    def guess(self, prev, marks):
        
#        print(prev, marks, len(self.words))
        if marks == None:
            guess = 'cared' # self.words[randint(0,len(self.words))]
        else:
            for i in range(5):
                if marks[i] == 2:
                    self.clear_words_by_index(i, prev[i])
            
            guess = self.words[0]
        
        self.words.remove(guess)
        return guess

    # Removes words that dont have the given char at the given index
    def clear_words_by_index(self, index, char):
        wrong_words = []
        for word in self.words:
            if word[index] != char:
                wrong_words.append(word)
                
        self.remove_words(wrong_words)
            
    # Removes a list of words from the word list
    def remove_words(self, wrong_words):
        for word in wrong_words:
            self.words.remove(word)
          

    # Main Controller - starts client and runs guesses until the game is won
class Controller:
    def __init__(self, port : 27993, tls : False, hostname, username):
        self.client = Client(port, tls, hostname, username)
        self.solver = Solver()
        
    # Starts client and guesses until the flag is found
    def run(self):
        guesses = 0
        self.client.start()
        
        results = None
        while True:
#            guess = self.solver.guess(results)
            
            print('Suggestion:', self.solver.guess(results['guesses'][-1]['marks']))
            guess = input()
            
            if guess not in self.words:
                print('Not a valid word')
                continue
            
            results = self.client.guess(guess)
            
            print(results['guesses'][-1]['marks'])
            
            guesses += 1
        
            res_type = results['type']
        
            if res_type == 'bye':
                flag = results['flag']
                print('The word was ', guess, '!', sep='')
                print('Number of guesses:', guesses)
                print(flag)
                return flag
            else:
#                print(results['guesses'][-1]['marks'])
                pass

    
def read_words():
    print('reading')
    return open('project1-words.txt').read().split()

class Words:
    words = read_words()
    

def get_words():
    return Words.words.copy()

class Tester:
    
    def __init__(self):
        self.words = get_words()
        self.tries = []
        self.total_tries = len(self.words)
        
    def run(self):
        
        most_tries = 0
        mt_word = ''
        
        for word in self.words:
            solver = Solver()
            guess = solver.guess([], None)
            tries = 1
            while True:
                marks = self.check(guess, word)
                if marks == [2, 2, 2, 2, 2]:
                    break
#                print(len(solßver.words))
                try:
                    guess = solver.guess(guess, marks)
                    tries += 1
                except Exception as e:
                    print(e)
            
                if tries == 1500:
                    print("More than 1500 attempts. Quitting...")
                    return
            
            if tries > most_tries:
                most_tries = tries
                mt_word = word
            
#            print('Word:', word, tries)
            self.tries.append(tries)
        return self.avg(), most_tries, mt_word
                    
    def avg(self):
        total = 0
        for t in self.tries:
            total += t
        return (float(total) / float(self.total_tries))
                
    def check(self, guess, secret):
        marks = []
        for i in range(5):
            if guess[i] == secret[i]:
                marks.append(2)
            else:
                marks.append(0)
#        print(guess,secret,marks)
        return marks
        
        
    # Main Function - checks for args and sets defaults
if __name__ == '__main__':
    
    # Process args
    args = sys.argv
    
    if len(args) == 1:
        test = Tester()
        print(test.run())