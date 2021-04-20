"""Views for blog application
"""
# from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from blog.models import Post, Comment

from blog.forms import EmailPostForm, CommentForm

# Function way
# def post_list(request):
#     object_list = Post.published.all()
#     paginator = Paginator(object_list=object_list, per_page=3)
#     page = request.GET.get("page")
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # Jeżeli dostaliśmy nie-int'a to zwracamy 1-wszą stronę
#         posts = paginator.page(1)
#     except EmptyPage:
#         # Jeżeli dostaliśmy stronę 5
#         # podczas gdy mamy w sumie 3 strony zwrócimy stronę 3
#         posts = paginator.page(paginator.num_pages)
#     return render(
#         request, "blog/post/list.html", {"page": page, "posts": posts}
#     )


class PostListView(ListView):
    """Class based way of creating views"""

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_detail(request, year, month, day, post):
    """Jeżeli wywołany jest POST przetwarzamy wysłany formularz
    w przypadku GET'a zwracamy formularz do wypełnienia

    Args:
        request ([type]): [description]
        year ([type]): [description]
        month ([type]): [description]
        day ([type]): [description]
        post ([type]): [description]

    Returns:
        [type]: [description]
    """
    post = get_object_or_404(
        Post,
        slug=post,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    # wykorzystanie menedżera obiektów powiązanych comments
    comments = post.comments.filter(active=True)

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Powoduje że powstaje egzemplarz modelu ale nie trafia do bazy
            # .save jest dostępny dla ModelForm ale nie dla Form
            new_comment = comment_form.save(commit=False)
            # dodajemy posta i wtedy zapisujemy
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request,
        "blog/post/detail.html",
        {"post": post, "comments": comments, "comment_form": comment_form},
    )


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="published")
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Gets validated data
            cleaned = form.cleaned_data
            # these two work together to make shareable lingo to post
            # build_absolute_uri adds HTTP schema and host name
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cleaned["name"]} ({cleaned["email"]}) zachęca do przeczytania "{post.title}"'
            message = f'Przeczytaj post "{post.title}" na stronie {post_url}\n\n Komentarz dodany przez {cleaned["name"]} : {cleaned["comments"]}'
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[cleaned["to"]],
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request,
        "blog/post/share.html",
        {"post": post, "form": form, "sent": sent},
    )
