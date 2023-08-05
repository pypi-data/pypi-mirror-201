import requests


class AlgoAccessClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.algoaccess.io/v1/'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
        }

        if not self.api_key:
            raise ValueError('Must provide user_id and api_key')

    def add_access(self, product_id: int, tradingview_username=None, discord_user_id=None):
        if not product_id:
            raise ValueError('Must provide product_id')
        if not tradingview_username and not discord_user_id:
            raise ValueError('Must provide either tradingview_username or discord_user_id')

        url = f'{self.base_url}grantAccess/'
        data = {'product_id': product_id}
        if tradingview_username:
            data['tradingview_username'] = tradingview_username
        if discord_user_id:
            data['discord_user_id'] = discord_user_id
        response = requests.post(url, headers=self.headers, data=data)
        return response.json()

    def remove_access(self, product_id: int, tradingview_username=None, discord_user_id=None):
        if not product_id:
            raise ValueError('Must provide product_id')
        if not tradingview_username and not discord_user_id:
            raise ValueError('Must provide either tradingview_username or discord_user_id')

        url = f'{self.base_url}revokeAccess/'
        data = {'product_id': product_id}
        if tradingview_username:
            data['tradingview_username'] = tradingview_username
        if discord_user_id:
            data['discord_user_id'] = discord_user_id
        response = requests.post(url, headers=self.headers, data=data)
        return response.json()
