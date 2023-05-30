from django_cron import CronJobBase, Schedule

from service.services import TruckService

class TruckCronJob(CronJobBase):
    RUN_EVERY_MINS = 3
    RETRY_AFTER_FAILURE_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    
    code = 'service.truck_cron_job'

    def do(self):
        return TruckService.update_location_random()
