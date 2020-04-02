from django import forms

from post.models import Post, Image


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('caption',)


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image', required=False)
    class Meta:
        model = Image
        fields = ('image', )