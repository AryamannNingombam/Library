from django.shortcuts import redirect,render,HttpResponse,reverse
from django import forms
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Books,Genre,UserInfo,Comment
#FORMS 
# Form to sign in to the website
class SignInForm(forms.Form):
    username = forms.CharField(max_length = 30,label = 'Username',widget  = forms.TextInput(attrs = {'id' : 'username','class' : 'formstyle','name' : 'username','placeholder':'Username'}))
    password= forms.CharField(max_length = 50,label = 'Password',widget  = forms.PasswordInput(attrs = {'id' : 'password','class' : 'formstyle','name'  : 'password','placeholder':'Password'}))
# Form to make an account in the website
class SignUpForm(forms.Form):
    username = forms.CharField(max_length = 40,label = 'Username',widget = forms.TextInput(attrs = {'id' : 'username','class': 'formstyle','name' : 'username','placeholder':'Username'}))
    first_name = forms.CharField(max_length = 40,label = 'First Name',widget = forms.TextInput(attrs = {'id' : 'first_name','class': 'formstyle','name' : 'first_name','placeholder':'First Name'}))
    last_name = forms.CharField(max_length = 40,label = 'Last Name',widget = forms.TextInput(attrs = {'id' : 'last_name','class': 'formstyle','name' : 'last_name','placeholder':'Last Name'}))
    password1= forms.CharField(max_length = 50,label = 'Password',widget  = forms.PasswordInput(attrs = {'id' : 'password1','class' : 'formstyle','name'  : 'password1','placeholder':'Password'}))
    password2 = forms.CharField(max_length = 50,label = 'Password Again',widget  = forms.PasswordInput(attrs = {'id' : 'password2','class' : 'formstyle','name'  : 'password2','placeholder':'Password Again'}))
    email = forms.EmailField(label = 'Email',widget  = forms.EmailInput(attrs = {'id' : 'email','class' : 'formstyle','name'  : 'email','placeholder':'Email Address'}))


# Form to change the account details once the account has been made(Only accessible if the user is himself/herself logged in) 
class SettingsForm(forms.Form):
    username = forms.CharField(max_length = 40,label = 'Username',widget = forms.TextInput(attrs = {'id' : 'username','class': 'formstyle','name' : 'username','placeholder':'Username'}))
    first_name = forms.CharField(max_length = 40,label = 'First Name',widget = forms.TextInput(attrs = {'id' : 'first_name','class': 'formstyle','name' : 'first_name','placeholder':'First Name'}))
    last_name = forms.CharField(max_length = 40,label = 'Last Name',widget = forms.TextInput(attrs = {'id' : 'last_name','class': 'formstyle','name' : 'last_name','placeholder':'Last Name'})) 
    email = forms.EmailField(label = 'Email',widget  = forms.EmailInput(attrs = {'id' : 'email','class' : 'formstyle','name'  : 'email','placeholder':'Email Address'}))




#CHECKING STRENGTH OF PASSWORD
def check_strength(username,password):
    if len(password) < 8:
        return False



    elif password == username:
        return None
    else:
        return True


# Create your views here.

#Home Page
def home(requests):
    #Getting all the books from the database   
    all_books = Books.objects.all()
    #If the user is logged in
    print(requests.user)
    if requests.user.is_authenticated:
        
        bbooksuser = UserInfo.objects.get(username = requests.user)
        #Getting the books that the user has borrowed
        bbooks = bbooksuser.books_borrowed.all() 
        #Making a set of recommended books for the user according to his preferences.
        #This has been made  a set to avoid repetition of books.
        recommended_list = set()
        #Making a for loop to get the recommended books
        for genre_user in bbooksuser.preferences.all():
            
            books = Books.objects.filter(genre = genre_user,borrowed = False)
            for book in books:
                #Adding to the set if the book's genre includes the users preferences 
                recommended_list.add(book)
        if len(recommended_list) == 0:
            recommended_list = []
        else:
            #Converting it to a list(Cuz why not)
             recommended_list =list(recommended_list)
       


            
                                            

        
          

        return render(requests,'library/index.html',{'books' :all_books,'borrowed_books': bbooks,'recommended_books' : recommended_list })
    else:
        return render(requests,'library/index.html',{'books' :all_books})
