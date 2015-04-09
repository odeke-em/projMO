#!/usr/bin/env python3

from tkinter import (
	Tk, W, Entry,
	Label, Button,
	Frame, END, Listbox,
)

import os

from predict import utils, constants

class Application(Frame):

	def createWidgets(self):
		"""
		Creates the various widgets for the gui.
		"""
		
		# label for Enter Word
		self.intruction = Label(self, text = "Enter word.")
		self.intruction.grid(row = 0, column = 0, columnspan = 2, sticky = W)
		# label for Suggested Words
		self.title_list = Label(self, text = "Suggested Words:")
		self.title_list.grid(row = 3, column = 0, columnspan = 2, sticky = W)
		# label for Similarity
		self.title_rating = Label(self, text = "Similarity:")
		self.title_rating.grid(row = 3, column = 1, columnspan = 2, sticky = W)
		# entry box
		self.entry = Entry(self)
		self.entry.grid(row = 1, column = 0, columnspan = 2, sticky = W)
		# submit button
		self.submit_button = Button(self, text = "Check Word", command = self.new_entry)
		self.submit_button.grid(row = 2, column = 0, columnspan = 2, sticky = W)
		# list for similar words
		self.similar_list = Listbox(self, width = 15, height = 15)
		self.similar_list.grid(row = 4, column = 0, sticky = W)
		# list for ratings of words
		self.similar_rating = Listbox(self, width = 8, height = 15)
		self.similar_rating.grid(row = 4, column = 1, sticky = W)

	def load_index(self, index_path):
		mem_index = self.__index_cache.get(index_path, None)
		if not mem_index:
			mem_index = utils.read_dict(index_path)
			self.__index_cache[index_path] = mem_index

		return mem_index
		
	def new_entry(self):
		"""
		When the submit button is pressed the lists clear themselves in
		preparation for new predicted words. 
		"""
		
		# deletes current entries in the lists
		self.similar_list.delete(0, END)
		self.similar_rating.delete(0, END)
		
		# gets the new entry and finds the closest matches to the word
		new_entry = self.entry.get()

		suggestions = self.get_matches(new_entry)
		# function call to get the list of suggested words and ratings
		# display the similar words using
		for rating, suggestion in suggestions:
			self.similar_list.insert(END, suggestion)
			self.similar_rating.insert(END, rating)

	def get_matches(self, query, fuzziness=0.65):
		return utils.find_matches(query, fuzziness, self.load_index(self.__index_path))
		
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.grid()
		self.createWidgets()

		self.__index_cache = {}
		self.__index_path  = os.path.join('predict', constants.DEFAULT_DICT_FILE)

def main():
	root = Tk()
	app = Application(master=root)
	app.mainloop()

if __name__ == '__main__':
	main()