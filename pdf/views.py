import pdfkit
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import Profile


# Create your views here.
def list(request):

  profiles = Profile.objects.all()

  return render(request, 'pdf/list.html', { 'profiles': profiles } )


def accept(request):

  if 'POST' == request.method:
    name = request.POST.get('name', '')
    email = request.POST.get('email', '')
    phone = request.POST.get('phone', '')
    summary = request.POST.get('summary', '')
    degree = request.POST.get('degree', '')
    school = request.POST.get('school', '')
    university = request.POST.get('university', '')
    previous_work = request.POST.get('previous_work', '')
    skills = request.POST.get('skills', '')

    profile = Profile(
      name = name,
      email = email,
      phone = phone,
      summary = summary,
      degree = degree,
      school = school,
      university = university,
      previous_work = previous_work,
      skills = skills
    )

    profile.save()
  
  return render(request, 'pdf/accept.html')


def resume(request, id):

  profile = Profile.objects.get(pk = id)
  
  template = loader.get_template('pdf/resume.html')

  html = template.render({ 'profile': profile })

  options = { 'page-size': 'Letter', 'encoding': 'UTF-8' }

  path_to_wkhtmltopdf = r'C:\Users\Jack Lee\Documents\Python\wkhtmltox\bin\wkhtmltopdf.exe'

  config = pdfkit.configuration(wkhtmltopdf = path_to_wkhtmltopdf)

  pdf = pdfkit.from_string(html, False, options, configuration = config)

  response = HttpResponse(pdf, content_type = 'application/pdf')
  response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
  
  return response
