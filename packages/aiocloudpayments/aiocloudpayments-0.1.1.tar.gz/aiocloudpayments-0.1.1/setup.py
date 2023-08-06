# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiocloudpayments',
 'aiocloudpayments.client',
 'aiocloudpayments.dispatcher',
 'aiocloudpayments.endpoints',
 'aiocloudpayments.endpoints.applepay',
 'aiocloudpayments.endpoints.notifications',
 'aiocloudpayments.endpoints.orders',
 'aiocloudpayments.endpoints.payments',
 'aiocloudpayments.endpoints.payments.cards',
 'aiocloudpayments.endpoints.payments.tokens',
 'aiocloudpayments.endpoints.subscriptions',
 'aiocloudpayments.types',
 'aiocloudpayments.types.notifications',
 'aiocloudpayments.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'aiocloudpayments',
    'version': '0.1.1',
    'description': 'CloudPayments Python Async Library',
    'long_description': '# aiocloudpayments\nPython Async [CloudPayments](https://developers.cloudpayments.ru/#api) Library\n# Client Basic Usage Example\n```\nfrom datetime import date\n\nfrom aiocloudpayments import AioCpClient\n\n\nasync def main():\n    client = AioCpClient(PUBLIC_ID, API_SECRET)\n\n    await client.test()\n\n    await client.charge_card(\n        amount=10,\n        currency="RUB",\n        invoice_id="1234567",\n        ip_address="123.123.123.123",\n        description="Payment for goods in example.com",\n        account_id="user_x",\n        name="CARDHOLDER NAME",\n        card_cryptogram_packet="01492500008719030128SMfLeYdKp5dSQVIiO5l6ZCJiPdel4uDjdFTTz1UnXY+3QaZcNOW8lmXg0H670MclS4lI+qLkujKF4pR5Ri+T/E04Ufq3t5ntMUVLuZ998DLm+OVHV7FxIGR7snckpg47A73v7/y88Q5dxxvVZtDVi0qCcJAiZrgKLyLCqypnMfhjsgCEPF6d4OMzkgNQiynZvKysI2q+xc9cL0+CMmQTUPytnxX52k9qLNZ55cnE8kuLvqSK+TOG7Fz03moGcVvbb9XTg1oTDL4pl9rgkG3XvvTJOwol3JDxL1i6x+VpaRxpLJg0Zd9/9xRJOBMGmwAxo8/xyvGuAj85sxLJL6fA==",\n        payer=Person(\n            first_name="Test",\n            last_name="Test",\n            middle_name="Test",\n            birth=date(1998, 1, 16),\n            address="12A, 123",\n            street="Test Avenue",\n            city="LosTestels, City of Test Angels",\n            country="Testland",\n            phone="+1 111 11 11",\n            post_code="101011010"\n        )\n    )\n\n    await client.disconnect()\n```\n# AiohttpDispatcher Basic Usage Example\n```\nfrom aiocloudpayments import AiohttpDispatcher, Result\nfrom aiocloudpayments.types import PayNotification, CancelNotification, CheckNotification\n\n\nCERT_FILE = "cert.pem"\nCERT_FILE = "pkey.pem"\n\n\ndef main():\n    dp = AiohttpDispatcher()\n\n    # router is not needed here, but I am just showing the logic\n    router = Router()\n\n    # register with router\n    @router.cancel(lambda n: 5 > n.amount > 1)\n    async def foo(notification: CancelNotification):\n        print(f"{notification=}")\n        # return {"result": 0}\n        return Result.OK\n\n    # register with router\n    @router.pay(lambda n: n.amount <= 1)\n    async def foo(notification: PayNotification):\n        print(f"{notification.amount=}")\n        # return {"result": 0}\n        return Result.OK\n        \n   # register with router\n    @router.check()\n    async def foo(notification: CheckNotification):\n        print(f"{notification.amount=}")\n        # return {"result": 12}\n        return Result.WRONG_AMOUNT\n\n    # register with dp\n    @dp.cancel(lambda n: n.amount > 5)\n    async def foo(notification: CancelNotification):\n        print(f"{notification.amount=}, > 5")\n        # if you don\'t return anything, Result.OK is assumed\n\n    dp.include_router(router)\n\n    ssl_context = SSLContext()\n    ssl_context.load_cert_chain(CERT_FILE, KEY_FILE)\n\n    dp.run_app(\n        AioCpClient(PUBLIC_ID, API_SECRET),\n        "/test",\n        pay_path="/pay",\n        cancel_path="/cancel",\n        ssl_context=ssl_context,\n        check_hmac=False  # disable hmac check, only use in development environments\n    )\n```\n\narchitecture inspired by [aiogram](https://github.com/aiogram/aiogram)',
    'author': 'drforse',
    'author_email': 'george.lifeslice@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/drforse/aiocloudpayments',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
