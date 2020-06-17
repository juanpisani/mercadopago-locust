import random

from locust import HttpUser, between, task, TaskSet


class AuthTasks(TaskSet):
    wait_time = between(0, 1)

    @task
    def auth(self):
        username_password = {
            'username': 'username' + str(random.randint(1, 10000)),
            'password': '123456'
        }
        self.client.post('/auth', json=username_password)


class TransactionTasks(TaskSet):
    wait_time = between(0, 1)

    @task
    def get_history(self):
        username = 'username' + str(random.randint(1, 10000))
        self.client.get('/transactions/' + username)

    @task
    def create_transactions(self):
        from_user = str(random.randint(1, 10000))
        to_user = str(random.randint(1, 10000))
        while from_user == to_user:
            to_user = str(random.randint(1, 10000))
        transaction_body = {
            'userFrom': 'username' + from_user,
            'userTo': 'username' + to_user,
            'amount': random.random()
        }
        self.client.post("/transactions", json=transaction_body)


class BalanceTasks(TaskSet):
    wait_time = between(0, 1)

    @task
    def get_balance(self):
        username = 'username' + str(random.randint(1, 10000))
        self.client.get('/users/balance/' + username)


class WebAuth(HttpUser):
    weight = 1
    tasks = {AuthTasks}


class WebTransactions(HttpUser):
    weight = 6
    tasks = {TransactionTasks}


class WebBalance(HttpUser):
    weight = 3
    tasks = {BalanceTasks}
