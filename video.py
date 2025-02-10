from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Text, Optional, List
from datetime import datetime
from uuid import uuid4 as uuid

class Post(BaseModel):
    id: Optional[str] = None
    title: str
    author: str
    content: Text
    created_at: datetime = Field(default_factory=datetime.now)
    published_at: Optional[datetime] = None
    published: bool = False

app = FastAPI()

posts = []

@app.get("/")
def read_root():
    return {"welcome": "Welcome to my API"}

@app.get("/posts")
def read_posts():
    return posts

@app.post("/posts")
def create_post(post: Post):
    post.id = str(uuid())
    posts.append(post.dict())
    return posts[-1]

@app.get("/posts/{post_id}")
def get_post(post_id: str):
    for post in posts:
        if post["id"] == post_id:
            return post
    return HTTPException(status_code=404, detail="Post not found")

@app.delete("/posts/{post_id}")
def delete_post(post_id: str):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts.pop(index)
            return {"message": "Post deleted successfully"}
    return HTTPException(status_code=404, detail="Post not found")

@app.put("/posts/{post_id}")
def update_post(post_id: str, updatedPost: Post):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts[index]["title"] = updatedPost.title
            posts[index]["author"] = updatedPost.author
            posts[index]["content"] = updatedPost.content
            return {"message": "Post updated successfully"}
    return HTTPException(status_code=404, detail="Post not found")