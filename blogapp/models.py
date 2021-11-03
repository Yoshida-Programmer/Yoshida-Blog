from django.db import models
from django.db.models.base import Model
from django.utils import timezone
from mdeditor.fields import MDTextField
from markdown import markdown

# Create your models here.

"""タグモデル"""
class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ('タグ一覧')
        verbose_name_plural = ('タグ一覧')

CATEGORY = (('Illustration','イラスト'),('life','日常'),('business','仕事関係'))

"""ブログモデル"""
class BlogModel(models.Model):
    title = models.CharField(max_length=100, verbose_name='タイトル')
    content = MDTextField(verbose_name='内容')
    postdate = models.DateField(auto_now_add=True, verbose_name='投稿日')
    category = models.CharField(
        max_length= 50,
        choices= CATEGORY,
        verbose_name= 'ジャンル'
    )
    #Tagモデルと紐づけ
    tag = models.ManyToManyField(Tag, blank=True, verbose_name="タグ")

    #管理サイトに表示されるオブジェクト名を「title」フィールド名に設定
    def __str__(self):
        return self.title

    #MarkDown記法で書かれたtextをHTML形式に変換して返す
    def get_markdown_text_as_html(self):
        return markdown(self.content)

    #メタデータ（付帯情報）を追加
    class Meta:
        verbose_name = ('ブログ記事投稿')
        verbose_name_plural = ('ブログ記事投稿')


"""コメントモデル"""
class Comment(models.Model):
    user_name = models.CharField('名前', max_length=255, default='名無し')
    message = models.TextField('本文')
    target = models.ForeignKey(BlogModel, on_delete=models.CASCADE, verbose_name='対象記事')
    created_at = models.DateTimeField('作成日', default=timezone.now)
 
    def __str__(self):
        return self.message[:20]

    class Meta:
        verbose_name = ('コメント一覧')
        verbose_name_plural = ('コメント一覧')

"""返信モデル"""
class Reply(models.Model):
    name = models.CharField('名前', max_length=255, default='名無し')
    text = models.TextField('本文')
    target = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='対象コメント')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.text[:20]

    class Meta:
        verbose_name = ('返信')
        verbose_name_plural = ('返信')


