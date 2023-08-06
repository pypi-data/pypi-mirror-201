
__all__ = ['TaskQueueRepository', 'TaskProcessRepository']

class Repository:
    pass


class TaskQueueRepository(Repository):
    def get_request(self):
        raise NotImplementedError
    
    def get_n_requests(self, n):
        raise NotImplementedError
    
    def save_item(self, item):
        raise NotImplementedError
    
    def save_items(self, items):
        raise NotImplementedError
    
    

class TaskProcessRepository(Repository):
    def preprocess(self, item):
        return True, item
    
    def preprocess_batch(self, items):
        return [True]*len(items), items

    def process(self, item):
        raise NotImplementedError
    
    def process_batch(self, items):
        raise NotImplementedError
    
    def postprocess(self, item):
        return True, item
    
    def postprocess_batch(self, items):
        return [True]*len(items), items