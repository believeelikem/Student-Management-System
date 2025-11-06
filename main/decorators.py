from django.http import HttpResponse

def allowed_role(role):
    def decorator(func):
        def innner(request,*args,**kwargs):
            if request.user.role != role:
                return HttpResponse(f"You are not allowed to this {role} page")
            
            return func(request,*args,**kwargs)
        return innner
    return decorator
    
def is_validate_extension(filename):
    return filename.endswith(".pdf")
