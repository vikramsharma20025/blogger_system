from django.shortcuts import render,HttpResponse, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import UserAccount,Post,OTPStorage,Comment,Reply,Following
from django.contrib.auth.decorators import login_required
import datetime
# import smtplib
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

def generate_otp_here()->str:
    import random
    import string
    # string.punctuation + 
    letters = string.ascii_letters
    return ( ''.join(random.choice(letters) for i in range(6)))

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        return redirect('/dashboard')

@login_required
def add(request):
    if request.method=='POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        try:
            user = UserAccount.objects.filter(user=request.user)
            post1 = Post.objects.create(username=user[0],timeposted=datetime.datetime.now(),title=title,desc=desc)
            post1.save()
            return redirect('/dashboard')
        except UserAccount.DoesNotExist:
            return HttpResponse('cannot add the post try again by opening dashboard')
    else:
        return render(request,'add.html',context={})

@login_required
def globalpage(request):
    posts = Post.objects.all()
    context={
        'usernameofuser':request.user.username,
        'allposted':posts,
    }
    return render(request,'globalpage.html',context=context)
# def change_pass(request):
#     return HttpResponse('dummy function')

@login_required
def addreply(request,title,id):
    if request.method == 'POST':
        content = request.POST.get('reply')
        comment = Comment.objects.filter(id=id)[0]
        user = UserAccount.objects.filter(user=request.user)[0]
        reply = Reply.objects.create(commentwhereposted=comment,userwhoposted=user,content=content,timeposted=datetime.datetime.now())
        reply.save()
        print(id)
        return redirect('comment/'+title+str(id)[-1])
    else:
        # path = request.get_full_path
        # return redirect(path)
        return redirect('comment/'+title+'/'+str(id)[-1])
        # return redirect('comment/'+title+'/'+str(id))

@login_required
def update_profile(request):
    if request.method == 'POST':
        first_name  = request.POST.get('fname')
        last_name = request.POST.get('lname')
        username = request.POST.get('username')
        users = User.objects.filter(username = username)
        if len(users)==1:
            pass
        else:
            return render(request,'updateprofile.html',context={'message':'username already exist'})
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        address = request.POST.get('address')
        to_update_user = User.objects.filter(username=request.user.username).update(first_name=first_name,last_name=last_name,username=username)
        userpersonal = UserAccount.objects.filter(user=to_update_user).update(city=city,state=state,country=country,address=address)
        # userpersonal.save()
        return redirect('/dashboard')
    else:
        return render(request,'updateprofile.html',context={})

def update_post(request):
    return HttpResponse('update post')

@login_required
def followthis(request,username,usernameby):
    username = User.objects.filter(username=username)[0]
    usernameby = UserAccount.objects.filter(user=User.objects.filter(username=usernameby)[0])[0]
    countfollow = Following.objects.filter(person=usernameby,userfollowed=username)
    if username.username == usernameby.user.username:
        return HttpResponse('how are you thinking of following yourself')
    if len(countfollow)==0:
        follow = Following.objects.create(person=usernameby,userfollowed=username)
        follow.save()
        return redirect('user/'+username.username)
    else:
        return HttpResponse('already following')

def show_commentandreplies(request,title,id):
    post = Post.objects.filter(title=title)[0]
    comment = Comment.objects.filter(id=id)[0]
    replies = Reply.objects.filter(commentwhereposted=comment)
    context = {
        'post':post,
        'comments':comment,
        'replies':replies,
    }
    return render(request,'showcomment.html',context=context)

def showuser(request,username):
    userthis = User.objects.filter(username = username)[0]
    useraccounthis = UserAccount.objects.filter(user=userthis)[0]
    posts = Post.objects.filter(username=useraccounthis)
    comments = Comment.objects.filter(userwhoposted = useraccounthis)
    totalfollowers = Following.objects.filter(userfollowed=userthis)
    context = {
        'usertotalposts':len(posts),
        'totalcomments':len(comments),
        'totalfollowers':len(totalfollowers),
        'usernameofuser':username,
        'username':posts,
    }
    return render(request,'showuserthis.html',context=context)

@login_required
def commentadding(request,title):
    if request.method == 'POST':
        content = request.POST.get('comment')
        timeposted = datetime.datetime.now()
        userwhoposted = UserAccount.objects.filter(user = User.objects.filter(username=request.user.username)[0])[0]
        postedwhere = Post.objects.filter(title = title)[0]
        comment = Comment.objects.create(postedwhere=postedwhere,userwhoposted=userwhoposted,content=content,timeposted=timeposted)
        comment.save()
        return redirect('/post/'+title)
    else:
        path = request.get_full_path
        return redirect(path)


def showpost(request,title):
    # user = User.objects.filter(id=request.user.id)[0]
    # username = UserAccount.objects.filter(user=user)[0]
    posts = Post.objects.filter(title=title)
    comments = Comment.objects.filter(postedwhere=Post.objects.filter(title=title)[0])
    # filter(postedwhere=posts[0])
    context = {
        # 'username':user.username,
        'post':posts[0],
        'comments':comments,
    }
    return render(request,'viewpostthis.html',context=context)

