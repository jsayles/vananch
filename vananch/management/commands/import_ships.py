from django.conf import settings
from django.utils.timezone import localtime, now
from django.core.management.base import BaseCommand, CommandError

from vananch.importer import ShipImporter

class Command(BaseCommand):
    help = "Import Ship Data"
    requires_system_checks = True

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--quiet',
            action='store_true',
            dest='run_quiet',
            default=False,
            help='Quiet all print statements',
        )

    def handle(self, *args, **options):
        if not hasattr(settings, 'PORT_URL'):
            raise CommandError("Missing PORT_URL setting")
        if not hasattr(settings, 'USER_AGENT'):
            raise CommandError("Missing USER_AGENT setting")

        importer = ShipImporter()
        importer.import_ships(quiet=options['run_quiet'])
