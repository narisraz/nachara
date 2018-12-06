def save_profile(backend, user, response, *args, **kwargs):
    language = 'fr'
    if backend.name == 'google-oauth2':
        url = response['image'].get('url')
        language = response['language']

    if url:
        user.oauth = True
        user.avatar = url
        user.is_staff = False
        user.language = language
        user.save()

