import sys
#version check
if sys.version_info < (3, 11): #for python 3.8-3.10 support
    from typing_extensions import NotRequired, TypedDict
else: # for python 3.11+ as per PEP 655
    from typing import NotRequired, TypedDict

class BerearResponse(TypedDict):
    access_token: str
    expires_in: int
    scope: str
    token_type: str


class RecipientPhoneDetails(TypedDict):
    "Phone informations of the giftcard receiver"
    countryCode: str
    "Country code of the phone number"
    phoneNumber: int
    "Phone number of the receiver"


class OrderData(TypedDict, total=False):
    productId: int
    "the id of the product"
    countryCode: NotRequired[str]
    "The country code of the card sender"
    quantity: int
    "The amount of cards to purchase"
    unitPrice: int
    "The desired price, and balance, of each giftcard"
    customIdentifier: str
    senderName: str
    "The name of the sender"
    recipientEmail: NotRequired[str]
    "The email the giftcard will be emailed to"
    recipientPhoneDetails: NotRequired[RecipientPhoneDetails]
    "The phone details of the receiver"


class ProductsParams(TypedDict, total=False):
    size: int
    "The number of gift card products to be retrieved on a page"
    page: int
    "The page of the product list being retrieved"
    productName: str
    "The name of the gift card product"
    countryCode: str
    "The ISO code of the country whose gift card products are to be retrieved"
    includeRange: str
    "The list of gift card products with the denominationType property specified as RANGE are to be retrieved, can be true or false"
    includeFixed: str
    "The list of gift card products with the denominationType property specified as FIXED are to be retrieved, can be true or false"


class DiscountParams(TypedDict):
    size: int
    page: int


#TODO Add types for every api response, should all be TypedDict