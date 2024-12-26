from django.shortcuts import render, redirect
from django.views import View

from Site_Module.models import SiteSetting
from .forms import ContactUsModelForm
from django.views.generic.edit import FormView, CreateView
from .models import UserProfile
from django.views.generic import ListView


# Create your views here.


# def contact_us_page(request):
#     if request.method == 'POST':
#         contact_form = ContactUsModelForm(request.POST)
#         if contact_form.is_valid():
#             # print(contact_form.cleaned_data)
#             # contact = ContactUs(
#             #     title=contact_form.cleaned_data.get('title'),
#             #     full_name=contact_form.cleaned_data.get('full_name'),
#             #     email=contact_form.cleaned_data.get('email'),
#             #     message=contact_form.cleaned_data.get('message')
#             # )
#             # contact.save()
#             contact_form.save()
#
#             return redirect('home-page')
#
#     else:
#         contact_form = ContactUsModelForm()
#
#     return render(request, 'Contact_Module/contact_us_page.html', {
#         'contact_form': contact_form
#     })

# class ContactUsView(View):
#     def get(self, request):
#         contact_form = ContactUsModelForm()
#         return render(request, 'Contact_Module/contact_us_page.html', {
#             'contact_form': contact_form
#         })
#
#     def post(self, request):
#         contact_form = ContactUsModelForm(request.POST)
#         if contact_form.is_valid():
#             contact_form.save()
#             return redirect('home-page')
#         return render(request, 'Contact_Module/contact_us_page.html', {
#             'contact_form': contact_form
#         })
# class CreateProfileView(View):
#
#     def get(self, request):
#         form = ProfileModelForm()
#         return render(request, 'Contact_Module/create_profile.html', {
#             'form': form
#         })
#
#     def post(self, request):
#         submitted_form = ProfileModelForm(request.POST, request.FILES)
#         if submitted_form.is_valid():
#             profile = UserProfile(image=request.FILES['image'])
#             profile.save()
#             return redirect('create-profile-page')
#         return render(request, 'Contact_Module/create_profile.html', {
#             'form': submitted_form
#         })


class ContactUsView(CreateView):
    template_name = 'Contact_Module/contact_us_page.html'
    form_class = ContactUsModelForm
    success_url = '/contact-us/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting: SiteSetting = SiteSetting.objects.filter(is_active=True).first()
        context['site_setting'] = setting
        return context


class CreateProfileView(CreateView):
    template_name = 'Contact_Module/create_profile.html'
    model = UserProfile
    fields = '__all__'
    success_url = '/'


class ProfileListView(ListView):
    template_name = 'Contact_Module/profile-list.html'
    model = UserProfile
    context_object_name = 'profiles'
