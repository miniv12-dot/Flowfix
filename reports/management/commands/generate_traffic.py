import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from reports.models import WaterFaultReport, WorkOrder

class Command(BaseCommand):
    help = 'Generates mock civic data to populate the live dashboard for portfolio display.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Initiating Civic Data Ingestion...'))
        WaterFaultReport.objects.all().delete()
        
        self.stdout.write(self.style.WARNING('Old data wiped. Generating fresh reports...'))

        # 1. Realistic Issue Dictionaries (Mapped to your exact SEVERITY_CHOICES)
        issues = [
            {"title": "Major Pipe Burst", "severity": "HIGH", "desc": "Water flooding the intersection rapidly."},
            {"title": "Steady Leak on Pavement", "severity": "MED", "desc": "Water pooling near the storm drain."},
            {"title": "Fire Hydrant Drip", "severity": "LOW", "desc": "Minor drip from the valve cap."},
            {"title": "Sewage Mix-up", "severity": "HIGH", "desc": "Contaminated water leaking into residential road."},
            {"title": "Underground Rumbling/Leak", "severity": "MED", "desc": "Can hear water rushing under the driveway."}
        ]

        # 2. Bounding Box Coordinates (Pinetown / Kloof / Hillcrest Area)
        lat_min, lat_max = -29.8200, -29.7500
        lng_min, lng_max = 30.7800, 30.8800

        # 3. Generate 15 Mock Reports
        reports_created = 0
        for i in range(15):
            issue = random.choice(issues)
            
            # Generate random coordinates within the bounding box
            lat = round(random.uniform(lat_min, lat_max), 6)
            lng = round(random.uniform(lng_min, lng_max), 6)

            # Create the Report using WaterFaultReport
            report = WaterFaultReport.objects.create(
                title=issue['title'],  # <-- Clean title here
                description=issue['desc'],
                latitude=lat,
                longitude=lng,
                severity=issue['severity'],
                street_address="Geospatial Auto-Pin",
            )
            
            # 4. Automate Work Orders
            status_choices = ['PENDING', 'DISPATCHED', 'IN_PROGRESS', 'RESOLVED']
            teams = ['Team Alpha', 'Team Bravo', 'Team Charlie', 'Delta Unit']
            
            # Weighted random choice so the map has active issues
            chosen_status = random.choices(status_choices, weights=[40, 30, 20, 10])[0]
            
            assigned = random.choice(teams) if chosen_status != 'PENDING' else ""

            WorkOrder.objects.create(
                report=report,
                status=chosen_status,
                assigned_team=assigned,
                date_updated=timezone.now()
            )
            
            reports_created += 1

        self.stdout.write(self.style.SUCCESS(f'✅ Successfully injected {reports_created} live tickets and dispatch workflows into the database!'))