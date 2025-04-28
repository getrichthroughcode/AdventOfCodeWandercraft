"""
File contains an implementation of solutions to the problems
given by https://adventofcode.com/2024
Author : Abdoulaye Diallo <abdoulayediallo338@gmail.com>
"""

# === Import Necessary libraries ===

import re
from collections import Counter

import numpy as np

# === solution of problems ===


class Solution:
    def __init__(self) -> None:
        print("<=== Solver Initialized ===>")
        self.helper = helperFunctions()

    def dayOnePartOne(self, leftList: list, rightList: list) -> int:
        """
        Day one puzzle solution.
        Parameters:
        -----------
        leftList (list):
            as defined in the problem

        rightList (list):
            as defined in the problem

        Returns:
        --------
        distance (int):
            based on the distance definition given in the problem.
        """
        leftList.sort()  # inplace sorting (Timsort) - O(n*log n) time complexity
        rightList.sort()  # inplace sorting (Timsort) - O(n*log n) time complexity
        leftArray = np.array(leftList)
        rightArray = np.array(rightList)

        distance = np.sum(np.abs(leftArray - rightArray))
        return distance

    def dayOnePartTwo(self, leftList: list, rightList: list) -> int:
        """
        day Two puzzle solution.
        Computes similarity score.
        Parameters:
        -----------
        leftList (list):
            as defined in the problem

        rightList (list):
            as defined in the problem

        Returns:
        --------
        similarityScore (int):
            based on the algorithm given in the problem.
        """
        tmp = Counter(rightList)
        tmp2 = {num: tmp[num] for num in leftList}
        tmpCoeff = Counter(leftList)
        similarityScore = 0
        for i, value in tmp2.items():
            similarityScore = similarityScore + tmpCoeff[i] * i * value
        return similarityScore

    def dayTwoPartOne(self, reportsPath: str) -> int:
        count = 0
        with open(reportsPath, "r") as f:
            for line in f:
                numbers = re.findall(r"\d+", line)
                numbers = [int(num) for num in numbers]
                if numbers == []:
                    continue
                print(numbers)
                aux = self.helper.isSafe(numbers)
                print(aux)
                print("===============================")
                if aux == True:
                    count += 1
        return count

    def dayTwoPartTwo(self, reportPaths: str) -> int:
        count = 0
        with open(reportPaths, "r") as f:
            for line in f:
                numbers = re.findall(r"\d+", line)
                numbers = [int(num) for num in numbers]
                if numbers == []:
                    continue
                print(numbers)
                aux = self.helper.isSafe(numbers)
                print(aux)
                print("===============================")
                if aux == True:
                    count += 1
                else:
                    if self.helper.canBecomeSafe(numbers):
                        count += 1
        return count

    def dayThreePartOne(self, corruptedFilePath: str) -> int:
        total = 0
        pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
        with open(corruptedFilePath, "r") as f:
            data = f.read()
        matches = pattern.findall(data)
        for x, y in matches:
            total += int(x) * int(y)

        return total

    def dayThreePartTwo(self, corruptedFilePath: str) -> int:
        total = 0
        mul_pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
        do_pattern = re.compile(r"do\(\)")
        dont_pattern = re.compile(r"don't\(\)")

        with open(corruptedFilePath, "r") as f:
            data = f.read()
        events = []

        for match in mul_pattern.finditer(data):
            events.append(("mul", match.start(), match.end(), match.groups()))

        for match in do_pattern.finditer(data):
            events.append(("do", match.start(), match.end(), None))

        for match in dont_pattern.finditer(data):
            events.append(("dont", match.start(), match.end(), None))

        events.sort(key=lambda x: x[1])

        enabled = True

        for event_type, start, end, groups in events:
            if event_type == "do":
                enabled = True
            elif event_type == "dont":
                enabled = False
            elif event_type == "mul" and enabled:
                x, y = groups
                total += int(x) * int(y)

        return total

    def dayFourPartOne(self, hugeInputPath: str) -> int:
        count = 0
        grid = []
        with open(hugeInputPath, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    grid.append(line)
        rows = len(grid)
        cols = len(grid[0])
        target = "XMAS"
        target_len = 4
        directions = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (-1, -1),
            (1, -1),
            (-1, 1),
        ]
        for y in range(rows):
            for x in range(cols):
                for dx, dy in directions:
                    found = True
                    for k in range(target_len):
                        nx = x + dx * k
                        ny = y + dy * k

                        if nx < 0 or ny < 0 or nx >= cols or ny >= rows:
                            found = False
                            break
                        if grid[ny][nx] != target[k]:
                            found = False
                            break
                    if found:
                        count += 1

        return count

    def dayFourPartTwo(self, HugeInputPath: str) -> int:
        count = 0
        grid = []
        with open(HugeInputPath, "r") as F:
            for line in F:
                line = line.strip()
                if line:
                    grid.append(line)

        rows = len(grid)
        cols = len(grid[0])

        for Y in range(1, rows - 1):
            for X in range(1, cols - 1):
                if grid[Y][X] != "A":
                    continue

                TL = grid[Y - 1][X - 1]
                BR = grid[Y + 1][X + 1]
                TR = grid[Y - 1][X + 1]
                BL = grid[Y + 1][X - 1]

                Diag1Ok = (TL == "M" and BR == "S") or (TL == "S" and BR == "M")
                Diag2Ok = (TR == "M" and BL == "S") or (TR == "S" and BL == "M")

                if Diag1Ok and Diag2Ok:
                    count += 1

        return count


class helperFunctions:
    def __init__(self):
        print("<=== Helper Functions Initialized ===>")

    def isSafe(self, report: list) -> bool:
        is_increasing = all(report[i] < report[i + 1] for i in range(len(report) - 1))
        is_decreasing = all(report[i] > report[i + 1] for i in range(len(report) - 1))

        if not (is_increasing or is_decreasing):
            return False

        return all(
            1 <= abs(report[i] - report[i + 1]) <= 3 for i in range(len(report) - 1)
        )

    def canBecomeSafe(self, report: list) -> bool:
        for i in range(len(report)):
            dummyReport = report[:i] + report[i + 1 :]  # remove the element at index i
            if self.isSafe(dummyReport):
                return True
        return False


if __name__ == "__main__":
    print("=== Solving problems ===")
    solver = Solution()
    input = "input/dayfour.txt"
    dot = solver.dayFourPartTwo(input)
    print(dot)
