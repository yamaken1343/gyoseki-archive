import datetime
import sys
import zipfile

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.views.generic import UpdateView, DetailView

from gyoseki_beta import settings
from .models import Author, Recode, Tag
from .forms import SearchForm, RegisterForm, TagRegisterForm
from django.db.models import Q

def mail(subject, message):
    emails = User.objects.values_list('email', flat=True)
    print(list(emails))
    """送信元メールアドレス"""
    from_email = settings.DEFAULT_FROM_EMAIL
    """宛先メールアドレス"""
    recipient_list = list(emails)
    flag = False
    try:
        flag = send_mail(subject, message, from_email, recipient_list)
    except:
        print('メール送信に失敗しています')
        print(sys.exc_info())
    return flag


# Create your views here.
def index(request):
    recode_list = Recode.objects.order_by('id').reverse()[:10]
    context = {'recode_list': recode_list}
    return render(request, 'gyoseki/index.html', context)


def detail(request, recode_id):
    recode = get_object_or_404(Recode, pk=recode_id)
    context = {'recode': recode}
    return render(request, 'gyoseki/detail.html', context)


def update(request, recode_id):
    recode = get_object_or_404(Recode, pk=recode_id)
    if request.method =="POST":
        print(request.POST)
        f = RegisterForm(data=request.POST, files=request.FILES, instance=recode)
        b = f.save()
        return HttpResponseRedirect(reverse('gyoseki:detail', args=(b.id, )))
    else:
        f = RegisterForm(instance=recode)
        context = {'formset': f}
        return render(request, 'gyoseki/update.html', context)


def authors(request):
    author_list = Author.objects.order_by('quited_at', 'joined_at')
    context = {'author_list': author_list}
    return render(request, 'gyoseki/authors.html', context)


def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    # recode_list = Author.objects.filter(id=author_id).prefetch_related("recode_set")[0].recode_set.all()
    # print(Author.objects.filter(id=author_id).prefetch_related("recode_set")[0])
    # print(author.recode_set.all())
    recode_list = author.recode_set.all().order_by('date').reverse()
    context = {'recode_list': recode_list, 'author': author}
    return render(request, 'gyoseki/author_detail.html', context)


def search(request):
    recode_list = Recode.objects.all()
    formset = SearchForm(request.POST or None)
    if request.method == 'POST':
        formset.is_valid()
        q_set = {}
        author_q_set = []
        en_author_q_set = []
        author_or_q_set = []
        en_author_or_q_set = []
        journal_q_set = []
        en_journal_q_set = []
        title_q_set = []
        en_title_q_set = []
        main_author = formset.cleaned_data.get('main_author')
        if main_author:
            q_set['main_author'] = main_author
            print(main_author)
        at_date = formset.cleaned_data.get('at_date')
        if at_date:
            q_set['date__gte'] = at_date
        end_date = formset.cleaned_data.get('end_date')
        if end_date:
            q_set['date__lte'] = end_date
        tags = formset.cleaned_data.get('tag')
        if tags:
            for t in tags:
                recode_list = recode_list.filter(tag__in=[t])  # マジで怪しい よくわからんがANDでつなぐとうまくいかない
        review = formset.cleaned_data.get('review')
        if review:
            q_set['review'] = review
        author = formset.cleaned_data.get('author')
        if author:
            for a in author.split():
                author_q_set.append(('author__icontains', a))
                en_author_q_set.append(('en_author__icontains', a))
        author_or = formset.cleaned_data.get('author_or')
        if author_or:
            for a in author_or.split():
                author_or_q_set.append(('author__icontains', a))
                en_author_or_q_set.append(('en_author__icontains', a))
        journal = formset.cleaned_data.get('journal')
        if journal:
            for a in journal.split():
                journal_q_set.append(('journal__icontains', a))
                en_journal_q_set.append(('en_journal__icontains', a))
        title = formset.cleaned_data.get('title')
        if title:
            for a in title.split():
                title_q_set.append(('title__icontains', a))
                en_title_q_set.append(('en_title__icontains', a))
        division = formset.cleaned_data.get('division')
        if division:
            q_set['division__in'] = division
            print(division)
            print(Q(**q_set))
        display_format = formset.cleaned_data.get('display_format')
        if display_format:
            print(display_format)
        if q_set or author_q_set or journal_q_set or title_q_set or author_or_q_set:
            recode_list = recode_list.filter(Q(**q_set)
                                             & (Q(*author_q_set) | Q(*en_author_q_set) | (Q(*author_or_q_set) | Q(*en_author_or_q_set)))
                                             & (Q(*journal_q_set) | Q(*en_journal_q_set))
                                             & (Q(*title_q_set) | Q(*en_title_q_set))
                                             )
            print(Q(**q_set)
                                             & (Q(*author_q_set) | Q(*en_author_q_set) | (Q(*author_or_q_set) | Q(*en_author_or_q_set)))
                                             & (Q(*journal_q_set) | Q(*en_journal_q_set))
                                             & (Q(*title_q_set) | Q(*en_title_q_set))
                                             )
    context = {
        'recode_list': recode_list.order_by('date').reverse(),
        'formset': formset,
    }
    if request.method == 'POST':
        if display_format == 'reference':
            context['recode_list'] = recode_list.order_by('division', '-date')
            return render(request, 'gyoseki/search_result_reference.html', context)
        elif display_format == 'bibtex':
            return render(request, 'gyoseki/search_result_bibtex.html', context)
        else:
            return render(request, 'gyoseki/search_result.html', context)
    else:
        return render(request, 'gyoseki/search.html', context)


def register(request):
    if request.method =="POST":
        print(request.POST)
        f = RegisterForm(data=request.POST, files=request.FILES)
        b = f.save()
        s = "新規業績登録のお知らせ[{}]".format(b.id)
        m = "{} さんの {} に関する業績が新しく登録されました!\nhttp://{}/{}\n\nこのメールに返信されても対応できません."\
            .format(b.main_author, b.title, request.get_host(), b.id)
        # mail(s, m)
        return HttpResponseRedirect(reverse('gyoseki:detail', args=(b.id, )))
    else:
        f = RegisterForm()
        context = {'formset': f}
        return render(request, 'gyoseki/register.html', context)


def tags(request):
    tag_list = Tag.objects.all()
    context = {'tag_list': tag_list}
    return render(request, 'gyoseki/tags.html', context)


def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    recode_list = tag.recode_set.all()
    context = {'recode_list': recode_list, 'tag': tag}
    return render(request, 'gyoseki/tag_detail.html', context)


def tag_register(request):
    if request.method == "POST":
        print(request.POST)
        f = TagRegisterForm(data=request.POST, files=request.FILES)
        b = f.save()
        return HttpResponseRedirect(reverse('gyoseki:tag_detail', args=(b.id,)))
    else:
        f = TagRegisterForm()
        context = {'formset': f}
        return render(request, 'gyoseki/tag_register.html', context)


def download(request):
    li = request.GET.get('list')
    li = li.split('!!!PARSER!!!')
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=matome.zip'
    zf = zipfile.ZipFile(response, 'w')
    for l in li:
        if l:
            zf.write(l)
    return response


def bibtex(request, recode_id):
    recode = get_object_or_404(Recode, pk=recode_id)
    context = {'recode': recode}
    return render(request, 'gyoseki/bibtex.html', context)


def man(request):
    return render(request, 'gyoseki/man.html')
