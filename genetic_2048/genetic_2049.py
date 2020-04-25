from random import shuffle, uniform, randint
import game_control as game
import numpy as np
import math
import json
import time


class Genetic2048:
    def __init__(self, move_limit=100, mutation_rate=0.015, mutation_step=1, num_generations=1000, population_size=10, save_arch="archive.json"):
        self.start_time = time.time()
        self.grid = self.get_grid()
        self.mutation_rate = mutation_rate
        self.num_generations = num_generations
        self.population_size = population_size
        self.move_limit = move_limit
        self.mutation_step = mutation_step
        self.save_arch = save_arch
        self.elapsed_time = ""
        self.archive = {
            "population_size": population_size,
            "generation": 0,
            "elites": [],
            "population": [],
            "best_score": 0,
            "largest_tile": 0,
            "elapsed_time": ""
        }
        self.move_algorithm = {}
        self.score = 0
        self.moves_taken = 0
        self.current_genome = -1
        self.generation = 0

    def get_grid(self):
        self.grid = game.getGrid()
        return self.grid

    def update_score(self, move):
        new_score = int(move["algorithm"]["points_earned"])
        self.score += new_score

    def print_status(self, move):
        self.elapsed_time = str(self.format_time(
            time.time() - self.start_time))
        print(" ========================================")
        print(" Generation: ", self.generation, "/", self.num_generations)
        print(" Genome: ", self.current_genome, "/", self.population_size)
        print(" Move: ", self.moves_taken, "/", self.move_limit)
        print(" Elapsed time: ", self.elapsed_time)
        print(" Current genome: ")
        self.pretty_print(self.population[self.current_genome])
        print(" ========================================")
        print(" ========================================")
        print(" Next move:", "\n")
        self.pretty_print(move)
        print(" Current score: ", self.score)
        print(" Best score: ", self.archive["best_score"])
        print(" Largest tile: ", self.archive["largest_tile"])
        print(" ========================================")

    def evolve(self):
        self.current_genome = 0
        self.generation += 1
        self.population = sorted(
            self.population, key=lambda genome: genome["fitness"], reverse=True)
        elite = dict(self.population[0])
        self.archive["elites"].append(elite)
        while len(self.population) > self.population_size/2:
            self.population.pop()

        children = [elite]
        while len(children) < self.population_size:
            parent1 = self.select_candidate()
            parent2 = self.select_candidate()
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            children.append(child)

        self.population = children
        self.archive["population"] = list(children)
        self.archive["generation"] = self.generation
        self.archive["elapsed_time"] = self.elapsed_time
        self.save_archive(self.save_arch)

    def create_genome(self):
        genome = {
            "id": uniform(0, 1),
            "eccentricity": uniform(-1, 1),
            "avg_dist_between_largest": uniform(-1, 1),
            "holes": uniform(-1, 1),
            "spaces_cleared": uniform(-1, 1),
            "points_earned": uniform(-1, 1),
        }
        return genome

    def run(self, file_name=None):
        if not file_name:
            self.create_initial_population()
        else:
            self.load_archive(file_name)
            if len(self.population) == 0:
                self.population_size = 10
                self.create_initial_population()
            else:
                self.evaluate_next_genome()
        while self.generation < self.num_generations:
            self.update()

    def create_initial_population(self):
        population = []
        for _ in range(self.population_size):
            new_genome = self.create_genome()
            population.append(new_genome)
        self.population = population
        self.evaluate_next_genome()

    def update_largest_tile(self, grid):
        currentLargestTile = int(self.archive["largest_tile"])
        newLargestTile = np.amax(grid)
        if newLargestTile > currentLargestTile:
            self.archive["largest_tile"] = str(newLargestTile)

    def evaluate_next_genome(self):
        self.current_genome += 1
        if self.current_genome == len(self.population):
            self.evolve()
        self.archive["best_score"] = game.getBestScore()
        game.restart_game()
        self.score = 0
        self.moves_taken = 0
        self.make_next_move()

    def make_next_move(self):
        self.moves_taken += 1
        if self.moves_taken > self.move_limit:
            self.population[self.current_genome]["fitness"] = self.score
            self.evaluate_next_genome()
        else:
            self.get_grid()
            possible_moves = self.get_all_possible_moves()
            for m in range(len(possible_moves)):
                next_move = self.get_highest_rated_move(possible_moves)
                possible_moves[m]["rating"] += next_move["rating"]

            if len(possible_moves) == 0:
                self.population[self.current_genome]["fitness"] = self.score
                self.evaluate_next_genome()
                return
            move = self.get_highest_rated_move(possible_moves)
            move_to_perform = game.moves_map(move["move"])
            game.performMove(move_to_perform)
            self.update_score(move)
            self.print_status(move)

    def update(self):
        if self.current_genome != -1:
            current_grid = self.get_grid()
            self.update_largest_tile(current_grid)

            if self.check_if_lost(current_grid):
                self.population[self.current_genome]["fitness"] = self.score
                self.evaluate_next_genome()
            else:
                self.make_next_move()

    def get_all_possible_moves(self):
        current_genome = self.population[self.current_genome]
        possible_moves = []
        moves = [i for i in range(4)]
        move_funcs = [self.slide_up, self.slide_down,
                      self.slide_left, self.slide_right]
        current_grid = self.grid
        for m in range(len(moves)):
            (new_grid, points_earned,
             new_holes) = move_funcs[moves[m]](current_grid)
            if new_grid == current_grid:
                continue
            algorithm = {
                "eccentricity": self.eccentricity(new_grid),
                "avg_dist_between_largest": self.avg_dist_between_largest(new_grid),
                "holes": self.count_holes(new_grid),
                "spaces_cleared": new_holes,
                "points_earned": points_earned
            }
            rating = 0

            rating += current_genome["eccentricity"] * \
                algorithm["eccentricity"]
            rating += current_genome["avg_dist_between_largest"] * \
                algorithm["avg_dist_between_largest"]
            rating += current_genome["holes"] * algorithm["holes"]
            rating += current_genome["spaces_cleared"] * \
                algorithm["spaces_cleared"]
            rating += current_genome["points_earned"] * \
                algorithm["points_earned"]

            if self.check_if_lost(new_grid):
                rating -= 500

            possible_moves.append(
                {"move": moves[m], "rating": rating, "algorithm": algorithm})
        return possible_moves

    def get_highest_rated_move(self, moves):
        max_move = 0
        max_rating = 0
        for m in range(len(moves)):
            if moves[m]["rating"] > max_rating:
                max_rating = moves[m]["rating"]
                max_move = m
        return moves[max_move]

    def mutate(self, genome):
        new_genome = dict(genome)
        for key in genome:
            if uniform(0, 1) < self.mutation_rate:
                new_genome[key] += (self.mutation_step * uniform(-1, 1))
        return new_genome

    def crossover(self, genome1, genome2):
        new_genome = {"id": uniform(0, 1)}
        for key in genome1:
            if key == "fitness":
                new_genome[key] = -1
                continue
            if key != "id":
                if uniform(0, 1) >= 0.5:
                    new_genome[key] = genome1[key]
                else:
                    new_genome[key] = genome2[key]

        return new_genome

    def select_candidate(self):
        rand_index = randint(0, len(self.population) - 1)
        candidate = self.population[rand_index]
        return candidate

    def mirror_mat(self, matrix):
        grid = [row[:] for row in matrix]
        n = len(grid)
        m = len(grid[0])
        m2 = round(m/2)
        for i in range(n):
            for j in range(m2):
                temp = grid[i][j]
                grid[i][j] = grid[i][m-j-1]
                grid[i][m-j-1] = temp
        return grid

    def transpose_mat(self, matrix):
        grid = [row[:] for row in matrix]
        grid = [list(tup) for tup in zip(*grid)]
        return grid

    def print_mat(self, grid, padding=2):
        n = len(grid)
        m = len(grid[0])
        pad = ""
        for i in range(padding):
            pad += " "
        for i in range(n):
            row = ""
            for j in range(m):
                row += str(grid[i][j]) + pad
            print(row)
        print("")

    def slide_left(self, matrix):
        grid = [row[:] for row in matrix]
        n = len(grid)
        score = 0
        cleared = 0
        for i in range(n):
            line = grid[i]
            removed = 0
            j = 0
            while j < len(line)-1:
                if line[j] == 0:
                    line.pop(j)
                    removed += 1
                elif line[j] == line[j+1]:
                    line.pop(j)
                    line[j] *= 2
                    removed += 1
                    score += line[j]
                    cleared += 1
                elif j + 1 < len(line) and line[j+1] == 0:
                    line.pop(j+1)
                    removed += 1
                else:
                    j += 1
            for _ in range(removed):
                line.append(0)
            grid[i] = line
        return (grid, score, cleared)

    def slide_right(self, matrix):
        grid = [row[:] for row in matrix]
        grid = self.mirror_mat(grid)
        (grid, score, cleared) = self.slide_left(grid)
        grid = self.mirror_mat(grid)
        return (grid, score, cleared)

    def slide_up(self, matrix):
        grid = self.transpose_mat(matrix)
        (grid, score, cleared) = self.slide_left(grid)
        grid = self.transpose_mat(grid)
        return (grid, score, cleared)

    def slide_down(self, matrix):
        grid = self.transpose_mat(matrix)
        (grid, score, cleared) = self.slide_right(grid)
        grid = self.transpose_mat(grid)
        return (grid, score, cleared)

    def count_holes(self, matrix):
        holes = 0
        for i in range(len(matrix)):
            holes += matrix[i].count(0)
        return holes

    def check_if_lost(self, matrix):
        if matrix == self.slide_left(matrix)[0] and matrix == self.slide_right(matrix)[0] and matrix == self.slide_down(matrix)[0] and matrix == self.slide_up(matrix)[0]:
            return True
        return False

    def eccentricity(self, matrix, num_sigma=1):
        n = len(matrix)
        m = len(matrix[0])
        grid = np.array(matrix)
        miu = grid.mean()
        sigma = grid.std()
        threshold = round(miu + num_sigma * sigma)
        threshold = 2 ** round(math.log(threshold, 2))
        relevant = np.argwhere(grid >= threshold)
        corners = [[0, 0], [0, m-1], [n-1, 0], [n-1, m-1]]
        score = 0
        for r in range(len(relevant)):
            dists = []
            for c in range(len(corners)):
                a = relevant[r]
                b = corners[c]
                dists.append(np.linalg.norm(a-b))
            min_distance = min(dists)
            score += min_distance
        return score

    def avg_dist_between_largest(self, matrix, num_sigma=1):
        grid = np.array(matrix)
        miu = grid[np.nonzero(grid)].mean()
        sigma = grid[np.nonzero(grid)].std()
        threshold = round(miu + num_sigma * sigma)
        threshold = 2 ** round(math.log(threshold, 2))
        relevant = np.argwhere(grid >= threshold)
        distances = []
        done = []
        for r0 in range(len(relevant)):
            for r1 in range(len(relevant)):
                if [r0, r1] not in done and [r1, r0] not in done:
                    distances.append(np.linalg.norm(relevant[r0]-relevant[r1]))
                    done.append([[r0, r1]])
        if(len(distances) == 0):
            return 0
        avg_dist = sum(distances)/len(distances)
        return avg_dist

    def format_time(self, seconds):
        days = seconds//86400
        hours = (seconds - days*86400)//3600
        minutes = (seconds - days*86400 - hours*3600)//60
        seconds = seconds - days*86400 - hours*3600 - minutes*60
        days = self.two_digits(days)
        hours = self.two_digits(hours)
        minutes = self.two_digits(minutes)
        seconds = self.two_digits(seconds)
        text = "%s:%s:%s:%s" % (days, hours, minutes, seconds)
        return text

    def two_digits(self, number):
        number = int(number)
        if number < 10:
            return "0"+str(number)
        return str(number)

    def pretty_print(self, data):
        print(json.dumps(data, sort_keys=False, indent=4))

    def save_archive(self, file_name="archive.json"):
        data = self.archive
        with open(file_name, 'w') as fp:
            json.dump(data, fp, sort_keys=False, indent=4)

    def load_archive(self, file_name):
        with open(file_name, 'r') as fp:
            data = json.load(fp)
            self.archive = {
                "population_size": 0,
                "generation": 0,
                "elites": [],
                "population": [],
                "best_score": 0,
                "largest_tile": 0,
                "elapsed_time": ""
            }
        self.archive = data
        self.population = data["population"]
        self.population_size = data["population_size"]
        self.generation = 0 # data["generation"]
        self.best_score = data["best_score"]
        self.largest_tile = data["largest_tile"]
        self.elapsed_time = data["elapsed_time"]


def learn(i=0):
    file_name = "hist_"+str(i) + ".json"
    g = Genetic2048(move_limit=100000, mutation_rate=0.6, mutation_step=0.3, num_generations=300, population_size=5, save_arch=file_name)
    g.run(file_name="./history/history2.json")


def keep_running(retries=0):
    if retries > 100:
        return
    try:
        learn()
    except:
        retries += 1
        keep_running(retries)


if __name__ == "__main__":
    learn(1)
