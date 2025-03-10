from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import User, Article, Project
import secrets
from django.core.mail import send_mail
from article_creator.settings import EMAIL_HOST_USER, ALLOWED_HOSTS, EMAIL_HOST_PASSWORD
import base64
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import PasswordConfirmationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password




@login_required
def password_confirmation_view(request):
    if request.method == "POST":
        form = PasswordConfirmationForm(user=request.user, data=request.POST)
        if form.is_valid():
            # Set a session variable to indicate password confirmation
            request.session['password_confirmed'] = True
            return redirect(reverse('account_settings'))  # Replace with your settings page URL
    else:
        form = PasswordConfirmationForm(user=request.user)
    return render(request, 'webapp/pages/password_confirmation.html', {'form': form})


@login_required
def account_settings_view(request):
    print(request.session.get('password_confirmed'))
    if not request.session.get('password_confirmed') and not 'regenerate_access_code' in request.POST:
        print('TESTTESTTEST')
        return redirect(reverse('password_confirmation'))
    # Clear the session variable to require re-confirmation next time
    user = request.user
    request.session['password_confirmed'] = False
    print('regenerate_access_code' in request.POST, "REGENERATE ACCESS CODE")
    if request.method == "POST" and 'regenerate_access_code' in request.POST:
        # Regenerate the access code
        user.regenerate_access_code()  # Generate a new access code
        request.session['access_code'] = user.accessCode  # Store in session for one-time display
        messages.success(request, "Access code regenerated successfully.")
        request.session['password_confirmed'] = True
        print('1', request.session.get('password_confirmed'))
        return redirect('account_settings')
    
    access_code = request.session.pop('access_code', None)
    return render(request, 'webapp/pages/settings.html', {
        'access_code': access_code,
    })










@login_required
def regenerate_access_code_view(request):
    user = request.user

    if request.method == "POST":
        user.regenerate_access_code()
        # Store the access code in the session for one-time display
        request.session['access_code'] = user.accessCode
        messages.success(request, "Access code regenerated successfully.")
        return redirect('view_access_code')  # Redirect to view the code

    return render(request, 'regenerate_access_code.html')

@login_required
def view_access_code_view(request):
    access_code = request.session.pop('access_code', None)  # Remove from session after viewing
    if not access_code:
        messages.error(request, "No access code to display. Please regenerate.")
        return redirect('regenerate_access_code')

    return render(request, 'view_access_code.html', {'access_code': access_code})








def upload_image_to_db(image_file):
    # Read the image file
    image_data = image_file.read()
    
    # Encode the image to base64
    encoded_image = base64.b64encode(image_data).decode('utf-8')
    
    # Format as a base64 data URI
    base64_image = f"data:{image_file.content_type};base64,{encoded_image}"
    
    return base64_image

# def pdf_to_html_with_styles(pdf_file):
#     pdf_stream = io.BytesIO(pdf_file.read())
#     # Load the PDF document
#     pdf_document = ap.Document(pdf_stream)
    
#     # Set up options for converting PDF to HTML
#     html_options = ap.HtmlSaveOptions()
#     html_options.is_html5_parser_enabled = True  # Enable HTML5 parser for modern HTML
#     html_options.css_style_sheet_type = ap.CssStyleSheetType.INLINE  # Use inline styles
    
#     # Save the PDF as HTML
#     output_html_file = "output_inline_css.html"
#     pdf_document.save(output_html_file, html_options)
    
#     return output_html_file


# def pdf_to_html_with_styles(pdf_file):
#     pdf_stream = io.BytesIO(pdf_file.read())
#     doc = ap.Document(pdf_stream)
#     options = ap.saving.HtmlSaveOptions()
#     options.save_format = ap.SaveFormat.HTML
#     options.css_style_sheet_type = ap.saving.CssStyleSheetType.INLINE
#     output_html_file = "output_inline_css.html"
#     doc.save(output_html_file, options)
    
#     # Read the content of the generated HTML file
#     with open(output_html_file, 'r', encoding='utf-8') as file:
#         html_content = file.read()

#     # Optional: Delete the file after reading if you don't need to keep it
#     os.remove(output_html_file)
    
#     return html_content


# def pdf_to_html_with_styles(pdf_file):
#     # Open the PDF file
#     doc = fitz.open(stream=pdf_file.read(), filetype="docx_file")
#     html_content = "<html><body>"

#     # Iterate through each page
#     for page_num in range(len(doc)):
#         page = doc[page_num]
#         # Extract HTML with inline styles
#         html_content += page.get_text("html")

#     html_content += "</body></html>"
#     return html_content




# Create your views here.

