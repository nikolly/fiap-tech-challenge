import sys
import os

projeto_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(projeto_raiz)

from security.auth import Auth
import pytest
from dotenv import load_dotenv
from jose import JWTError, jwt
import bcrypt


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

class TestAuth:
    
    @pytest.fixture
    def auth(self):
        return Auth()

    def test_create_access_token_with_right_secret_key(self, auth):
        data = {"sub": "test_user"}
        token = auth.create_access_token(data)
        
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        assert decoded_payload["sub"] == "test_user"
        assert "exp" in decoded_payload

    def test_create_access_token_with_wrong_secret_key(self, auth):
        data = {"sub": "test_user"}
        token = auth.create_access_token(data)
        
        with pytest.raises(JWTError):
            jwt.decode(token, "wrong_secret_key", algorithms=[ALGORITHM])

    def test_verify_password(self, auth):
        password = "fakehashedpassword"
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        assert auth.verify_password(password, hashed_password)
        assert not auth.verify_password("wrong_password", hashed_password)

    def test_authenticate_user(self, auth):
        username = "fiap"
        password = "fakehashedpassword"
        
        user = auth.authenticate_user(username, password)
        
        assert user is not None
        assert user['username'] == username

    def test_authenticate_user_with_wrong_username(self, auth):
        username = "non_existent_username"
        password = "fakehashedpassword"
        
        user = auth.authenticate_user(username, password)
        
        assert not user

    def test_authenticate_user_with_wrong_password(self, auth):
        username = "fiap"
        password = "wrong_password"
        
        user = auth.authenticate_user(username, password)
        
        assert not user
