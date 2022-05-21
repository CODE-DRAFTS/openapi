from fastapi import status,HTTPException,Response, APIRouter
from app import schemas, utils , main


router = APIRouter(
    prefix="/users",
    tags=["USERS"]  #tags are used to group routes with same functionality
)


@router.post("/" , status_code=status.HTTP_201_CREATED)
def create_user( user: schemas.NewUser):
    user.password = utils.hash_function(user.password)
    print( user.password)
    main.cursor.execute(""" INSERT INTO users(email,password) VALUES(%s, %s)  RETURNING *""", (user.email, user.password,))

    new_user = main.cursor.fetchone()
    main.conn.commit()
    if new_user == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="creating user failed")
    return (new_user) 


@router.get("/{id}", response_model= schemas.ResponseGetUSer)
def get_user(id: int):
    main.cursor.execute("""SELECT * FROM users WHERE id = %s """, (str(id), ))
    user = main.cursor.fetchone()
    if  user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"user with {id} was not found")

    return user