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
                if len(row) >= 5:
                    lat, lng, city, state_name, *_ = row
                    zip_code = ""

                    if len(row) > 5:
                        zip_code = row[0]
                    try:
                        latitude = Decimal(lat) #NEED_TO_FIX
                        longitude = Decimal(lng)
                    except Decimal.InvalidOperation:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Invalid format of decimal: {lat}, {lng}"
                            )
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
                    self.stdout.write(
                        self.style.SUCCESS(f'Location "{location}" created.')
                    )
        self.stdout.write(self.style.SUCCESS("Data unloading completed."))
