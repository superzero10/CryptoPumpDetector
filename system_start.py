from exchange_services.bittrex_service import BittrexService
from exchange_services.yobit_service import YobitService
from detection.bittrex_detector import BittrexDetector
from detection.yobit_detector import YobitDetector
from threading import Timer, Thread, Event

yobit_detector = YobitDetector()
bittrex_detector = BittrexDetector()