def sign_in(requests):
    #If the user is already logged in and still so dumb to access the sign in page. He gets redirected to the HomePage.
    if requests.user.is_authenticated:
        return redirect(reverse('home'))
    #When the user submits the data
    elif requests.method == "POST":
        #Making an instance of the submitted form
       check_form  =SignInForm(requests.POST)
      #Checking if the form is valid (Would be in 99.99% of the cases as HTML itself does some validation)
       if check_form.is_valid:
            username = requests.POST.get('username')
            password = requests.POST.get('password')
            #Checking if the user exists.
            checkAuth = authenticate(username = username,password = password)
            if checkAuth == None:
                #If the user doesn't exist, send this message.
                messages.warning(requests,'You Seem To Have Entered Something Wrong. Please Check Again.')
                return render(requests,'library/sign_in.html',{'form' : SignInForm(),})
            
            else:
                #Logging in the user if he/she exists.
                login(requests,checkAuth)
                return redirect(reverse('home'))
            
       else:
           #If the form is not valid (Very Rare)
            messages.warning(requests,'You Seem To Have Entered Something Wrong. Please Check Again.')
            return render(requests,'library/sign_in.html',{'form' : form,})
    else:
        #Sending a new form when user visits the page for the first time
        form  = SignInForm()
    
        return render(requests,'library/sign_in.html',{'form' : form,})



def sign_up(requests):
    #When the user sends the data
    if requests.method == 'POST':
        #Making the instance of the form with the data that the user enters
        formCheck = SignUpForm(requests.POST)
        #Checking if the form is valid (Would be in 99.99% of the cases as HTML itself does some validation)
        if formCheck.is_valid:
            genres  = requests.POST.getlist('genres')
            username = requests.POST.get('username')
            #Checking if the username already exists.(IMP)
            usercheck = User.objects.filter(username = username)
           #If the username doesn't exist
            if len(usercheck) == 0:
                password1 = requests.POST.get('password1')
                password2 = requests.POST.get('password2')
                email = requests.POST.get('email')
                first_name = requests.POST.get('first_name')
                last_name = requests.POST.get('last_name')
                #If the passwords don't match
                if password1 != password2:
                    messages.warning(requests,"Your passwords don't match. Please try again.")
                    return redirect(reverse('sign_up'),{'form' : SignUpForm(),'genres' : Genre.objects.all()})
                else:
                    check = check_strength(username,password1)
                    if check:
                        new_user = User.objects.create_user(username = username,password = password1,email = email)
                        new_user.first_name = first_name
                        new_user.last_name = last_name
                        
                        new_user.save()
                        user_genre = UserInfo(username = User.objects.get(username = username))
                        user_genre.save()
                        for genre in genres:
                           add_genre = Genre.objects.get(name = genre)
                           user_genre.preferences.add(add_genre)
                        

                        userlog = authenticate(username = username,password =password1)
                        login(requests,userlog)
                        messages.success(requests,f'Your account has been successfully made. Welcome {username}')
                        return redirect(reverse('home'))
                        
                                                      
                    elif check == None:
                        messages.warning(requests,"Your username and password are too similar. Please try again.")
                        return redirect(reverse('sign_up'),{'form' : SignUpForm(),'genres' : Genre.objects.all()})

                    else:
                        messages.warning(requests,"Your password is too weak. Please enter a better password.")
                        return redirect(reverse('sign_up'),{'form' : SignUpForm(),'genres' :Genre.objects.all()})

                
            else:
                #If the username already exists
                messages.warning(requests,'We are sorry, this username is already taken. Please enter some other username.')
                return redirect(reverse('sign_up'),{'form' : SignUpForm(),'genres' : Genre.objects.all()})

    else:
        #Sending a new form when user visits the page for the first time
        form  = SignUpForm()
        #Sending genres along with form to add options.
        genres = Genre.objects.all()
        
        return render(requests,'library/sign_up.html',{'form' : form,'genres' : genres})


#When user clicks the logout button on the navbar, Logout.
def logout_wt(requests):
    logout(requests)
    return redirect(reverse('home'))


#Giving more information about the book when user clicks the 'Read More' button when the book is displayed
def book_spec(requests,sno):
  
    


    book = Books.objects.get(sno = sno)
    comments = Comment.objects.filter(book_name = book )
    comments= comments[::-1]
    return render(requests,'library/book_spec.html',{'book': book,'book_genres' : book.genre.all(),'comments' : comments})


