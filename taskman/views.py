from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import ActivityFeed, Task
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginForm
from django.http import HttpResponseRedirect
from .serializers import TaskSerializer
from rest_framework import generics, status
from django.core.signals import request_finished
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver

class ListTask(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class DeleteTask(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'taskman/login.html'


class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'taskman/register.html'
    success_url = reverse_lazy('login')


# class CustomLoginView(LoginView):
#     template_name = 'taskman/login.html'
#     fields = '__all__'
#     redirect_authenticated_user = True

#     def get_success_url(self):
#         return reverse_lazy('tasks')

# class RegisterPage(FormView):
#     template_name = 'taskman/register.html'
#     form_class = UserCreationForm
#     redirect_authenticated_user = True
#     success_url = reverse_lazy('tasks')

#     def form_valid(self, form):
#         user = form.save()
#         if user is not None:
#             lgin(self.request, user)
#         return super(RegisterPage, self).form_valid(form)


def register(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserRegistrationForm()

    context = {"form": form}
    return render(request, "taskman/register.html", context)

class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)
        context['search_input'] = search_input
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    template_name ='taskman/task.html'

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title', 'description','complete','deadlineDate']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title', 'description','complete','deadlineDate']
    success_url = reverse_lazy('tasks')
    
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

# class SearchResultsList(ListView):
#     model = Task
#     context_object_name = "tasks"
#     template_name = "taskman/search.html"

#     def get_queryset(self):
#         search = self.request.user
#         return Task.objects.filter(title=search)

def search(request):
    if request.method=='POST':
        title = request.POST.get("query")
        flt=Task.objects.filter(name__contains=title)
        return render(request,'taskman/search.html',{'form':flt,'a':title})
    else:
        return render(request, 'taskman/search.html')

def activityFeeds(request):
    activity = ActivityFeed.objects.all()
    return render(request, 'taskman/activity_feed.html', {'activity': activity})

