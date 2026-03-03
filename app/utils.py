from passlib.context import CryptContext

#ハッシュ化する設定
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

#ハッシュ化
def hash_password(password: str):
    return pwd_context.hash(password)

#入力されたパスワードが正しいかの確認
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)