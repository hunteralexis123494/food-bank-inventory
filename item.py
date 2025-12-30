class Item:
    def __init__(self, name, container, food_group, weight, quantity):
        self.name = name.lower()
        self.container = container.lower()
        self.food_group = food_group.lower()
        self.weight = weight.lower()
        self.quantity = int(quantity)