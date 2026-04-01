from django.urls import path
from . import views

urlpatterns = [
    # main pages
    path("", views.homepage, name="homepage"),
    path("index/", views.index, name="index"),

    # auth
    path("login/", views.login_page, name="login"),
    path("signup/", views.signup_page, name="signup"),
    path("logout/", views.logout_page, name="logout"),

    # generic info pages
    path("phobia/", views.phobia_intro_full, name="phobia_intro"),
    path("pretherapy/", views.pre_therapy_questions, name="pre_therapy"),
    path("vrtherapy-info/", views.vr_therapy_info_full, name="vr_therapy_info"),

    # dashboard & profile
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.edit_profile, name="edit_profile"),
    path("assessment/edit/", views.edit_pre_assessment, name="edit_pre_assessment"),

    # about screens (heights flow uses this)
    path("about/heights/", views.about_heights, name="about_heights"),
    path("about/spider/", views.about_spider, name="about_spider"),
    path("about/public/", views.about_public, name="about_public"),

    # *** IMPORTANT: dynamic pre-assessment + VR routes ***
    path("pre/<slug:phobia>/", views.pre_assessment, name="pre_assessment"),
    path("vr/<slug:phobia>/", views.vr_module, name="vr_module"),

   
]

