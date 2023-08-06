import asyncio
from .rmq_functions import run_consumer


class WorkerThreader:

    def __init__(self, consumers_conf, credentials):
        self.consumers_conf = consumers_conf
        self.credentials = credentials
        self.get_workers()

    def get_workers(self):
        self.workers = []
        self.consumer_classes = [workers_data["consumer_class"] for workers_data in self.consumers_conf]
        for workers_data in self.consumers_conf:
            workers_count = workers_data["workers_count"]
            consumer_class = workers_data["consumer_class"]
            consumer_settings = workers_data["consumer_settings"]
            queue_parameters = workers_data["queue_parameters"]
            exchange_parameters = workers_data["exchange_parameters"]
            dead_letter_params = workers_data["dead_letter_params"]

            consumer_functions = [run_consumer(consumer_class,
                                               queue_parameters,
                                               exchange_parameters,
                                               **self.credentials,
                                               **consumer_settings,
                                               **dead_letter_params) for i in range(1, workers_count + 1)]
            self.workers.extend(consumer_functions)

    def stop_consumers(self):
        import gc
        consumer_objs = [ob for ob in gc.get_objects() if isinstance(ob, tuple(self.consumer_classes))]

        for obj in consumer_objs:
            obj.stop_consuming()


    async def run(self):
        await asyncio.gather(*self.workers)
