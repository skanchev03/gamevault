
from django.core.validators import (
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.db import models


class Review(models.Model):
    game = models.ForeignKey(
        "library.Game",
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message="The minimum rating is 1."),
            MaxValueValidator(10, message="The maximum rating is 10."),
        ],
        help_text="Rate the game from 1 to 10.",
    )

    title = models.CharField(
        max_length=120,
        help_text="Give your review a short title.",
    )

    review_text = models.TextField(
        validators=[
            MinLengthValidator(
                20,
                message="Your review must contain at least 20 characters.",
            ),
        ],
        help_text="Share your thoughts in at least 20 characters.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["rating"]),
        ]

    def __str__(self):
        return f"{self.game.title} — {self.rating}/10"


class PlaySession(models.Model):
    game = models.ForeignKey(
        "library.Game",
        on_delete=models.CASCADE,
        related_name="play_sessions",
    )

    played_on = models.DateField(
        help_text="The date you played this game.",
    )

    duration_minutes = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                1,
                message="A play session must last at least 1 minute.",
            ),
        ],
        help_text="Duration of this session in minutes.",
    )

    notes = models.TextField(
        blank=True,
        help_text="Optional notes about this session.",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-played_on", "-created_at"]
        indexes = [
            models.Index(fields=["played_on"]),
        ]
        verbose_name = "play session"
        verbose_name_plural = "play sessions"

    def __str__(self):
        return (
            f"{self.game.title} — "
            f"{self.played_on:%Y-%m-%d} "
            f"({self.duration_minutes} min)"
        )
