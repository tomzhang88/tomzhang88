
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic  #导入通用视图
from .models import Choice,Question
from django.utils import timezone


# Create your views here.
class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name='latest_question_list'   #要传给模板的变量
    def get_queryset(self):        #要生成的结果集
         return Question.objects.filter( pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
  model =Question     #要使用的数据模型，默认捕获pk（url模式中一致）
  template_name='polls/detail.html'  #要使用的模板

class ResultsView(generic.DetailView):
   model=Question
   template_name='polls/results.html'

def vote(request,question_id):
   p=get_object_or_404(Question,pk=question_id)
   try:
       selected_choice=p.choice_set.get(pk=request.POST['choice'])
   except(KeyError,Choice.DoesNotExist):
       return render(request,'polls/detail.html',{
           'question':p,
           'error_message':"you did not select a choice",
       })
   else:
       selected_choice.votes+=1
       selected_choice.save()
       return HttpResponseRedirect(reverse('polls:results',args=(p.id,)))