import random
import numpy as np

import Exceptions


class SampleSelector:
    """
    The class responsible for randomly selecting three samples.

    A surprisingly complex problem, due to the requirement of selecting the samples randomly.
    A depth-first-search approach is used where at each decision vertex the list of next steps is randomized.

    This ensures that the program is guaranteed to return a solution if one is possible, while also not running
    infinitely. The solution is not very fast due to preserving as close to true randomness as possible.
    """

    def __init__(self, image_width: int, image_height: int, sample_width: int, sample_height: int):
        self.grid = np.zeros((image_width, image_height), dtype=int)
        self.sample_width = sample_width
        self.sample_height = sample_height

    def _get_free_positions(self) -> list[tuple[int, int]]:
        free_positions = []
        for x in range(self.grid.shape[0] - self.sample_width + 1):
            for y in range(self.grid.shape[1] - self.sample_height + 1):
                if self._is_position_free((x, y)):
                    free_positions.append((x, y))
        return free_positions

    def _is_position_free(self, sample_position: tuple[int, int]) -> bool:
        x, y = sample_position
        return np.all(self.grid[x:x + self.sample_width, y:y + self.sample_height] == 0)

    def _reserve_rectangle_for_sample(self, sample_position: tuple[int, int]) -> None:
        for x in range(sample_position[0], sample_position[0] + self.sample_width):
            for y in range(sample_position[1], sample_position[1] + self.sample_height):
                self.grid[x, y] = 1

    def _free_rectangle_for_selection(self, sample_position: tuple[int, int]) -> None:
        for x in range(sample_position[0], sample_position[0] + self.sample_width):
            for y in range(sample_position[1], sample_position[1] + self.sample_height):
                self.grid[x, y] = 0

    def _depth_first_search(self, samples: list[tuple[int, int]], number_of_samples=3) -> bool:
        if len(samples) == number_of_samples:
            return True

        free_positions = self._get_free_positions()
        if len(free_positions) == 0:
            return False
        random.shuffle(free_positions)

        for position in free_positions:
            self._reserve_rectangle_for_sample(position)
            samples.append(position)
            if self._depth_first_search(samples, number_of_samples):
                return True
            del samples[-1]
            self._free_rectangle_for_selection(position)
        return False

    def _handle_edge_cases(self) -> None:
        if self.sample_width <= 0 or self.sample_height <= 0:
            raise Exceptions.InvalidSampleDimensions
        if self.sample_width > self.grid.shape[0]:
            raise Exceptions.SampleWidthExceedsImageWidth
        if self.sample_height > self.grid.shape[1]:
            raise Exceptions.SampleHeightExceedsImageHeight
        if self.sample_height * self.sample_width > self.grid.shape[0] * self.grid.shape[1]:
            raise Exceptions.SampleAreaExceedsImageArea

    def generate_random_samples(self, number_of_samples: int = 3) -> list[tuple[int, int]]:
        self._handle_edge_cases()
        samples = []
        if self._depth_first_search(samples, number_of_samples):
            return samples
        raise Exceptions.NoFreePositionError
