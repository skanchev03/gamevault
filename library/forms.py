
from django import forms
from django.utils import timezone

from .models import Game, Genre, Platform


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = [
            "title",
            "description",
            "developer",
            "release_date",
            "cover_image_url",
            "status",
            "genres",
            "platforms",
        ]
        labels = {
            "title": "Game Title",
            "description": "Description",
            "developer": "Developer / Studio",
            "release_date": "Release Date",
            "cover_image_url": "Cover Image URL",
            "status": "Library Status",
            "genres": "Genres",
            "platforms": "Available Platforms",
        }
        help_texts = {
            "title": "Enter the official name of the game.",
            "status": "Choose the current status in your collection.",
            "genres": "Select one or more genres.",
            "platforms": "Select every platform you own or use.",
        }
        error_messages = {
            "title": {
                "required": "Please enter a game title.",
            },
            "cover_image_url": {
                "invalid": "Enter a valid URL for the cover image.",
            },
        }
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "e.g. The Witcher 3: Wild Hunt"}
            ),
            "description": forms.Textarea(
                attrs={"placeholder": "What is this game about?", "rows": 4}
            ),
            "developer": forms.TextInput(
                attrs={"placeholder": "e.g. CD Projekt Red"}
            ),
            "release_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "cover_image_url": forms.URLInput(
                attrs={"placeholder": "https://example.com/game-cover.jpg"}
            ),
            "status": forms.Select(),
            "genres": forms.SelectMultiple(
                attrs={"class": "form-select", "size": 4}
            ),
            "platforms": forms.SelectMultiple(
                attrs={"class": "form-select", "size": 4}
            ),
        }

    def clean_title(self):
        title = self.cleaned_data["title"].strip()

        if not title:
            raise forms.ValidationError(
                "A game title cannot contain only whitespace."
            )

        return title

    def clean_release_date(self):
        release_date = self.cleaned_data.get("release_date")

        if release_date and release_date > timezone.localdate():
            raise forms.ValidationError(
                "Release date cannot be in the future."
            )

        return release_date


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ["name", "description"]
        labels = {
            "name": "Genre Name",
            "description": "Description",
        }
        help_texts = {
            "name": "Use a short, recognizable genre name.",
            "description": "Optional details about this genre.",
        }
        error_messages = {
            "name": {
                "required": "Please enter a genre name.",
                "unique": "A genre with this name already exists.",
            },
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "e.g. Role-Playing Game"}
            ),
            "description": forms.TextInput(
                attrs={"placeholder": "Describe this genre briefly"}
            ),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if len(name) < 2:
            raise forms.ValidationError(
                "Genre names must contain at least 2 characters."
            )

        return name


class PlatformForm(forms.ModelForm):
    class Meta:
        model = Platform
        fields = ["name", "manufacturer"]
        labels = {
            "name": "Platform Name",
            "manufacturer": "Manufacturer",
        }
        help_texts = {
            "name": "Enter the console or platform name.",
            "manufacturer": "Optional hardware manufacturer.",
        }
        error_messages = {
            "name": {
                "required": "Please enter a platform name.",
                "unique": "A platform with this name already exists.",
            },
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "e.g. PlayStation 5"}
            ),
            "manufacturer": forms.TextInput(
                attrs={"placeholder": "e.g. Sony"}
            ),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if len(name) < 2:
            raise forms.ValidationError(
                "Platform names must contain at least 2 characters."
            )

        return name
