from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import User, Article, Project
import secrets
from django.core.mail import send_mail
from article_creator.settings import EMAIL_HOST_USER, ALLOWED_HOSTS, EMAIL_HOST_PASSWORD
import base64

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
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return render(request, 'webapp/pages/index.html')
                else:
                    return render(request, 'webapp/pages/signup.html', {'error': 'Sign Up Failed'})
            else:
                return render(request, 'webapp/pages/signup.html', {'error': 'Unverified Account'})
    else:
        return render(request, 'webapp/pages/signup.html')
    
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
    else:
        return render(request, 'webapp/pages/signup.html')
    

def verification_email(email, VerificationCode):
    subject = "Verify Your Email"
    print("TESTETSTETSTETETSTETTESTESTESTESTESTETSETSTESTSETETEST")
    # print(ALLOWED_HOSTS, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    message = f"Verification Link http://{ALLOWED_HOSTS[0]}/verify_email/{VerificationCode}"
    recipient_list = [email]
    send_mail(subject, message, EMAIL_HOST_USER, recipient_list)
    # EMSG = EmailMessage(subject, message, to=recipient_list)
    # EMSG.send()

def verify_email(request, VerificationCode):
    user = User.objects.get(VerificationCode=VerificationCode)
    user.isVerified = True
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
                article = Article.objects.create(title=title, File=html_file, Image=image, content=html_content, author=author, description=description, image_base64=base64_image)
            elif not image:
                article = Article.objects.create(title=title, File=html_file, content=html_content, author=author, description=description)
            article.projects.set(projects)
            print(article.Image)
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
                    article.Image = image
                    article.image_base64 = upload_image_to_db(image)
            elif request.POST.get('keep_image') == "No":
                print("UI355HTRGELGERUWIGHERIFRHEUQOIHFREQUWHFRUQIEIRFQUWHRQIOEWHFRIQUWQUIEWFUIHWFEU")
                print("NO IMAGE:")
                article.Image = None
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
            project = Project.objects.create(name=name, description=description, author=author, image=image, projectSubThemes=sub_themes, image_base64=base64_image)
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
                    project.image = image
                    project.image_base64 = upload_image_to_db(image)
            elif request.FILES.get('keep_image') == "No":
                project.image = None
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