from flask import Blueprint, redirect, url_for, session, request, current_app, render_template
from authlib.integrations.flask_client import OAuth
from app.extensions import oauth_client, get_table
import uuid

auth_bp = Blueprint('auth', __name__)

# Configure the google remote app when blueprint loaded
@auth_bp.before_app_first_request
def configure_oauth():
    oauth_client.register(
        name='google',
        client_id=current_app.config.get('GOOGLE_CLIENT_ID'),
        client_secret=current_app.config.get('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

@auth_bp.route('/login')
def login():
    redirect_uri = url_for('auth.auth_callback', _external=True)
    return oauth_client.google.authorize_redirect(redirect_uri)

@auth_bp.route('/auth/callback')
def auth_callback():
    token = oauth_client.google.authorize_access_token()
    userinfo = oauth_client.google.parse_id_token(token)
    # store minimal user in session
    user = {
        'user_id': userinfo.get('sub'),
        'email': userinfo.get('email'),
        'name': userinfo.get('name')
    }
    session['user'] = user

    # Ensure user record exists in DynamoDB (no-op for per-stock table)
    table = get_table(current_app.config['DYNAMODB_TABLE'])
    # Put a lightweight user marker item (optional)
    try:
        table.put_item(Item={'user_id': user['user_id'], 'symbol': '__meta__', 'email': user['email']})
    except Exception:
        pass

    return redirect(url_for('watch.view_watchlist'))

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')
