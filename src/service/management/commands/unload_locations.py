import csv
from decimal import Decimal
from django.core.management.base import BaseCommand
from service.models import Location


class Command(BaseCommand):
    help = "Unload location data from CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", help="Path to the CSV file")

    def handle(self, *args, **options):
        csv_file = options["csv_file"]
        with open(csv_file, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                zip_code = row[0]
                lat = row[1]
                lng = row[2]
                city = row[3]
                state_name = row[5]
                try:
                    latitude = Decimal(lat)
                    longitude = Decimal(lng)
                except Decimal.InvalidOperation:
                    self.stdout.write(
                        self.style.WARNING(f"Invalid format of decimal: {lat}, {lng}")
                    )
                    continue
                locations = Location.objects.filter(zip_code=zip_code)
                if locations.exists():
                    self.stdout.write(
                        self.style.WARNING(
                            f"Duplicate location with latitude={latitude}, longitude={longitude} found"
                        )
                    )
                    continue
                location = Location.objects.create(
                    latitude=latitude,
                    longitude=longitude,
                    city=city,
                    state=state_name,
                    zip_code=zip_code,
                )
                self.stdout.write(self.style.SUCCESS(f'Location "{location}" created.'))
        self.stdout.write(self.style.SUCCESS("Data unloading completed."))
