
# router to ensure that all databse operation happening in the 
# metrics app fall to the "extra_db" databse

class extra_db_router(object): 
    def db_for_read(self, model, **hints):
        
        # Point all operations on chinook models to 'chinookdb
        if model._meta.app_label == 'metrics':
            return 'extra_db'
        return 'default'

    def db_for_write(self, model, **hints):
        
        # Point all operations on chinook models to 'chinookdb'"
        if model._meta.app_label == 'metrics':
            return 'extra_db'
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        
        # "Allow any relation if a both models in chinook app"
        if obj1._meta.app_label == 'metrics' and obj2._meta.app_label == 'metrics':
            return True
        # Allow if neither is chinook app
        elif 'metrics' not in [obj1._meta.app_label, obj2._meta.app_label]: 
            return True
        return False
    
    def allow_syncdb(self, db, model):
        if db == 'extra_db' or model._meta.app_label == "metrics":
            return False # we're not using syncdb on our legacy database
        else: # but all other models/databases are fine
            return True
        
    def allow_migrate(self, db, app_label, model_name=None, **hints):

        if app_label == 'metrics':
            return db == 'extra_db'
        return None