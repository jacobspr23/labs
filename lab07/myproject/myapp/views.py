import segno
from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        qrcode = segno.make(data)
       
        #generate a data URI to display qr code
        qr_uri = qrcode.svg_data_uri(scale=4)

        context = {'qr_uri': qr_uri, 'data': data}
        return render(request, 'myapp/home.html', context)
    
    return render(request, 'myapp/home.html')

