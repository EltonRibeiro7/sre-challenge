import sys
sys.path.append('../')
from apscheduler.schedulers.background import BackgroundScheduler
from breed_controller import BreedController
from category_controller import CategoryController
from shared.log import Log
import os

class Scheduler():
    _execution_interval_minutes=int(os.getenv('CASE_EXECUTION_INTERVAL_MINUTES', 1))


    def execute(self):
        _category = CategoryController()
        _breed = BreedController()
        self._sched.add_job(_breed.syncronize_breeds, 'interval', minutes=self._execution_interval_minutes, jitter=30)
        self._sched.add_job(_breed.syncronize_breed_images, 'interval', minutes=self._execution_interval_minutes, jitter=30)
        self._sched.add_job(_category.syncronize_category, 'interval', minutes=self._execution_interval_minutes, jitter=30)
        self._sched.add_job(_category.syncronize_category_images, 'interval', minutes=self._execution_interval_minutes, jitter=30)
        self._sched.print_jobs()
        try:
            self._sched.start()
            print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))  
        except (KeyboardInterrupt, SystemExit) as err:
            self._logging.error('Error while trying to start scheduler, details {}'.format(err))
            self._sched.shutdown()
            
    def __init__(self):
        self._sched = BackgroundScheduler()
        self._logging = Log('apscheduler').logger()
        self.execute()

if __name__ == "__main__":
    Scheduler()
