from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from data.models import Vacansy, Resume
from user.models import Employer, Candidate


class LoginView(LoginView):
    template_name = 'base/login.html'
    success_url = reverse_lazy('leads')
    redirect_authenticated_user = True

class Leads(LoginRequiredMixin, TemplateView):
    template_name = 'leads.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = Vacansy.objects.filter(is_verify=False)
        context['seven'] = Vacansy.objects.filter(is_verify=True)
        context['month'] = Vacansy.objects.filter(is_verify=True)
        return context

class Employers(LoginRequiredMixin, TemplateView):
    template_name = 'employer.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['leads'] = Employer.objects.filter(is_verify=False, black_list=False)
        context['verify'] = []
        for emploer in Employer.objects.filter(is_verify=True, black_list=False):
            vacansies = Vacansy.objects.filter(employer=emploer)
            if not vacansies: context['verify'].append(emploer)
            for vacansy in vacansies:
                if not vacansy.is_verify:
                    context['verify'].append(emploer)
                    break
        context['search'] = []
        for emploer in Employer.objects.filter(is_verify=True, black_list=False):
            for vacansy in Vacansy.objects.filter(employer=emploer):
                if vacansy.is_verify:
                    context['search'].append(emploer)
                    break
        context['black'] = Employer.objects.filter(black_list=True)
        return context


class Condidats(LoginRequiredMixin, TemplateView):
    template_name = 'condidat.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['leads'] = Candidate.objects.filter(is_verify=False, black_list=False)
        context['verify'] = []
        for condidate in Candidate.objects.filter(is_verify=True, black_list=False):
            for resume in Resume.objects.filter(candidate=condidate):
                if resume.is_verify:
                    context['verify'].append(condidate)
                    break
        context['white'] = []
        for condidate in Candidate.objects.filter(is_verify=True, black_list=False):
            resumes = Resume.objects.filter(candidate=condidate)
            if not resumes: context['white'].append(condidate)
            for resume in resumes:
                if not resume.is_verify:
                    context['white'].append(condidate)
                    break
        context['black'] = Candidate.objects.filter(black_list=True)
        return context


class VacansyView(LoginRequiredMixin, TemplateView):
    template_name = 'vacansy.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacansy = Vacansy.objects.get(id=self.kwargs['id'])
        context['vacansy'] = vacansy
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST
        vacansy = Vacansy.objects.get(id=self.kwargs['id'])
        vacansy.position = data['position']
        vacansy.experience = data['experience']
        vacansy.age = data['age']
        vacansy.description = data['description']
        vacansy.salary = data['salary']
        vacansy.comments_admin = data['comments_admin']
        if data.get('verify'):
            vacansy.is_verify = True
        else:
            vacansy.is_verify = False
        vacansy.save()

        return redirect('/')

class CondidatView(LoginRequiredMixin, TemplateView):
    template_name = 'condidatSingle.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        condidat = Candidate.objects.get(id=self.kwargs['id'])
        context['condidat'] = condidat
        context['resumes'] = Resume.objects.filter(candidate=condidat)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST
        condidat = Candidate.objects.get(id=self.kwargs['id'])
        condidat.name = data['name']
        condidat.secondname = data['secondname']
        condidat.email = data['email']
        condidat.phone = data['phone']
        condidat.comments_admin = data['comments_admin']

        if data.get('verify'):
            condidat.is_verify = True
        else:
            condidat.is_verify = False

        if data.get('black_list'):
            condidat.black_list = True
        else:
            condidat.black_list = False

        condidat.save()
        return redirect('/condidats/')

class EmploerView(LoginRequiredMixin, TemplateView):
    template_name = 'emploerSingle.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        emploer = Employer.objects.get(id=self.kwargs['id'])
        context['emploer'] = emploer
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST
        emploer = Employer.objects.get(id=self.kwargs['id'])
        emploer.company = data['company']
        emploer.fio = data['fio']
        emploer.category = data['category']
        emploer.phone = data['phone']
        emploer.email = data['email']
        emploer.comments_admin = data['comments_admin']

        if data.get('verify'):
            emploer.is_verify = True
        else:
            emploer.is_verify = False

        if data.get('black_list'):
            emploer.black_list = True
        else:
            emploer.black_list = False
        emploer.save()

        return redirect('/employers/')