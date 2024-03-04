from django.shortcuts import render,get_object_or_404
from login.models import CustomUser
from django.contrib import auth
from .forms import PostForm, CommentForm
from .models import Post, Comment



# Create your views here.

#login_and_signups
def signup_admin(request):
    if request.method=="POST":
        if request.POST['a_password1']==request.POST['a_password2']:
            admin=CustomUser.objects.create_superuser(
                       username=request.POST['admin_name'],
                       password=request.POST['a_password1']
            )

            return render(request,'login_admin.html')
    return render(request, "signup_admin.html")    

def signup_staff(request):
    if request.method=="POST":
        if request.POST['s_password1']==request.POST['s_password2']:
            staff=CustomUser.objects.create_staff(
                username=request.POST['staff_name'],
                password=request.POST['s_password1']
            )

            return render(request,'login_staff.html')
    return render(request,"signup_staff.html") 


def signup_common(request):
    if request.method=="POST":
        if request.POST['c_password1']==request.POST['c_password2']:
            common=CustomUser.objects.create_user(
                username=request.POST['common_name'],
                password=request.POST['c_password1']
            )
          
            return render(request,'login_common.html')
    return render(request,"signup_common.html")



def login_admin(request): 

    
    if request.user.is_authenticated:
          return render(request,'log_confirm.html')

    if request.method=="POST":
        admin_username=request.POST.get('admin_name')
        admin_password=request.POST.get('a_password')

        admin_user=auth.authenticate(
            request, username=admin_username, password=admin_password 
        )
    
        if admin_user is not None:
            auth.login(request, admin_user)
            

            return render(request,'log_confirm.html')
            
        
        else:
            return render(request,"login_admin.html", {
                'error':'Username or Password is incorrect.',
            })
        
    else:
        return render(request,"login_admin.html")
    

#login_required
def login_staff(request):

    if request.user.is_authenticated: 
    #and request.user.is_staff:
          return render(request,'log_confirm.html')


    if request.method=="POST":
        staff_username=request.POST['staff_name']
        staff_password=request.POST['s_password']

        staff_user=auth.authenticate(
            request, username=staff_username, password=staff_password 
        )
    
        if staff_user is not None:
            auth.login(request, staff_user)
            return render(request,'log_confirm.html')
        else:
            return render(request,'login_staff.html', {
                'error':'Username or Password is incorrect.',
            })
        
    else:
        return render(request, 'login_staff.html')




    
def login_common(request):

    if request.user.is_authenticated:
        return render(request,'log_confirm.html')

    if request.method=="POST":
        common_username=request.POST['common_name']
        common_password=request.POST['c_password']

        common_user=auth.authenticate(
            request, username=common_username, password=common_password 
        )
    
        if common_user is not None:
            auth.login(request, common_user)
            return render(request,'log_confirm.html')
        else:
            return render(request,"login_common.html", {
                'error':'Username or Password is incorrect.',
            })
        
    else:
        return render(request, "login_common.html")
    

#Welcome!
def welcome(request):
    return render(request,'welcome.html') #redirect not working idk why


def log_confirm(request):
    return render(request,'log_confirm.html')


def admin_only(request):
    print(f"Does superuser is activated?:{request.user.is_superuser}")
    if request.user.is_superuser:
        return render(request, 'admin_only.html')
    else:
        return render(request,'denied.html')
    
def everyone(request):
    return render(request,'everyone.html')

def no_commons(request):
    print(f"Does superuser is activated?:{request.user.is_superuser}")
    print(f"Does staff is activated?:{request.user.is_staff}")
    if request.user.is_superuser:
        return render(request,'no_commons.html')
    elif request.user.is_staff:
        return render(request,'no_commons.html')
    else:
        return render(request,'denied.html')    

def denied(request):
    return render(request,'denied.html')

def logout(request):
    if request.method == 'GET':
        auth.logout(request)
    return render(request,'welcome.html')


#Board and comments
def create_post(request):   #게시글 생성
    if request.method=='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'posted.html')
    else:
        form=PostForm()
    return render(request,'create_post.html',{'form':form})


def post_list(request):  #올린 게시글 열람
    #post = get_object_or_404(Post, pk=post_id)
    posts=Post.objects.all() #get_object_404의 id값 추가도 실습해보기
    comments=Comment.objects.all()
    #comment=post.comment_set.all() if post.comment_set.exists() else None
    return render(request, 'post_list.html',{'posts':posts,'comments':comments})


def delete_post(request, post_id):  #게시글 제거. _id는 객체 생성 시 자동으로 만들어짐(Primary Key와 같은 취급).
    specific_post=get_object_or_404(Post, pk=post_id) #특정 id의 객체를 가져와 변수에 저장해라
    try:
        specific_comment=Comment.objects.get(pk=post_id) #id가 pk여서 이렇게 함. 정확히는 내가 그렇게 views.py의 객체 생성 코드를 정의했으니까
    except Comment.DoesNotExist:
        specific_comment=None #try, except한 이유는 댓글 존재 여부에 상관없이 게시글 삭제가 가능하게 하기 위함이다.
        
    posts=Post.objects.all() #post_list의 html 변수와 이름이 같아야 렌더링 된다
    comments=Comment.objects.all()
  
    if request.method=='POST':
        specific_post.delete() 
        return render(request,'post_list.html',{'posts':posts,'comments':comments}) #남은 객체들을 렌더링
    return render(request, 'delete_post.html',{'specific_post':specific_post,'specific_comment':specific_comment})   #'specific_comment':specific_comment}) #가져온 객체를 페이지에 렌더링 할 것.


def comment(request, post_id):
    #post_written=get_object_or_404(Post,pk=post_id)
    if request.method=="POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form=comment_form.save(commit=False) #True 로 하면 post_id cannot be null 오류
            comment_form.post_id=post_id  #아마 여기하고 밑에 코드들을 돌리니까 먼저 commit=False하고 나중에 save()를 제대로 하는 듯
            comment_form.id=post_id #이거 안하면 delete 페이지 들어갈 때 id 불일치로 댓글 객체 못 불러와서 오류난다.
            comment_form.user=request.user
            comment_form.save()
            return render(request,'commented.html')
    else:
        comment_form=CommentForm()
    return render(request, 'comment.html',{'form':comment_form})
