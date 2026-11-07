from django.urls import path

from . import views


app_name = "portfolio"

urlpatterns = [
    path("", views.home, name="home"),
    path("tema/<slug:theme_slug>/", views.home, name="theme"),
    path("frentes/<slug:slug>/", views.front_detail, name="front_detail"),
    path("projetos/<slug:slug>/", views.project_detail, name="project_detail"),
    path("painel/", views.panel_dashboard, name="panel_dashboard"),
    path("painel/entrar/", views.panel_login, name="panel_login"),
    path("painel/sair/", views.panel_logout, name="panel_logout"),
    path("painel/cases/novo/", views.panel_project_create, name="panel_project_create"),
    path(
        "painel/cases/<int:pk>/editar/",
        views.panel_project_update,
        name="panel_project_update",
    ),
    path("sitemap.xml", views.sitemap, name="sitemap"),
    path("robots.txt", views.robots, name="robots"),
]
