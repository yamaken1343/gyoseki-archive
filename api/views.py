from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, decorators

# Create your views here.
from rest_framework.parsers import MultiPartParser, FormParser

from gyoseki import forms
from gyoseki.models import Recode, Author, Division, Language, Tag
from django.core import serializers
from .serializer import RegisterSerializer
import json


def search(request):
    recode_list = Recode.objects.all()
    q_set = {}
    author_q_set = []
    en_author_q_set = []
    journal_q_set = []
    en_journal_q_set = []
    title_q_set = []
    en_title_q_set = []
    main_author = request.GET.get('main_author')  # フルネームが許される
    if main_author:
        author = Author.objects.get(name=main_author)
        q_set['main_author'] = author
        print(main_author)
    at_date = request.GET.get('at_date')  # YYYY-MM-DDの形式が許される
    if at_date:
        q_set['date__gte'] = at_date
    end_date = request.GET.get('end_date')  # YYYY-MM-DDの形式が許される
    if end_date:
        q_set['date__lte'] = end_date
    tags = request.GET.get('tag')  # 複数指定する場合はカンマ区切り(AND検索)
    if tags:
        tags = tags.split(',')
        for t in tags:
            t = Tag.objects.get(name=t)
            recode_list = recode_list.filter(tag__in=[t])  # マジで怪しい よくわからんがANDでつなぐとうまくいかない
    review = request.GET.get('review')  # ありの場合は1, そうでないばあいは0
    if review:
        q_set['review'] = review
    author = request.GET.get('author')  # 複数指定する場合はカンマ区切り(AND検索)
    if author:
        for a in author.split(','):
            author_q_set.append(('author__icontains', a))
            en_author_q_set.append(('en_author__icontains', a))
    journal = request.GET.get('journal')  # 複数指定する場合はカンマ区切り(AND検索)
    if journal:
        for a in journal.split(','):
            journal_q_set.append(('journal__icontains', a))
            en_journal_q_set.append(('en_journal__icontains', a))
    title = request.GET.get('title')  # 複数指定する場合はカンマ区切り(AND検索)
    if title:
        for a in title.split(','):
            title_q_set.append(('title__icontains', a))
            en_title_q_set.append(('en_title__icontains', a))
    division = request.GET.get('division')  # "論文 ( 技術報告 )"とかそういう感じ. 複数指定する場合はカンマ区切り(OR検索)
    if division:
        division_list = []
        for d in division.split(','):
            division_list.append(Division.objects.get(name=d))
        q_set['division__in'] = division_list
    if q_set or author_q_set or journal_q_set or title_q_set:
        recode_list = recode_list.filter(Q(**q_set)
                                         & (Q(*author_q_set) | Q(*en_author_q_set))
                                         & (Q(*journal_q_set) | Q(*en_journal_q_set))
                                         & (Q(*title_q_set) | Q(*en_title_q_set))
                                         )
        print(Q(**q_set)
              & (Q(*author_q_set) | Q(*en_author_q_set))
              & (Q(*journal_q_set) | Q(*en_journal_q_set))
              & (Q(*title_q_set) | Q(*en_title_q_set))
              )

    js = serializers.serialize("json", recode_list.order_by('date').reverse(), ensure_ascii=False, indent=2)

    # relation Keyがそのまま出てくるのでイイ感じにする. もっといいやり方があるように思う
    jsd = json.loads(js)
    for i in jsd:
        i['fields']['main_author'] = Author.objects.get(pk=i['fields']['main_author']).name
        if i['fields']['language']:
            i['fields']['language'] = Language.objects.get(pk=i['fields']['language']).name
        if i['fields']['division']:
            i['fields']['division'] = Division.objects.get(pk=i['fields']['division']).name
            tag = []
        for j in i['fields']['tag']:
            tag.append(Tag.objects.get(pk=j).name)
        i['fields']['tag'] = tag

    return HttpResponse(json.dumps(jsd), content_type='application/json')


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = Recode.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.POST, files=request.FILE)
        serializer.save()