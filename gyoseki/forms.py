from django import forms
import re

from .models import Recode, Author, Tag, Division

FORMAT = (
    ('table', '表形式'),
    ('reference', '参考文献風形式'),
    ('bibtex', 'bibtex形式')
)


class SearchForm(forms.Form):
    main_author = forms.ModelChoiceField(Author.objects.all().order_by('quited_at','joined_at'), label='主著者', required=False,
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    author = forms.CharField(label='著者', max_length=128, required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    author_or = forms.CharField(label='著者(OR)', max_length=128, required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    title = forms.CharField(label='タイトル', max_length=128, required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    journal = forms.CharField(label='出典', max_length=128, required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    at_date = forms.DateField(label='検索開始日', required=False,
                              widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_date = forms.DateField(label='検索終了日', required=False,
                               widget=forms.DateInput(attrs={"type": "date", 'class': 'form-control'}))
    division = forms.ModelMultipleChoiceField(queryset=Division.objects.all(), label='業績区分', required=False,
                                              widget=forms.CheckboxSelectMultiple)
    tag = forms.ModelMultipleChoiceField(Tag.objects.all(), label='タグ', required=False,
                                         widget=forms.CheckboxSelectMultiple)
    review = forms.BooleanField(label='査読の有無', required=False, )
    display_format = forms.ChoiceField(label='表示形式', choices=FORMAT, required=True,
                                       widget=forms.Select(attrs={'class': 'form-control'}))


def to_half_width(s):
    if s:
        s = s.replace('，', ', ')
        s = s.replace('　', ' ')
        s = re.sub(" +", ' ', s)
    return s


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Recode
        exclude = {}
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'}),
            'tag': forms.CheckboxSelectMultiple,
            'file': forms.FileInput(attrs={'class': 'form-control-file'})
        }
        labels = {
            'main_author': '主著者',
            'author': '著者',
            'en_author': '著者(英語表記)',
            'title': 'タイトル',
            'en_title': 'タイトル(英語表記)',
            'journal': '雑誌名',
            'en_journal': '雑誌名(英語表記)',
            'vol': '巻',
            'no': '号',
            'page': 'ページ',
            'date': '発表年月日',
            'language': '言語',
            'division': '業績区分',
            'place': '場所',
            'en_place': '場所(英語表記)',
            'tag': 'タグ',
            'review': '査読の有無',
            'note': '備考',
            'file': 'PDFファイル'
        }

    def clean_author(self):
        author = self.cleaned_data.get('author')
        return to_half_width(author)

    def clean_en_author(self):
        a = self.cleaned_data.get('en_author')
        return to_half_width(a)

    def clean_place(self):
        a = self.cleaned_data.get('place')
        return to_half_width(a)


class TagRegisterForm(forms.ModelForm):
    class Meta:
        model = Tag
        exclude = {}
        labels = {
            'name': '新規タグ名'
        }
