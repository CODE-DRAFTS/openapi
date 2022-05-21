from fastapi import FastAPI,Response,status, HTTPException , APIRouter
from app import schemas, main

router = APIRouter(
    prefix="/posts",
    tags=["POSTS"]  #tags are used to group routes with same functionality
)

@router.get("/")
def get_poss():
    main.cursor.execute(""" SELECT * FROM posts """)
    posts = main.cursor.fetchall()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_posts( post: schemas.CreatePost):
    main.cursor.execute(""" INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published)  )
    new_post = main.cursor.fetchall()
    main.conn.commit()

    return new_post



@router.get("/{id}")
def get_post( id: int ):
    
    main.cursor.execute(""" SELECT * FROM posts WHERE id=%s """, ( str(id), ))
    post = main.cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with {id} was not found")
    return  post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
        
        main.cursor.execute(""" DELETE  FROM posts WHERE id = %s RETURNING * """, ( str(id), ))
        deleted_post = main.cursor.fetchone()
        main.conn.commit()
        if deleted_post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist" )
        
        return  Response( status_code= status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id: int, post: schemas.PostBase ):
    
    main.cursor.execute(""" UPDATE posts SET title=%s , content =%s, published=%s WHERE id=%s RETURNING * """, (post.title, post.content, post.published , str(id) ,))
    updated_post = main.cursor.fetchone()
    main.conn.commit()
    if updated_post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist" )
    
    return  updated_post
 
