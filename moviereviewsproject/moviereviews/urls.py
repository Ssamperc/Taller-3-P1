from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from movie import views as movieViews

urlpatterns = [
    path('admin/', admin.site.urls),

    # ====== Movie app ======
    path('', movieViews.home, name='home'),
    path('about/', movieViews.about, name='about'),
    path('statistics/', movieViews.statistics_view, name='statistics'),
    path('signup/', movieViews.signup, name='signup'),
    path("recommend/", movieViews.recommend_movie, name="recommend"),

    path('test/', movieViews.mi_vista, name='mi_vista'),

    # ====== News app (si existe) ======
    path('news/', include('news.urls')),
]

# Media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
