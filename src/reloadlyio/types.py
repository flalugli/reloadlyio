from typing import Required, TypedDict


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
    productId: Required[int]
    "the id of the product"
    countryCode: str
    "The country code of the card sender"
    quantity: Required[int]
    "The amount of cards to purchase"
    unitPrice: Required[int]
    "The desired price, and balance, of each giftcard"
    customIdentifier: str
    senderName: Required[str]
    "The name of the sender"
    recipientEmail: str
    "The email the giftcard will be emailed to"
    recipientPhoneDetails: RecipientPhoneDetails
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