def index(request):
    if request.user.is_authenticated:
        articles = Article.objects.filter(author=request.user).order_by('-creation_date')
        return render(request, 'webapp/pages/index.html', {'articles': articles, 'projects': Project.objects.filter(author=request.user)})
    return render(request, 'webapp/pages/index.html')

def login_view(request):
    if request.method == "POST":
        if request.POST.get('username') and request.POST.get('password'):
            username = request.POST.get('username')
            password = request.POST.get('password')
            if User.objects.get(username=username).isVerified:
                # print('password: ',password)
                # print(User.objects.get(username=username).password)

                # print(User.objects.get(username=username))
                # print(User.objects.get(username=username).isVerified)
                user = authenticate(request, username=username, password=password)
                # if check_password(password, User.objects.get(username=username).password):
                #     print('THINROGUIEJIORFEJOIREFQJI WORKS')
                # else:
                #     print('THINROGUIEJIORFEJOIREFQJI DOESNT WORK')
                # print('eeeee', user)
                if user:
                    login(request, user)
                    return render(request, 'webapp/pages/index.html')
                else:
                    return render(request, 'webapp/pages/signup.html', {'message': 'Sign Up Failed'})
            else:
                return render(request, 'webapp/pages/signup.html', {'message': 'Unverified Account'})
    else:
        return render(request, 'webapp/pages/signup.html')
    
def forgot_password_view(request):
    if request.method == "POST":
        if request.POST.get('email'):
            email = request.POST.get('email')
            user = User.objects.filter(email=email)
            user = user[0]
            access_code = user.accessCode
            send_mail('Forgot Password', f'Access Code Link http://{ALLOWED_HOSTS[0]}/password_reset/{access_code}', EMAIL_HOST_USER, [email])
            return render(request, 'webapp/pages/index.html')
        else:
            return render(request, 'webapp/pages/signup.html', {'message': 'Missing Required Fields'})
    else:
        return render(request, 'webapp/pages/forgot_password.html')

def password_reset_view(request, access_code):
    if request.method == "POST":

        if request.POST.get('password'):
            user = User.objects.get(accessCode=access_code)
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if user and password and password == confirm_password:
                user.set_password(request.POST.get('password'))
                user.save()
                # if check_password(password, user.password):
                #     print(user.password)
                #     print('THINROGUIEJIORFEJOIREFQJI WORKS')
                # else:
                #     print('THINROGUIEJIORFEJOIREFQJI DOESNT WORK')
                return render(request, 'webapp/pages/index.html')

            return render(request, 'webapp/pages/index.html')
        else:

            return render(request, 'webapp/pages/signup.html', {'message': 'Missing Required Fields'})
    else:
        return render(request, 'webapp/pages/reset_password.html', {'access_code': access_code})
    
def logout_view(request):
    logout(request)
    return render(request, 'webapp/pages/index.html')

def signup_view(request):  
    if request.method == "POST":
        if request.POST.get('username') and request.POST.get('email') and request.POST.get('password'):
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            VerificationCode = secrets.token_urlsafe(50)
            if password != confirm_password:
                return render(request, 'webapp/pages/signup.html', {'error': 'Passwords do not match'})
            user = User.objects.create_user(username, email, password, VerificationCode=VerificationCode)
            verification_email(email, VerificationCode)
            # user = authenticate(username=username, password=password)
            # if user is not None:
            #     login(request, user)
            #     return render(request, 'webapp/pages/index.html')
            # else:
            #     return render(request, 'webapp/pages/signup.html', {'error': 'Sign Up Failed'})
            return index(request)
    else:
        return render(request, 'webapp/pages/signup.html')
    

def verification_email(email, VerificationCode):
    subject = "Verify Your Email"

    # print(ALLOWED_HOSTS, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    message = f"Verification Link http://{ALLOWED_HOSTS[0]}/verify_email/{VerificationCode}"
    recipient_list = [email]
    send_mail(subject, message, EMAIL_HOST_USER, recipient_list)
    # EMSG = EmailMessage(subject, message, to=recipient_list)
    # EMSG.send()

def verify_email(request, VerificationCode):
    user = User.objects.get(VerificationCode=VerificationCode)
    user.isVerified = True
    user.regenerate_access_code()
    user.save()
    user = authenticate(username=user.username, password=user.password)
    if user is not None:
        login(request, user)
        return render(request, 'webapp/pages/index.html')
    else:
        return render(request, 'webapp/pages/signup.html', {'error': 'Sign Up Failed'})
    








# ARTICLE VIEWS 
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\











