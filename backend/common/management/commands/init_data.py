import datetime
import logging
import pathlib
import csv

from django.core import serializers
from django.core.management.base import BaseCommand

from stock_trading.models.asset_allocation_recommendation import (
    AssetAllocationRecommendation,
)
from system_settings.models.social_media_link import SocialMediaLink

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, **options):
        logger.debug("Init data called.")

        try:
            if not AssetAllocationRecommendation.objects.exists():
                AssetAllocationRecommendation.objects.create(
                    money=70,
                    stock=30,
                )
                logger.debug(
                    "Creating asset allocation recommendation data called success."
                )
            if not SocialMediaLink.objects.exists():
                SocialMediaLink.objects.create(
                    facebook_link="https://www.facebook.com/tdkcapital",
                    zalo_link="https://zalo.me/tdkcapital",
                    youtube_link="https://www.youtube.com/tdkcapital",
                    instagram_link="https://www.instagram.com/tdkcapital",
                    tiktok_link="https://www.tiktok.com/tdkcapital",
                    linkedin_link="https://www.linkedin.com/tdkcapital",
                    twitter_link="https://www.twitter.com/tdkcapital",
                    telegram_link="https://t.me/tdkcapital",
                    whatsapp_link="https://wa.me/tdkcapital",
                )
                logger.debug("Creating social media link data called success.")
        except Exception as e:
            logger.error("Init data data FAILED", exc_info=e)