@login_required
def commentsall(request):
    #comments = Comment.objects.filter(username = UserAccount.objects.filter(user=request.user))
    user=User.objects.filter(username=request.user.username)[0]
    username = UserAccount.objects.filter(user=user)[0]
    userwhoposted=Post.objects.filter(username=username)[0]
    comments = Comment.objects.filter(postedwhere=userwhoposted)
    context = {
        'usernameofuser':request.user.username,
        'comments':comments
    }
    return render(request,'commentsall.html',context=context)

def change_pass(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username)
        if user is not None:
            otp = generate_otp_here()
            userobj = UserAccount.objects.filter(user=user[0])
            # UserAccount.objects.filter(user=request.user.id)
            otp_object = OTPStorage.objects.create(username=userobj[0],otphere=otp,timecreation=datetime.datetime.now(),timevalid=(datetime.datetime.now()+datetime.timedelta(minutes=10)))
            otp_object.save()
            return HttpResponse('your otp is:'+otp+' please work')
        else:
            return render(request,'changepassword.html',context={'message':'otp problem'})
        # except:
        #     return render(request,'changepassword.html',context={'message':'something is off'})
    else:
        return render(request,'changepassword.html',context={'message':'first time coming'})
    #return render(request,'changepassword.html',context={'message':'something is off'})

def checkotp(request):
    if request.method == 'POST':
        username = str(request.POST.get('username'))
        otpentered = request.POST.get('otp')
        password = request.POST.get('newpassword')
        confirmpassword = request.POST.get('newpasswordconfirm')
        timeonentry = datetime.datetime.now()
        getted_Query_set = OTPStorage.objects.filter(username=request.user.id).all()
        if otpentered == getted_Query_set.otphere:
            if getted_Query_set.timevalid.time() >= timeonentry.time():
                try:
                    if password == confirmpassword:
                        password = make_password(password=password,hasher='default')
                        # User = get_user_model()
                        # user = User.objects.filter(username=username)[0]
                        # #.update(username=username,password=password)
                        # user.set_password(password)
                        # user.save()
                        # passwords=make_password(password,hasher='default')
                        user=User.objects.filter(username=username)
                        # .update(username=username,password=password)
                        user = user.update(username=username,password=password)
                        user.save()
                        # from django.contrib.auth import authenticate
                        # user = authenticate(username='username',password='passwd')
                        # try:
                        #     if user is not None:
                        #         user.set_password('new password')
                        #     else:
                        #         return render(request,'checkotp.html',context={'message':'user does not exist'})
                        # except:
                        #     return render(request,'checkotp.html',context={'message':'not setted'})
                        OTPStorage.objects.filter(username= request.user.id).delete()
                        if user is not None:
                            auth.login(request,user)
                            return redirect('/dashboard')
                        else:
                            return render(request,'checkotp.html',context={'message':'user problem '})
                        # return redirect('/login')
                    else:
                        return render(request,'checkotp.html',context = {'message':'both passwords did not matched try again'})
                except:
                    return render(request,'checkotp.html',context = {'message':'something wrong with otp try again and if it still does not work try again later'})
            else:
                return render(request,'checkotp.html',context = {'message':'otp timed out try generating new one'})
        else:
            return render(request,'checkotp.html',context = {'message':'otp not correct'})
    else:
        return render(request,'checkotp.html',context = {})


# def send_mail(receiver_mail,title,content):
#     s = smtplib.SMTP('smtp.gmail.com',587)
#     s.starttls()
#     s.login("jarvisa357@gmail.com","anything@ican")
#     message = "this is just a test mail to test this code"
#     s.sendmail("jarvisa357@gmail.com",receiver_mail,message)
#     s.quit()

@login_required
def personalinfo(request):
    user = User.objects.filter(username=request.user.username)[0]
    userpersonal = UserAccount.objects.filter(user=user)[0]
    context = {
        'user':user,
        'userpersonal':userpersonal,
    }
    return render(request,'personaldetails.html',context = context)


@login_required
def dashboard(request):
    # if currUser != 'vikramss':
    #posted = Post.objects.filter(id=currUser)
    posted = Post.objects.filter(username=UserAccount.objects.filter(user=request.user.id)[0]).all()
    # posted = Post.objects.filter(username=UserAccount.objects.filter(user = request.user.id)).all()
    # use list of dictionaries
    # for showing multiple values in django jinja template 
    # and use {{ forloop.counter }}
    # for keeping a count of the list number of index we can say
    # the it works like for i in dictkey
    # for external dict
    # then i.dictkey for internal dict
    context = {
        'username':posted,
        'usernameofuser':request.user.username,
    }
    return render(request,'index.html',context)

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name)
            phone = request.POST.get('phone')
            city = request.POST.get('city')
            state = request.POST.get('state')
            country = request.POST.get('country')
            address = request.POST.get('address')
            finaluser = UserAccount.objects.create(user=user,phone=phone,city=city,state=state,country=country,address=address)
            finaluser.save()
            return redirect('/login')
        except:
            return HttpResponse('username already exist try registring again')
    else:
        return render(request,'accounts/register.html',context={})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/dashboard')
        else:
            return render(request,'accounts/login.html',context={'message':'user problem visit'})
    else:
        return render(request,'accounts/login.html',context={'message':'first visit'})

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')
