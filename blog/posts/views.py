from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect,Http404
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.utils import timezone



# Create your views here.
def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form =PostForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        print("fomr validation")
        instance=form.save(commit=False)
        instance.user=request.user

        print (form.cleaned_data.get("title"))

        instance.save()
        messages.success(request,"Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
        print("after return")
    else:
        messages.error(request,"not Successfully created")
        print("context")
    context={
    "form":form,


    }
    return render(request,"post_form.html",context)



def post_detail(request,slug=None):
    instance=get_object_or_404(Post,slug=slug)
    context={
    "title":"title",
    "instance":instance,
    }
    return render(request,"post_Detail.html",context)

def post_list(request):
    queryset_list=Post.objects.filter(draft=False).filter(publish__lte=timezone.now())    #all()#.order_by("-timestamp")
    paginator = Paginator(queryset_list, 3) # Show 25 contacts per page
    page_request_var="page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context={
        "title":"list",
        "objects":queryset,
        "page_request_var":page_request_var,
    }


    return render(request,"post_list.html",context)




def post_update(request,slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance=get_object_or_404(Post,slug=slug)
    form =PostForm(request.POST or None,request.FILES or None,instance=instance)
    if form.is_valid():
        instance=form.save(commit=False)

        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())



    context={
    "title":"title",
    "instance":instance,
    "form":form,
    }
    return render(request,"post_form.html",context)



def post_delete(request,slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance=get_object_or_404(Post,slug=slug)

    messages.success(request,"Successfully deleted")
    instance.delete()

    return redirect("posts:lists")
