from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.core import exceptions
from django.utils.decorators import method_decorator
from django.views.generic import ListView, View
from django.views.generic import ListView, View, DetailView, CreateView, UpdateView, DeleteView
from core import models
from core.exceptions import PermissionDenied
from core.forms import PostForm, CommentForm
from core.models import Post


class IndexView(ListView):
    model = models.Post
    template_name = "core/index.html"
    context_object_name = "popular_posts"

    def get_queryset(self):
        return models.Post.objects.annotate(like_nums=Sum('likes')).order_by('-like_nums')[:10]


class FeedView(View):
    template_name = 'core/feed.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = {}
            posts = models.Post.objects.filter(author__in=request.user.profile.friends.all()).order_by('-date_pub')[:10]
            context['feed'] = posts
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name)


class PostView(DetailView):
    model = Post
    comment_form = CommentForm
    pk_url_kwarg = 'post_id'
    template_name = 'core/post.html'

    def get(self, request, post_id, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['comments'] = models.Comment.objects.filter(in_post__pk=post_id).order_by('-date_publish')
        context['comment_form'] = None
        if request.user.is_authenticated:
            context['comment_form'] = self.comment_form
        return self.render_to_response(context)

    @method_decorator(login_required)
    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, pk=post_id)
        form = self.comment_form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.date_publish = timezone.now()
            comment.author = request.user
            comment.in_post = post
            comment.save()
            return render(request=request, template_name=self.template_name, context={'comment_form': self.comment_form,
                                                                                      'post': post,
                                                                                      'comments': post.comment_set.order_by(
                                                                                       '-date_publish')})
        else:
            return render(request=request, template_name=self.template_name, context={'comment_form': form,
                                                                                      'post': post,
                                                                                      'comments': post.comment_set.order_by(
                                                                                       '-date_publish')})


class CreatePostView(CreateView):
    form_class = PostForm
    template_name = 'core/post_create.html'

    @method_decorator(login_required)
    def post(self, request,  *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        context = {}
        if form.is_valid():
            post = form.save(commit=False)
            post.date_pub = timezone.now()
            post.author = request.user
            post.save()
            context['post_was_created'] = True
            context['form'] = self.form_class
            return render(request=request, template_name=self.template_name, context=context)
        else:
            context['post_was_created'] = False
            context['form'] = form
            return render(request=request, template_name=self.template_name, context=context)


class EditPostView(UpdateView):
    model = models.Post
    pk_url_kwarg = 'post_id'
    template_name = 'core/post_edit.html'
    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied("You are not author of this post")
        return super(EditPostView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return reverse('core:post', args=(post_id, ))


class LikePostView(View):
    def get(self, request, post_id, *args, **kwargs):
        return redirect(reverse('core:post', args=(post_id,)))

    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, pk=post_id)
        if post.likes.filter(pk=request.user.id).exists():
            like = post.likes.get(pk=request.user.id)
            post.likes.remove(like)
        else:
            post.likes.add(request.user)
            post.save()
        return redirect(request.META.get('HTTP_REFERER'), request)


class DeletePostView(DeleteView):
    model = models.Post
    pk_url_kwarg = 'post_id'
    template_name = 'core/post_delete.html'

    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return reverse('core:delete-post-success', args=(post_id,))


