from urllib import response
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CommentForm, ReviewForm
from .models import Comment, Review
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.


def index(request):
    reviews = Review.objects.order_by("-pk")
    context = {"reviews": reviews}
    return render(request, "review/index.html", context)


def create(request):
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect("review:detail", review.pk)
    else:
        review_form = ReviewForm()
    context = {"review_form": review_form}

    return render(request, "review/create.html", context)


def detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    comment_form = CommentForm()
    context = {
        "review": review,
        "comment_form": comment_form,
        "comments": review.comment_set.all(),
    }

    return render(request, "review/detail.html", context)


def update(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES, instance=review)
        if review_form.is_valid():
            review_form.save()
            return redirect("review:detail", review.pk)
    else:
        review_form = ReviewForm(instance=review)
    context = {"review_form": review_form}

    return render(request, "review/update.html", context)


def delete(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    review.delete()
    return redirect("review:index")


@login_required
def comment_create(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
    return redirect("review:detail", review.pk)


def comment_delete(request, comment_pk, review_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect("review:detail", review_pk)


def comment_update(request, review_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)

    data = {"comment_content": comment.content}

    return JsonResponse(data)


def comment_update_complete(request, review_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment_form = CommentForm(request.POST, instance=comment)

    if comment_form.is_valid():
        comment = comment_form.save()

        data = {
            "comment_content": comment.content,
        }

        return JsonResponse(data)

    data = {
        "comment_content": comment.content,
    }

    return JsonResponse(data)


@login_required
def like(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    # 만약에 로그인한 유저가 이 글을 좋아요를 눌렀다면,
    # if review.like_users.filter(id=request.user.id).exists():
    if request.user in review.like_users.all():
        # 좋아요 삭제하고
        review.like_users.remove(request.user)

    else:
        # 좋아요 추가하고
        review.like_users.add(request.user)

    # 상세 페이지로 redirect

    data = {
        "like_cnt": review.like_users.count(),
    }

    return JsonResponse(data)


def search(request):
    all_data = Review.objects.order_by("-pk")
    search = request.GET.get("search", "")
    if search:
        search_list = all_data.filter(
            Q(title__icontains=search)
            | Q(content__icontains=search)
            # | Q(user__icontains=search) #FK라서 검색불가
        )

        context = {
            "search_list": search_list,
        }
    else:
        context = {
            "search_list": all_data,
        }

    return render(request, "review/search.html", context)
