from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # For local dev only: allow OAuth over HTTP
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(host='0.0.0.0', port=5000, debug=True)
