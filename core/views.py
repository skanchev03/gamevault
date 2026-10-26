from django.db.models import Avg, Sum
from django.shortcuts import render

from activity.models import PlaySession, Review
from library.models import Game, Genre, Platform


def dashboard(request):
    games = Game.objects.all()

    stats = {
        "total_games": games.count(),
        "completed_games": games.filter(
            status=Game.Status.COMPLETED
        ).count(),
        "playing_games": games.filter(
            status=Game.Status.PLAYING
        ).count(),
        "total_genres": Genre.objects.count(),
        "total_platforms": Platform.objects.count(),
        "total_reviews": Review.objects.count(),
        "total_playtime": (
            PlaySession.objects.aggregate(
                total=Sum("duration_minutes")
            )["total"]
            or 0
        ),
        "average_rating": (
            Review.objects.aggregate(avg=Avg("rating"))["avg"]
            or 0
        ),
    }

    context = {
        "stats": stats,
        "recent_games": games.order_by("-date_added")[:6],
        "recent_reviews": Review.objects.select_related("game")[:5],
        "recent_sessions": PlaySession.objects.select_related("game")[:5],
    }

    return render(request, "core/dashboard.html", context)


def custom_404(request, exception):
    return render(
        request,
        "core/404.html",
        status=404,
    )