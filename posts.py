from db import db
from users import get_user_id

def new_post(title, content, category_id):
    user_id = get_user_id()
    sql = 'insert into posts (title, content, user_id, category_id, sent_at) '\
        'values (:title, :content, :user_id, :category_id, now())'
    db.session.execute(sql, {'title':title, 'content':content, 'user_id':user_id, \
        'category_id':category_id})
    db.session.commit()

def edit_post(post_id, content):
    sql = 'update posts set content=:content, sent_at=now() where id=:post_id'
    db.session.execute(sql, {'content':content, 'post_id':post_id})
    db.session.commit()

def delete_post(post_id):
    sql = 'delete from posts where id=:post_id'
    db.session.execute(sql, {'post_id':post_id})
    db.session.commit()

def show_posts(id):
    sql = 'select p.id, p.title, p.content, p.sent_at, p.user_id, u.username '\
        'from posts p, users u where p.category_id=:category_id '\
        'and p.user_id=u.id order by p.id desc'
    return db.session.execute(sql, {'category_id':id}).fetchall()

def show_post(post_id):
    sql = 'select p.id, p.title, p.content, p.sent_at, p.user_id, u.username '\
        'from posts p, users u where p.id=:post_id and u.id=p.user_id'
    return db.session.execute(sql, {'post_id':post_id}).fetchone()

def get_post(post_id):
    sql = 'select title, content from posts where id=:post_id'
    return db.session.execute(sql, {'post_id':post_id}).fetchone()

def count_posts(id):
    sql = 'select count(title) from posts where category_id=:id'
    return db.session.execute(sql, {'id':id}).fetchone()[0]

def search_posts(search):
    sql = 'select p.id, p.title, p.content, p.sent_at, p.category_id, u.username '\
        'from posts p, users u where p.user_id=u.id '\
        'and (p.title like :search or p.content like :search)'
    return db.session.execute(sql, {'search':'%'+search+'%'}).fetchall()
