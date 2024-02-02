from django.shortcuts import render, HttpResponse
from .forms import AboutForm

# Create your views here.
def home(request):
    form = AboutForm()
    if request.method == 'POST':
        form = AboutForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return HttpResponse('saved successfully')
    return render(request, 'example/home.html', {'form': form})