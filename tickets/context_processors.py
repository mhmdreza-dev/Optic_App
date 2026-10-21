from .forms import NewTicketForm

def global_ticket_form(request):
    return {
        'ticket_form': NewTicketForm()
    }