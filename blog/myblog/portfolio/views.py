from django.shortcuts import get_object_or_404, render
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

from .models import Post


def home(request):
    posts = Post.objects.all()[:5]
    return render(request, "portfolio/home.html", {"posts": posts})


#def post_detail(request, slug):
   # post = get_object_or_404(Post, slug=slug)
    #return render(request, "portfolio/post_detail.html", {"post": post})

def about(request):
    return render(request, "portfolio/about.html")


#def portfolio_page(request):
    #return render(request, "portfolio/portfolio_page.html")

def services_page(request):
    return render(request, "portfolio/services_page.html")

#def resume(request):
    #return render(request, "portfolio/resume.html")


def contact_page(request):
    # Keep existing form behavior for non-API (traditional POST)
    if request.method == "POST" and request.headers.get('x-requested-with') != 'XMLHttpRequest':
        msg_name = request.POST.get("msg_name")
        msg_email = request.POST.get("msg_email")           
        msg_subject = request.POST.get("msg_subject")
        message = request.POST.get("message")

        try:
            send_mail(
                msg_subject,
                message,
                msg_email,
                ['wilsonmaseko94@gmail.com'],
            )
        except Exception as e:
            #return render(request, "portfolio/contact_page.html", {'error': str(e)})

         return render(request, "portfolio/contact_page.html", {'msg_name': msg_name})

    return render(request, "portfolio/contact_page.html", {})


@csrf_exempt
def contact_api(request):
    """
    Dedicated API endpoint for contact submissions.
    Accepts JSON body: {msg_name, msg_email, msg_subject, message}
    Returns JSON: {success: True, msg_name: ...} or {success: False, error: '...'}
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

    # Parse JSON body (fallback to POST form data)
    try:
        if request.content_type == 'application/json':
            payload = json.loads(request.body.decode('utf-8'))
        else:
            payload = request.POST.dict()
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Invalid request payload'}, status=400)

    msg_name = payload.get('msg_name') or payload.get('name') or ''
    msg_email = payload.get('msg_email') or payload.get('email') or ''
    msg_subject = payload.get('msg_subject') or payload.get('subject') or 'Contact Form Message'
    message = payload.get('message') or ''

    if not msg_name or not msg_email or not message:
        return JsonResponse({'success': False, 'error': 'Name, email and message are required'}, status=400)

    try:
        send_mail(
            msg_subject,
            f"Message from: {msg_name} <{msg_email}>\n\n{message}",
            # Use a configured from address if available to avoid SMTP rejections
            getattr(settings, 'DEFAULT_FROM_EMAIL', msg_email),
            [getattr(settings, 'CONTACT_RECIPIENT_EMAIL', 'wilsonmaseko94@gmail.com')],
            fail_silently=False,
        )
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': True, 'msg_name': msg_name})
