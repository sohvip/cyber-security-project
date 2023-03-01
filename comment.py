from db import db
from users import get_user_id

def new_comment(comment, post_id):
    user_id = get_user_id()
    sql = 'insert into comments (comment, user_id, post_id, sent_at) values '\
        '(:comment, :user_id, :post_id, now())'
    db.session.execute(sql, {'comment':comment, 'user_id':user_id, 'post_id':post_id})
    db.session.commit()

def show_comments(post_id):
    sql = 'select c.id, c.comment, c.user_id, c.sent_at, u.username from comments c, users u '\
        'where c.post_id=:post_id and c.user_id=u.id order by c.id desc'
    return db.session.execute(sql, {'post_id':post_id}).fetchall()

def show_comment(post_id):
    sql = 'select c.id, c.comment, c.user_id, c.sent_at, u.username from comments c, users u '\
        'where c.post_id=:post_id and c.user_id=u.id order by c.id desc'
    return db.session.execute(sql, {'post_id':post_id}).fetchone()
