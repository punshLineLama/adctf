import sched
import time
import sys
from gamelib import *
sys.path.append("checkers/saarxiv/")
import saarxiv
sys.path.append("checkers/saarlender/")
import saarchecker



# Initialize the scheduler
scheduler = sched.scheduler(time.time, time.sleep)
# Define the interval in seconds (5 minutes = 300 seconds)
interval = 5
global round_g
round_g = 0

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
    service = saarchecker.SaarlendarChecker(2)

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
    global round_g
    round_g +=1
    print("Running service checks started at:", time.ctime())
    for team in teams:
        saarxiv_check(team, round_g)
        saarlendar_check(team, round_g)


def main():
    # Schedule the initial task
    scheduler.enter(interval, 1, run_checks, ([[1,]]))
    scheduler.run()
    while True:
        time.sleep(1000)

# If run_checkers is called as main program, just run the checkers every 5 minutes.
#  This automatically places new flags every 5 minutes and checks the services.
if __name__ == "__main__":
    main() 