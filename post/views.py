from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    edit)

from .forms import PostForm, ImageForm
from .models import Post, Image, PostComment


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home_page.html'
    context_object_name = 'posts'
    ordering = ['-created']
    paginate_by = 8

class PostDetailView(LoginRequiredMixin, DetailView, ):
	model = Post

@login_required
def post_create(request):

    ImageFormSet = modelformset_factory(Image,
                                        form=ImageForm,
                                        extra=3)

    if request.method == 'POST':

        postForm = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Image.objects.none())


        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.author = request.user
            post_form.save()
            print(formset.cleaned_data)
            for form in formset.cleaned_data:
                try:

                    image = form['image']
                    photo = Image(post=post_form, image=image)
                    photo.save()
                except:
                    pass
            messages.success(request,
                             "Posted!")
            return HttpResponseRedirect("/")
        else:
            print (postForm.errors, formset.errors)
    else:
        postForm = PostForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request, 'post/post_create.html',
                  {'postForm': postForm, 'formset': formset},
                  )


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, edit.UpdateView):
    model = Post
    fields = ['caption']
    template_name_suffix = '_form'

    def form_valid(self, form):
        form.instance.author = self.request.user  # take that instance and set the author to current login user
        return super().form_valid(form)  # run form valid method in parent class(validate the form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

