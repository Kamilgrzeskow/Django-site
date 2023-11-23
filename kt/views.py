from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Kontakt, Post
from .forms import KontaktForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Avg
import pickle


class PostListView(ListView):
    model = Post
    template_name = 'kt/post.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# Create your views here.
def home(request):
    listaKontaktow = Kontakt.objects.all()
    return render(request, "kt/home.html", {"dane":listaKontaktow, "title":"Kontakty"})
def dodaj(request):

    if request.method == "POST":

        ob = KontaktForm(request.POST)
        if ob.is_valid():
            ob.save()
            return redirect("home")
        else:
            formularz = KontaktForm()
            return render(request, "kt/dodaj.html", {"formKontakt": formularz, "title":"Dodaj"})
    else:
        formularz = KontaktForm()
        return render(request, "kt/dodaj.html", {"formKontakt":formularz, "title":"Dodaj"})

def edytuj(request, pk):

    obiekt = get_object_or_404(Kontakt, pk=pk)

    if request.method == "POST":

        ob = KontaktForm(request.POST, instance=obiekt)
        if ob.is_valid():
            ob.save()
            return redirect("home")
        else:
            formularz = KontaktForm(instance=obiekt)
            return render(request, "kt/edytuj.html", {"formKontakt": formularz, "title":"Edytuj"})
    else:
        formularz = KontaktForm(instance=obiekt)
        return render(request, "kt/edytuj.html", {"formKontakt":formularz,"title":"Edytuj"})

def usun(request, pk):
    Kontakt.objects.filter(pk=pk).delete()
    return redirect("home")

# def avg_visit_count(request):
#     avg_visits = Page.objects.aggregate(
#         avg_visits=Avg('visits_count')
#     )['avg_visits']
#     plik = open("dane.txt", "a")
#     plik.write(f"{avg_visits}hej")
#     plik.close()

def post(request):
    context = {
        "posts":Post.objects.all(),
        "title":"Posty"
    }
    return render(request, "kt/post.html", context)