
class DB_cache_test:
    def __init__(self):
        
        self.cache = {}

    def handle(self, requete):
        response = self.cache[requete]

        return response
    
    def adding(self, requete, value):
        self.cache[requete] = value