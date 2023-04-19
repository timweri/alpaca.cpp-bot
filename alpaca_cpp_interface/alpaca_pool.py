import threading
import asyncio
from alpaca_interface import AlpacaCppInterface

# This worker pool is not really a pool
# Each instance is binded to a key
# The purpose is to assign one Alpaca instance to a user, represented by a key
class AlpacaCppPool:
    def __init__(self, alpaca_exec_path, model_path, capacity=4):
        self.pool = {}
        self.capacity = capacity
        self.pool_lock = threading.RLock()
        self.alpaca_exec_path = alpaca_exec_path
        self.model_path = model_path

    async def create_worker(self, key):
        self.pool_lock.acquire()
        if len(self.pool) >= self.capacity:
            return False
        if key in self.pool:
            self.pool[key].restart()
        else:
            self.pool[key] = AlpacaCppInterface(self.alpaca_exec_path, self.model_path)
            await self.pool[key].start()
        self.pool_lock.release()

        return True
        
    def get_worker(self, key):
        if key not in self.pool:
            return None

        return self.pool[key]

    async def get_worker_create(self, key):
        if key not in self.pool:
            if not await self.create_worker(key):
                return None

        return self.pool[key]

    async def terminate_all(self, key):
        self.pool_lock.acquire()
        await asyncio.gather([instance])
        for key in self.pool:
            await self.pool[key].terminate()
        self.pool_lock.release()
        return True
    
    async def clear(self):
        self.pool_lock.acquire()
        await terminate_all()
        self.pool = {}
        self.pool_lock.release()
        return True

    async def __aenter__(self):
        return self

    async def __aexit__(self):
        self.pool_lock.acquire()
        await terminate_all()
        self.pool_lock.release()
