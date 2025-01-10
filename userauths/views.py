from django.shortcuts import render
from django.shortcuts import redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import User
from .models import otpToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail


def register(request):

    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully, An OTP has been sent to your email")
            return redirect("userauths:verify-email", username=request.POST['username'])

    context = {
        'form': form,
    }
    return render(request, 'register.html', context)

def verify_email(request, username):
    user = get_user_model().objects.get(username=username)
    user_otp = otpToken.objects.filter(user=user).last()
    email = user.email

    if request.method == 'POST':
        # otp_code = request.POST.get('otp_code')
        # if user_otp.otp_code == request.POST['otp_code']: 
        otp_code = request.POST.get('otp_code')

        if user_otp and user_otp.otp_code == otp_code:
            if user_otp.otp_expires_at > timezone.now():
                user.is_active = True
                user.save()
                user.is_email_verified = True
                messages.success(request, "Account activated successfully, You can Login now.")
                print('Account activated successfully, You can Login now.')
                return redirect("userauths:sign-in")
            else:
                messages.warning(request, "The OTP has expired, get a new OTP!")
                print('The OTP has expired, get a new OTP!')
        else:
            messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
            print('Invalid OTP entered, enter a valid OTP!')

    return render(request, 'verify-token.html', {'username': username, 'email': email})

def resend_otp(request):
    if request.method == 'POST':
        user_email = request.POST['otp_email']
        if get_user_model().objects.filter(email=user_email).exists():
            user = get_user_model().objects.get(email=user_email)
            otp = otpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))

            subject = "Email verification"
            message = f"""

                                Hi {user.username}, here is your OTP - {otp.otp_code}
                                it expires in 5 minutes, user url below to redirect back to the website
                                http://127.0.0.1:8000/user/verify-email/{user.username}

                        """
            
            sender = "taskmanagerprojectmail@gmail.com"
            receiver = [user.email, ]


            send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )

            messages.success(request, "A new OTP has been send to your Email")
            return redirect("userauths:verify-email", username=user.username)

        else:
            messages.success(request, "The Email doesn't exist in the database!")
            return redirect("userauths:resend-otp")

    context = {}

    return render(request, 'resend-otp.html', context)



