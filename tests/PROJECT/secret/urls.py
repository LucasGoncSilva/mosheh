# ruff: noqa

from typing import Final

from django.urls import path, URLPattern

from secret import views as v


app_name: Final[str] = 'secret'

credentials_urls: list[URLPattern] = [
    path(
        'credentials/',
        v.credential_list_view,
        name='credential_list_view',
    ),
    path(
        'credentials/new',
        v.CredentialCreateView.as_view(),
        name='credential_create_view',
    ),
    path(
        'credentials/<slug:slug>',
        v.credential_detail_view,
        name='credential_detail_view',
    ),
    path(
        'credentials/<slug:slug>/edit',
        v.CredentialUpdateView.as_view(),
        name='credential_update_view',
    ),
    path(
        'credentials/<slug:slug>/delete',
        v.CredentialDeleteView.as_view(),
        name='credential_delete_view',
    ),
]

payment_cards_urls: list[URLPattern] = [
    path(
        'payment-cards/',
        v.card_list_view,
        name='card_list_view',
    ),
    path(
        'payment-cards/new',
        v.CardCreateView.as_view(),
        name='card_create_view',
    ),
    path(
        'payment-cards/<slug:slug>',
        v.card_detail_view,
        name='card_detail_view',
    ),
    path(
        'payment-cards/<slug:slug>/edit',
        v.CardUpdateView.as_view(),
        name='card_update_view',
    ),
    path(
        'payment-cards/<slug:slug>/delete',
        v.CardDeleteView.as_view(),
        name='card_delete_view',
    ),
]

notes_urls: list[URLPattern] = [
    path(
        'notes/',
        v.note_list_view,
        name='note_list_view',
    ),
    path(
        'notes/new',
        v.NoteCreateView.as_view(),
        name='note_create_view',
    ),
    path(
        'notes/<slug:slug>',
        v.note_detail_view,
        name='note_detail_view',
    ),
    path(
        'notes/<slug:slug>/edit',
        v.NoteUpdateView.as_view(),
        name='note_update_view',
    ),
    path(
        'notes/<slug:slug>/delete',
        v.NoteDeleteView.as_view(),
        name='note_delete_view',
    ),
]

urlpatterns: list[URLPattern] = [
    path('', v.index, name='index'),
    # Login Credentials views
    *credentials_urls,
    # Payment Cards views
    *payment_cards_urls,
    # Security Notes views
    *notes_urls,
]
