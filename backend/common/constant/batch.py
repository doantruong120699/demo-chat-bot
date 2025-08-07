from enum import Enum


class BatchDefinition(str, Enum):
    """Enumerate all possible batch categories.
    The format of each enum member: [Batch_Code] = [Batch_Name]
    """

    BT001 = "BT001"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class BatchStatus(int, Enum):
    """Batch running status."""

    RUNNING = 1
    NOT_RUNNING = 2
    STOPPED = 3


class BatchSleepSeconds(int, Enum):
    """Time duration between 2 consecutive batch running."""

    BT001 = 60


class BatchManagement(str, Enum):
    BT001 = "BT001"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class BatchTimeSetting(Enum):
    BT000 = "*", "*", "*", "*", "*", 00  # Every minute

    @property
    def cron_job_scheduler(self):
        return dict(
            year=self.value[0],
            month=self.value[1],
            day=self.value[2],
            hour=self.value[3],
            minute=self.value[4],
            second=self.value[5],
        )
