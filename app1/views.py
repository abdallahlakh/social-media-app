import datetime,random
from django.shortcuts import  render
from .models import Comment, Like, Publication,Profile,Follow
from django.shortcuts import render,redirect
from .models import Publication
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# this fonction used to handle the registration process
def register(request):
    #when we click in the submit button the server of django handle the form in request format with post method
    if request.method == 'POST':
        #handling into python varibles the content of lableles in register.html page
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        email = request.POST['email']
        username = request.POST['username']
        #creating user row in user.auth table in database have this attributes
        user = User.objects.create_user(is_superuser = True,is_staff = True,first_name=first_name, last_name=last_name, password=password, email=email, username=username)
        user.save()
        #creating profile row in profile.auth table in database have this attributes
        Profile.objects.create(followers_num=0, following_num=0, post_num=0, profile_img=None, username=username, user_id=user.id)
        #handling the request and user created to making the login succesfully
        login(request, user)
        #go to the princple page
        return redirect('test')
    #when we go to the registration link the server of django handle the form in request format with get method and render the template to the user
    else:
        return render(request, 'register.html')



def logining(request):
     #when we run the server, the server of django handle the form in request format with get method and render the template to the user
    if request.method == "GET":
        return render(request, 'login.html')
    #when we click in the submit button the server of django handle the form in request format with post method to login user
    else:
        #fetching in the user.auth table wherein user exist or no with this username and password
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        #proccessing the none existing user in the table by rendering new format of login template
        if user is None:
            display_user_not_exit = True
            return render(request, 'login.html', {'display_user_not_exit': display_user_not_exit})
        else:
        #in this case the user exist so we login them after that we fetch from the database the needed things and we render them in the principle template    
           login(request, user)
           comment_box_generated = False
           data = Publication.objects.all().order_by('-id')
           all_profiles = Profile.objects.exclude(user_id=request.user.id)
           random_profiles = random.sample(list(all_profiles), 3)
           profile = Profile.objects.get(user_id=request.user.id)
           return render(request, 'test.html', {'data': data, 'comment_box_generated': comment_box_generated, 'profile': profile, 'pro': random_profiles})

    
#this is used when we click in logout link to process the logouting operation    
def logouting(request): 
    logout(request)
    return redirect('/')

#this fonction used to handle the like of publication process            
@login_required
def like(request):
    
    if request.method == 'POST':
        #we try to get liked publication id from database according to the input of the request
        publication_id = request.POST.get('publication_id')
        publication = Publication.objects.get(id=publication_id)
        
        
        
        #after that we verifiy  if this user already make like to this publication from like table in database
        try:
            like = Like.objects.get(publication_id=publication_id, user_id=request.user.id)
        except Like.DoesNotExist:
            like = Like.objects.create(publication_id=publication_id, user_id=request.user.id)
        
        #here we process the logic of like operation as the social media apps and ew modifiy the database
        if like.status == False:
            publication.likes_num += 1
            like.status = True
        else:
            publication.likes_num -= 1
            like.status = False
        
        publication.save()
        like.save()
        
        return redirect('test')

           

