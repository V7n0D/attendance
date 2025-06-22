
from .sheets_manager import mark_attendance
from django.shortcuts import render 

def mark_attendance_view(request):
    print(f"DEBUG: Received {request.method} request")  # 👈 Add this
    if request.method == 'POST':
        action = request.POST.get("action")
        print(f"DEBUG: action = {action}")  # 👈 Add this
        if action in ["clock_in","clock_out"]:
            print("✅ Calling mark_attendance()")  # Add this
            mark_attendance(action)
    return render(request, 'mark.html')


# Create your views here.
