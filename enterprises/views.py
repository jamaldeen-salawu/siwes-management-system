from django.shortcuts import render, redirect, reverse
from .models import Enterprise
from .forms import EnterpriseCreationForm
from django.views import generic

# Create your views here.
class EnterpriseDetailView(generic.DetailView):
    model = Enterprise
    template_name = 'enterprises/enterprise_detail.html'

class EnterpriseCreationView(generic.CreateView):
    form_class = EnterpriseCreationForm
    template_name = 'enterprises/enterprise_create.html'
    def get_success_url(self):
        return reverse("enterprises:list")

class EnterpriseList(generic.ListView):
    model = Enterprise
    template_name = None
    context_object_name = 'enterprises'