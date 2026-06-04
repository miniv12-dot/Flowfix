import json # <-- Make sure this is at the very top of your file!
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReportFaultForm
from .models import WaterFaultReport # <-- Add this to your model imports!
from django.db.models import Count, Q
from .models import WorkOrder
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import CommunityMessage


def community_hub(request):
    # Safely check if the user is logged in before checking their suburb
    if request.user.is_authenticated:
        try:
            user_suburb = request.user.residentprofile.suburb or 'Pinetown'
        except:
            user_suburb = 'Pinetown'
    else:
        user_suburb = 'Pinetown' # Recruiters will default to Pinetown to see the demo data
        
    return render(request, 'reports/community_hub.html', {'suburb': user_suburb})


def fetch_messages(request, suburb):
    messages = CommunityMessage.objects.filter(suburb=suburb).order_by('timestamp')
    data = []
    for msg in messages:
        data.append({
            'sender': msg.sender.username if msg.sender else 'Unknown',
            'content': msg.content,
            'timestamp': msg.timestamp.strftime('%I:%M %p'),
            'is_me': msg.sender == request.user if request.user.is_authenticated else False
        })
    return JsonResponse({'messages': data})

@login_required
def send_message(request, suburb):
    # This API receives new messages from the chat box
    if request.method == 'POST':
        data = json.loads(request.body)
        content = data.get('content')
        if content:
            CommunityMessage.objects.create(sender=request.user, suburb=suburb, content=content)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def report_fault(request):
    if request.method == 'POST':
        form = ReportFaultForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form to the database
            report = form.save()
            request.session['recent_ticket_id'] = report.id
            
            # Format the ID into a cool tracking code
            tracking_code = f"FIX-{report.id}"
            
            # Show the NEW success message with the code
            messages.success(request, f"Report submitted successfully! Your tracking code is: {tracking_code}")
            
            return redirect('report_fault') 
    else:
        form = ReportFaultForm()

    return render(request, 'reports/report_form.html', {'form': form})

    return render(request, 'reports/report_form.html', {'form': form})

def public_map(request):
    """
    Fetches all active reports and passes them as JSON to the frontend map.
    """
    reports = WaterFaultReport.objects.all()
    
    # We build a simple dictionary for each report so JavaScript can read it
    reports_list = []
    for report in reports:
        if report.latitude and report.longitude: # Only grab ones with GPS data
            reports_list.append({
                'id': report.id,
                'title': report.title,
                'severity': report.get_severity_display(),
                'lat': float(report.latitude),
                'lng': float(report.longitude)

            })
            
    # Convert the Python list into a JSON string
    context = {
        'reports_json': json.dumps(reports_list)
    }
    
    return render(request, 'reports/public_map.html', context)

def municipality_dashboard(request):
    """
    Internal dashboard for city workers to track metrics and triage work orders.
    """
    active_orders = WorkOrder.objects.exclude(status='RESOLVED').order_by('-date_updated')
    total_faults = WaterFaultReport.objects.count()
    
    # 1. Top Level Metrics
    severity_stats = WaterFaultReport.objects.aggregate(
        high_priority=Count('id', filter=Q(severity='HIGH')),
        pending_review=Count('work_order', filter=Q(work_order__status='PENDING'))
    )

    # 2. Data Preparation for Chart.js (Severity Breakdown)
    severity_data = {
        'High (Burst/Flood)': WaterFaultReport.objects.filter(severity='HIGH').count(),
        'Medium (Steady Leak)': WaterFaultReport.objects.filter(severity='MED').count(),
        'Low (Minor Drip)': WaterFaultReport.objects.filter(severity='LOW').count(),
    }

    # 3. Data Preparation for Chart.js (Work Order Status)
    status_data = {
        'Pending Review': WorkOrder.objects.filter(status='PENDING').count(),
        'Team Dispatched': WorkOrder.objects.filter(status='DISPATCHED').count(),
        'In Progress': WorkOrder.objects.filter(status='IN_PROGRESS').count(),
        'Fully Resolved': WorkOrder.objects.filter(status='RESOLVED').count(),
    }

    context = {
        'active_orders': active_orders,
        'total_faults': total_faults,
        'high_priority': severity_stats['high_priority'],
        'pending_review': severity_stats['pending_review'],
        
        # We use json.dumps so JavaScript can read these Python lists
        'sev_labels': json.dumps(list(severity_data.keys())),
        'sev_values': json.dumps(list(severity_data.values())),
        'stat_labels': json.dumps(list(status_data.keys())),
        'stat_values': json.dumps(list(status_data.values())),
    }

    return render(request, 'reports/dashboard.html', context)

from .models import WaterFaultReport # Make sure this is imported at the top

def track_report(request):
    report_obj = None
    work_order_obj = None
    search_query = request.GET.get('code')

    # 1. Figure out which ticket to look for (from search bar or session)
    if search_query:
        clean_id = search_query.replace('FIX-', '').strip()
        report_obj = WaterFaultReport.objects.filter(id=clean_id).first()
    else:
        recent_id = request.session.get('recent_ticket_id')
        if recent_id:
            report_obj = WaterFaultReport.objects.filter(id=recent_id).first()

    # 2. If we found a report, grab its active Work Order status
    if report_obj:
        try:
            work_order_obj = report_obj.work_order
        except:
            work_order_obj = None

    # 3. Send it to the template using the exact names the HTML expects!
    return render(request, 'reports/track_report.html', {
        'report': report_obj,           # Changed from 'ticket' to 'report'
        'work_order': work_order_obj,   # Passes the dispatch status
        'auto_loaded': not search_query and report_obj is not None,
        'query': search_query or ''     # Keeps the search bar populated
    })

def home(request):
    """
    The landing page for the FlowFix application.
    """
    return render(request, 'reports/home.html')

