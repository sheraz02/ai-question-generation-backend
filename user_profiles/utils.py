# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from django.conf import settings



# def send_activation_email(recipient_email, activation_url):
#     subject = f"Activate your account on {settings.SITE_NAME}."
#     from_email = settings.EMAIL_HOST_USER
#     to = [recipient_email]

#     html_content = render_to_string('account/activation_email.html', {'activation_url': activation_url})

#     text_content = strip_tags(html_content)
#     email = EmailMultiAlternatives(subject, text_content, from_email, to)
#     email.attach_alternative(html_content, "text/html")
#     email.send()



from django.core.mail import send_mail
from django.conf import settings

def send_activation_email(recipient_email, activation_url):
    
    subject = "Activate your account"
    message = f"Click the link to activate your account:\n\n{activation_url}"
    from_email = settings.EMAIL_HOST_USER

    send_mail(
        subject,
        message,
        from_email,
        [recipient_email],
        fail_silently=False,
    )
