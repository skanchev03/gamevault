from django import forms
from django.utils import timezone

from .models import PlaySession, Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["game", "title", "rating", "review_text"]
        labels = {
            "game": "Game",
            "title": "Review Title",
            "rating": "Your Rating",
            "review_text": "Your Review",
        }
        help_texts = {
            "rating": "Choose a rating between 1 and 10.",
            "review_text": "Write at least 20 characters.",
        }
        error_messages = {
            "title": {
                "required": "Please give your review a title.",
            },
            "rating": {
                "required": "Please select a rating.",
            },
            "review_text": {
                "required": "Please write your review.",
            },
        }
        widgets = {
            "game": forms.Select(),
            "title": forms.TextInput(
                attrs={"placeholder": "e.g. A masterpiece worth replaying"}
            ),
            "rating": forms.Select(
                choices=[(i, f"{i}/10") for i in range(1, 11)]
            ),
            "review_text": forms.Textarea(
                attrs={
                    "placeholder": "Share your experience with this game...",
                    "rows": 6,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["game"].disabled = True
            self.fields["game"].help_text = (
                "The game cannot be changed after a review is created."
            )

    def clean_review_text(self):
        review_text = self.cleaned_data["review_text"].strip()

        if len(review_text) < 20:
            raise forms.ValidationError(
                "Your review must contain at least 20 characters."
            )

        return review_text


class PlaySessionForm(forms.ModelForm):
    class Meta:
        model = PlaySession
        fields = ["game", "played_on", "duration_minutes", "notes"]
        labels = {
            "game": "Game Played",
            "played_on": "Date Played",
            "duration_minutes": "Duration (minutes)",
            "notes": "Session Notes",
        }
        help_texts = {
            "duration_minutes": "Enter the total number of minutes played.",
            "notes": "Optional notes about your progress or experience.",
        }
        error_messages = {
            "duration_minutes": {
                "required": "Please enter the session duration.",
                "invalid": "Enter a valid duration in minutes.",
            },
        }
        widgets = {
            "game": forms.Select(),
            "played_on": forms.DateInput(
                attrs={"type": "date"}
            ),
            "duration_minutes": forms.NumberInput(
                attrs={"min": 1, "placeholder": "e.g. 90"}
            ),
            "notes": forms.Textarea(
                attrs={"placeholder": "What did you play today?", "rows": 3}
            ),
        }

    def clean_played_on(self):
        played_on = self.cleaned_data["played_on"]

        if played_on > timezone.localdate():
            raise forms.ValidationError(
                "A play session cannot be dated in the future."
            )

        return played_on

    def clean_duration_minutes(self):
        duration = self.cleaned_data["duration_minutes"]

        if duration <= 0:
            raise forms.ValidationError(
                "Session duration must be greater than zero."
            )

        return duration
