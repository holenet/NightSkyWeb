from django import forms
from .models import Log, Piece, Watch


class TextLogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ('text',)


class ImageLogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ('image',)


class PieceForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = ('title', 'comment')


class PieceCommentForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = ('comment',)


class WatchEditForm(forms.ModelForm):
    piece = forms.ModelChoiceField(queryset=Piece.objects.all())
    logs = forms.ModelMultipleChoiceField(queryset=Log.objects.all())

    class Meta:
        model = Watch
        fields = ('start', 'end', 'etc')


class WatchAddForm(forms.Form):
    logs = forms.ModelMultipleChoiceField(queryset=Log.objects.all())