def login_view(request):

    context = {}
    
    if request.user.is_authenticated:
        messages.success(request, f"You are already logged in")
        print('You are already logged in')
        return redirect('core:index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:

                login(request, user)
                messages.success(request, f"You are logged in {email}")
                print('You are logged in')
                return redirect('core:index')
            

                # if user.is_email_verified:
                #     login(request, user)
                #     messages.success(request, f"You are logged in {email}")
                #     print('You are logged in')
                #     return redirect('core:index')
                # else:
                #     messages.success(request, "User email is not verfied, verify your email with OTP")
                #     return redirect('userauths: verify-email', username=request.POST['username'])

            else:
                messages.warning(request, "User does not exist, Create and account!")
                print('User does not exist, Create an account !')
                
        except:
            messages.warning(request, "Invalid credentials !")
            print('Invalid credentials !')
            error_msg = "Invalid credentials !"
            context['error_msg'] = error_msg

    return render(request, "login.html", context)

def logout_view(request):
    logout(request)
    messages.success(request, "You are logged out")
    return redirect('userauths:sign-in')













# def sent_action_email(user, request):
#     try:
#         current_site = get_current_site(request)
#         email_subject = 'Activate your account'
#         email_body = render_to_string('activate.html', {
#             'user': user,
#             'domain': current_site.domain,
#             'uid': urlsafe_base64_decode(force_bytes(user.pk)),
#             'token': generate_token.make_token(user),
#         })

#         email = EmailMessage(
#             subject=email_subject,
#             body=email_body,
#             from_email=settings.EMAIL_FROM_USER,
#             to=[user.email]
#         )
#         email.send()
#     except Exception as e:
#         print(f"Error sending email: {e}")


# def sent_action_email(user, request):
#     current_site = get_current_site(request)
#     email_subject = 'Activate your account'
#     email_body = render_to_string('activate.html',{
#         'user': user,
#         'domain': current_site,
#         'uid': urlsafe_base64_decode(force_bytes(user.pk)),
#         'token': generate_token.make_token(user),
#     })

#     email = EmailMessage(subject=email_subject, body=email_body,
#                   from_email=settings.EMAIL_FROM_USER,
#                   to=[user.email]
#                   )
#     email.send()



# def verify_email(request, username):
#     user = get_user_model().objects.get(username=username)
#     user_otp = otpToken.objects.filter(user=user).last()
#     email = user.email

#     if request.method == 'POST':

#         if user_otp.otp_code == request.POST['otp_code']:
#             if user_otp.otp_expires_at > timezone.now():
#                 user.is_active=True
#                 user.save()
#                 messages.success(request, "Account activated successfully, You can Login now.")
#                 print('Account activated successfully, You can Login now.')
#                 return redirect("userauths:sign-in")
            
#             else:
#                 messages.warning(request, "The OTP has expired, get a new OTP!")
#                 print('The OTP has expired, get a new OTP!')
#                 return redirect("verify-email", username=user.username)
        
#         else:
#             messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
#             print('Invalid OTP entered, enter a valid OTP!')
#             return redirect('verify-email', username=user.username)
        
#     return render(request, 'verify-token.html', {'username': username, 'email': email})
        


# def login_view(request):
#     context = {}

#     if request.user.is_authenticated:
#         print("You are already logged in!")
#         return redirect('core:index')

#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         try:
#             user = User.objects.get(email=email)
#             user = authenticate(request, email=email, password=password)

#             if not user.is_email_verified:
#                 print('Please Varify you email address, Check your inbox!')
#                 return render(request, 'login.html', context)

#             if user is not None:
#                 login(request, user)
#                 return redirect('core:index')

#             else:
#                 print("User does not exist, Creat an account!")

#         except:
#             error_msg = 'Invalid credentials !'
#             context['error_msg'] = error_msg

#     return render(request, 'login.html', context)

# def activate_user(request, uidb64, token):

#     try:
#         uid = force_bytes(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)

#     except Exception as e:

#         user = None

#     if user and generate_token.check_token(user, token):
#         user.is_email_verified = True
#         user.save()

#         messages.add_message(request, messages.SUCCESS, 'Email verfied, You can now login')
#         return redirect(reverse('userauths:sign-in'))
    
#     return render(request, 'activate-failed.html', {'user': user})



# Unused imports

# from django.conf import settings
# from django.urls import reverse
# from django.core.mail import EmailMessage
# from django.utils.http import urlsafe_base64_decode
# from django.template.loader import  render_to_string
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError

# Create your views here.

# API Authentication
# class RegisterView(APIView):

#     @method_decorator(csrf_protect)
#     @method_decorator(ensure_csrf_cookie)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)
    
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


#JWT Auhentication imports
# from rest_framework.views import APIView
# from .serializers import UserSerializer
# from rest_framework.response import Response

# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import AllowAny
# from .serializers import UserSerializer, TokenSerializer
# from rest_framework_simplejwt.tokens import RefreshToken

# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_protect
# from django.views.decorators.csrf import ensure_csrf_cookie


# from django.http import HttpResponseNotAllowed

# @api_view(['POST', 'GET'])
# @permission_classes([AllowAny])
# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             if user:
#                 refresh = RefreshToken.for_user(user)
#                 serializer = TokenSerializer(data={
#                     'access': str(refresh.access_token),
#                     'refresh': str(refresh)
#                 })
#                 serializer.is_valid(raise_exception=True)
#                 messages.success(request, "Account created successfully, An OTP has been sent to your email")
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#     else:
#         form = UserRegisterForm()
    
#     context = {
#         'form': form,
#     }
#     return render(request, 'register.html', context)

#     return HttpResponseNotAllowed(['POST', 'GET'])


