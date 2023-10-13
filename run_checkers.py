import sched
import time
import sys
from gamelib import *
sys.path.append("checkers/saarxiv/")
sys.path.append("checkers/saarlender/")
import saarchecker
import saarxiv
import saarchecker
import threading

# Initialize the scheduler
scheduler = sched.scheduler(time.time, time.sleep)

# Define the interval in seconds (10 seconds)
interval = 180
results = [False] * 10

global round_g
round_g = 0

def id_to_ip(id):
    if id in [1,2,3,4]:
        return "192.168.42.3"+str(id)
    elif id in [31,32,33,34]:
        return "192.168.42."+str(id)
    else:
        print("[-] Error converting id to ip, returning 192.168.42.31!!")
        return "192.168.42.31"



# Define a function to run saarxiv_check in a thread with a timeout
def run_saarxiv_check(team_nb, round):
    thread = threading.Thread(target=saarxiv_check, args=(team_nb, round, results))
    thread.daemon = True
    thread.start()
    thread.join(timeout=15)  # Wait for at most 15 seconds
    print("returning results 0: "+str(results[0]))

    return results[0]


# Define a function to run saarlender_check in a thread with a timeout
def run_saarlender_check(team_nb, round):
    thread = threading.Thread(target=saarlender_check, args=(team_nb, round, results))
    thread.daemon = True
    thread.start()
    thread.join(timeout=15)  # Wait for at most 15 seconds
    print("returning results 1: "+str(results[1]))
    return results[1]

def saarxiv_check(team_nb, round, results):
    team = saarxiv.Team(2, '', id_to_ip(team_nb))
    service = saarxiv.SaarXivInterface(1)

    print('[1] Integrity check...')
    integrity = service.check_integrity(team, round)
    print('Passed.')

    print('[2] Store flags...')
    flags_store = service.store_flags(team, round)
    print('Done ({} flags).'.format(flags_store))

    print('[3] Retrieve the flags in the next round')
    flags = service.retrieve_flags(team, round)
    print('Done ({} flags).'.format(flags))

    if integrity and flags_store:
        results[0] = True
    else:
        results[0] = False
        

def saarlender_check(team_nb, round, results):
    team = Team(2, 'n00bs', id_to_ip(team_nb))
    print("Round:", round)
    service = saarchecker.SaarlendarChecker(2)

    print('[1] Integrity check...')
    integrity = service.check_integrity(team, round)
    print('Passed.')

    print('[2] Store flags...')
    flags_store = service.store_flags(team, round)
    print('Done ({} flags).'.format(flags_store))

    print('[3] Retrieve the flags in the next round')
    flags = service.retrieve_flags(team, round)
    print('Done ({} flags).'.format(flags))

    if flags_store and integrity:
        results[1] = True
    else:
        results[1] = False


# Define a function to execute the task
def run_checks(teams):
    global round_g
    round_g += 1
    print("Running service checks started at:", time.ctime())
    res = []  # Initialize the result list
    for team in teams:
        try:
            run_saarxiv_check(team, round_g)
            run_saarlender_check(team, round_g)
        except Exception as e:
            print(f"Error occurred: {e}")

def schedule_checks():
    scheduler.enter(interval, 1, schedule_checks, ())
    run_checks([1])  # Pass teams as needed

def main():
    # Schedule the initial task
    scheduler.enter(interval, 1, schedule_checks, ())
    scheduler.run()

# If run_checkers is called as the main program, just run the checkers every 10 seconds.
# This automatically places new flags every 10 seconds and checks the services.
if __name__ == "__main__":
    main()
