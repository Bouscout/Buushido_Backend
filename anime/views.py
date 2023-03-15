from django.shortcuts import render
def maintenance(request, exception):
    return render(request, 'maintenance.html', status=404)