from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question
#Insecure Deserialization
import pickle
from django.http import JsonResponse, HttpResponse
import json
from .models import Document
from django.db import connection
from .models import User
from django.shortcuts import render, redirect
#from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(generic.ListView):
    #login_url = 'polls:login'  # Redirects to the login page if not logged in
    #redirect_field_name = 'next'
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
    
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
        :5
    ]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def poll_view(request, poll_id):
    if 'user_id' not in request.session:  # Check session for authentication
        return redirect('login')  # Redirect to login if not authenticated


def vote(request, question_id):
    #if 'user_id' not in request.session:   # user authentication
        #return redirect(f'/polls/login/') #?next=/polls/{question_id}/vote'
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.GET["choice"]) # POST
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    

#    Insecure Deserialization

def deserialization_view(request):
    if request.method == "POST": 
        serialized_data = request.body  #delete this for improvement
        try:
            #serialized_data = request.body.decode('utf-8')
            deserialized_object = pickle.loads(serialized_data)
            #deserialized_object = json.loads(serialized_data)
            return JsonResponse({"deserialized_object": str(deserialized_object)})
            #return JsonResponse({"deserialized_object": deserialized_object})
        except Exception as e:
        #except json.JSONDecodeError as e:    
            return JsonResponse({"error": str(e)}, status=400)
    return HttpResponse("Send a POST request with serialized data.", status=405)


def question_details(request):
    question_id = request.GET.get("question_id")  # User-supplied input
    if not question_id or not question_id.isdigit():
        return HttpResponse("Invalid question ID.")
    """
    with connection.cursor() as cursor:
        # Vulnerable raw SQL query: not using parameterized queries
        cursor.execute(f"SELECT * FROM polls_question WHERE id = {question_id}")  # SQL Injection Vulnerability
        question = cursor.fetchone()
        """
    try:
        question = Question.objects.get(id=question_id)  # Use ORM instead of raw SQL
    except Question.DoesNotExist:
        return HttpResponse("Question not found.")
    # Fetch choices for the question
   

    return render(request, "polls/detail.html", {"question": question})


def question_xss(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def malicious_page(request):
    return render(request, "polls/malicious.html")



# user authentication
def login(request):
    if request.method == 'POST':  #POST
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if user.password == password:  # Weak password comparison
                request.session['user_id'] = user.id
                  # Default to 'polls' if no next parameter
                return redirect('polls:index')
        except User.DoesNotExist:
            pass

        return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')
# Logout view
def logout(request):
    request.session.flush()  # Clear session
    return redirect('polls:login')
    

def trigger_error(request):
    # Intentionally raise an error to expose debug information
    1 / 0  # Division by zero