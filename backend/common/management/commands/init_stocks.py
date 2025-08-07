import datetime
import logging
import pathlib
import csv

from django.core import serializers
from django.core.management.base import BaseCommand

from stock_trading.models import StockSymbol

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def _insert_data(self, folder):
        folder_path = pathlib.Path(folder)
        for file in folder_path.rglob("*.csv"):
            logger.debug(f"File: {file}")
            try:
                if file.is_file():
                    with file.open(newline="") as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            logger.debug(f"Symbol: {row['symbol']}")
                            stock_symbol, created = StockSymbol.objects.get_or_create(
                                symbol=row["symbol"],
                                defaults={
                                    "exchange": row["exchange"],
                                    "type": row["type"],
                                    "organ_short_name": row["organ_short_name"],
                                    "organ_name": row["organ_name"],
                                    "created_at": datetime.datetime.now(
                                        datetime.timezone.utc
                                    ),
                                    "updated_at": datetime.datetime.now(
                                        datetime.timezone.utc
                                    ),
                                },
                            )
                            if not created:
                                # Update fields if the stock symbol already exists
                                stock_symbol.exchange = row["exchange"]
                                stock_symbol.type = row["type"]
                                stock_symbol.organ_short_name = row["organ_short_name"]
                                stock_symbol.organ_name = row["organ_name"]
                                stock_symbol.updated_at = datetime.datetime.now(
                                    datetime.timezone.utc
                                )
                                stock_symbol.save()
            except Exception as e:
                logger.error(f"Error while inserting data from file {file}", exc_info=e)

    def handle(self, **options):
        logger.debug("Creating stocks data called.")

        try:
            self._insert_data("common/management/assets")
            logger.debug("Creating stocks data called success.")
        except Exception as e:
            logger.error("Creating stocks data FAILED", exc_info=e)