#this is the main fonction of the app
@login_required
def test(request):
    #this is processing of following operation 
    #here we verifiy if the request contains follow key with the corresponding user id value that we want to follow
    if request.POST.get('follow')!=None and request.POST.get('follow')!="":
            #here we handle the user id that we want to follow
            user_id = request.POST.get('follow')
            #here we try to verfiy of this user is already follow this guy here
            try:
               follow2= Follow.objects.get(user_follower_id=request.user.id,user_followed_id=user_id)
            except Follow.DoesNotExist:
               follow2= Follow.objects.create(user_follower_id=request.user.id,user_followed_id=user_id,following_status=False)
            #here we fetch from database the profile of this two guys follower and followed   
               
            profile_followed_person = Profile.objects.get(id=user_id)
            profile_following_person = Profile.objects.get(user_id=request.user.id)
            #here we make the process of following operation 
            #in this case the user already follow this guy so we must unfollowed the two guys by making modifcation in profile and following status
            if follow2.following_status==True:
               profile_followed_person.followers_num-=1
               profile_following_person.following_num-=1
               follow2.following_status=False
               follow2.save()
               profile_followed_person.save()
               profile_following_person.save()
               return redirect('test')
           
            #in this case the user already unfollow this guy so we must follow the two guys by making modifcation in profile and following status
            if follow2.following_status==False: 
               profile_followed_person.followers_num+=1  
               profile_following_person.following_num+=1
               follow2.following_status=True
               follow2.save() 
               profile_followed_person.save()
               profile_following_person.save()
               return redirect('test')
            #end of following process      
           
           
    #this is processing of view the profile user clicked operation 
    #here we verifiy if the request contains follow key with the corresponding user id value that we want to see his profile       
    if request.POST.get('user_idd')!="" and request.POST.get('user_idd')!=None:
        user_id = request.POST.get('user_idd')
        profile = Profile.objects.get(id=user_id)    
        return render(request, 'view_profile.html', {'profile': profile})    
    #end of view profile user clicked operation 
    
    
    #this is processing of fetching data from database in the normal case wehere there is no follow operation and view profile operation     
    if request.POST.get('follow')==None and request.POST.get('user_idd')==None:
        print(request.POST)
        comment_box_generated = False
        data = Publication.objects.all().order_by('-id')
        all_profiles = Profile.objects.exclude(user_id=request.user.id)
        random_profiles = random.sample(list(all_profiles), 3)
        profile = Profile.objects.get(user_id=request.user.id)
        follow=Follow.objects.all()
        return render(request, 'test.html', {'data': data, 'comment_box_generated': comment_box_generated, 'profile': profile, 'pro': random_profiles,'follow':follow})



#this is process of writing comment operation in publication by user
def comment(request):
    #here we verifiy if user is clicked in confirm coment button
    if 'comment_box'  in request.POST:
        textarea_content = request.POST.get('comment_box')
        #this is the case if comment is empty the other we create a row in comment table 
        if textarea_content=="":
            return redirect('/')
        else:
            publication_id = request.POST.get('publication_id')
            comment = Comment.objects.create(publication_id=publication_id, user_id=request.user.id,content=textarea_content,created=datetime)
            comment.save()
            return redirect('test')

     
#this is the process of seeing the comments fo publication      
def comments_detail(request):
    
    #the data needed to redner it in test.html
    data = Publication.objects.all().order_by('-id')
    comment_detail_generated=True
    publication_id = request.POST.get('publication_id')
    all_profiles = Profile.objects.exclude(user_id=request.user.id)
    profile = Profile.objects.get(user_id=request.user.id)
    random_profiles = random.sample(list(all_profiles), 3)
    
    #here we filter the comments of the correesponding publication 
    comments = Comment.objects.filter(publication_id=publication_id)
    return render(request,'test.html',{'comment_detail_id':publication_id,'data':data,'comments':comments,'comment_detail_generated':comment_detail_generated,'pro':random_profiles,'profile':profile})  
     



#this is the process of creating a publication 
def create_publication(request):
    #here we render the template to fill the textareas
    if request.method == "GET":
        return render(request, 'create_publication.html')
    else:
        # Retrieve form data
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('imageInput')
        print(image)
        # Create a new Publication object
        publication = Publication(user=request.user, title=title, description=description, img=image, likes_num=0, created=datetime)
        
        # Save the publication in the database
        publication.save()
        return redirect('test')

def edit_profile(request):
    #here we render the template to fill the textareas
    if request.method == "GET":
        return render(request, 'edit_profile.html')
    
    #here we fetch the data from request and update the database
    else:
        username = request.POST.get('username')
        image = request.FILES.get('imageInput')

        # Retrieve the current user's profile
        profile = Profile.objects.get(user=request.user)

        # Update the profile fields
        profile.username = username
        profile.profile_img = image
        profile.save()

        return redirect('/test')


    
#this is the process of viewing the authenticated user informations     
def view_profile(request):
    if request.method == "GET":
       profile=Profile.objects.get(user_id=request.user.id)
       return render(request, 'view.html',{'profile':profile})