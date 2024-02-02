from django.shortcuts import render, HttpResponse
from example.forms import AboutForm
from example.models import About

# Create your views here.
def home(request):
    form = AboutForm()
    if request.method == 'POST':
        form = AboutForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            about = form.save()
            return HttpResponse(f'About succesfully updated. \n {about.name} | {about.state} | {about.lga}')
    return render(request, 'example/home.html', {'form': form})


def update_about(request, pk):
    about = About.objects.get(pk=pk)
    form = AboutForm(instance=about)
    if request.method == 'POST':
        form = AboutForm(request.POST, instance=about)
        if form.is_valid():
            about = form.save()
            return HttpResponse(f'About succesfully updated. \n {about.name} | {about.state} | {about.lga}')
    return render(request, 'example/update_about.html', {'form': form})