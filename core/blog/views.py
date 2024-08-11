from django.shortcuts import render
from .models import Post
from django.views.generic.base import TemplateView , RedirectView
from django.shortcuts import get_object_or_404
from .forms import PostForm
from django.views.generic import ListView  , DetailView , FormView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin , PermissionRequiredMixin
# Create your views here.
'''
def indexView(request):
    """
    a fuction based view to show index page
    """
    name = "ali"
    context = {'name':name}
    return render(request,"index.html",context)
'''
class IndexView(TemplateView):
    """
    a class based view to show index page
    """
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "ali"
        context["posts"] = Post.objects.all
        return context
    
'''FBV for redirect
from django.shortcuts import redirect
def redirectToMaktab(request):
    return redirect('https://maktabkhooneh.com')

'''

class RedirectToMaktab(RedirectView):
    url = 'https://maktabkhooneh.com'
    
    def get_redirect_url(self,*args, **kwargs):
        post = get_object_or_404(Post,pk=kwargs['pk'])
        print(post)
        return super().get_redirect_url(*args, **kwargs)
    
class PostListView(PermissionRequiredMixin,LoginRequiredMixin,ListView):
    permission_required = "blog.view_post"
    queryset = Post.objects.all()
    # model = Post
    context_object_name = 'posts'
    # paginate_by=1
    ordering = '-id'
    # def get_queryset(self):
    #     posts = Post.objects.filter(status=True)
    #     return posts
    
class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post
    
    
# class PostCreateView(FormView):
#     template_name = 'contact.html'
#     form_class = PostForm
#     success_url = '/blog/post/'
    
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)
class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    # fields = ['author','title','content','status','category','published_date']
    form_class = PostForm
    success_url = '/blog/post/'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostEditView(LoginRequiredMixin,UpdateView):
    model = Post
    form_class = PostForm
    success_url = '/blog/post/'

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model=Post
    success_url= '/blog/post/'