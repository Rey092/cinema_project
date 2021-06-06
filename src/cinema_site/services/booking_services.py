from django.shortcuts import get_object_or_404
from cinema_site.models import Ticket, Seance
from profiles.models import UserProfile


def handle_booking_ajax(request):
    tickets_count = int(request.POST['tickets_count'])
    process_type = request.POST['process_type']
    seance_id = request.POST['seance']
    is_paid = True if process_type == 'buyBtn' else False
    seance = get_object_or_404(Seance, pk=seance_id)
    buyer = UserProfile.objects.first()

    tickets = []

    for i in range(tickets_count):
        ticket_data = str(request.POST['ticket' + str(i + 1)]).split('.')

        row = ticket_data[0]
        seat_place = ticket_data[1]

        new_ticket = Ticket(
            row=row,
            seat_place=seat_place,
            is_paid=is_paid,
            seance=seance,
            buyer=buyer,
        )
        new_ticket.full_clean()
        tickets.append(new_ticket)

    for ticket in tickets:
        ticket.save()
    return {'status': 'success'}
