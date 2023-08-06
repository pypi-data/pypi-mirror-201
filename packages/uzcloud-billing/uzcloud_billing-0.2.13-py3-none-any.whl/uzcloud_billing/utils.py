import requests
import jwt
import json

from django.conf import settings

from .decorators import auth_required


class Singleton(type):
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(Singleton, self).__call__(*args, **kwargs)
        return self._instances[self]


class UzcloudBilling(metaclass=Singleton):
    AUTH_URL = settings.UZCLOUD_BILLING["AUTH_URL"]
    BILLING_BASE_URL = settings.UZCLOUD_BILLING["BASE_URL"]
    ADD_ACCOUNT_URL = f"{BILLING_BASE_URL}/api/Account/AddAccount"
    GET_BALANCE_URL = f"{BILLING_BASE_URL}/api/Balance/GetBalance"
    MAKE_INVOICE_URL = f"{BILLING_BASE_URL}/api/Invoice/MakeInvoice"
    REFUND_INVOICE_URL = f"{BILLING_BASE_URL}/api/Invoice/RefoundInvoice"
    PAYMENT_LINKS_URL = f"{BILLING_BASE_URL}/api/Service/PaymentLinks"
    PAYMENT_PROVIDERS_URL = f"{BILLING_BASE_URL}/api/Service/PaymentList"

    AUTH_TOKEN = None
    REQUEST_CONFIG = {"verify": False}

    def authorize(self):
        response = requests.post(
            url=self.AUTH_URL,
            data={"grant_type": "client_credentials"},
            auth=(
                settings.UZCLOUD_BILLING["CLIENT_ID"],
                settings.UZCLOUD_BILLING["CLIENT_SECRET"],
            ),
            **self.REQUEST_CONFIG,
        )
        if response.status_code != 200:
            raise ValueError(response.content)
        self.AUTH_TOKEN = response.json()["access_token"]
        self.DECODED = jwt.decode(self.AUTH_TOKEN, options={"verify_signature": False})

    @auth_required
    def add_account(self, personType: int = 1) -> dict:
        payload = {"personType": personType}
        response = requests.post(
            url=self.ADD_ACCOUNT_URL,
            data=json.dumps(payload),
            headers=self.get_headers(),
            **self.REQUEST_CONFIG,
        )
        if response.status_code != 200:
            raise ValueError(response.content)
        return response.json()

    @auth_required
    def get_balance(self, account_number: str) -> float:
        response = requests.get(
            url=self.GET_BALANCE_URL,
            params={"accountNumber": account_number},
            headers=self.get_headers(),
            **self.REQUEST_CONFIG,
        )
        if response.status_code != 200:
            raise ValueError(response.content)
        return response.json()["Amount"]

    @auth_required
    def make_invoice(self, account_number: str, amount: float, reason: str) -> dict:
        payload = {
            "accountNumber": account_number,
            "amount": amount,
            "reason": reason,
        }
        response = requests.post(
            self.MAKE_INVOICE_URL,
            data=json.dumps(payload),
            headers=self.get_headers(),
            **self.REQUEST_CONFIG,
        )
        if response.status_code != 200:
            raise ValueError(response.json())
        response = response.json()

        return response

    @auth_required
    def refund_invoice(
        self,
        account_number: str,
        invoice_id: str,
        amount: float,
        reason: str,
    ) -> dict:
        payload = {
            "accountNumber": account_number,
            "invoiceId": invoice_id,
            "amount": amount,
            "reason": reason,
        }
        response = requests.post(
            self.REFUND_INVOICE_URL,
            data=json.dumps(payload),
            headers=self.get_headers(),
            **self.REQUEST_CONFIG,
        )
        if response.status_code != 200:
            raise ValueError(response.json())

        return response.json()

    @auth_required
    def transaction_history(self, account_number: str):
        pass

    @auth_required
    def generate_payment_links(self, account_number: str, amount: float) -> dict:
        payload = {
            "accountNumber": account_number,
            "amount": amount,
        }

        response = requests.get(
            self.PAYMENT_LINKS_URL,
            params=payload,
            headers=self.get_headers(),
            **self.REQUEST_CONFIG,
        )
        if response.status_code != 200:
            raise ValueError(response.json())

        return response.json()

    @auth_required
    def payment_providers(self) -> list:
        response = requests.get(
            self.PAYMENT_PROVIDERS_URL,
            headers=self.get_headers(),
            **self.REQUEST_CONFIG,
        )

        if response.status_code != 200:
            raise ValueError(response.json())

        return response.json()

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.AUTH_TOKEN}",
            "Content-Type": "application/json",
        }


uzcloud_service = UzcloudBilling()
