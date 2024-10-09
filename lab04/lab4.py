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
        return print(f"{self.name} (Rarity: {self.rarity}, Owned by: {self._ownership or 'No one'})")
    
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
    
long_bow = Weapon(name='Belthronding', rarity='legendary', damage= 5000, weapon_type='bow')
long_bow.pick_up('Beleg') # Belthronding is now owned by Beleg
long_bow.equip() # Belthronding is equipped by Beleg
long_bow.use() # Belthronding is used, dealing 5750 damage
broken_pot_lid = Shield(name='wooden lid', description='A lid made of wood, useful in cooking. No one will choose it willingly for a shield', defense = 5, broken = True)
long_bow.pick_up('Beleg') # wooden lid is now owned by Beleg
broken_pot_lid.equip() # wooden lid is equiped by Beleg
broken_pot_lid.use() # wooden lid is used, blocking 2.5 damage
broken_pot_lid.throw_away() # wooden lid is thrown away
broken_pot_lid.use() # NO OUTPUT
attack_potion = Potion.from_ability(name='atk potion temp', owner ='Beleg', type='attack')
attack_potion.use() # Beleg used atk potion temp, and attack increase 50 for 30s
attack_potion.use() # NO OUTPUT
isinstance(long_bow, Item) # True
isinstance(broken_pot_lid, Shield) # True
isinstance(attack_potion, Weapon) # False