from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.
from django.http import HttpResponse
from django.forms import ModelForm
from forms import AddMangaForm
from .models import Manga, ReadingProgress
from django.contrib import messages
from parser.mangapanda import *


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def mymangas(request):
    manga_list = Manga.objects.filter(user=request.user)
    return render(request, 'mymangas/view.html', {'manga_list': manga_list})


@login_required
def addmangas(request):
    manga_form = AddMangaForm()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AddMangaForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            manga = form.save(commit=False)
            manga.user = request.user
            manga.save()
            return redirect('/tomabi/mymangas/')
        return render(request, 'mymangas/add.html', { 'manga_form': form})
    else:
            return render(request, 'mymangas/add.html', { 'manga_form': manga_form})


@login_required
def deletemangas(request, id):
    manga_id = id
    manga_user_id = Manga.objects.filter(id=manga_id).values_list('user')[0]
    if (manga_user_id[0] == int(request.user.id)):
        manga_to_delete = get_object_or_404(Manga, pk=id).delete()
        return redirect('/tomabi/mymangas/')
    else:
        return render(request, '403.html')


@login_required
def resetmangas(request, id):
    manga_id = id
    manga_user_id = Manga.objects.filter(id=manga_id).values_list('user')[0]
    if (manga_user_id[0] == int(request.user.id)):
        # manga_to_delete = get_object_or_404(Manga, pk=id).delete()
        ReadingProgress.objects.filter(user=request.user.id).filter(manga=manga_id).delete()
        return redirect('/tomabi/mymangas/')
    else:
        return render(request, '403.html')


@login_required
def markasread(request, id, chapter):
    manga_id = id
    chapter_inst = Chapter.objects.filter(manga_id=manga_id,number=chapter)[0]
    print(chapter_inst.number)
    manga_user_id = Manga.objects.filter(id=manga_id).values_list('user')[0]
    if (manga_user_id[0] == int(request.user.id)):
        ReadingProgress.objects.filter(user=request.user.id).filter(manga=manga_id).delete()
        chap = ReadingProgress(user=request.user, manga_id=manga_id, last_chapter=chapter_inst)
        chap.save()
        return redirect('/tomabi/myprogress/')
    else:
        return render(request, '403.html')


@user_passes_test(lambda u: u.is_superuser)
def manageusers(request):
    return HttpResponse('toto!')


@login_required
def refresh(request):
    manga_set = Manga.objects.filter(user_id=request.user.id)
    # print('manga_list'+str(manga_set))
    for manga in manga_set:
        print(manga.id)
        parser_name = Manga.objects.filter(id=manga.id)[0].parser.methodname
        globals()[parser_name](request, manga.id)
    return redirect('/tomabi/myprogress/')

@login_required
def myprogress(request):
    manga_set = Manga.objects.filter(user_id=request.user.id)
    manga_dict = collections.OrderedDict()
    for manga in manga_set:
        print('id:'+str(manga.id))
        chapter_set = Chapter.objects.filter(manga=manga.id)
        try:
            last_read_chapter = ReadingProgress.objects.filter(user=request.user.id).filter(manga=manga.id)[0].last_chapter.number
        except Chapter.DoesNotExist:
            print("Either the entry or blog doesn't exist.")
            last_read_chapter = 1
        chapter_dict = collections.OrderedDict()
        for chapter in chapter_set:
            if last_read_chapter <= chapter.number:
                chapter_dict[chapter.number] = chapter.url
        reversed_chapter_dict = collections.OrderedDict(reversed(list(chapter_dict.items())))
        manga_dict[manga] = reversed_chapter_dict
    return render(request, 'myprogress.html', { 'manga_dict': manga_dict})
