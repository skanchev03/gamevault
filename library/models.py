
from django.core.validators import MinLengthValidator
from django.db import models


class Genre(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            MinLengthValidator(
                2,
                message="Genre names must contain at least 2 characters.",
            ),
        ],
        error_messages={
            "unique": "This genre already exists.",
            "blank": "Please enter a genre name.",
        },
        help_text="Enter a unique genre name, e.g. RPG or Strategy.",
    )

    description = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional short description of this genre.",
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "genres"

    def __str__(self):
        return self.name


class Platform(models.Model):
    name = models.CharField(
        max_length=80,
        unique=True,
        validators=[
            MinLengthValidator(
                2,
                message="Platform names must contain at least 2 characters.",
            ),
        ],
        error_messages={
            "unique": "This platform already exists.",
            "blank": "Please enter a platform name.",
        },
        help_text="Enter a platform name, e.g. PC or PlayStation 5.",
    )

    manufacturer = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional manufacturer name.",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name



class Game(models.Model):
    class Status(models.TextChoices):
        BACKLOG = "backlog", "Backlog"
        PLAYING = "playing", "Currently Playing"
        COMPLETED = "completed", "Completed"
        ABANDONED = "abandoned", "Abandoned"

    title = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(
                1,
                message="The game title cannot be empty.",
            ),
        ],
        error_messages={
            "blank": "Please enter a game title.",
        },
        help_text="Enter the game's official title.",
    )

    description = models.TextField(
        blank=True,
        help_text="Optional description of the game.",
    )

    developer = models.CharField(
        max_length=150,
        blank=True,
        help_text="The studio that developed the game.",
    )

    release_date = models.DateField(
        null=True,
        blank=True,
        help_text="Leave empty if the release date is unknown.",
    )

    cover_image_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Cover image URL",
        help_text="Optional URL pointing to the game's cover image.",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.BACKLOG,
    )

    genres = models.ManyToManyField(
        Genre,
        related_name="games",
        blank=True,
    )

    platforms = models.ManyToManyField(
        Platform,
        related_name="games",
        blank=True,
    )

    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["release_date"]),
        ]

    def __str__(self):
        return self.title

    @property
    def total_playtime_minutes(self):
        total = self.play_sessions.aggregate(
            total=models.Sum("duration_minutes")
        )["total"]

        return total or 0

    @property
    def total_playtime_hours(self):
        return round(self.total_playtime_minutes / 60, 1)
