import traceback
from retry import retry
from ddd_interface.objects.do import APIGatewayRequestDO
from ddd_interface.objects.lib import deserialize, serialize
from ..domain.repository import TaskQueueRepository



@retry(tries=2, delay=0.5)
def _save_item(gateway_ao, redis_ao, domain, redis_token, task_id, item_str, timeout):
    if gateway_ao:
        assert redis_token
        gateway_request = APIGatewayRequestDO(
            service_name='redis',
            method = 'set_response',
            auth = {'token': redis_token},
            data = {
                'domain': domain,
                'request_id': task_id,
                'response': item_str,
                'timeout': timeout
            }
        )
        gateway_ao.send_request(gateway_request)
    else:
        redis_ao.set_response(
            domain=domain, 
            request_id=task_id, 
            response=item_str, 
            timeout=timeout
        )


class TaskQueueFactory:
    def gen_redis_repo(
        self, 
        domain, 
        request_key, 
        request_class, 
        request_converter,
        item_converter,
        redis_ao=None, 
        gateway_ao = None,
        redis_token = None,
        item_timeout = 86400,
        fetch_request_timeout = 3
    ):
        if not redis_ao and not (gateway_ao and redis_token):
            raise ValueError('redis ao or gateway ao should be defined at least one')
        class RedisTaskQueueRepositoryImpl(TaskQueueRepository):
            @retry(tries=2, delay=0.5)
            def get_task(self):
                if gateway_ao:
                    assert redis_token, 'redis token is not set'
                    gateway_request = APIGatewayRequestDO(
                        service_name='redis',
                        method = 'get_request2',
                        auth = {'token': redis_token},
                        data = {
                            'domain': domain,
                            'key': request_key,
                        }
                    )
                    request_id, request = gateway_ao.send_request(gateway_request, fetch_request_timeout)
                    
                else:
                    request_id, request = redis_ao.get_request2(domain=domain, key=request_key)

                if request is None:
                    return None, None
                request = deserialize(request, request_class)
                request = request_converter.to_entity(request)
                return request_id, request
            

            def get_n_tasks(self, n):
                requests = []
                for i in range(n):
                    request_id, request = self.get_task()
                    if request is None:
                        break
                    else:
                        requests.append((request_id, request))
                return requests
                

            def save_item(self, item):
                try:
                    item = item_converter.to_do(item)
                    item_str = serialize(item)
                    task_id = item.item_id
                    timeout = item_timeout
                    _save_item(gateway_ao, redis_ao, domain, redis_token, 
                                task_id, item_str, timeout)
                    return True
                except:
                    traceback.print_exc()
                    return False
            

            def save_items(self, items):
                succeed_symbols = []
                for item in items:
                    succeed = self.save_item(item)
                    succeed_symbols.append(succeed)
                return succeed_symbols
        repo = RedisTaskQueueRepositoryImpl()
        return repo

