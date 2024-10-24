import json
class Inventory:
    def __init__(self, owner):
        self.owner = owner
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
    
    def to_json(self):
        return {
            'owner': self.owner,
            'items': [item.to_json() for item in self.items]
        }

    # Deserialize inventory from JSON
    @classmethod
    def from_json(cls, data):
        inventory = cls(owner=data['owner'])
        for item_data in data['items']:
            item_class = globals()[item_data.pop('class')]
            item = item_class.from_json(item_data)
            inventory.add_item(item, "Hero")
        return inventory

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
    
    def to_json(self):
        return {
            'class': self.__class__.__name__,
            'name': self.name,
            'description': self.description,
            'rarity': self.rarity,
            'ownership': self._ownership
        }

    # Deserialization from JSON
    @classmethod
    def from_json(cls, data):
        return cls(**data)

class Weapon(Item):
    def __init__(self, name, description="", rarity="common", damage=0, weapon_type="", ownership=""):
        super().__init__(name, description, rarity, ownership)
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
    
    def to_json(self):
        data = super().to_json()
        data.update({'damage': self.damage, 'weapon_type': self.weapon_type})
        return data

    # Deserialization for Weapon
    @classmethod
    def from_json(cls, data):
        return cls(**data)

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
    def __init__(self, name, description="", rarity="common", defense=0, broken=False, ownership=""):
        super().__init__(name, description, rarity, ownership)
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
    
    def to_json(self):
        data = super().to_json()
        data.update({'defense': self.defense, 'broken': self.broken})
        return data

    # Deserialization for Shield
    @classmethod
    def from_json(cls, data):
        return cls(**data)
class Potion(Item):
    def __init__(self, name, description="", rarity="common", value=0, type="HP", effective_time=0, ownership=""):
        super().__init__(name, description, rarity, ownership)
        self.value = value
        self.type = type
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
    
    def to_json(self):
        data = super().to_json()
        data.update({'type': self.type})
        return data

    # Deserialization for Potion
    @classmethod
    def from_json(cls, data):
        return cls(**data)
    
def custom_serializer(obj):
    if hasattr(obj, 'to_json'):
        return obj.to_json()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable.")


if __name__ == "__main__":
   
    excalibur = Weapon(name="Excalibur", damage=100, weapon_type="sword", rarity="legendary")
    aegis = Shield(name="Aegis", defense=50, broken=False, rarity="rare")
    health_potion = Potion(name="Health Elixir", type="hp", rarity="common")

  
    hero_inventory = Inventory(owner="Hero")
    
   
    print(hero_inventory.add_item(excalibur, "Hero"))
    print(hero_inventory.add_item(aegis, "Hero"))
    print(hero_inventory.add_item(health_potion, "Hero"))

 
    inventory_json = json.dumps(hero_inventory, default=custom_serializer, indent=4)
    print("\nSerialized Inventory:")
    print(inventory_json)

  
    deserialized_inventory = Inventory.from_json(json.loads(inventory_json))

   
    print("\nDeserialized Inventory:")
    print(deserialized_inventory.display_items())