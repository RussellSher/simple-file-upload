from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from uploads.core.models import Document
from uploads.core.forms import DocumentForm
from django.core.exceptions import ObjectDoesNotExist


def home(request):
    documents = Document.objects.all()
    # try:
    #     document1 = Document.objects.get(pk=41)
    #     print(document1[0])
    # except ObjectDoesNotExist:
    #     print("does not exist")
    return render(request, 'core/home.html', { 'documents': documents })


def delete(request, pk):
    if request.method =='POST':
        book =  Document.objects.get(pk=pk)
        #book.delete
        print(book.uploaded_at)
        print(book.document) 
        delete_result = book.delete()
        print(delete_result)
           
        return HttpResponseRedirect(reverse("home"))       


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'core/simple_upload.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })
