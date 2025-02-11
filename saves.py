class Saves():
    def __init__(self):
        """Dictionary with custom methods."""
        self.saves = {}

    
    def __str__(self):
        return str(self.saves)
    

    def __iter__(self):
        return iter(self.saves.items())
    

    def __len__(self):
        return len(self.saves)
    

    def to_dict(self) -> dict:
        """For json converting."""
        return self.saves
        

    def add_save(self, name: str, content: str):
        """Adds save (item).

        Args:
            name (str): key
            content (str): value
        """
        self.saves[name] = content


    def rename_save(self, old_name: str, new_name: str):
        """Renames save (replaces its key).

        Args:
            old_name (str): old key
            new_name (str): new key
        """
        if old_name in self.saves and new_name and new_name not in self.saves:
            self.saves[new_name] = self.saves.pop(old_name)


    def delete_save(self, name: str):
        """Deletes save (item).

        Args:
            name (str): key
        """
        self.saves.pop(name)

    
    def load_save(self, name: str) -> str:
        """Loads save.

        Args:
            name (str): key

        Returns:
            str: value
        """
        return self.saves[name]

