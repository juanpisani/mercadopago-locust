import random

from locust import HttpUser, between, task, TaskSet, constant

AUTH_MAP = {
    1: {
        'username': 'Juan Cruz',
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
    1: 'Juan Cruz',
    2: 'Mariano',
    3: 'Lautaro',
    4: 'Matias'
}


class AuthTasks(TaskSet):
    wait_time = between(0, 1)

    @task
    def auth(self):
        username_password = AUTH_MAP[random.randint(1, 4)]
        self.client.post('/auth', json=username_password)


class TransactionTasks(TaskSet):
    wait_time = between(0, 1)

    @task
    def get_history(self):
        username = USER_MAP[random.randint(1, 4)]
        self.client.get('/transactions/' + username)

    @task
    def create_transactions(self):
        transaction_body = {
            'userFrom': USER_MAP[random.randint(1, 4)],
            'userTo': USER_MAP[random.randint(1, 4)],
            'amount': 0.1
        }
        self.client.post("/transactions", json=transaction_body)


class BalanceTasks(TaskSet):
    wait_time = between(0, 1)

    @task
    def get_balance(self):
        username = USER_MAP[random.randint(1, 4)]
        self.client.get('users/balance/' + username)


class WebAuth(HttpUser):
    weight = 1
    tasks = {AuthTasks}


class WebTransactions(HttpUser):
    weight = 6
    tasks = {TransactionTasks}


class WebBalance(HttpUser):
    weight = 3
    tasks = {BalanceTasks}
