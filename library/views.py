from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import GameForm, GenreForm, PlatformForm
from .models import Game, Genre, Platform


def game_list(request):
    games = Game.objects.prefetch_related("genres", "platforms")

    search_query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    genre_id = request.GET.get("genre", "").strip()
    platform_id = request.GET.get("platform", "").strip()
    sort = request.GET.get("sort", "title")

    # Search by game title, developer, or description.
    if search_query:
        games = games.filter(
            Q(title__icontains=search_query)
            | Q(developer__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    # Filter by game status.
    if status in Game.Status.values:
        games = games.filter(status=status)
    else:
        status = ""

    # Filter by genre.
    if genre_id.isdigit():
        games = games.filter(genres__id=int(genre_id))
    else:
        genre_id = ""

    # Filter by platform.
    if platform_id.isdigit():
        games = games.filter(platforms__id=int(platform_id))
    else:
        platform_id = ""

    # Only allow supported sorting options.
    allowed_sort_fields = {
        "title": "title",
        "-title": "-title",
        "release_date": "release_date",
        "-release_date": "-release_date",
        "date_added": "date_added",
        "-date_added": "-date_added",
    }

    if sort not in allowed_sort_fields:
        sort = "title"

    # Avoid duplicate games after relationship filtering.
    games = games.distinct()

    # Add the primary key as a consistent tie-breaker.
    games = games.order_by(allowed_sort_fields[sort], "pk")

    context = {
        "games": games,
        "query": search_query,
        "search_query": search_query,
        "selected_status": status,
        "selected_genre": genre_id,
        "selected_platform": platform_id,
        "selected_sort": sort,
        "genres": Genre.objects.all(),
        "platforms": Platform.objects.all(),
        "statuses": Game.Status.choices,
    }

    return render(request, "library/game_list.html", context)


def game_detail(request, pk):
    game = get_object_or_404(
        Game.objects.prefetch_related(
            "genres",
            "platforms",
            "reviews",
            "play_sessions",
        ),
        pk=pk,
    )

    return render(
        request,
        "library/game_detail.html",
        {"game": game},
    )


def game_create(request):
    form = GameForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        game = form.save()
        return redirect("library:game_detail", pk=game.pk)

    return render(
        request,
        "library/game_form.html",
        {
            "form": form,
            "title": "Add a Game",
        },
    )


def game_update(request, pk):
    game = get_object_or_404(Game, pk=pk)
    form = GameForm(request.POST or None, instance=game)

    if request.method == "POST" and form.is_valid():
        game = form.save()
        return redirect("library:game_detail", pk=game.pk)

    return render(
        request,
        "library/game_form.html",
        {
            "form": form,
            "title": f"Edit {game.title}",
            "game": game,
        },
    )


def game_delete(request, pk):
    game = get_object_or_404(Game, pk=pk)

    if request.method == "POST":
        game.delete()
        return redirect("library:game_list")

    return render(
        request,
        "library/game_confirm_delete.html",
        {"game": game},
    )


def genre_list(request):
    genres = Genre.objects.prefetch_related("games")

    return render(
        request,
        "library/genre_list.html",
        {"genres": genres},
    )


def genre_create(request):
    form = GenreForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("library:genre_list")

    return render(
        request,
        "library/simple_form.html",
        {
            "form": form,
            "page_title": "Add a Genre",
            "cancel_url": "library:genre_list",
        },
    )


def genre_delete(request, pk):
    genre = get_object_or_404(Genre, pk=pk)

    if request.method == "POST":
        genre.delete()
        return redirect("library:genre_list")

    return render(
        request,
        "library/genre_confirm_delete.html",
        {"genre": genre},
    )


def platform_list(request):
    platforms = Platform.objects.prefetch_related("games")

    return render(
        request,
        "library/platform_list.html",
        {"platforms": platforms},
    )


def platform_create(request):
    form = PlatformForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("library:platform_list")

    return render(
        request,
        "library/simple_form.html",
        {
            "form": form,
            "page_title": "Add a Platform",
            "cancel_url": "library:platform_list",
        },
    )


def platform_delete(request, pk):
    platform = get_object_or_404(Platform, pk=pk)

    if request.method == "POST":
        platform.delete()
        return redirect("library:platform_list")

    return render(
        request,
        "library/platform_confirm_delete.html",
        {"platform": platform},
    )
