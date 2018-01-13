import threading
import time

from detection.bittrex_detector import BittrexDetector
from detection.bittrex_constants import SNAPSHOT_FREQUENCY_SEC
from detection.yobit_detector import YobitDetector

yobit_detector = YobitDetector()
bittrex_detector = BittrexDetector()


# yobit_thread = threading.Thread(target=yobit_detector.detect())
# yobit_thread.start()

bittrex_thread = threading.Thread(target=bittrex_detector.detect())
bittrex_thread.start()
