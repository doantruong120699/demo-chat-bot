# Generated migration for pgvector and DocumentChunk model

from django.db import migrations
from django.contrib.postgres.operations import CreateExtension


class Migration(migrations.Migration):

    dependencies = [
        ('document_training', '0002_chatsession_and_more'),
    ]

    operations = [
        # Enable pgvector extension
        CreateExtension('vector'),
    ]
