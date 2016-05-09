from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect  # We can use this to test our views also
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


from .forms import PostForm
from .models import Post


@login_required(login_url='/accounts/login')
def post_detail(request, id=None):  # retrieve method

    instance = get_object_or_404(Post, id=id)

    context = {
        "first_name": instance.first_name,
        "last_name": instance.last_name,
        "instance": instance,

    }

    return render(request, "post_detail.html", context)


@login_required(login_url='/accounts/login/')
def post_list(request):
    queryset_list = Post.objects.all()  # .filter(draft=False).filter(publish__lte=timezone.now()) .all().order_by("-publish") .active()
    query = request.GET.get('q')
    if query:
        queryset_list = queryset_list.filter(
            # Q(first_name__icontains=query) |
            # Q(last_name__icontains=query) |
            Q(pounds_lost__gte=query)
            # Q(pounds_lost__range=query)
        ).distinct()

    paginator = Paginator(queryset_list, 50)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "title": "List"
    }
    return render(request, "post_list.html", context)


@login_required(login_url='/accounts/login')
def post_create(request):
    # if not request.user.is_authenticated():
    #     raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, "Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)