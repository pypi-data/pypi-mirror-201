class Calculator: 
    
    def __init__(self, starting_number =0):
        self.memory = starting_number

    def add(self, second_number):
        result = self.memory + second_number
        self.memory = result
        return result

    def subtract(self, second_number):
        result = self.memory - second_number
        self.memory = result
        return result

    def multiply(self, second_number):
        result = self.memory * second_number
        self.memory = result
        return result

    def divide(self, second_number):
        if second_number == 0:
            raise ValueError("Cannot divide by zero")
        result = self.memory / second_number
        self.memory = result
        return result
    
    def nth_root(self, second_number):
        if self.memory < 0 and second_number % 2 == 0:
            raise ValueError("Cannot take an even-number root of a negative number")
        elif second_number == 0:
            raise ValueError(" 0 root of any number doesn't exist")
        result = self.memory ** (1 / second_number)
        self.memory = result
        return result

    def recall_memory(self):
        return self.memory

    def clear_memory(self):
        self.memory = 0
