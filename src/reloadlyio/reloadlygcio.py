import aiohttp
import json
import time
from logging import getLogger
from .types import *

logger = getLogger(__name__)

class ReloadlyGCIO:
    
    def __init__(self, client_id:str, client_secret:str, test_mode:bool = False, api_version:int = 1) -> None:

        self.client_id = client_id
        self.client_secret = client_secret

        test = "-sandbox" if test_mode else ""
        self.base_url = f"https://giftcards{test}.reloadly.com/"

        self.bearer_response : BerearResponse = None
        self.bearer_exipiries_at : int = None

        self.api_version = api_version
    
    async def get_bearer_response(self) -> tuple[BerearResponse,int]:
        """retrieves the berear token from Reloadly giftcard API

        Returns
        -------
        tuple[BerearResponse,int]
            Bearer token, used to authenticate all api requests and the expiree date
        """

        url = f"https://auth.reloadly.com/oauth/token"

        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "audience" : self.base_url
        }

        headers = {
	        "Content-Type": "application/json",
	        "Accept": "application/json"
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(url=url, data=json.dumps(data)) as response:
                result : BerearResponse = await response.json()
        expires_at = time.time().__int__() + (result["expires_in"] - 1) #1 second of threshold

        return result,expires_at

    
    async def update_bearer(self) -> None:
        """Update the bearer token if it expired or create it if it hasn't gotten set yet
        """
        if self.bearer_response == None:
            self.bearer_response,self.bearer_exipiries_at = await self.get_bearer_response()
        elif self.bearer_exipiries_at != None:
            try:
                if self.bearer_exipiries_at > time.time().__int__():
                    self.bearer_response,self.bearer_exipiries_at = await self.get_bearer_response()
            except TypeError:
                self.bearer_response,self.bearer_exipiries_at = await self.get_bearer_response()
        else:
            pass

    async def _request(self, method:str, url:str, headers:dict = None, **kwargs) -> dict:
        """perform a get or post request to the Reloadly Giftcard API"""
        if not headers:

            await self.update_bearer()

            headers = {
                "Accept": "application/com.reloadly.giftcards-v1+json",
                "Authorization": f"Bearer {self.bearer_response['access_token']}"
            }
        
        async with aiohttp.ClientSession(headers=headers) as session:
            
            if method.lower() == "get":
                async with session.get(url=url, **kwargs) as response:
                    result = await response.json()
                
            elif method.lower() == "post":
                
                async with session.post(url=url, **kwargs) as response:
                    result = await response.json()
            
            return result
    
    async def get(self, url, **kwargs) -> dict:
        logger.debug(f"Performing a get request to {url}")
        return await self._request("get", url=url, **kwargs)
    
    async def post(self, url, data = None, **kwargs) -> dict:
        logger.debug(f"Performing a post request to {url}")
        return await self._request("post", url=url, data=data, **kwargs)

    async def api_post_request(self ,endpoint:str, data = None, **kwargs):

        url = self.base_url+endpoint
        result = await self.post(url=url, data=data, **kwargs)
    
        return result
    
    async def api_get_request(self ,endpoint:str, **kwargs):

        url = self.base_url+endpoint
        result = await self.get(url=url, **kwargs)
    
        return result
    
    async def balance(self, **kwargs) -> dict:
        """Retrieve the user's balance information

        Returns
        -------
        dict
            The API response containing user balance informations
            
        """

        endpoint = "accounts/balance"
        result = await self.api_get_request(endpoint=endpoint, **kwargs)

        return result
    
    async def countries(self, **kwargs) -> dict:
        """Retrieve the details of every country where a gift card order can be made

        Returns
        -------
        dict
            The API response containing the countries informations
        """

        endpoint = "countries"
        result = await self.api_get_request(endpoint=endpoint, **kwargs)

        return result
    
    async def country_by_isocode(self, isocode:str, **kwargs) -> dict:
        """Retrieve the details of a country by making a request with its ISO code. 

        Parameters
        ----------
        isocode : int
            The ISO code of the country to retrieve the details of

        Returns
        -------
        dict
            The API response containing details of the country
        """

        endpoint = f"countries/{isocode}"

        result = await self.api_get_request(endpoint=endpoint, **kwargs)

        return result
    
    async def products(self, params: ProductsParams | dict, **kwargs):
        """Retrieve the details of every gift card product that can be purchased on Reloadly

        Parameters
        ----------
        params : ProductsParams | dict
            The parameters to pass in order to get the product informations

        Returns
        -------
        dict
            The API response containing products informations
        """
        endpoint = "products"
        
        result = await self.api_get_request(endpoint=endpoint, params=params, **kwargs)
        
        return result
    
    async def product_by_id(self, productid:int, **kwargs) -> dict:
        """Retrieve the details of a gift card  

        Parameters
        ----------
        productid : int
            The id of the giftcard to retrieve the details of

        Returns
        -------
        dict
            The API response containing the giftcard informations
        """

        endpoint = f"products/{productid}"
        result = await self.api_get_request(endpoint=endpoint, **kwargs)

        return result
    
    async def product_by_isocode(self, isocode:str, **kwargs) -> dict:
        """Retrieve the details of every giftcard product available to a country by making a request with the country's ISO code. 

        Parameters
        ----------
        isocode : str
            The country code you want to retrieve the giftcards of 

        Returns
        -------
        dict
            The API response containing every giftcard for the chosen ISO code
        """

        endpoint = f"countries/{isocode}/products"
        result = await self.api_get_request(endpoint=endpoint, **kwargs)

        return result
    
    async def redeem_instructions(self, **kwargs) -> dict:
        """Retrieves the redeem Instructions for all the giftcards 

        Returns
        -------
        dict
            The API response containing the redeem instruction for every giftcard 
        """
        endpoint = "redeem-instructions"
        result = await self.api_get_request(endpoint=endpoint, **kwargs)

        return result
    
    async def redeem_instructions_by_id(self, brandid:int, **kwargs) -> dict:
        """Retrieves the redeem Instructions for the giftcards the brand which id was given

        Returns
        -------
        dict
            The API response containing the redeem instruction for the brand's giftcard 
        """
        endpoint = f"redeem-instructions/{brandid}"
        result = await self.api_get_request(endpoint=endpoint, **kwargs)

        return result
    
    async def discounts(self, size:int, page:int, **kwargs) -> dict:
        """Retrieves the discounts for all the giftcards

        Parameters
        ----------
        size : int
            The number of gift card products offering discounts to be retrieved on a page
        page : int
            The page of the list of gift card products offering discounts

        Returns
        -------
        dict
            The API response containing all the giftcard discounts
        """

        params:DiscountParams = {
            "size":size, 
            "page":page
            }
        
        endpoint = "discounts"
        result = await self.api_get_request(endpoint=endpoint, params=params, **kwargs)

        return result
    
    async def discount_by_id(self, productid:int, **kwargs) -> dict:
        """Retrieves the discounts for giftcard of which the id was given

        Parameters
        ----------
        productid : int
            the id of the product

        Returns
        -------
        dict
            The API response containing the product discount
        """
        endpoint = f"products/{productid}/discounts"
        result = await self.api_get_request(endpoint=endpoint, **kwargs)

        return result
    
    async def transactions(self, **kwargs) -> dict:
        """Retrieves information on every gift card purchased by an account

        Returns
        -------
        dict
            The API response containing informations on the transactions
        """

        endpoint = "reports/transactions"
        result = await self.api_get_request(endpoint=endpoint, **kwargs)

        return result
    
    async def transaction_by_id(self, transactionid:int, **kwargs) -> dict:
        """Retrieve information on a gift card transaction by making a request with its transaction identification number

        Parameters
        ----------
        transactionid : int
            The id of the transaction

        Returns
        -------
        dict
            The API response containing informations on the transaction
        """

        endpoint = f"reports/transactions/{transactionid}"
        result = await self.api_get_request(endpoint=endpoint, *kwargs)

        return result

    async def order(self, order_data:OrderData, **kwargs) -> dict:
        """Create a giftcard order with Reloadly

        Parameters
        ----------
        order_data : OrderData
            The information reguarding the product and the receiver

        Returns
        -------
        dict
            The API response containing the giftcard info
        """

        await self.update_bearer()

        headers = {
	        "Content-Type": "application/json",
	        "Accept": f"application/com.reloadly.giftcards-v{self.api_version}+json",
	        "Authorization": f"Bearer {self.bearer_response['access_token']}"
        }   
        endpoint = "orders"
        result = await self.api_post_request(endpoint=endpoint, data=json.dumps(order_data), headers=headers, **kwargs)
        
        return result
    
    async def redeem_code(self, transactionid:int, **kwargs) -> dict:
        """Retrieve details of a gift card's redeem code after a successful transaction by making a request with the gift card's transaction identification number

        Parameters
        ----------
        transactionid : int
            The id of the transaction

        Returns
        -------
        dict
            The API response containing the details of a giftcard redeem code
        """
        endpoint = f"orders/transactions/{transactionid}/cards"
        result = await self.api_get_request(endpoint=endpoint, **kwargs)
        
        return result
        
        