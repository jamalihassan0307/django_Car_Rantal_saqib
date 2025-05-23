from social_core.pipeline.user import create_user
from .models import User, Role
from django.contrib.auth import login
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import get_user_model

def get_or_create_role(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        # Get or create a default role for Google users
        role, created = Role.objects.get_or_create(name='Customer')
        user.role = role
        user.save()
    return {'user': user}

def save_google_user(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        # Update user details from Google
        if response.get('email'):
            user.email = response['email']
        if response.get('name'):
            name_parts = response['name'].split(' ', 1)
            user.first_name = name_parts[0]
            user.last_name = name_parts[1] if len(name_parts) > 1 else ''
        if response.get('picture'):
            # You might want to download and save the profile picture here
            pass
        user.save()
    return {'user': user}

def create_session(backend, user, response, *args, **kwargs):
    """Create a session for the user after successful authentication"""
    if backend.name == 'google-oauth2':
        try:
            # Create a new session
            session = SessionStore()
            session.create()
            
            # Store user information in session
            session['user_id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            session['is_authenticated'] = True
            
            # Save the session
            session.save()
            
            # Return the session key
            return {'session_key': session.session_key}
        except Exception as e:
            print(f"Error creating session: {str(e)}")
            return None
    return None 