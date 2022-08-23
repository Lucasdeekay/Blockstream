from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse

from SiteHome.forms import ContactForm
from mysite.settings import EMAIL_HOST_USER


def home(request):
    return render(request, "sitehome/home.html")


def about(request):
    return render(request, "sitehome/about.html")


def faq(request):
    return render(request, "sitehome/faq.html")


def contact(request):
    # Check if form was submitted
    if request.method == 'POST':
        # get form
        form = ContactForm(request.POST)
        # Check if form is valid
        if form.is_valid():
            # Get form data
            name = form.cleaned_data.get('name').strip()
            email = form.cleaned_data.get('email').strip()
            message = form.cleaned_data.get('message').strip()
            msg = f'from: {name.capitalize()}<br>email: {email}<br><br><p><b>{message}</b></p>'

            # Create and send mail to the clientele
            subject = 'Password Recovery'
            context = {'subject': subject, 'msg': msg, 'clientele': "Admin"}
            html_message = render_to_string('useraccount/msg.html', context=context)

            send_mail(subject, message, EMAIL_HOST_USER, [EMAIL_HOST_USER], html_message=html_message,
                      fail_silently=False)
            # Display message
            messages.success(request, "Message successfully sent")
            # Redirect to password retrieval page
            return HttpResponseRedirect(reverse('SiteHome:contact'))

    # Check if form was not submitted
    else:
        # Get form
        form = ContactForm()
    # Render contact password page
    return render(request, "sitehome/contact.html", {'form': form})


def legal_doc(request):
    return render(request, "sitehome/legal_doc.html")


def privacy(request):
    return render(request, "sitehome/privacy.html")


def error_404(request, exception):
    return render(request, 'useraccount/404.html')
