# vrproapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import UserProfile
from .models import UserProfile, PreAssessment
from .forms import PreAssessmentForm
from .models import UserProfile, PreAssessment, PHOBIA_CHOICES
from django.http import Http404
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render, redirect
from django.db import models


# ---------------- PHOBIA CONFIG ----------------
PHOBIA_CONFIG = {
    "heights": {
        "label": "Fear of Heights",
        "pre_template": "preassessment_heights.html",  # <- your heights pre page
        "vr_template": "height.html",                  # <- your VR scene
    },
    "spider": {
        "label": "Fear of Spiders",
        "pre_template": "preassessment_spider.html",
        "vr_template": "spidervr.html",                # you can adjust later
    },
    "publicspeaking": {
        "label": "Public Speaking",
        "pre_template": "preassessment_publicspeaking.html",
        "vr_template": "therapy_publicspeaking.html",  # whatever you have
    },
}

# -------------- PRE-ASSESSMENT VIEW --------------
def pre_assessment(request, phobia):
    """
    Show the correct pre-assessment page based on the phobia slug.
    e.g. /pre/heights/  or  /pre/spider/
    """
    cfg = PHOBIA_CONFIG.get(phobia)
    if not cfg:
        raise Http404("Phobia not found")

    context = {
        "phobia_slug": phobia,
        "phobia_label": cfg["label"],
    }
    return render(request, cfg["pre_template"], context)


# -------------- VR MODULE VIEW -------------------
def vr_module(request, phobia):
    """
    Show the VR scene after pre-assessment.
    e.g. /vr/heights/ → height.html
    """
    cfg = PHOBIA_CONFIG.get(phobia)
    if not cfg:
        raise Http404("Phobia not found")

    context = {
        "phobia_slug": phobia,
        "phobia_label": cfg["label"],
    }
    return render(request, cfg["vr_template"], context)



def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        # find user by email
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            username = None

        if username:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully.")
                # 👇 IMPORTANT: use 'next' if given, else go to dashboard
                next_url = request.GET.get('next') or reverse('dashboard')
                return redirect(next_url)

        messages.error(request, "Invalid email or password.")
        return redirect('login')

    return render(request, 'login.html')

