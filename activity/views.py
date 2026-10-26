from django.shortcuts import get_object_or_404, redirect, render

from library.models import Game

from .forms import PlaySessionForm, ReviewForm
from .models import PlaySession, Review


def review_list(request):
    reviews = Review.objects.select_related("game")

    rating = request.GET.get("rating", "").strip()
    if rating.isdigit() and 1 <= int(rating) <= 10:
        reviews = reviews.filter(rating=int(rating))
    else:
        rating = ""

    return render(
        request,
        "activity/review_list.html",
        {
            "reviews": reviews,
            "selected_rating": rating,
            "ratings": range(1, 11),
        },
    )


def review_detail(request, pk):
    review = get_object_or_404(
        Review.objects.select_related("game"),
        pk=pk,
    )
    return render(
        request,
        "activity/review_detail.html",
        {"review": review},
    )


def review_create(request):
    form = ReviewForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        review = form.save()
        return redirect("activity:review_detail", pk=review.pk)

    return render(
        request,
        "activity/review_form.html",
        {"form": form, "page_title": "Write a Review"},
    )


def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    form = ReviewForm(request.POST or None, instance=review)

    if request.method == "POST" and form.is_valid():
        review = form.save()
        return redirect("activity:review_detail", pk=review.pk)

    return render(
        request,
        "activity/review_form.html",
        {
            "form": form,
            "page_title": "Edit Review",
            "review": review,
        },
    )


def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if request.method == "POST":
        review.delete()
        return redirect("activity:review_list")

    return render(
        request,
        "activity/review_confirm_delete.html",
        {"review": review},
    )


def session_list(request):
    sessions = PlaySession.objects.select_related("game")

    game_id = request.GET.get("game", "").strip()
    if game_id.isdigit():
        sessions = sessions.filter(game_id=int(game_id))
    else:
        game_id = ""

    return render(
        request,
        "activity/session_list.html",
        {
            "sessions": sessions,
            "selected_game": game_id,
            "games": Game.objects.order_by("title"),
        },
    )


def session_create(request):
    form = PlaySessionForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        session = form.save()
        return redirect("activity:session_list")

    return render(
        request,
        "activity/session_form.html",
        {"form": form, "page_title": "Log a Play Session"},
    )


def session_update(request, pk):
    session = get_object_or_404(PlaySession, pk=pk)
    form = PlaySessionForm(request.POST or None, instance=session)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("activity:session_list")

    return render(
        request,
        "activity/session_form.html",
        {
            "form": form,
            "page_title": "Edit Play Session",
            "session": session,
        },
    )


def session_delete(request, pk):
    session = get_object_or_404(PlaySession, pk=pk)

    if request.method == "POST":
        session.delete()
        return redirect("activity:session_list")

    return render(
        request,
        "activity/session_confirm_delete.html",
        {"session": session},
    )
