import re

class CheckerRegistry:
    def __init__(self):
        self.checkers = []

    def register(self, pattern, checker_class):
        self.checkers.append((re.compile(pattern), checker_class))

    def get_checker(self, quota_name):
        for pattern, checker_class in self.checkers:
            match = pattern.match(quota_name)
            if match:
                return checker_class()
