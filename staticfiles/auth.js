
document.addEventListener('DOMContentLoaded', () => {
    const SignupForm = document.getElementById('signUpForm')
    const LoginForm = document.getElementById('LoginForm')
    const SignupLink = document.getElementById('SignUpLink')
    const LoginLink = document.getElementById('LoginLink')
    LoginForm.style.display = 'block'
    SignupForm.style.display = 'none'
    LoginLink.parentElement.style.display = 'none'
    SignupLink.parentElement.style.display = 'block'

    SignupLink.addEventListener('click', () => {
        LoginForm.style.display = 'none'
        SignupForm.style.display = 'block'
        LoginLink.parentElement.style.display = 'block'
        SignupLink.parentElement.style.display = 'none'
    })

    LoginLink.addEventListener('click', () => {
        LoginForm.style.display = 'block'
        SignupForm.style.display = 'none'
        LoginLink.parentElement.style.display = 'none'
        SignupLink.parentElement.style.display = 'block'
    })
})