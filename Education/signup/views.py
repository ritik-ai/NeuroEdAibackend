from django.shortcuts import render
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse



# Create your views here.
@csrf_exempt
def send_verification_email(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if email:
            verification_code = get_random_string(length=6,allowed_chars='012345679')
            request.session['verification_code'] = verification_code

            send_mail(
                'your erification code ',
                f'your verification code is {verification_code}',
                'ritikparte93@gmail.com',
                [email],
                fail_silently=False,
            )
            
            return JsonResponse({'message': 'Verification code sent successfully'})
        return JsonResponse({'error': 'Email is required'}, status=400)



