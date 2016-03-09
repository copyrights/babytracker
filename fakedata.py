from db import BabyDB
import random
import time

actions = ['linkebrust','rechtebrust','pipi','kacka']
start = 60*60*24*12/2
maxstep = 60*60*20
minstep = (60*60*3)/2

def rafu(minv,maxv):
    r = random.random()
    val = (((0.5+r)**-3)/8.0*(maxv-minv))+minv
    return val

if __name__ == '__main__':
    db = BabyDB()
    random.seed()
    now = int(time.time())
    for action in actions:
        cur = now - start
        cur += rafu(minstep,maxstep)
        while cur < now:
            sql = 'INSERT INTO babytracker (timestamp,action) VALUES (%i, "%s");' % (cur,action)
            db.c.execute(sql)
            cur += rafu(minstep,maxstep)
        db.commit()
    db.close()


