import abc
from datetime import datetime
import schedule
import json
import logging
import time

from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal

from rss_tube.database.feeds import Feeds
from rss_tube.database.settings import Settings
from rss_tube.download import Downloader


logger = logging.getLogger("logger")
settings = Settings()


class Tasks(QtCore.QThread):
    job_update_info = pyqtSignal(datetime, datetime)

    def __init__(self):
        super(Tasks, self).__init__()
        self.running = False

        self.feed_update_task = FeedsUpdateTask()

        self.interval = settings.value("tasks/interval", type=int)

        self.set_schedule()

    def _feed_update_task_finished_callback(self):
        if self.feed_update_job.last_run is None:
            self.feed_update_job.last_run = datetime.now()
        self.job_update_info.emit(self.feed_update_job.last_run, self.feed_update_job.next_run)

        # Start purge task
        if settings.value("purge/enabled", type=bool):
            self.purge_task = PurgeFeedsTask()
            self.purge_task.start()
            self.purge_task.started.connect(lambda: logger.debug("Auto PurgeFeedsTask started."))
            self.purge_task.finished.connect(lambda: logger.debug("Auto PurgeFeedsTask finished."))

    def set_schedule(self):
        schedule.clear("update-feed")
        self.feed_update_job = schedule.every(settings.value("feeds/update_interval/minutes", type=int)).minutes.do(self.feed_update_task.start).tag("update-feed")

        self.job_update_info.emit(self.feed_update_job.last_run or datetime.now(), self.feed_update_job.next_run or datetime.now())
        self.feed_update_task._finished.connect(self._feed_update_task_finished_callback)

    def run(self):
        self.running = True
        try:
            schedule.run_all()
            while self.running:
                time.sleep(self.interval)
                schedule.run_pending()
        except Exception as e:
            logger.error(f"Tasks: {e}")
        finally:
            self.running = False


class BaseTask(QtCore.QThread):
    failed = pyqtSignal()

    def __init__(self):
        super(BaseTask, self).__init__()
        self.running = False

    @abc.abstractmethod
    def task(self):
        ...

    def run(self):
        self.running = True
        try:
            self.task()
        except Exception as e:
            logger.error(f"{self.__class__.__name__} failed: {e}")
            self.failed.emit()
        finally:
            self.running = False


class PurgeFeedsTask(BaseTask):
    maximum = pyqtSignal(int)
    current = pyqtSignal(str)
    report = pyqtSignal(dict) # {"progress": <int>, "entries": <int>, "feeds": <int>}

    def __init__(self):
        super(PurgeFeedsTask, self).__init__()
        self.request_stop = False

    def task(self):
        self.request_stop =  False

        feeds = Feeds()
        feeds_list = feeds.get_purgeable_feeds()

        self.maximum.emit(len(feeds_list))

        report = {
            "progress": 0,
            "entries": 0,
            "feeds": 0
        }

        for i, feed in enumerate(feeds_list):
            if self.request_stop:
                break

            self.current.emit(feed["author"])

            num_purged = feeds.purge_feed(
                feed["id"],
                settings.value("purge/entries_to_keep", type=int),
                settings.value("purge/keep_unviewed",  type=bool)
            )

            report["entries"] += num_purged
            report["feeds"] += num_purged > 0
            report["progress"] = i+1
            self.report.emit(report)

        logger.debug(f"Purged {report['entries']} entries in {report['feeds']} feeds.")


class PurgeFeedTask(BaseTask):
    def __init__(self, feed_id: int):
        super(PurgeFeedTask, self).__init__()
        self.feed_id = feed_id

    def task(self):
        feeds = Feeds()
        feeds.purge_feed(
            self.feed_id,
            settings.value("purge/entries_to_keep", type=int),
            settings.value("purge/keep_unviewed",  type=bool)
        )


class FeedsUpdateTask(BaseTask):
    _finished = pyqtSignal()

    def task(self):
        Feeds().update_feeds(interval=0.5)
        self._finished.emit()


class FeedUpdateTask(BaseTask):
    def __init__(self, feed_id: int):
        super(FeedUpdateTask, self).__init__()
        self.feed_id = feed_id

    def task(self):
        Feeds().update_feed(feed_id=self.feed_id)


class AddFeedTask(BaseTask):
    added = pyqtSignal(int)

    def __init__(self, url: str, category: str, name: str):
        super(AddFeedTask, self).__init__()
        self.url = url
        self.category = category
        self.name = name

    def task(self):
        feeds = Feeds()
        feed_id = feeds.add_feed(self.url, self.category, self.name)
        if feed_id is None:
            logger.error(f"AddFeedTask: adding '{self.url}' failed.")
            self.failed.emit()
            return
        feeds.update_feed_entries(feed_id)
        self.added.emit(feed_id)


class ImportFeedsTask(BaseTask):
    imported = pyqtSignal(int)

    def __init__(self, fname: str):
        super(ImportFeedsTask, self).__init__()
        self.fname = fname

    def task(self):
        try:
            with open(self.fname, "r") as f:
                j = json.load(f)
        except FileNotFoundError:
            logger.error(f"ImportFeedsTask failed: {self.name} does not exist.")
            self.failed.emit()
            return

        feeds = Feeds()

        for entry in j:
            feed_id = feeds.add_feed(entry["url"], entry["category"], feed_name=entry["author"])
            if feed_id is None:
                logger.error(f"ImportFeedsTask: adding '{entry['url']}' failed.")
                continue
            self.imported.emit(feed_id)


class ExportFeedsTask(BaseTask):
    def __init__(self, fname: str):
        super(ExportFeedsTask, self).__init__()
        self.fname = fname

    def task(self):
        feeds = Feeds()

        j = [
            {
                "author": feed["author"],
                "category": feed["category"],
                "url": feed["url"]
            }
            for feed in feeds.get_feeds()
        ]

        with open(self.fname, "w") as f:
            json.dump(j, f, indent=4)


class ImportFiltersTask(BaseTask):
    imported = pyqtSignal(int)

    def __init__(self, fname: str):
        super(ImportFiltersTask, self).__init__()
        self.fname = fname

    def task(self):
        try:
            with open(self.fname, "r") as f:
                j = json.load(f)
        except FileNotFoundError:
            logger.error(f"ImportFiltersTask failed: {self.name} does not exist.")
            self.failed.emit()
            return

        ...


class ExportFiltersTask(BaseTask):
    def __init__(self, fname: str):
        super(ExportFiltersTask, self).__init__()
        self.fname = fname

    def task(self):
        ...

        # with open(self.fname, "w") as f:
        #     json.dump(j, f, indent=4)


class SaveThumbnailTask(BaseTask):
    def __init__(self, img_url: str, fname: str):
        super(SaveThumbnailTask, self).__init__()
        self.img_url = img_url
        self.fname = fname

    def task(self):
        downloader = Downloader()
        if content := downloader.get_bytes(self.img_url):
            with open(self.fname, "wb") as f:
                f.write(content)


class ExportSettingsTask(BaseTask):
    success = pyqtSignal()

    def __init__(self, path: str):
        super(ExportSettingsTask, self).__init__()
        self.path = path

    def task(self):
        settings.export(self.path)
        self.success.emit()


class ImportSettingsTask(BaseTask):
    success = pyqtSignal()

    def __init__(self, path: str):
        super(ImportSettingsTask, self).__init__()
        self.path = path

    def task(self):
        settings.load(self.path)
        self.success.emit()
