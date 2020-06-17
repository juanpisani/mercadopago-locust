import random

from locust import HttpUser, between, task, TaskSet

maxUser = 1000
class AuthTasks(TaskSet):
    wait_time = between(0, 1)

    @task
    def auth(self):
        username_password = {
            'username': 'user' + str(random.randint(1, maxUser)),
            'password': '123456'
        }
        self.client.post('/auth', json=username_password)


class TransactionTasks(TaskSet):
    wait_time = between(0, 1)

    @task
    def get_history(self):
        username = 'user' + str(random.randint(1, maxUser))
        self.client.get('/transactions/' + username)

    @task
    def create_transactions(self):
        from_user = str(random.randint(1, maxUser))
        to_user = str(random.randint(1, maxUser))
        while from_user == to_user:
            to_user = str(random.randint(1, maxUser))
        transaction_body = {
            'userFrom': 'user' + from_user,
            'userTo': 'user' + to_user,
            'amount': round(random.random(), 2)
        }
        self.client.post("/transactions", json=transaction_body)


class BalanceTasks(TaskSet):
    wait_time = between(0, 1)

    @task
    def get_balance(self):
        username = 'user' + str(random.randint(1, maxUser))
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
