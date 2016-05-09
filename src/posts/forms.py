from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .models import Post


class PostForm(forms.ModelForm):
    def clean_content(self):
        content = self.cleaned_data['content']
        content_type = content.content_type.split('/')[0]
        if content_type in settings.CONTENT_TYPES:
            if content._size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (
                filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
        else:
            raise forms.ValidationError(_('File type is not supported'))
        return content

    class Meta:
        model = Post
        fields = [
            'first_name',
            'last_name',
            'pounds_lost',
            'beforeimage',
            'afterimage',

        ]
