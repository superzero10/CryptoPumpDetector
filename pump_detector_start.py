import threading

from exchange_pumps.detection.bittrex_detector import BittrexDetector
from exchange_pumps.detection.yobit_detector import YobitDetector

yobit_detector = YobitDetector()
bittrex_detector = BittrexDetector()


# yobit_thread = threading.Thread(target=yobit_detector.detect())
# yobit_thread.start()

bittrex_thread = threading.Thread(target=bittrex_detector.detect())
bittrex_thread.start()
