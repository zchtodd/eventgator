from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from core.models import Event, UserEventRegistration
from core.forms import EventForm


def search_view(request):
    events = []

    if request.method == "POST":
        query = request.POST.get("q")
        if query:
            events = Event.objects.prefetch_related("registrations").filter(name__icontains=query)

    if not events:
        events = Event.objects.prefetch_related("registrations").all()

    return render(request, "core/event_search.html", {"events": events})


@login_required
def event_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user = request.user
    
    # try:
    #     event = Event.objects.get(pk=event_id)
    # except Event.DoesNotExist:
    #     raise Http404("Event does not exist")
        
    registration = UserEventRegistration.objects.filter(user=user, event=event).first()
    return render(
        request, "core/event.html", {"event": event, "registration": registration}
    )

    
@login_required
def event_create_view(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return redirect("event", event_id=event.id)
    else:
        form = EventForm()
    return render(request, "core/event_edit.html", {"form": form, "event": None})


@login_required
def event_edit_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            return redirect("event", event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, "core/event_edit.html", {"form": form, "event": event})


@login_required
def event_register_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    registration = UserEventRegistration.objects.filter(
        user=request.user, event=event
    ).first()

    if not registration:
        UserEventRegistration.objects.create(user=request.user, event=event)

    return redirect("event", event_id=event.id)


@login_required
def event_unregister_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user = request.user

    registration = UserEventRegistration.objects.filter(user=user, event=event).first()

    if registration:
        registration.delete()

    return redirect("event", event_id=event.id)