import datetime
import os
from optparse import make_option

from django.utils.timezone import utc
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction

from house.main import models
from house.main.api import process_document_text


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--dry-run', action='store_true', dest='dry_run', default=False,
                    help="Run but cancel the whole transaction in the end"),
    )
    def handle(self, dry_run=False, **options):
        verbosity = int(options['verbosity'])
        verbose = verbosity > 1

        # start transaction
        transaction.enter_transaction_management()
        transaction.managed(True)

        count = 0

        for document in models.Document.objects.filter(text_extracted=False):
            if verbose:
                print "PROCESS", repr(document)

            process_document_text(document)

            count += 1

        if verbose:
            print "\nIN SUMMARY".ljust(70, '=')
            print count, "documents records processed"
            print "\n"
        if dry_run:
            transaction.rollback()
        else:
            transaction.commit()

        transaction.leave_transaction_management()
