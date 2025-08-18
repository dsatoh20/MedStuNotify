from django.views.generic import TemplateView

class PrivacyPolicyView(TemplateView):
    template_name = 'pages/privacy_policy.html'

class AboutView(TemplateView):
    template_name = 'pages/about.html'

class ContactView(TemplateView):
    template_name = 'pages/contact.html'