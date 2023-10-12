import sched
import time
import sys
from gamelib import *
sys.path.append("saarXiv/checkers/")
import saarxiv
sys.path.append("saarlendar/checkers/")
import gameserver



# Initialize the scheduler
scheduler = sched.scheduler(time.time, time.sleep)
# Define the interval in seconds (5 minutes = 300 seconds)
interval = 300 
round = 0

def saarxiv_check(team_nb, round):
    team = saarxiv.Team(2, '', '192.168.42.3'+str(team_nb))    
    service = saarxiv.SaarXivInterface(1)

    print('[1] Integrity check...')
    service.check_integrity(team, round)
    print('Passed.')

    print('[2] Store flags...')
    flags = service.store_flags(team, round)
    print('Done ({} flags).'.format(flags))

    print('[3] Retrieve the flags in the next round')
    flags = service.retrieve_flags(team, round)
    print('Done ({} flags).'.format(flags))


def saarlendar_check(team_nb, round):
    # TEST CODE
    team = Team(2, 'n00bs', '192.168.42.3'+str(team_nb))
    print("Round:", round)
    service = SaarlendarChecker(2)

    print('[1] Integrity check...')
    service.check_integrity(team, round)
    print('Passed.')

    print('[2] Store flags...')
    flags = service.store_flags(team, round)
    print('Done ({} flags).'.format(flags))

    print('[3] Retrieve the flags in the next round')
    flags = service.retrieve_flags(team, round)
    print('Done ({} flags).'.format(flags))
    

# Define a function to execute the task
def run_checks(teams):
    round +=1
    print("Running service checks started at:", time.ctime())
    for team in teams:
        saarxiv_check(team, round)
        saarlendar_check(team, round)


# Start the scheduler
print("Task scheduler started. Press Ctrl+C to exit.")
schedule_next_task(interval)

def main():
    # Schedule the initial task
    scheduler.enter(interval, 1, run_checks, ())
    scheduler.run()
    while True:
        run_checks()
        time.sleep(1000)

# If run_checkers is called as main program, just run the checkers every 5 minutes.
#  This automatically places new flags every 5 minutes and checks the services.
if __name__ == "__main__":
    main() 