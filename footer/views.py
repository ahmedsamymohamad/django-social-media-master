from django.shortcuts import render
from .forms import ContactForm
from django.http import JsonResponse
from .models import Facts
import random
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def contact(request):

	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			form.save()
   
			message = form.cleaned_data['message']
			email = form.cleaned_data['email']
   
			send_mail(
				'Subject: Contact Form Submission',
				f'from: {email},\nMessage:\n{message}',
				settings.EMAIL_HOST_USER,  # Sender's email address
				['ahmed01223330@gmail.com'],  # Receiver's email address
				fail_silently=False,
			)
			message = "Your Message/Feedback is sent, manager@postchatub will contact you soon. Thank You."
			return render(request,'footer/contact.html',{'message':message})
	else:
		form = ContactForm()
		context = {'form':form}
		return render(request,'footer/contact.html',context)

def contribute(request):
	return render(request,'footer/contribute.html')

def sponsor(request):
	return render(request,'footer/sponsor.html')

def guidelines(request):
	return render(request,'footer/guidelines.html')

def about(request):
	return render(request,'footer/about.html')

def facts(request):
	# facts = Facts.objects.all()
	# facts_list = []
	# for fact in facts:
	# 	facts_list.append(fact.fact)
	# random_facts = random.sample(facts_list, 3)
	data = {

		'facts':[]

	}
	return JsonResponse(data)
	

def error_404_view(request,exception):
	return render(request,'footer/404.html')