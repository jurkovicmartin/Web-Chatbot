class Saves():
    def __init__(self):
        self.saves = {}

    
    def __str__(self):
        return str(self.saves)
    

    def __iter__(self):
        return iter(self.saves.items())
    

    def __len__(self):
        return len(self.saves)
        

    def add_save(self, name: str, content: str):
        self.saves[name] = content


    def rename_save(self, old_name: str, new_name: str):
        if old_name in self.save and new_name and new_name not in self.save:
            self.saves[new_name] = self.saves.pop(old_name)


    def delete_save(self, name: str):
        self.saves.pop(name)

    
    def load_save(self, name: str) -> str:
        return self.saves[name]
