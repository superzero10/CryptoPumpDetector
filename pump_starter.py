import threading
import time

from mcafee_pumps.pump_detector import track_that_mcafee_bastard

while True:
    mcafee_thread = threading.Thread(target=track_that_mcafee_bastard())
    mcafee_thread.start()

    time.sleep(5)
