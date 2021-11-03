from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponseRedirect, request
from .models import BlogModel, Tag, Comment
from .forms import CommentCreateForm
from django.urls import reverse_lazy
from django.views.generic.detail import SingleObjectMixin
from django.views import generic
from django import forms
from django.core.checks import messages
from django.contrib import messages
from django.db.models import Q
from functools import reduce
from operator import and_

'''ブログ一覧'''
class BlogList(ListView):
    template_name = 'list.html'
    model = BlogModel
    paginate_by = 10

    # クエリを実行してレコードを抽出（投稿日付【降順】に並べ替え）
    def get_queryset(self):
        posts = BlogModel.objects.order_by('-postdate')
        return posts


'''ブログ詳細'''
class BlogDetail(DetailView):
    template_name = 'detail.html'
    model = BlogModel


'''ブログ作成'''
class BlogCreate(CreateView):
    template_name = 'create.html'
    model = BlogModel
    fields = ('title', 'content', 'category')
    success_url = reverse_lazy('list')


'''ブログ削除'''
class BlogDelete(DeleteView):
    template_name = 'delete.html'
    model = BlogModel
    success_url = reverse_lazy('list')


'''ブログ更新'''
class BlogUpdate(UpdateView):
    template_name = 'update.html'
    model = BlogModel
    fields = ('title', 'content', 'category')
    success_url = reverse_lazy('list')


class TagDetail(SingleObjectMixin, ListView):
    model = Tag
    paginate_by = 10
    template_name = "tag_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Tag.objects.all())
        return super().get(request, *args, **kwargs)

    # 辞書形式のデータとして取得し、テンプレートにデータベースのデータを出力
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.object
        return context

    # クエリを実行してレコードを抽出（投稿日付【降順】に並べ替え）
    def get_queryset(self):
        return self.object.post_set.all().order_by('-postdate')


"""タグ表示"""
class TagView(generic.ListView):
    model = BlogModel
    template_name = 'list.html'

    def get_queryset(self):
        tag = Tag.objects.get(name=self.kwargs['tag'])
        queryset = BlogModel.objects.order_by('-id').filter(tag=tag)
        messages.success(self.request, '検索完了しました')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_key'] = self.kwargs['tag']
        return context


class CommentView(generic.CreateView):
    template_name = 'comment_form.html'
    model = Comment
    form_class = CommentCreateForm

    def form_valid(self, form):
        post_pk = self.kwargs['pk']
        post = get_object_or_404(BlogModel, pk=post_pk)
        comment = form.save(commit=False)
        comment.target = post
        comment.save()
        return redirect('blogapp:detail', pk=post_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(BlogModel, pk=self.kwargs['pk'])
        return context

    '''検索機能'''
class SearchView(View):
    def get(self, request, *args, **kwargs):
        post_data = BlogModel.objects.order_by('-postdate')
        keyword = request.GET.get('keyword')

        if keyword:
            exclusion_list = set([' ', '　'])
            query_list = ''
            for word in keyword:
                if not word in exclusion_list:
                    query_list += word
            #Qオブジェクトを使用して、投稿データを検索入力したキーワードでフィルターをかける(or検索)
            query = reduce(and_, [Q(title__icontains=q) | Q(content__icontains=q) for q in query_list])
            post_data = post_data.filter(query)

        return render(request, 'list.html', {
            'keyword' : keyword,
            'post_data' : post_data
        })