def create_article(request):
    if request.method == "POST":
        if request.POST.get('title') and (request.POST.get('content') or request.FILES.get('html_file')):
            title = request.POST.get('title')
            html_file = request.FILES.get('html_file')
            if request.FILES.get('image'):
                image = request.FILES.get('image')
                base64_image = upload_image_to_db(image)
            else:  
                base64_image = None
                image = None
            author = request.user

            if html_file:
                html_content = html_file.read().decode('utf-8')
            else:
                html_content = request.POST.get('content', '')
                print(html_content)
            description = request.POST.get('description')

            projects = []
            for i in Project.objects.filter(author=request.user):
                if request.POST.get(i.name):
                    projects.append(i)

            print('PROJECTS::::::::::::::::::::::::: ', projects)
            
            if image:
                article = Article.objects.create(title=title, content=html_content, author=author, description=description, image_base64=base64_image)
            elif not image:
                article = Article.objects.create(title=title, content=html_content, author=author, description=description)
            article.projects.set(projects)
            print(article.projects.all())
            print(article)
            return redirect(f"view_article", article_name=article.title)
            # return render(request, 'webapp/pages/index.html', {'article': article})
        else:
            return render(request, 'webapp/pages/index.html', {'message': "Missing Required Fields"})
    else:
        return index(request)
    

def edit_article(request, article_name): 
    print("EDIT ARTICLE: ", request.method)
    print("IMAGE: ", request.POST.get('keep_image'))
    if request.method == "POST":
        article = Article.objects.get(title=article_name, author=request.user)
        if article:
            article.title = request.POST.get('title')
            html_file = request.FILES.get('html_file')
            image = request.FILES.get('image')
            author = request.user

            if html_file:
                article.File = html_file
                article.content = html_file.read().decode('utf-8')
            elif (not article.File) and article.content and request.POST.get('content') and not html_file:
                article.content = request.POST.get('content')


            article.description = request.POST.get('description')

            projects = request.POST.get('projects')
            if projects:
                projects = projects.split(',')
                projects = [int(project) for project in projects]
                projects = Project.objects.filter(id__in=projects)
            else:
                projects = []
            article.projects.set(projects)

            print("IMAGE: ", request.POST.get('keep_image'))
            if request.POST.get('keep_image') == "Yes":
                if image:
                    # article.Image = image
                    article.image_base64 = upload_image_to_db(image)
            elif request.POST.get('keep_image') == "No":
                # print("UI355HTRGELGERUWIGHERIFRHEUQOIHFREQUWHFRUQIEIRFQUWHRQIOEWHFRIQUWQUIEWFUIHWFEU")
                # print("NO IMAGE:")
                # article.Image = None
                article.image_base64 = None

            if article.author == author:
                article.save()
            else:
                return render(request, 'webapp/pages/index.html', {'message': "You're not the author of this article. How did you get here?"})
            
            return redirect(f"view_article", article_name=article.title)
            # return render(request, 'webapp/pages/index.html', {'article': article})
        else:
            return render(request, 'webapp/pages/index.html', {'message': "Article doesn't exist. How did you get here?"})
    else:
        return index(request)
    
def delete_article(request, article_name):
    article = Article.objects.get(title=article_name, author=request.user)
    if article:
        article.delete()
        return index(request)
    else:
        return render(request, 'webapp/pages/index.html', {'message': "Article doesn't exist. How did you get here?"})
    
def view_article(request, article_name):
    article = Article.objects.get(title=article_name)
    return render(request, 'webapp/pages/article.html', {'article': article})






# PROJECT VIEWS 
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\





def create_project(request):
    if request.method == "POST":
        if request.POST.get('name') and request.POST.get('description'):
            name = request.POST.get('name')
            description = request.POST.get('description')
            image = request.FILES.get('image')
            if not image:
                image = None
                base64_image = None
            else:
                base64_image = upload_image_to_db(image)
            author = request.user
            sub_themes = str(request.POST.get('themes')).split(',')
            if not sub_themes:
                sub_themes = []
            project = Project.objects.create(name=name, description=description, author=author, projectSubThemes=sub_themes, image_base64=base64_image)
            return index(request)
        else:
            return render(request, 'webapp/pages/index.html', {'message': "Missing Required Fields"})
    else:
        return index(request)
    

def edit_project(request, project_name):
    if request.method == "POST":
        project = Project.objects.get(name=project_name, author=request.user)
        if project:
            project.name = request.POST.get('name')
            project.description = request.POST.get('description')
            image = request.FILES.get('image')
            if request.FILES.get('keep_image') == "Yes":
                if image:
                    project.image_base64 = upload_image_to_db(image)
            elif request.FILES.get('keep_image') == "No":
                project.image_base64 = None
            sub_themes = str(request.POST.get('themes')).split(',')
            if not sub_themes:
                sub_themes = []
            project.projectSubThemes = sub_themes
            if project.author == request.user:
                project.save()
            else:
                return render(request, 'webapp/pages/index.html', {'message': "You're not the author of this project. How did you get here?"})
            return index(request)
        else:
            return render(request, 'webapp/pages/index.html', {'message': "Project doesn't exist. How did you get here?"})
    else:
        return index(request)
    
