from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='quiz-home'),
    path('about/', views.about, name='quiz-about'),
    path('quiz/<int:quiz_id>', views.quiz, name='quiz-take'),
    path('quiz/save', views.save, name='quiz-save'),
    path('result/<int:uqa_id>', views.result, name='quiz-result')
]