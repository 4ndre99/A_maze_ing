import random
from collections import deque

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

ALL_WALLS = NORTH | EAST | SOUTH | WEST
#north (0, -1)
#east (1, 0)
#south (0, 1)
#west (-1, 0)
class MazeGen:

	def __init__(self, width: int, height: int, seed: int) -> None:

		if width <= 0 or height <= 0:
			raise ValueError("Width and Height must be positive values!")
		
		self.width = width
		self.height = height
		self.seed = seed

		self.maze = [
			[ALL_WALLS for _ in range(self.width)] 
			for _ in range(self.height)
			]

		self.visited = [
			[False for _ in range(self.width)] 
			for _ in range(self.height)
			]

	def open_path(self, y: int, x: int, direction: int) -> None:
		if direction not in (NORTH, EAST, SOUTH, WEST):
			print("invalid dir")
			return
		if (x < 0 or x >= self.width or y < 0 or y >= self.height
			or (x == 0 and direction == WEST)
		    or (x == self.width - 1 and direction == EAST)
			or (y == 0 and direction == NORTH)
		    or (y == self.height - 1 and direction == SOUTH)):
			print("cant do dat")
			return
		match direction:
			case 1:
				self.maze[y][x] &= ~NORTH
				self.maze[y - 1][x] &= ~SOUTH
			case 2:
				self.maze[y][x] &= ~EAST
				self.maze[y][x + 1] &= ~WEST
			case 4:
				self.maze[y][x] &= ~SOUTH
				self.maze[y + 1][x] &= ~NORTH
			case 8:
				self.maze[y][x] &= ~WEST
				self.maze[y][x - 1] &= ~EAST

	def get_valid_neighbors(self, y: int, x: int) -> list[tuple]:
		result = [(y - 1, x, NORTH), (y, x + 1, EAST), 
		          (y + 1, x, SOUTH), (y, x - 1, WEST)]
		
		return [
        	(ny, nx, direction)
        	for ny, nx, direction in result
        	if 0 <= ny < self.height
        	and 0 <= nx < self.width
        	and not self.visited[ny][nx]
    		]

	def generate(self) -> None:

		random.seed(self.seed)
		start = (random.randint(0, self.height - 1), random.randint(0, self.width - 1))
		print(f"start({start[0]}, {start[1]})")

		stack = [start]
		self.visited[start[0]][start[1]] = True

		while stack:
			pos = stack[len(stack) - 1]
			posy = pos[0]
			posx = pos[1]
			neighbors = self.get_valid_neighbors(posy, posx)

			if neighbors:
				print("neighbors :", neighbors)
				next = random.choice(neighbors)
				print("next :", next)
				self.visited[next[0]][next[1]] = True
				self.open_path(posy, posx, next[2])
				self.show_grid()
				self.show_visited()
				print("--------------------")
				stack.append((next[0], next[1]))
			else:
				stack.pop()

	def give_next_cells(self, y: int, x: int) -> list[tuple]:
		result = []
		if not self.maze[y][x] & NORTH:
			result.append((y - 1, x))
		if not self.maze[y][x] & EAST:
			result.append((y , x + 1))
		if not self.maze[y][x] & SOUTH:
			result.append((y + 1, x))
		if not self.maze[y][x] & WEST:
			result.append((y, x - 1))

		return result

	@staticmethod
	def get_code(solution: list[tuple]) -> str:
		directions = []
		for i in range(len(solution) - 1):
			y1, x1 = solution[i]
			y2, x2 = solution[i + 1]

			y = y2 - y1
			x = x2 - x1

			if y == -1:
				directions.append('N')
			elif y == 1:
				directions.append('S')
			elif x == -1:
				directions.append('W')
			else:
				directions.append('E')

		return "".join(directions)

	def maze_solver(self, entry: tuple, exit: tuple) -> str:
		beenThere = [
			[False for _ in range(self.width)] 
			for _ in range(self.height)
			]

		queue = deque([entry])
		beenThere[entry[0]][entry[1]] = True

		parent = {}

		while queue and not beenThere[exit[0]][exit[1]]:
			print(queue)
			pos = queue.popleft()
			new = self.give_next_cells(pos[0], pos[1])
			
			print("vizinhos:", new)
			if new:
				for i in new:
					if not beenThere[i[0]][i[1]]:
						beenThere[i[0]][i[1]] = True
						parent[(i[0], i[1])] = (pos[0], pos[1])
						queue.append(i)

		print("dicionario:", parent)

		path = []
		current = exit

		while current != entry:
			path.append(current)
			current = parent[current]

		path.append(entry)
		path.reverse()

		code = self.get_code(path)
		return code

	def show_grid(self) -> None:
		for i in self.maze:
			print(i)

	def show_visited(self) -> None:
		for i in self.visited:
			print(i)

	def get_grid(self) -> list[list[int]]:
		return self.maze

if __name__ == "__main__":
	new = MazeGen(4, 4, 12)
	new.show_grid()
	print("----------")
	new.show_visited()
	print("--/n--")
	new.generate()
	new.show_grid()
	print("----------")
	new.show_visited()
	print(new.maze_solver((0,0), (3, 3)))