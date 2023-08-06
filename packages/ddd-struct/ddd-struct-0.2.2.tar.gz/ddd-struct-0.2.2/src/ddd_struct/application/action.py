import time
from copy import copy
from typing import Optional, List
from ..domain.repository import TaskQueueRepository, TaskProcessRepository




__all__ = ['CacheQueue', 'SimpleTaskProcessor']
class CacheQueue:
    def __init__(self) -> None:
        self.cache = {}
        self.queue = None


    def _next(self):
        while True:
            index = next(self.queue)
            if index in self.cache:
                return index
    

    def _pop(self):
        if self.queue is None:
            self.queue = iter(copy(self.cache))
        try:
            return self.cache[self._next()]
        except StopIteration:
            self.queue = iter(copy(self.cache))
            return None
    

    def _pop_index(self):
        if self.queue is None:
            self.queue = iter(copy(self.cache))
        try:
            return self._next()
        except StopIteration:
            self.queue = iter(copy(self.cache))
            return None
    
    
    def delete(self, index)->bool:
        if index in self.cache:
            del self.cache[index]
            return True
        else:
            return False
    

class SimpleTaskProcessor:
    def __init__(
        self, 
        queue_repo:TaskQueueRepository, 
        process_repo: TaskProcessRepository,
        delay:int = 1,
        batch_size = 5
    ) -> None:
        self.queue_repo = queue_repo
        self.process_repo = process_repo
        self.delay = delay
        self.batch_size = batch_size
    

    def set_queue_repo(self, queue_repo: TaskQueueRepository):
        self.queue_repo = queue_repo
    

    def set_process_repo(self, process_repo: TaskProcessRepository):
        self.process_repo = process_repo
    
    def set_batch_size(self, batch_size):
        self.batch_size = batch_size


    def gen_item(self, request_id, request):
        raise NotImplementedError
    

    def gen_items(self, requests):
        raise NotImplementedError

    def get_request(self, queue_repo: Optional[TaskQueueRepository]=None):
        queue_repo = queue_repo or self.queue_repo
        return queue_repo.get_task()
    

    def get_requests(self, n=10, queue_repo: Optional[TaskQueueRepository]=None):
        queue_repo = queue_repo or self.queue_repo
        return queue_repo.get_n_tasks(n)
    

    def process_task(self, item, process_repo:Optional[TaskProcessRepository]=None):
        process_repo = process_repo or self.process_repo
        return process_repo.process(item)
    

    def process_tasks(self, items, process_repo:Optional[TaskProcessRepository]=None):
        if process_repo is None:
            process_repo = self.process_repo
        return process_repo.process_batch(items)

    
    def save_item(self, item, queue_repo: Optional[TaskQueueRepository]=None)->bool:
        queue_repo = queue_repo or self.queue_repo
        return queue_repo.save_item(item)
    

    def save_items(self, items, queue_repo: Optional[TaskQueueRepository]=None)->List[bool]:
        queue_repo = queue_repo or self.queue_repo
        return queue_repo.save_items(items)
    

    def process_when_failed(self, item, error_code:str):
        # log or warning by email
        raise NotImplementedError
    

    def process_when_failed_batch(self, items, error_code:str):
        raise NotImplementedError
    

    def postprocess(self, item, process_repo:Optional[TaskProcessRepository]=None)->bool:
        return True, item
    

    def postprocess_batch(
        self, 
        items, 
        process_repo:Optional[TaskProcessRepository]=None
    )->List[bool]:
        return [True]*len(items), items


    def preprocess(self, item, process_repo:Optional[TaskProcessRepository]=None):
        return True, item
    

    def preprocess_batch(
        self, 
        items, 
        process_repo:Optional[TaskProcessRepository]=None
    ):
        return [True]*len(items), items

    
    def process_all(
        self, 
        item, 
        process_repo: TaskProcessRepository, 
        queue_repo: TaskQueueRepository
    ):
        '''处理所有的步骤
        '''
        # preprocess
        succeed, item = self.preprocess(item, process_repo)
        if not succeed:
            self.process_when_failed(item, 'preprocess')
            return 

        # process
        item = self.process_task(item)
        succeed = self.save_item(item, queue_repo)
        if not succeed:
            self.process_when_failed(item, 'save')
            return 

        # postprocess
        succeed, item = self.postprocess(item, process_repo)
        if not succeed:
            self.process_when_failed(item, 'postprocess')
            return

    
    def process_all_batch(
        self, 
        items, 
        process_repo: TaskProcessRepository, 
        queue_repo: TaskQueueRepository
    ):
        '''处理所有步骤，并且是批量处理
        '''
        # preprocess
        succeed_symbols, items = self.preprocess_batch(items, process_repo)
        failed_items = [i for i,s in zip(items, succeed_symbols) if not s]
        if failed_items:
            self.process_when_failed_batch(failed_items, 'preprocess')

        # process
        items = [i for i,s in zip(items, succeed_symbols) if s]
        if not items:
            return
        items = self.process_tasks(items)
        succeed_symbols = self.save_items(items, queue_repo)
        failed_items = [i for i,s in zip(items, succeed_symbols) if not s]
        if failed_items:
            self.process_when_failed_batch(failed_items, 'save')

        # postprocess
        items = [i for i,s in zip(items, succeed_symbols) if s]
        if not items:
            return
        succeed_symbols, items = self.postprocess_batch(items, process_repo)
        failed_items = [i for i,s in zip(items, succeed_symbols) if not s]
        if failed_items:
            self.process_when_failed_batch(failed_items, 'postprocess')

   

    def run(
        self, 
        queue_repo: Optional[TaskQueueRepository]=None, 
        process_repo: Optional[TaskProcessRepository]=None,
        delay=None, 
        n_loop=1000000000,
        auto_change_delay=True
    ):
        queue_repo = queue_repo or self.queue_repo
        process_repo = process_repo or self.process_repo
        delay = delay or self.delay
        ignore_delay = False
        for i in range(n_loop):
            if not auto_change_delay or not ignore_delay:
                time.sleep(delay)
            request_id, request = self.get_request(queue_repo)
            if not request:
                continue
            else:
                ignore_delay = True

            # generate item
            item = self.gen_item(request_id, request)
            succeed = self.save_item(item, queue_repo)
            if not succeed:
                self.process_when_failed(item, 'save')
                continue

            # process item
            try:
                self.process_all(item, process_repo, queue_repo)
            except:
                self.process_when_failed(item, 'process_all') 
                
    

    def run_batch(
        self, 
        queue_repo: Optional[TaskQueueRepository]=None, 
        process_repo: Optional[TaskProcessRepository]=None,
        delay=None, 
        n_loop=1000000000,
        auto_change_delay=True
    ):
        queue_repo = queue_repo or self.queue_repo
        process_repo = process_repo or self.process_repo
        delay = delay or self.delay
        ignore_delay = False
        for i in range(n_loop):
            if not auto_change_delay or not ignore_delay:
                time.sleep(delay)
            requests = self.get_requests(self.batch_size, queue_repo)
            if not requests:
                continue
            else:
                ignore_delay = True

            # generate item
            items = self.gen_items(requests)
            succeed_symbols = self.save_items(items, queue_repo)
            failed_items = [i for i,s in zip(items, succeed_symbols) if not s]
            if failed_items:
                self.process_when_failed_batch(failed_items, 'save')
            items = [i for i,s in zip(items, succeed_symbols) if s]
            if not items:
                continue
            try:
                self.process_all_batch(items, process_repo, queue_repo)
            except:
                self.process_when_failed_batch(items, 'process_all')

            

