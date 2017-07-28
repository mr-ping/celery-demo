from celery import Celery

app = Celery(broker='pyamqp://guest@rabbit//', backend='rpc')


@app.task
def add(x, y):
    return x + y

@app.task
def multi(x, y):
    return x * y
