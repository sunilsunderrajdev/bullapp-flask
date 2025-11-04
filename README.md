# bullapp-flask-v2
Flask app scaffold that uses Google OAuth (Authlib) and local DynamoDB for a per-user stock watchlist.
This version includes CSRF protection, WTForms validation, and a DynamoDB schema where each stock is stored as its own item.

## Quickstart (local)
1. Install requirements: `pip install -r requirements.txt`
2. Run local DynamoDB (example using Docker):
   ```bash
   docker run -p 8000:8000 amazon/dynamodb-local
   ```
3. Copy `.env.example` to `.env` and fill in values (Google OAuth client ID/secret).
4. Create DynamoDB table (name matches `DYNAMODB_TABLE` in .env). Example using AWS CLI:
   ```bash
   aws dynamodb create-table --table-name watchlist --attribute-definitions AttributeName=user_id,AttributeType=S AttributeName=symbol,AttributeType=S --key-schema AttributeName=user_id,KeyType=HASH AttributeName=symbol,KeyType=RANGE --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 --endpoint-url http://localhost:8000 --region us-east-1
   ```
5. Start app: `python run.py`
6. Open `http://localhost:5000` and use "Login with Google"