def  borrow_book(requests,sno):
    #When the user wants to borrow the specific book
    #Option shown when user enters the 'book_spec' view of a book.
    #This option will not be shown to the user if the book is already borrowed
    if requests.method == 'GET' and requests.user.is_authenticated:
        
        book_to_borrow =Books.objects.get(sno = sno)
        #THis is for error handling if there is a problem internally(Rare).
        if book_to_borrow.borrowed == True:
            book = Books.objects.get(sno = sno)
            messages.warning(requests,'There is some error.We are sorry for the inconvenience caused.')
            return render(requests,'library/book_spec.html',{'book': book})
        else:
            
            user_to_borrow = requests.user
            user_info = UserInfo.objects.get(username = user_to_borrow)
            #Adding the book to the borrowed list of the user
            user_info.books_borrowed.add(book_to_borrow)
            #Setting the value to True (False if the book is not borrowed)
            book_to_borrow.borrowed = True
            book_to_borrow.save()
            user_info.save()
            return HttpResponse('Success')


    else:
        #If by any chance the user gets access to this without logging in, he would be redirected back
        #to the sign in page
         return redirect(reverse('sign_in'))



def return_book(requests,sno):
    if requests.method == 'GET':
        #RETURN BOOK
        user1 = requests.user
        if user1.is_authenticated:
            book_to_return = Books.objects.get(sno = sno)
            #Setting the value to False(True if the book is borrowed)           
            book_to_return.borrowed = False
            user_info = UserInfo.objects.get(username = user1)
            #Removing the book from the user's borrowed list.
            user_info.books_borrowed.remove(book_to_return)
            
            
            
            book_to_return.save()
            return HttpResponse('Success')
    else:
        return HttpResponse('There Was Some Error.')


#SETTINGS
#TODO
def settings(requests):
    if requests.method == 'POST':
        current_user = requests.user
        userInfo = UserInfo.objects.get(username = current_user)
        username_entered  =requests.POST.get('username')
        user_check = User.objects.filter(username= username_entered)
        user_to_change = user_check[0]
        if len(user_check)>0 and user_check[0] == current_user:
            email_entered = requests.POST.get('email')
            first_entered = requests.POST.get('first_name')
            last_entered = requests.POST.get('last_name')
            genre_changes = requests.POST.getlist('genres')
            for genre in userInfo.preferences.all():
                userInfo.preferences.remove(genre)
            user_to_change.first_name = first_entered
            user_to_change.last_name = last_entered
            user_to_change.email = email_entered
            for genre in genre_changes:
                
                genre_selected = Genre.objects.get(name = str(genre))
                userInfo.preferences.add(genre_selected)
            user_to_change.save()
            userInfo.save()
            messages.success(requests,'Your settings have been changed!')
            return redirect(reverse('home'))
        
            
        elif len(user_check) == 0:
            email_entered = requests.POST.get('email')
            first_entered = requests.POST.get('first_name')
            last_entered = requests.POST.get('last_name')
            genre_changes = requests.POST.getlist('genres')
            for genre in userInfo.preferences.all():
                userInfo.preferences.remove(genre)
            user_to_change.first_name = first_entered
            user_to_change.last_name = last_entered
            user_to_change.email = email_entered
            user_to_change.username = username_entered

            for genre in genre_changes:
                print(genre)
                genre_selected = Genre.objects.get(name = str(genre))
                userInfo.preferences.add(genre_selected)
            user_to_change.save()
            userInfo.save()
            messages.success(requests,'Your settings have been changed!')
            return redirect(reverse('home'))
        else:
          
            messages.success(requests,'This Username Already Exists')
            return redirect(reverse('settings'))
    
    elif requests.user.is_authenticated:
        newform = SettingsForm()
        userInfo = UserInfo.objects.get(username = requests.user)
        allGenres = Genre.objects.all()
        userGenres = userInfo.preferences.all()
        newform['username'].initial = requests.user.username
        newform['email'].initial = requests.user.email
        newform['first_name'].initial = requests.user.first_name
        newform['last_name'].initial = requests.user.last_name

        return render(requests,'library/settings.html',{'form' : newform,'allgenres' : allGenres,'usergenres' : userGenres})
    else:
        

        return redirect(reverse('sign_in'))




def submit_comment(requests):
    #id = models.AutoField(primary_key = True)
    #commenter = models.ForeignKey(User,on_delete  = models.CASCADE)
    #content = models.TextField(default = '')
    #book_name=
    if requests.method == "POST":
        commenter = requests.user
        content = requests.POST.get('content')
        book_id = requests.POST.get('book_id')
        new_comment = Comment(commenter = commenter,content = content,book_name = Books.objects.get(sno= book_id))
        print('Done')
        new_comment.save()
        return HttpResponse('Done')

    else:
        return HttpResponse('You Cannot Access This Page. Sorry.')
