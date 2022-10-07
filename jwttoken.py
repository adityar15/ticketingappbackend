from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt

# security topic
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from scripts import user_script


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60 * 60

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt





############################################### Security topic #################################################################


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# create refresh token


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


#  generate access token based on refresh token

def generate_new_accesstoken(refreshToken, db):
    credentials_exception = HTTPException( 
    status_code=status.HTTP_401_UNAUTHORIZED, 
    detail="Could not validate credentials", 
    headers={"WWW-Authenticate": "Bearer"},)
    try:
        decoded = jwt.decode(refreshToken, SECRET_KEY, ALGORITHM)
        return {"access_token": create_access_token(decoded)}
    except JWTError:
        raise credentials_exception



security = HTTPBearer()
def hasValidToken(credentials: HTTPAuthorizationCredentials= Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except JWTError:
        raise credentials_exception
 

def refreshAccessToken(token: str, refreshToken: str):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except:
        try: 
            decoded = jwt.decode(refreshToken, SECRET_KEY, algorithms=[ALGORITHM])
            # print(decoded)
            return {"access_token": create_access_token(decoded)}
        
        except:
            raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )