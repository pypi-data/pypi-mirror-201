from enum import Enum

class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

class OrderType(Enum):
    LIMIT = "limit"
    MARKET = "market"
    IOC = "ioc"
    FOK = "fok"
    POST_ONLY = "post_only"

class PriceFormat(Enum):
    PROBABILITY = "probability"
    DECIMAL = "decimal"
    AMERICAN = "american"

class QuantityFormat(Enum):
    PAYOUT = "payout"
    STAKE = "stake"

class PersistenceType(Enum):
    INCLUDE_IN_AUCTION = "include_in_auction"
    LAPSE = "lapse"
    PERSIST = "persist"

class OrderStatus(Enum):
    OPEN = "open"
    PENDING = "pending"
    CLOSED = "closed"
    FAILED = "failed"