def delete_project(request, project_name):
    project = Project.objects.get(name=project_name, author=request.user)
    if project:
        project.delete()
        return index(request)
    else:
        return render(request, 'webapp/pages/index.html', {'message': "Project doesn't exist. How did you get here?"})
    

def view_project(request, project_name):
    project = Project.objects.get(name=project_name, author=request.user)
    if project:
        print('thing1')
        articles = Article.objects.filter(projects__name=project_name, author=request.user)
        articles = Article.objects.filter(projects__name=project_name, author=request.user).order_by('-creation_date')
        if articles:
            print('thing1')
            print(articles)
        return render(request, 'webapp/pages/project.html', {'project': project, 'articles': articles})
    else:
        return index(request, {'message': "Project doesn't exist. How did you get here?"})
    




@csrf_exempt
def client_fetch_view_article(request, access_code, article_name):
    user = User.objects.get(accessCode=access_code)
    if user:
        article = Article.objects.get(title=article_name, author=user)
        if article:
            return JsonResponse({'article': article, 'content': article.content, 'image': article.image_base64, 'description': article.description, 'creation_date': article.creation_date})
        else:
            JsonResponse({'message': "Article doesn't exist."})
    else:
        return JsonResponse({'message': "Incorrect Access Code."})
    
@csrf_exempt
def  client_fetch_project_articles(request, access_code, project_name):
    user = User.objects.get(accessCode=access_code)
    if user:
        project = Project.objects.get(name=project_name, author=user)
        if project:
            articles = Article.objects.filter(projects__name=project_name, author=user)
            return JsonResponse({'project': project, 'articles': articles})
        else:
            JsonResponse({'message': "Project doesn't exist."})
    else:
        return JsonResponse({'message': "Incorrect Access Code."})
    

@csrf_exempt    
def client_fetch_nonproject_articles(request, access_code):
    user = User.objects.get(accessCode=access_code)
    if user:
        articles = Article.objects.filter(author=user, projects=None)
        return JsonResponse({'articles': articles})
    else:
        return JsonResponse({'message': "Incorrect Access Code."})
    







@csrf_exempt
def fetch_articles(request):
    if request.method == "POST":
        access_code = request.POST.get('accessCode')
        if not access_code:
            return JsonResponse({'error': 'Access code is required'}, status=400)

        try:
            user = User.objects.get(accessCode=access_code)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid access code'}, status=404)

        # Fetch articles authored by the user
        articles = Article.objects.filter(author=user, projects=None).values(
            'title', 'description', 'content', 'creation_date'
        )

        return JsonResponse({'articles': list(articles)}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
def fetch_project_articles(request):
    if request.method == "POST":
        access_code = request.POST.get('accessCode')
        project_name = request.POST.get('project')

        if not access_code:
            return JsonResponse({'error': 'Access code is required'}, status=400)

        if not project_name:
            return JsonResponse({'error': 'Project name is required'}, status=400)

        try:
            user = User.objects.get(accessCode=access_code)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid access code'}, status=404)

        try:
            project = Project.objects.get(name=project_name)
        except Project.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=404)

        # Fetch articles authored by the user and associated with the project
        articles = Article.objects.filter(author=user, projects=project).values(
            'title', 'description', 'content', 'creation_date', 'image_base64'
        )

        return JsonResponse({'articles': list(articles)}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def fetch_view_article(request):
    if request.method == "POST":
        print('00')
        access_code = request.POST.get('accessCode')
        article_name = request.POST.get('articleTitle').replace('%20', ' ')
        if not access_code:
            print('10')
            return JsonResponse({'error': 'Access code is required'}, status=400)

        try:
            user = User.objects.get(accessCode=access_code)
        except User.DoesNotExist:
            print('22')
            return JsonResponse({'error': 'Invalid access code'}, status=404)

        if not article_name:
            print('11')
            return JsonResponse({'error': 'Project not found'}, status=404)

        # Fetch articles authored by the user
        articles = Article.objects.filter(author=user, title=article_name).values(
            'title', 'description', 'content', 'creation_date'
        )
        # print('test0: ',Article.objects.filter(author=user, title='This is a test article'))
        # print('article name: ', article_name)
        # print('test1: ', Article.objects.filter(author=user, title=article_name))
        # print({'articles': list(articles)})
        return JsonResponse({'articles': list(articles)}, status=200)
    print('01')
    return JsonResponse({'error': 'Invalid request method'}, status=405)