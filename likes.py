from db import db
from users import get_user_id

def liked(post_id):
    user_id = get_user_id()
    sql1 = 'select liked from likes where user_id=:user_id and post_id=:post_id'
    result = db.session.execute(sql1, {'user_id':user_id, 'post_id':post_id}).fetchone()
    if result is not None:
        result = result[0]
    if result == 0:
        sql2 = 'update likes set liked=1 where user_id=:user_id and post_id=:post_id'
        db.session.execute(sql2, {'user_id':user_id, 'post_id':post_id})
        db.session.commit()
    elif result == 1:
        sql3 = 'update likes set liked=0 where user_id=:user_id and post_id=:post_id'
        db.session.execute(sql3, {'user_id':user_id, 'post_id':post_id})
        db.session.commit()
    else:
        sql4 = 'insert into likes (liked, user_id, post_id) values (1, :user_id, :post_id)'
        db.session.execute(sql4, {'user_id':user_id, 'post_id':post_id})
        db.session.commit()
    return result

def get_likes(post_id):
    sql = 'select sum(liked) from likes where post_id=:post_id'
    return db.session.execute(sql, {'post_id':post_id}).fetchone()[0]
