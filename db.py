import sqlite3
import time
import os

class BabyDB:
    filename = 'bt.db'
    def __init__(self):
        create = not os.path.isfile(self.filename)
        self.conn = sqlite3.connect(self.filename)
        self.c = self.conn.cursor()
        if create:
            self.create()
    def create(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS babytracker (timestamp int,action text);")
        self.commit()
    def commit(self):
        return self.conn.commit()
    def close(self):
        return self.conn.close()
    def add(self,action,ts=None):
        if ts is None:
            ts=time.time()
        sql = 'INSERT INTO babytracker (timestamp,action) VALUES (%i,"%s");' % (int(ts),action)
        self.c.execute(sql)
        self.commit()
        return int(ts)
    def getlast(self,action):
        sql ='Select timestamp FROM babytracker WHERE action="%s" ORDER BY timestamp DESC LIMIT 1;' % action
        for row in  self.c.execute(sql):
            return row[0]
        return 0
    def preparePlot(self, start=0,step=60):
        actions=dict()
        sql = "SELECT DISTINCT action FROM babytracker ORDER BY timestamp ASC;"
        for row in self.c.execute(sql):
            actions[row[0]]=list()

        sql = "SELECT timestamp FROM babytracker ORDER BY timestamp ASC LIMIT 1;"
        for row in self.c.execute(sql):
            start=max(row[0],start)
            start = start - start % step
        sql = "SELECT timestamp FROM babytracker WHERE timestamp>=%i ORDER BY timestamp ASC;" % start
        xaxis=set()
        for row in self.c.execute(sql):
            xaxis.add(row[0]-1)
            xaxis.add(row[0])
        xaxis.add(int(time.time()))
        xaxis=list(xaxis)
        xaxis.sort()
        xaxis.pop(0)
        xl=len(xaxis)
        for action in actions.keys():
            sql='SELECT timestamp FROM babytracker WHERE action="%s" AND timestamp>=%i ORDER BY timestamp ASC;' % (action,start)
            runner = 0
            last=xaxis[0]
            for row in self.c.execute(sql):
                ts=row[0]
                if runner >= xl:
                    break
                cur=xaxis[runner]
                while(cur<ts):
                    actions[action].append(cur-last)
                    runner+=1
                    cur=xaxis[runner]
                last=ts
                actions[action].append(cur-last)
                runner+=1

            while(len(actions[action]) < xl):
                cur=xaxis[runner]
                actions[action].append(cur-last)
                runner+=1
        return xaxis, actions




if __name__ == '__main__':
    db = BabyDB()
    db.close()
