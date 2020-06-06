import random

from locust import HttpUser, between, task, TaskSet

AUTH_MAP = {
    1: {
        'username': 'Juan',
        'password': '123456'
    },
    2: {
        'username': 'Mariano',
        'password': '123456'
    },
    3: {
        'username': 'Lautaro',
        'password': '123456'
    },
    4: {
        'username': 'Matias',
        'password': '123456'
    }
}

USER_MAP = {
    1: 'Juan',
    2: 'Mariano',
    3: 'Lautaro',
    4: 'Matias'
}


class TransactionTasks(TaskSet):
    wait_time = between(0, 1)

    @task
    def create_transactions(self):
        username_password = AUTH_MAP[random.randint(1, 4)]
        self.client.post('/auth', json=username_password)
        transaction_body = {
            'userFrom': USER_MAP[random.randint(1, 4)],
            'userTo': USER_MAP[random.randint(1, 4)],
            'amount': random.randint(0, 20)
        }
        self.client.post("/transactions", json=transaction_body)

    def on_stop(self):
        self.interrupt()


class WebTest(HttpUser):
    wait_time = between(5, 120)
    tasks = {TransactionTasks}