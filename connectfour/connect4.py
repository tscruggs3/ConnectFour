"""
CS 111 Final Project
By Thomas Scruggs
Connect Four Game
"""

import graphics
import math
import random
from time import sleep

class GraphicInterfaceAndLocation:
	"""The GraphicInterfaceAndLocation class contains the graphics portion of the connect four 
	game. It also contains all the functions that relate to where pieces have been played,
	such as the lists of played pieces and the functions to check if a player has won. Its my 
	Jack of all trades class.

	Note: Game coordinates represent the grid of possible playing locations. Its a grid with 7
	columns and 6 rows, where (0, 0) is the bottom left square.
	"""

	def __init__(self):
		"""Constructor that initializes the graphics window, the game board, and the lists of
		locations where pieces have been played"""

		#initialize window
		window_length = 800
		window_height = 700
		self.win = graphics.GraphWin("Connect Four", window_length, window_height)
		self.win.setCoords(0,0, 800, 700)

		#draw the game board
		board_center = graphics.Point(window_length//2, window_height//2-50)
		board = graphics.Image(board_center, "Connect4Board.gif")
		board.draw(self.win)

		#initialize lists of where game pieces have been played
		self.col0 = [0,0,0,0,0,0]
		self.col1 = [0,0,0,0,0,0]
		self.col2 = [0,0,0,0,0,0]
		self.col3 = [0,0,0,0,0,0]
		self.col4 = [0,0,0,0,0,0]
		self.col5 = [0,0,0,0,0,0]
		self.col6 = [0,0,0,0,0,0]
		self.list_of_columns = [self.col0, self.col1, self.col2, self.col3, self.col4, self.col5, self.col6]


		#initialize scaling factors to convert coordinates to the graphics window
		#The constant is the distance from the edge of the game board to the center of the
		#closest circle
		self.X_constant = 128
		self.X_scalar = 90.5
		self.Y_constant = 99
		self.Y_scalar = 80.3
		#initialize the radius of the playing pieces
		self.radius = 36

		#draw background text
		heading_center = graphics.Point(self.X_constant + 3 * self.X_scalar, self.Y_constant + 7 * self.Y_scalar)
		heading = graphics.Text(heading_center, "Connect Four")
		heading.setSize(36)
		heading.setStyle("bold italic")
		heading.draw(self.win)

		self.player_turn = 1
		self.player1_color = "yellow"
		self.player2_color = "red"

		#initialize center for subtitle text
		self.subtitle_center = graphics.Point(self.X_constant + 3 * self.X_scalar, 10 + self.Y_constant + 6 * self.Y_scalar)
		self.question = None

	def get_current_player(self):
		#Gets the current player
		return self.player_turn

	def get_fill_color(self):
		#Gets the current player's piece color
		if self.player_turn == 1:
			return self.player1_color
		else:
			return self.player2_color

	def update(self):
		"""Updates whose turn it is after a turn is taken"""
		if self.player_turn == 1:
			self.player_turn = 2
		else:
			self.player_turn = 1

	def draw_piece(self, color, Xpos, Ypos, animation):
		"""
		A function that draws a piece on the game board with a given color, and (x, y) coordinate.
		It also updates self.list_of_columns with the new played piece.

		Parameters:
		color - the color of the game piece, either "red" or "yellow"
		Xpos - an integer between 0-6
		Ypos - an integer between 0-5
		animation - If animation is turned on, the pieces have a falling animation when played
		"""

		X_coord = self.X_constant + self.X_scalar * Xpos
		Y_coord = self.Y_constant + self.Y_scalar * Ypos
		accelleration = -1
		velocity = accelleration - 6
		curr_Y_coord = self.Y_constant + 6 * self.Y_scalar
		if animation == 1:
			piece_center = graphics.Point(X_coord, curr_Y_coord)
			piece = graphics.Circle(piece_center, self.radius)
			piece.setFill(color)
			piece.draw(self.win)

		while curr_Y_coord > Y_coord and animation == 1:
			piece.undraw()
			velocity += accelleration
			curr_Y_coord += velocity
			if curr_Y_coord < Y_coord:
				curr_Y_coord = Y_coord
			piece_center = graphics.Point(X_coord, curr_Y_coord)
			piece = graphics.Circle(piece_center, self.radius)
			piece.setFill(color)
			piece.draw(self.win)
			sleep(0.001)

		if animation != 1:
			piece_center = graphics.Point(X_coord, Y_coord)
			piece = graphics.Circle(piece_center, self.radius)
			piece.setFill(color)
			piece.draw(self.win)

		#Update self.list_of_columns
		col = self.list_of_columns[Xpos]
		col[Ypos] = self.get_current_player()

	def find_first_zero(self, a_list):
		"""Finds the first zero entry of a list and returns its index. If there are no
		0 entries, it returns -1

		Parameters:
		a_list - the list to be searched
		"""
		for idx in range (len(a_list)):
			val = a_list[idx]
			if val == 0:
				return idx
		return -1

	def find_column(self, point):
		"""
		Finds which column of the game board a point is in, if any. Returns the number of the 
		column if the point is in a column, otherwise returns -1

		Parameters:
		point - the point to determine whether it's in the game board
		"""
		x_val = point.getX()
		x_minus_constant = x_val - self.X_constant
		if x_minus_constant < 0:
			return -1
		x_minus_constant += self.X_scalar//2
		x_column = (x_minus_constant//self.X_scalar)
		if x_column > 6:
			return -1
		else:
			return x_column

	def in_circle(self, point, center, radius):
		"""Checks if a point is within a circle with a given center and radius

		Parameters:
		self - GraphicInterfaceAndLocation object
		point - the point to check
		center - the center of the circle
		radius - the radius of the circle
		"""
		dx = point.getX() - center.getX()
		dy = point.getY() - center.getY()
		distance = math.sqrt((dx ** 2) + (dy ** 2))
		if distance <= radius:
			return True
		else:
			return False

	def get_piece_location(self):
		""" This function creates up to 7 'buttons' that the user can click on to choose to
		play a piece. The buttons aren't actually drawn, because the game board already has
		white circles that represent possible playing locations.
		It waits until the user clicks on one of the 'buttons' and then returns the a list
		with the x and y position in game (not graphical) coordinates
		"""
		successful_click = False
		while successful_click == False:
			click = self.win.getMouse()
			x = click.getX()
			y = click.getY()
			column = int(self.find_column(click))
			if column != -1:
				a_list = self.list_of_columns[column]
				idx_col = self.find_first_zero(a_list)
				#(column, idx_col) is the game coordinates of the button that 
				#the click was closest to
				y_coordinate = self.Y_constant + self.Y_scalar * idx_col
				center = graphics.Point(self.X_constant + self.X_scalar * column, y_coordinate)
				if self.in_circle(click, center, self.radius) == True:
					return [column, idx_col]

	def check_horizontal(self, ai_move):
		"""Checks how many pieces the current player has in a row horizontally. Returns a list
		with the form [w, x, y] where w is the number of pieces in a row, and x and y are the
		x and y position of the leftmost piece.

		Parameters:
		ai_move - if True, the function checks if the other player has four in a row horizontally
		"""
		result = [0, 0, 0]
		if ai_move == True:
			self.update()
		curr_player = self.player_turn
		in_a_row = 0
		for row in range(6):
			col_index = 0
			for col in self.list_of_columns:
				val = col[row]
				if val == curr_player:
					in_a_row += 1
					if result[0] <= in_a_row:
						result = [in_a_row, col_index - in_a_row + 1, row]
				else:
					in_a_row = 0
				col_index += 1

		if ai_move == True:
			self.update()

		return result

	def check_verticle(self, ai_move):
		"""Checks how many pieces the current player has in a row vertically. Returns a list
		with the form [w, x] where w is the number of pieces in a row and x is the column
		the pieces are in.

		Parameters:
		ai_move - if True, the function checks if the other player has four in a row vertically
		"""
		#idx is the current row, col_index is the current column
		if ai_move == True:
			self.update()
		curr_player = self.player_turn
		result = [0, 0]
		col_index = 0
		for col in self.list_of_columns:
			val = 0
			idx = -1
			while val != curr_player and idx < 5:
				idx += 1
				val = col[idx]
			in_a_row = 0
			while val == curr_player and idx < 5:
				in_a_row += 1
				idx += 1
				val = col[idx]
				if val != curr_player and idx <= 3:
					in_a_row = 0
					idx += 1
					val = col[idx]

			if idx == 5 and val == curr_player:
				in_a_row += 1

			if result[0] < in_a_row:
				result = [in_a_row, col_index]
			col_index += 1

		if ai_move == True:
			self.update()

		return result

	def check_diagonal(self, ai_move):
		"""Checks how many pieces the current player has in a row diagonally. Returns a list
		with the form [w, x, y, z] where w is the number of pieces in a row, x and y are the
		position of the leftmost piece, and z is -1 if the leftmost piece's y coordinate is lowest
		and z is 1 if the leftmost piece's y coordinate is highest.

		Parameters:
		ai_move - if True, the function checks if the other player has four in a row diagonally
		"""

		if ai_move == True:
			self.update()
		curr_player = self.player_turn
		result = [0, 0, 0, 0]
		in_a_row = 0

		for z in range(-1, 2, 2):
			for col_index in range(7):
				for row in range(6):
					col = self.list_of_columns[col_index]
					val = col[row]
					new_col_index = col_index
					new_row = row

					while val == curr_player and new_col_index < 6 and -1 < new_row - z and new_row + z <= 5:
						in_a_row += 1

						if result[0] < in_a_row and z == -1:
							result = [in_a_row, new_col_index - in_a_row + 1, new_row - in_a_row - z, z]

						elif result[0] < in_a_row and z == 1:
							result = [in_a_row, new_col_index - in_a_row + 1, new_row + in_a_row + z, z]

						new_col_index += 1
						col = self.list_of_columns[new_col_index]
						new_row += -z
						if new_row == 6:
							new_row = 0
							in_a_row = 0
						val = col[new_row]

					if val == curr_player:
						#account for if the check is going to fall off the board
						in_a_row += 1
						if result[0] < in_a_row and z == -1:
							result = [in_a_row, new_col_index - in_a_row + 1, new_row - in_a_row - z, z]

						elif result[0] < in_a_row and z == 1:
							result = [in_a_row, new_col_index - in_a_row + 1, new_row + in_a_row + z, z] 

					in_a_row = 0

		if ai_move == True:
			self.update()

		return result

	def check_if_four(self, ai_move):
		"""
		Checks if the player who moved last has created four in a row by checking if they have
		four in a row either diagonally, horizontally, or vertically. Returns True if they have,
		otherwise returns False

		Parameters:
		ai_move - set to False unless the function is being called to help the AI decide their move
		"""
		if self.check_horizontal(ai_move)[0] >= 4 or self.check_verticle(ai_move)[0] >= 4 or self.check_diagonal(ai_move)[0] >= 4:
			return True
		return False

	def human_victory(self, opponent):
		"""Creates the graphical image for human victory

		Parameters:
		self - GraphicInterfaceAndLocation object
		opponent - the opponent the human beat, either "AI" or "human"
		"""
		if opponent == "human":
			if self.player_turn == 1:
				fill_color = "Yellow"
			else:
				fill_color = "Red"

			text = "Congratulations, " + fill_color + ", You Won!"
		else:
			text = "Congratulations, You Won!"
		message = graphics.Text(self.subtitle_center, text)
		message.setSize(26)
		message.setStyle("bold")
		message.draw(self.win)
		self.win.getMouse()

	def AI_victory(self):
		"""Creates the graphical image for AI victory"""
		text = "You Lost! Better Luck Next Time!"
		message = graphics.Text(self.subtitle_center, text)
		message.setSize(26)
		message.draw(self.win)
		self.win.getMouse()

	def ask_question(self, question_text, response1_text, response2_text, color1, color2):
		"""A function that's used to streamline the process of asking the user questions
		before the game begins. Returns either 1 or 2.

		Parameters:
		self - GraphicInterfaceAndLocation object
		question_text - the text for the question to be asked
		response1_text - the text the user clicks on if they want to choose option 1
		response2_text - the text the user clicks on if they want to choose option 2
		color1 - the color of the first box
		color2 - the color of the second box
		"""
		width = 130
		height = 46

		question_center = graphics.Point(self.X_constant + 3 * self.X_scalar, 45 + self.Y_constant + 6 * self.Y_scalar)
		question = graphics.Text(question_center, question_text)
		question.setSize(22)
		question.draw(self.win)

		human_left = self.X_constant + 50
		human_low = self.Y_constant - 18 + 6 * self.Y_scalar
		AI_left = self.X_constant - 70 + 5 * self.X_scalar
		AI_low = self.Y_constant - 18 + 6 * self.Y_scalar


		p1 = graphics.Point(human_left, human_low)
		p2 = graphics.Point(human_left + width, human_low + height)
		human = graphics.Rectangle(p1, p2)
		human.setFill(color1)
		human.draw(self.win)
		
		p3 = graphics.Point(AI_left, AI_low)
		p4 = graphics.Point(AI_left + width, AI_low + height)
		AI = graphics.Rectangle(p3, p4)
		AI.setFill(color2)
		AI.draw(self.win)

		human_center = graphics.Point((human_left + width//2), (human_low + height//2))
		human_text = graphics.Text(human_center, response1_text)
		human_text.setSize(22)
		human_text.draw(self.win)

		AI_center = graphics.Point((AI_left + width//2), (AI_low + height//2))
		AI_text = graphics.Text(AI_center, response2_text)
		AI_text.setSize(22)
		AI_text.draw(self.win)

		choice = 0
		while choice == 0:
			click = self.win.getMouse()
			if human_left <= click.getX() <= (human_left + width) and human_low <= click.getY() <= (human_low + height):
					choice = 1
			if AI_left <= click.getX() <= (AI_left + width) and AI_low <= click.getY() <= (AI_low + height):
				choice = 2

		question.undraw()
		human_text.undraw()
		AI_text.undraw()
		human.undraw()
		AI.undraw()

		return choice

	def turn_info(self):
		"""Displays the current human player's color and prompts them to play a piece
		"""
		if self.player_turn == 1:
			fill_color = "Yellow"
		else:
			fill_color = "Red"
		question_text = fill_color + ", it's your turn"
		question_center = graphics.Point(self.X_constant + 3 * self.X_scalar, 25 + self.Y_constant + 6 * self.Y_scalar)
		self.question = graphics.Text(question_center, question_text)
		self.question.setSize(26)
		self.question.draw(self.win)

	def undraw_question(self):
		"""Undraws the question self.question"""

		self.question.undraw()

	def initialize_game(self):
		"""Asks the user to choose the game options. Returns a list with the game options the user choose.
		Values of the list are in the following form:
		[human vs human?, AI difficulty, add animation?, go first or second?]
		"""
		choices = [0, 0, 0, 0]
		q = self.ask_question("Would you like to play with the default settings?", "Yes", "No", "green", "red")
		if q == 2:
			q0 = self.ask_question("Would you like to play against another human or the computer?", "Human", "Computer", "orange", "purple")
			#chose to play vs human
			if q0 == 1:
				choices[0] = 1
			else:
				q1 = self.ask_question("Choose the computer's difficulty", "Easy", "Hard", "green", "yellow")
				if q1 == 2:
					choices[1] = 1
			q2 = self.ask_question("Would you like to play with animation turned on?", "Yes", "No", "purple", "brown")
			if q2 == 1:
				choices[2] = 1
			if q0 == 2:
				q3 = self.ask_question("Would you like to go first or second?", "First", "Second", "coral", "gold")
				if q3 == 2:
					choices[3] = 1

		return choices

	def computer_move(self, difficulty):
		"""Determines the AI's strategy. Returns a list in the form [x, y] in game coordinates,
		which is where the computer choose to move

		Parameters:
		difficulty - either 0 or 1, represents whether the computer is playing on hard mode or not"""
		if difficulty == 0:
			index = random.randint(0, 6)
			current_col = self.list_of_columns[index]
			if current_col[5] == 0:
				idx = self.find_first_zero(current_col)
				return [index, idx]
			else:
				#recursively call the AI until it chooses a valid move
				return self.computer_move(difficulty)
		else:
			move = self.hard_AI()
			if self.check_if_playable(move[0], move[1]) == True:
				return move
			else:
				return self.computer_move(0)

	def hard_AI(self):
		"""The function that codes for the computer's strategy if it is on hard mode"""

		#If opponent is about to connect four horizontally, block them
		horiz_test = self.check_horizontal(True)
		if horiz_test[0] >= 2:
			col = horiz_test[1]
			if col - 1 >= 0:
				y = self.find_first_zero(self.list_of_columns[col-1])
			else:
				y = -1
			if col + 3 <= 6:
				y0 = self.find_first_zero(self.list_of_columns[col+3])
			else:
				y0 = -1
			if y == y0 or horiz_test[0] == 3:
				if y == horiz_test[2] and self.check_if_playable(col-1, y) == True:
					return [col -1, y]
				elif y0 == horiz_test[2] and self.check_if_playable(col + 3, y0) == True:
					return [col + 3, y0]

		#Focus on playing in the middle of the board
		for i in range(10):
			move = self.computer_move(0)
			if 2 <= move[0] <= 4 and move[1] <= 4:
				return move

		return[-1, -1]

	def check_if_playable(self, Xpos, Ypos):
		"""Checks if a given given set of game coordinates is a valid game move.

		Parameters:
		Xpos - the x game-coordinate
		Ypos - the y game-coordinate
		"""
		if 0 <= Xpos <= 6 and 0 <= Ypos <= 5:
			col = self.list_of_columns[Xpos]
			if self.find_first_zero(col) == Ypos:
				return True
		return False

	def check_if_tie(self):
		"""Checks if the entire board is filled, thus making it a tied game"""
		for index in range (len(self.list_of_columns)):
			current_col = self.list_of_columns[index]
			if current_col[5] == 0:
				return False
		else:
			return True

	def tie_game(self):
		"""Displays the ending graphics if the game ends in a draw"""
		text = "The Board is full! Tie Game!"
		message = graphics.Text(self.subtitle_center, text)
		message.setSize(26)
		message.draw(self.win)
		self.win.getMouse()

class Connect4Game:
	"""
	A class that plays connect four when the play function is run
	"""
	def __init__ (self):
		#Constructor
		self.interface = GraphicInterfaceAndLocation()
		self.choices = self.interface.initialize_game()

		if self.choices[0] == 1:
			player1 = "human"
			player2 = "human"
		elif self.choices[3] == 0:
			player1 = "human"
			player2 = "computer"
		else:
			player1 = "computer"
			player2 = "human"
		self.list_of_players = [player1, player2]

	def play(self):
		"""
		Plays a turn of connect four while neither player has won the game
		"""
		curr_player = self.interface.get_current_player()
		check = False
		
		while check == False:
			curr_player = self.interface.get_current_player()
			color = self.interface.get_fill_color()

			if self.list_of_players[curr_player-1] == "human":
				self.interface.turn_info()
				coords = self.interface.get_piece_location()
				self.interface.undraw_question()
			else:
				difficulty = self.choices[1]
				coords = self.interface.computer_move(difficulty)

			animation = self.choices[2]
			self.interface.draw_piece(color, coords[0], coords[1], animation)
			check = self.interface.check_if_four(False)

			if check == True:
				self.end_game(False)
			tie = self.interface.check_if_tie()
			if tie == True:
				self.end_game(True)
				check = False
			else:
				self.interface.update()

	def end_game(self, tie):
		"""The function that gets called when somebody has connected four"""
		if tie == False:
			curr_player = self.interface.get_current_player()
			if self.list_of_players[curr_player - 1] == "human":

				#human vs human game
				if self.list_of_players[0] == self.list_of_players[1]:
					self.interface.human_victory("human")
				#human vs AI game
				else:
					self.interface.human_victory("AI")
			#AI won
			else:
				self.interface.AI_victory()
		else:
			self.interface.tie_game()

def main():
	"""The main function. Calling this function will allow the user to play a game of connect four"""
	game = Connect4Game()
	game.play()

if __name__ == '__main__':
	main()