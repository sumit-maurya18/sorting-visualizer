import pygame
import random
import math

pygame.init()


class DrawInformation:
	# Commonly used colors
	BLACK = 0, 0, 0
	WHITE = 255, 255, 255
	GREEN = 0, 255, 0
	RED = 255, 0, 0

	# Background color of the window
	BACKGROUND_COLOR = WHITE

	# Gradient colors for alternate bars
	GRADIENTS = [
		(128, 128, 128),
		(160, 160, 160),
		(192, 192, 192)
	]

	# Fonts adn style for texts
	FONT = pygame.font.SysFont('comicsans', 30)
	LARGE_FONT = pygame.font.SysFont('comicsans', 40)

	# Padding values
	SIDE_PAD = 100
	TOP_PAD = 150

	def __init__(self, width, height, lst):

		#Initializes the window and sets initial configs
		#width: Width of illustration window
		#height: Height of illustration window
		#lst: List of numbers

		self.width = width
		self.height = height

		# Create new window
		self.window = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Sorting Algorithm Visualization")

		self.set_list(lst)

	def set_list(self, lst):
		"""
		Setting new list to visualize
		Resetting on changes
		"""
		self.lst = lst
		self.min_val = min(lst)
		self.max_val = max(lst)

		# Width of bar
		self.block_width = round((self.width - self.SIDE_PAD) / len(lst))

		# HHeight scaling factor for bars
		self.block_height = math.floor(
			(self.height - self.TOP_PAD) / (self.max_val - self.min_val)
		)

		# Starting x-position
		self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
	"""
	Draws the complete frame:
	- Background
	- Title
	- Controls
	- Current list visualization
	"""
	draw_info.window.fill(draw_info.BACKGROUND_COLOR)

	# sorting algorithm name and order
	title = draw_info.LARGE_FONT.render(
		f"{algo_name} - {'Ascending' if ascending else 'Descending'}",
		1,
		draw_info.GREEN
	)
	draw_info.window.blit(
		title,
		(draw_info.width / 2 - title.get_width() / 2, 5)
	)

	# ontrol instructions
	controls = draw_info.FONT.render(
		"R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending",
		1,
		draw_info.BLACK
	)
	draw_info.window.blit(
		controls,
		(draw_info.width / 2 - controls.get_width() / 2, 45)
	)

	# selection info
	sorting = draw_info.FONT.render(
		"I - Insertion Sort | B - Bubble Sort",
		1,
		draw_info.BLACK
	)
	draw_info.window.blit(
		sorting,
		(draw_info.width / 2 - sorting.get_width() / 2, 75)
	)

	# Draw bars
	draw_list(draw_info)

	pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
	"""
	Draws the list as vertical bars.
	Optionally highlights specific indices using color_positions.
	"""
	lst = draw_info.lst

	# Clear only the bar area during updates
	if clear_bg:
		clear_rect = (
			draw_info.SIDE_PAD // 2,
			draw_info.TOP_PAD,
			draw_info.width - draw_info.SIDE_PAD,
			draw_info.height - draw_info.TOP_PAD
		)
		pygame.draw.rect(
			draw_info.window,
			draw_info.BACKGROUND_COLOR,
			clear_rect
		)

	for i, val in enumerate(lst):
		# Calculate bar position
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

		# Colour using gradients
		color = draw_info.GRADIENTS[i % 3]

		if i in color_positions:
			color = color_positions[i]

		# Draw the bar
		pygame.draw.rect(
			draw_info.window,
			color,
			(x, y, draw_info.block_width, draw_info.height)
		)

	if clear_bg:
		pygame.display.update()


def generate_starting_list(n, min_val, max_val):

	#Generates a list of random integers.

	lst = []

	for _ in range(n):
		val = random.randint(min_val, max_val)
		lst.append(val)

	return lst


def bubble_sort(draw_info, ascending=True):
	# Bubble sort implementation using generator
	lst = draw_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]

				# hghlight swapped elements
				draw_list(
					draw_info,
					{j: draw_info.GREEN, j + 1: draw_info.RED},
					True
				)
				yield True

	return lst


def insertion_sort(draw_info, ascending=True):
	
	#Insertion Sort implementation using a generator
	lst = draw_info.lst

	for i in range(1, len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			lst[i] = lst[i - 1]
			i -= 1
			lst[i] = current

			# Visualize movement
			draw_list(
				draw_info,
				{i - 1: draw_info.GREEN, i: draw_info.RED},
				True
			)
			yield True

	return lst


def main():
	
	#Main driver function.

	run = True
	clock = pygame.time.Clock()

	# List configuration
	n = 40
	min_val = 0
	max_val = 100

	# Initial setup
	lst = generate_starting_list(n, min_val, max_val)
	draw_info = DrawInformation(1050, 650, lst)

	sorting = False
	ascending = True

	sorting_algorithm = bubble_sort
	sorting_algo_name = "Bubble Sort"
	sorting_algorithm_generator = None

	while run:
		clock.tick(5)  # animation speed

		if sorting:
			try:
				next(sorting_algorithm_generator)
			except StopIteration:
				sorting = False
		else:
			draw(draw_info, sorting_algo_name, ascending)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type != pygame.KEYDOWN:
				continue

			# kkey bindings
			if event.key == pygame.K_r:
				lst = generate_starting_list(n, min_val, max_val)
				draw_info.set_list(lst)
				sorting = False

			elif event.key == pygame.K_SPACE and not sorting:
				sorting = True
				sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)

			elif event.key == pygame.K_a and not sorting:
				ascending = True

			elif event.key == pygame.K_d and not sorting:
				ascending = False

			elif event.key == pygame.K_i and not sorting:
				sorting_algorithm = insertion_sort
				sorting_algo_name = "Insertion Sort"

			elif event.key == pygame.K_b and not sorting:
				sorting_algorithm = bubble_sort
				sorting_algo_name = "Bubble Sort"

	pygame.quit()


if __name__ == "__main__":
	main()
