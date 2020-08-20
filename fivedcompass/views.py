from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Quiz, User_Quiz_Answers
from django.contrib.auth.decorators import login_required
from .logic.quiz_solver import quiz_solver


def index(request):
    context = {
        'quizlist': Quiz.objects.all()
    }
    return render(request, 'fivedcompass/index.html', context)


def about(request):
    context = {
        'title': 'About Page'
    }
    return render(request, 'fivedcompass/about.html', context)


@login_required
def quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.question_set.all()

    context = {
        'quiz_name': quiz,
        'questions': questions
    }
    return render(request, 'fivedcompass/quiz.html', context)


@login_required
def save(request):
    if request.user.is_authenticated:
        if request.method == "POST":

            # Extract the answers and convert them to a string for database storage
            questionNum = len(request.POST.dict()) - 2
            answerList = []
            for i in range(questionNum):
                answerList.append(request.POST.get(f'{i + 1}'))

            # Collect all of the variables required to create associative table entry
            user = request.user            
            quiz = Quiz.objects.get(title=request.POST.get('quiz_name'))
            answers = ','.join(map(str, answerList))

            # Create and save entry
            newCompletedQuiz = User_Quiz_Answers(quiz=quiz, user=user, answers = answers, is_complete= True)
            newCompletedQuiz.save()    

        # Return the PK of the newest entry
        return redirect(f'/result/{newCompletedQuiz.pk}')
    else:
        return render(request, 'users/signin.html')


@login_required
def result(request, uqa_id):
    
    uqa_obj = User_Quiz_Answers.objects.get(id=uqa_id)
    user = request.user
    quiz_name = uqa_obj.quiz
    quiz_id = uqa_obj.quiz.pk
    answer_str = uqa_obj.answers

    orientationDict = quiz_solver(quiz_id, answer_str)

    # Change the dict so that dimensions have names instead of numbers

    finalResults = {
        "Economic": orientationDict.get("1"),
        "Government": orientationDict.get("2")
    }

    context = {
        'quiz_name': quiz_name,
        'user_name': user,
        'orientations' : finalResults
    }

    return render(request, 'fivedcompass/result.html', context)