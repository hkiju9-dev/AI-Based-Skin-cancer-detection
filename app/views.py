from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from .forms import ContactForm
from .models import ContactMessage

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Users
from .forms import SignUpForm,UserUpdateForm, ProfileUpdateForm
from django.core.mail import send_mail


from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .models import ContactMessage
from .forms import ReplyForm


def about(request):
    return render(request,'about.html')

def ai(request):
    return render(request,'ai.html')

def contact(request):
    return render(request,''
                          'contact_us.html')



def Forgotpass(request):
    return render(request,'forgotpass.html')

def history(request):
    return render(request,'history.html')

def index(request):
    return render(request,'index.html')

def logins(request):
  if request.method == "POST":
    username = request.POST.get('username')
    password=request.POST.get('password')
    user = authenticate(request,username=username, password=password)
    if user is not None:
        login(request, user)
        messages.success(request,'login')
        return redirect('/')
    else:
        messages.error(request,'login failed')
  return render(request, 'login.html')

def profile(request):
    return render(request,'2profile.html')


def Register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            # Sending Email
            subject = 'About Registration'
            message = 'Hi, you are successfully registered!'
            email_from = 'hussnainkhawar82@gmail.com'
            recipient_list = [form.cleaned_data['email']]

            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                print(f"Email error: {e}")  # Debugging if email fails

            return redirect('/login')  # Redirect to login page
    else:
        form = SignUpForm()  # Corrected Form Initialization

    return render(request, 'Register.html', {'form': form})


def service(request):
    return render(request,'service.html')

def resetpass(request):
    return render(request,'reset pass.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile


def is_registered(user):
    """Checks if the user is authenticated and has a registered email."""
    return user.is_authenticated and bool(user.email)


@login_required(login_url='/login')  # Redirects unauthenticated users
def profile_edit(request):
    """Allows users to edit their profile & change password, only if registered."""

    # Ensure the profile exists for the user
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Redirect unregistered users
    if not is_registered(request.user):
        messages.error(request, 'You must be registered to access this page!')
        return redirect('/Register/')

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        password_form = PasswordChangeForm(request.user, request.POST)  # Use Django's built-in form

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            # Handle password update only if old_password is provided
            if 'old_password' in request.POST and request.POST['old_password']:
                if password_form.is_valid():
                    user = password_form.save()
                    update_session_auth_hash(request, user)  # Prevents logout
                    messages.success(request, "Profile & Password updated successfully!")
                else:
                    messages.error(request, "Error updating password. Please check again.")

            return redirect('/profile/')  # Redirect after successful update

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
        password_form = PasswordChangeForm(request.user)  # Empty password form for GET request

    return render(request, 'editprofile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,  # Pass this to the template
    })


@login_required
def profile_view(request):
    """ View for users to see their profile (non-editable) """
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile, 'user': request.user})


@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = request.user

        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
        elif new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, "Password changed successfully!")
            return redirect('/login')

    return render(request, 'change_password.html')


def user_logout(request):
    logout(request)  # Logs out the user
    return redirect('/login/')





def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()

            # Send Email to Admin
            send_mail(
                subject=f"New Contact Message from {contact_message.name}",
                message=contact_message.message,
                from_email=contact_message.email,
                recipient_list=['hussnainkhawar82@gmail.com'],  # Change this to your admin email
                fail_silently=False,
            )

            return JsonResponse({'success': True, 'message': "Message sent successfully!"})
        else:
            return JsonResponse({'success': False, 'message': "Invalid form data!"})

    form = ContactForm()
    return render(request, 'contact_us.html', {'form': form})





@login_required
def reply_message(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)

    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            message.admin_reply = form.cleaned_data['admin_reply']
            message.replied_at = now()
            message.save()

            # Send email to user
            send_mail(
                subject=f"Reply to: {message.subject}",
                message=f"Dear {message.name},\n\n{message.admin_reply}\n\nBest regards,\nAdmin",
                from_email="hussnainkhawar82@gmail.com",
                recipient_list=[message.email],
            )

            return redirect("contact_us")  # Redirect to admin page

    else:
        form = ReplyForm(initial={'admin_reply': message.admin_reply})

    return render(request, "reply_message.html", {"form": form, "message": message})



@login_required
def user_messages(request):
    messages = ContactMessage.objects.filter(email=request.user.email).order_by('-created_at')
    return render(request, 'user_messages.html', {'messages': messages})


def check_usernames(request):
    usernames = list(User.objects.values_list('username', flat=True))

    return JsonResponse({'usernames': usernames})


def check_username(request):
    usernames = list(User.objects.values_list('username', flat=True))
    emails = list(User.objects.values_list('email', flat=True))
    return JsonResponse({'usernames': usernames,'emails': emails})

from django.shortcuts import render
from .ml_model import predict_image

def home(request):
    return render(request, "ai.html")


from django.http import JsonResponse
from .ml_model import predict_image

def predict(request):
    if request.method == "POST":
        image = request.FILES["image"]

        result = predict_image(image)

        return JsonResponse({"result": result})