def signup_page(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        fullname = request.POST.get("fullname", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        role = request.POST.get("role", "")
        age = request.POST.get("age") or None
        gender = request.POST.get("gender", "")
        license_no = request.POST.get("license", "")
        experience = request.POST.get("experience") or None
        specialization = request.POST.get("specialization", "")
        institution = request.POST.get("institution", "")
        research_field = request.POST.get("research_field", "")

        if not fullname or not email or not password:
            messages.error(request, "Please fill in all required fields.")
            return render(request, "signup.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please login.")
            return redirect('login')

        base_username = email.split('@')[0]
        username = base_username
        i = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{i}"
            i += 1

        user = User.objects.create_user(username=username, email=email, password=password, first_name=fullname)
        UserProfile.objects.create(
            user=user,
            role=role,
            age=int(age) if age else None,
            gender=gender,
            license_no=license_no,
            experience=int(experience) if experience else None,
            specialization=specialization,
            institution=institution,
            research_field=research_field
        )

        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, "signup.html")



@login_required(login_url='login')
def index(request):
    profile = getattr(request.user, "profile", None)
    return render(request, "index.html", {"profile": profile})

def logout_page(request):
    logout(request)
    return redirect('login')
def homepage(request):
    return render(request, 'homepage.html')

@login_required(login_url='login')
def index(request):
    profile = getattr(request.user, "profile", None)
    return render(request, 'index.html', {"profile": profile})

def phobia_intro_full(request):
    return render(request, 'phobia_intro_full.html')

def pre_therapy_questions(request):
    return render(request, 'pre_therapy_questions.html')

def vr_therapy_info_full(request):
    return render(request, 'vr_therapy_info_full.html')

def logout_page(request):
    logout(request)
    return redirect('login')
def homepage(request):
    return render(request, 'homepage.html')

@login_required
def pre_assessment(request, phobia):
    cfg = PHOBIA_CONFIG.get(phobia)
    if not cfg:
        raise Http404("Phobia not found")

    # mark this phobia as active for this user
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    profile.current_phobia = phobia
    profile.save()

    # get or create the short pre-assessment record
    assessment, _ = PreAssessment.objects.get_or_create(
        user=request.user,
        phobia=phobia,
    )

    if request.method == "POST":
        # ⚠️ these names must match your form field names
        severity_raw = (
            request.POST.get('severity_now')  # preferred
            or request.POST.get('severity')   # fallback if you used another name
            or "5"
        )
        try:
            assessment.severity_now = int(severity_raw)
        except ValueError:
            assessment.severity_now = 5

        assessment.main_triggers = request.POST.get('main_triggers', '')
        assessment.physical_symptoms = request.POST.get('physical_symptoms', '')
        assessment.main_goal = request.POST.get('main_goal', '')
        assessment.save()

        # ✅ after finishing pre-assessment, go straight to VR page
        return redirect('vr_module', phobia=phobia)

    # GET – just show the big pre-assessment page
    return render(request, cfg['pre_template'], {
        "phobia": cfg,
        "slug": phobia,
    }
    )
def vr_module(request, phobia):
    cfg = PHOBIA_CONFIG.get(phobia)
    if not cfg:
        raise Http404("Phobia not found")

    return render(request,cfg["vr_template"],
        {
            'phobia_label': cfg['label'],
        'slug': phobia,
    })
@login_required
def dashboard(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    assessment = None
    if profile.current_phobia:
        assessment = PreAssessment.objects.filter(
            user=request.user,
            phobia=profile.current_phobia
        ).order_by('-updated_at').first()

    return render(request, 'dashboard.html', {
        "profile": profile,
        "assessment": assessment,
    })


@login_required
def edit_profile(request):
    user = request.user

    # where to go after successful save
    default_next = reverse('dashboard')
    next_url = request.GET.get('next', default_next)

    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()

        if not email:
            messages.error(request, "Email cannot be empty.")
        else:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            messages.success(request, "Profile updated successfully.")
            # 🔙 go back (usually dashboard)
            return redirect(next_url)

    return render(request, "edit_profile.html", {"user_obj": user})


@login_required
def pre_assessment(request, phobia):
    cfg = PHOBIA_CONFIG.get(phobia)
    if not cfg:
        raise Http404("Phobia not found")

    template_name = cfg["pre_template"]

    return render(
        request,
        template_name,
        {
            "phobia_slug": phobia,
            "phobia_label": cfg["label"],
        },
    )
@login_required
def dashboard(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'dashboard.html', {"profile": profile})

@login_required
def edit_pre_assessment(request):
    """
    Short editable pre-assessment page, opened from dashboard.
    Edits only the *active* phobia for this user.
    """
    # get current phobia from profile
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if not profile.current_phobia:
        messages.error(request, "You don't have an active phobia yet. Start a module first.")
        return redirect('dashboard')

    phobia = profile.current_phobia

    # get or create assessment record
    assessment, _ = PreAssessment.objects.get_or_create(
        user=request.user,
        phobia=phobia,
    )

    if request.method == "POST":
        form = PreAssessmentForm(request.POST, instance=assessment)
        if form.is_valid():
            form.save()
            messages.success(request, "Pre-assessment details updated.")
            return redirect('dashboard')
    else:
        form = PreAssessmentForm(instance=assessment)

    return render(request, 'edit_pre_assessment.html', {
        'form': form,
        'phobia_name': dict(PHOBIA_CHOICES).get(phobia, phobia),
    })


#from django.shortcuts import render

def about_heights(request):
    return render(request, 'about_heights.html')

def about_spider(request):
    return render(request, 'about_spider.html')

def about_public(request):
    return render(request, 'about_public.html')

def vrtherapy_heights(request):
    return render(request, "vrtherapy_heights.html")


