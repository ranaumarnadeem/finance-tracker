from django.shortcuts import render # type: ignore
from django.http import HttpResponse # type: ignore
from django.views import View # type: ignore
from .forms import ReservationForm
from django.shortcuts import render # type: ignore

def hello_world(request):
    return HttpResponse("Hello, World!")

class Helloethopia(View):
    def get(self, request):
        return HttpResponse("Hello, Ethiopia!")

def home(request):
    print(">>> HOME VIEW CALLED <<<") 
    form = ReservationForm()
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Reservation successful!")
    return render(request, 'index.html', {'form': form})
