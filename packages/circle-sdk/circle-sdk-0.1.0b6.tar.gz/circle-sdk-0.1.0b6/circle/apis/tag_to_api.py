import typing_extensions

from circle.apis.tags import TagValues
from circle.apis.tags.ach_api import ACHApi
from circle.apis.tags.addresses_api import AddressesApi
from circle.apis.tags.crypto_address_book_api import CryptoAddressBookApi
from circle.apis.tags.balances_api import BalancesApi
from circle.apis.tags.cards_api import CardsApi
from circle.apis.tags.payment_tokens_api import PaymentTokensApi
from circle.apis.tags.channels_api import ChannelsApi
from circle.apis.tags.chargebacks_api import ChargebacksApi
from circle.apis.tags.crypto_payment_intents_api import CryptoPaymentIntentsApi
from circle.apis.tags.deposits_api import DepositsApi
from circle.apis.tags.encryption_api import EncryptionApi
from circle.apis.tags.crypto_exchange_rates_api import CryptoExchangeRatesApi
from circle.apis.tags.health_api import HealthApi
from circle.apis.tags.management_api import ManagementApi
from circle.apis.tags.payments_api import PaymentsApi
from circle.apis.tags.pull_crypto_payments_api import PullCryptoPaymentsApi
from circle.apis.tags.payouts_api import PayoutsApi
from circle.apis.tags.returns_api import ReturnsApi
from circle.apis.tags.reversals_api import ReversalsApi
from circle.apis.tags.sen_api import SENApi
from circle.apis.tags.sepa_api import SEPAApi
from circle.apis.tags.settlements_api import SettlementsApi
from circle.apis.tags.signet_api import SignetApi
from circle.apis.tags.cbit_api import CBITApi
from circle.apis.tags.stablecoins_api import StablecoinsApi
from circle.apis.tags.subscriptions_api import SubscriptionsApi
from circle.apis.tags.transfers_api import TransfersApi
from circle.apis.tags.wallets_api import WalletsApi
from circle.apis.tags.wires_api import WiresApi
from circle.apis.tags.checkout_sessions_api import CheckoutSessionsApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.ACH: ACHApi,
        TagValues.ADDRESSES: AddressesApi,
        TagValues.CRYPTO_ADDRESS_BOOK: CryptoAddressBookApi,
        TagValues.BALANCES: BalancesApi,
        TagValues.CARDS: CardsApi,
        TagValues.PAYMENT_TOKENS: PaymentTokensApi,
        TagValues.CHANNELS: ChannelsApi,
        TagValues.CHARGEBACKS: ChargebacksApi,
        TagValues.CRYPTO_PAYMENT_INTENTS: CryptoPaymentIntentsApi,
        TagValues.DEPOSITS: DepositsApi,
        TagValues.ENCRYPTION: EncryptionApi,
        TagValues.CRYPTO_EXCHANGE_RATES: CryptoExchangeRatesApi,
        TagValues.HEALTH: HealthApi,
        TagValues.MANAGEMENT: ManagementApi,
        TagValues.PAYMENTS: PaymentsApi,
        TagValues.PULL_CRYPTO_PAYMENTS: PullCryptoPaymentsApi,
        TagValues.PAYOUTS: PayoutsApi,
        TagValues.RETURNS: ReturnsApi,
        TagValues.REVERSALS: ReversalsApi,
        TagValues.SEN: SENApi,
        TagValues.SEPA: SEPAApi,
        TagValues.SETTLEMENTS: SettlementsApi,
        TagValues.SIGNET: SignetApi,
        TagValues.CBIT: CBITApi,
        TagValues.STABLECOINS: StablecoinsApi,
        TagValues.SUBSCRIPTIONS: SubscriptionsApi,
        TagValues.TRANSFERS: TransfersApi,
        TagValues.WALLETS: WalletsApi,
        TagValues.WIRES: WiresApi,
        TagValues.CHECKOUT_SESSIONS: CheckoutSessionsApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.ACH: ACHApi,
        TagValues.ADDRESSES: AddressesApi,
        TagValues.CRYPTO_ADDRESS_BOOK: CryptoAddressBookApi,
        TagValues.BALANCES: BalancesApi,
        TagValues.CARDS: CardsApi,
        TagValues.PAYMENT_TOKENS: PaymentTokensApi,
        TagValues.CHANNELS: ChannelsApi,
        TagValues.CHARGEBACKS: ChargebacksApi,
        TagValues.CRYPTO_PAYMENT_INTENTS: CryptoPaymentIntentsApi,
        TagValues.DEPOSITS: DepositsApi,
        TagValues.ENCRYPTION: EncryptionApi,
        TagValues.CRYPTO_EXCHANGE_RATES: CryptoExchangeRatesApi,
        TagValues.HEALTH: HealthApi,
        TagValues.MANAGEMENT: ManagementApi,
        TagValues.PAYMENTS: PaymentsApi,
        TagValues.PULL_CRYPTO_PAYMENTS: PullCryptoPaymentsApi,
        TagValues.PAYOUTS: PayoutsApi,
        TagValues.RETURNS: ReturnsApi,
        TagValues.REVERSALS: ReversalsApi,
        TagValues.SEN: SENApi,
        TagValues.SEPA: SEPAApi,
        TagValues.SETTLEMENTS: SettlementsApi,
        TagValues.SIGNET: SignetApi,
        TagValues.CBIT: CBITApi,
        TagValues.STABLECOINS: StablecoinsApi,
        TagValues.SUBSCRIPTIONS: SubscriptionsApi,
        TagValues.TRANSFERS: TransfersApi,
        TagValues.WALLETS: WalletsApi,
        TagValues.WIRES: WiresApi,
        TagValues.CHECKOUT_SESSIONS: CheckoutSessionsApi,
    }
)
