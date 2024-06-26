from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()
from sqlalchemy import CheckConstraint

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
       if phone_number and (not phone_number.isdigit() or len(phone_number) != 10):
           raise ValueError("Phone number must be 10 digits")
       return phone_number
    
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author cannot be empty.")

        existing_author = Author.query.filter(Author.name == name).first()
        
        if existing_author and existing_author.id != self.id:
            raise ValueError("Author with this name already exists.")
        return name


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    __table_args__ = (
        CheckConstraint("category IN ('Fiction', 'Non-Fiction')"),
        CheckConstraint("length(content) >= 250"),
        CheckConstraint("length(summary) <= 250")
    )
    
    @validates('content')
    def validate_content(self, key, post_content):
        if len(post_content) < 250:
            raise ValueError("Content must be at least 250 characters")
        return post_content

    @validates('summary')
    def validates_summary(self, key, sum):
        if len(sum) > 250:
            raise ValueError("Post summary must be under 250 characters")
        return sum
    
    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Post must have a title.")
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(keyword in title for keyword in clickbait_keywords):
            raise ValueError("Post title must contain one of the following: 'Won't Believe', 'Secret', 'Top [number]', 'Guess'")
        return title
    
    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ["Fiction", "Non-Fiction"]
        if category not in valid_categories:
            raise ValueError("Post category must be either 'Fiction' or 'Non-Fiction'.")
        return category


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
