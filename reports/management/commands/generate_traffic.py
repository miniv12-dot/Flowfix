import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from reports.models import WaterFaultReport, WorkOrder, CommunityMessage

class Command(BaseCommand):
    help = 'Generates mock civic data and chat history to populate the live dashboard for portfolio display.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Initiating Civic Data Ingestion...'))

        # Wipe old data for a fresh demo state
        WaterFaultReport.objects.all().delete()
        CommunityMessage.objects.all().delete()
        
        self.stdout.write(self.style.WARNING('Old data wiped. Generating fresh reports and chat...'))

        # ---------------------------------------------------------
        # 1. GENERATE MAP PINS (Water Faults & Work Orders)
        # ---------------------------------------------------------
        issues = [
            {"title": "Major Pipe Burst", "severity": "HIGH", "desc": "Water flooding the intersection rapidly."},
            {"title": "Steady Leak on Pavement", "severity": "MED", "desc": "Water pooling near the storm drain."},
            {"title": "Fire Hydrant Drip", "severity": "LOW", "desc": "Minor drip from the valve cap."},
            {"title": "Sewage Mix-up", "severity": "HIGH", "desc": "Contaminated water leaking into residential road."},
            {"title": "Underground Rumbling/Leak", "severity": "MED", "desc": "Can hear water rushing under the driveway."}
        ]

        lat_min, lat_max = -29.8200, -29.7500
        lng_min, lng_max = 30.7800, 30.8800

        reports_created = 0
        for i in range(15):
            issue = random.choice(issues)
            lat = round(random.uniform(lat_min, lat_max), 6)
            lng = round(random.uniform(lng_min, lng_max), 6)

            report = WaterFaultReport.objects.create(
                title=issue['title'],
                description=issue['desc'],
                latitude=lat,
                longitude=lng,
                severity=issue['severity'],
                street_address="Geospatial Auto-Pin",
            )
            
            status_choices = ['PENDING', 'DISPATCHED', 'IN_PROGRESS', 'RESOLVED']
            teams = ['Team Alpha', 'Team Bravo', 'Team Charlie', 'Delta Unit']
            chosen_status = random.choices(status_choices, weights=[40, 30, 20, 10])[0]
            assigned = random.choice(teams) if chosen_status != 'PENDING' else ""

            WorkOrder.objects.create(
                report=report,
                status=chosen_status,
                assigned_team=assigned,
                date_updated=timezone.now()
            )
            reports_created += 1

        # ---------------------------------------------------------
        # 2. GENERATE COMMUNITY CHAT DEMO (The Neighborhood Hub)
        # ---------------------------------------------------------
        # Create 3 fake neighbor accounts
        sarah, _ = User.objects.get_or_create(username="Sarah_Kloof")
        mike, _ = User.objects.get_or_create(username="Mike_Pinetown")
        dave, _ = User.objects.get_or_create(username="Dave_M13")

        # Create a realistic conversation script
        demo_conversation = [
            (sarah, "Anyone else experiencing low water pressure around Fields Hill?"),
            (mike, "Yes! Just noticed it about 10 minutes ago while washing dishes."),
            (dave, "I just checked the FlowFix live radar. Looks like a major pipe burst was just reported nearby on the M13."),
            (sarah, "Ah, that explains it. Hopefully the municipal team is dispatched soon."),
            (mike, "Looks like the ticket status just changed to 'Team Dispatched' on the map! FlowFix is pretty fast today."),
            (dave, "Awesome. Keep an eye out for the water truck guys.")
        ]

        # Inject the conversation into the database
        demo_suburb = "Pinetown" # Must match your default view fallback
        
        for user, text in demo_conversation:
            CommunityMessage.objects.create(
                sender=user,
                suburb=demo_suburb,
                content=text
            )

        self.stdout.write(self.style.SUCCESS(f'✅ Successfully injected {reports_created} tickets and 1 active community chat thread!'))