class Inventory:
    def __init__(self):
        # Inventory will be a list of items
        self.items = []
    
    # Add an item to the inventory
    def add_item(self, item, owner):
        item.pick_up(owner)  # Change ownership to the player/owner
        self.items.append(item)
        print(f"{item.name} has been added to the inventory.")
    
    # Remove an item from the inventory
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            item.throw_away()  # Remove ownership when item is removed
            print(f"{item.name} has been removed from the inventory.")
        else:
            print(f"{item.name} is not in the inventory.")
    
    # Display all items in the inventory
    def display_items(self):
        if not self.items:
            print("Inventory is empty.")
        else:
            print("Inventory contains:")
            for item in self.items:
                print(item)  # This will use the __str__ method of each item
    
    # Check if an item is in the inventory
    def __contains__(self, item):
        return item in self.items
    
    # Make the inventory iterable
    def __iter__(self):
        return iter(self.items)

class Item:
    def __init__(self, name, description="", rarity="common", ownership=""):
        self.name = name
        self.description = description
        self.rarity = rarity
        self._ownership = ownership

    def pick_up(self, character: str):
        self._ownership = character
        return print(f"{self.name} is now owned by {character}")
    
    def throw_away(self):
        self._ownership = ""
        return print(f"{self.name} has been thrown away")
    
    def use(self):
        if self._ownership:
            return print(f"{self.name} is used by {self._ownership}")
        else:
            return print(f"{self.name} is not owned by anyone")
        
    def __str__(self):
        if self.rarity == "legendary":
            return f"*** LEGENDARY ITEM ***\nName: {self.name}\nDescription: {self.description}\nRarity: {self.rarity}\nOwnership: {self._ownership or 'No owner'}\n"
        else:
            return f"{self.name} (Rarity: {self.rarity}, Owned by: {self._ownership or 'No one'})"
    
    def get_ownership(self):
        return self._ownership
    
    def set_ownership(self, new_owner):
        self._ownership = new_owner

class Weapon(Item):
    def __init__(self, name, description="", rarity="common", damage=0, weapon_type=""):
        super().__init__(name, description, rarity)
        self.weapon_type = weapon_type
        self.damage = damage
        self.active = False
    
    def equip(self):
        self.active = True
        return print(f"{self.name} has been equipped")
    
    def use(self):
        if self._ownership and self.active:
            attack_modifier = 1.0
            if self.rarity == "legendary":
                attack_modifier = 1.15
            total_damage = self.damage * attack_modifier
            return print(f"{self.name} is used, dealing {total_damage} damage.")
        elif not self._ownership:
            return print(f"{self.name} cannot be used because it has no owner.")
        else:
            return print(f"{self.name} is not equipped.")
    
    def attack_move(self):
        raise NotImplementedError("This method should be overridden by specific weapon types.")

class SingleHandedWeapon(Weapon):
    def attack_move(self):
        if self.active:
            return f"{self.name} performs a quick slash attack, dealing {self.damage} damage!"
        else:
            return f"{self.name} is not equipped and cannot attack."

class DoubleHandedWeapon(Weapon):
    def attack_move(self):
        if self.active:
            return f"{self.name} performs a powerful spin attack, dealing {self.damage * 1.5} damage!"
        else:
            return f"{self.name} is not equipped and cannot attack."

class RangedWeapon(Weapon):
    def attack_move(self):
        if self.active:
            return f"{self.name} shoots an arrow, dealing {self.damage} damage from afar!"
        else:
            return f"{self.name} is not equipped and cannot attack."

class Pike(Weapon):
    def attack_move(self):
        if self.active:
            # Thrusting attack for a Pike
            return f"{self.name} performs a long-range thrust attack, dealing {self.damage * 1.2} damage!"
        else:
            return f"{self.name} is not equipped and cannot attack."

        
class Shield(Item):
    def __init__(self, name, description="", rarity="common", defense=0, broken=False):
        super().__init__(name, description, rarity)
        self.defense = defense
        self.broken = broken
        self.active = False
    
    def equip(self):
        self.active = True
        return print(f"{self.name} is equipped.")
    
    def use(self):
        if self._ownership and self.active:
            defense_modifier = 1.0
            if self.rarity == "legendary":
                defense_modifier = 1.10
            if self.broken:
                defense_modifier *= 0.5
            total_defense = self.defense * defense_modifier
            return print(f"{self.name} is used, blocking {total_defense} damage.")
        elif not self._ownership:
            return print(f"{self.name} cannot be used because it has no owner.")
        else:
            return print(f"{self.name} is not equipped.")
        
class Potion(Item):
    def __init__(self, name, description="", rarity="common", value=0, type="HP", effective_time=0):
        super().__init__(name, description, rarity)
        self.value = value
        self.type = type  # e.g., 'HP', 'attack', 'defense'
        self.effective_time = effective_time
        self.empty = False
    
    def use(self):
        if self.empty:
            return print(f"{self.name} cannot be used because it is empty.")
        elif self._ownership:
            effect_description = f"{self.name} is used, {self.type} increased by {self.value} for {self.effective_time} seconds."
            self.empty = True  # After use, the potion is empty
            return print(effect_description)
        else:
            return print(f"{self.name} cannot be used because it has no owner.")
    
    @classmethod
    def from_ability(cls, name, owner, type):
        # Creating a common potion generated by player abilities
        potion = cls(name, rarity="common", value=50, type=type, effective_time=30)
        potion._ownership = owner
        return potion
    
# Test the inventory system
inventory = Inventory()

# Create some items
long_sword = Weapon(name="Long Sword", damage=100)
great_axe = Weapon(name="Great Axe", damage=150, rarity="legendary")
long_pike = Pike(name="Long Pike", damage=120)

# Add items to the inventory
inventory.add_item(long_sword, owner="Arthur")
inventory.add_item(great_axe, owner="Lancelot")
inventory.add_item(long_pike, owner="Gawain")

# Display all items in the inventory
inventory.display_items()

# Remove an item from the inventory
inventory.remove_item(great_axe)

# Display all items again to confirm removal
inventory.display_items()

# Check if an item is in the inventory
if long_sword in inventory:
    print(f"{long_sword.name} is in the inventory.")

# Iterate over the inventory
for item in inventory:
    print(f"Iterating through: {item.name}")