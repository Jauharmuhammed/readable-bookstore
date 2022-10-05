from accounts.models import UserProfile

def profile_picture(request):
  try:
    profile = UserProfile.objects.get(user = request.user)
    profile_pic = profile.profile_picture.url
    print(profile_pic)
    return dict(profile_picture=profile_pic)
  except:
    return dict()
  