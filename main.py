import json

class PerkManager:
    def __init__(self, json_path):
        with open(json_path, 'r') as f:
            self.data = json.load(f)
        self.banned_perks = self.data.get('bannedPerks', [])
        self.allowed_perks = self.data.get('bannedCombinations', [])

    def get_banned_perks(self):
        return self.banned_perks

    def get_allowed_perks(self):
        return self.allowed_perks
    def search_perks(self, query):
        """
        Search for perks containing the query string (case-insensitive) in banned or allowed perks.
        Returns a dict with matches from both lists.
        """
        query = query.lower()
        banned_matches = [perk for perk in self.banned_perks if query in perk.lower()]
        allowed_matches = []
        for combo in self.allowed_perks:
            if isinstance(combo, list):
                if any(query in perk.lower() for perk in combo):
                    allowed_matches.append(combo)
            elif isinstance(combo, str):
                if query in combo.lower():
                    allowed_matches.append(combo)
        return {
            "banned": banned_matches,
            "allowed": allowed_matches
        }
    

    ]
    def validate_build(self, build):
        """
        Validate a build against banned perks and combinations.
        Returns True if valid, False if invalid.
        """
        for perk in build:
            if perk in self.banned_perks:
                return False
        for combo in self.allowed_perks:
            if isinstance(combo, list):
                if all(perk in build for perk in combo):
                    return True
            elif isinstance(combo, str):
                if combo in build:
                    return True
        return True

if __name__ == "__main__":
    perk_manager = PerkManager('general_balancing.json')
    
    print("Banned Perks:", perk_manager.get_banned_perks())
    print("Allowed Combinations:", perk_manager.get_allowed_perks())
    
    search_query = "perk"
    search_results = perk_manager.search_perks(search_query)
    print(f"Search results for '{search_query}':", search_results)
    
    for i, build in enumerate(perk_manager.test_builds):
        is_valid = perk_manager.validate_build(build)
        print(f"Build {i+1} is {'valid' if is_valid else 'invalid'}.")