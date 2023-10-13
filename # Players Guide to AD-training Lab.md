# Players Guide to AD-training Lab

## You should have been granted access to at least the following machines:
- vulnbox (192.168.42.31)
- player-server (192.168.42.3)
- kali (192.168.42.10)

On the vulnbox, there are various vulnerable services. It is taken 1:1 from the saarCTF 2020.
The player-server is a simple Ubuntu server, which is meant to run your tools (tulip, ataka)

The kali machine is meant to be your client from which you can test your exploits, or send them to the player server, or connect to the vulnbox e.t.c.


## Other machines in the network:
- gameserver (192.168.42.2)
- vulnbox 2 (192.168.42.32) - to test your exploits
- vulnbox 3 (192.168.42.33) - to test your exploits

The gameserver has two services running:
- The submissions service, running on port 6666
- The checker and exploit service running on port 12345

### Submission service
You can submit your captured flags to the submission service, it tells you if your flags are valid or not.
You are greeted with a welcome message, thereafter you can send your flags one per line.

### Checker and exploit service
The checker service checks if a service of a given vulnbox is still running correctly. (See the prompt of the service for details)
The exploit service is meant to run exploits against your vulnbox (192.168.42.31). This is meant for you to be able to capture the attack traffic and be able to analyse and reproduce the exploit using tulip and ataka.