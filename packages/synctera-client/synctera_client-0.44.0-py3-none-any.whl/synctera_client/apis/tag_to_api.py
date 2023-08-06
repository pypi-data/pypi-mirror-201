import typing_extensions

from synctera_client.apis.tags import TagValues
from synctera_client.apis.tags.account_products_api import AccountProductsApi
from synctera_client.apis.tags.accounts_api import AccountsApi
from synctera_client.apis.tags.account_templates_api import AccountTemplatesApi
from synctera_client.apis.tags.ach_api import ACHApi
from synctera_client.apis.tags.ach_transaction_simulations_api import ACHTransactionSimulationsApi
from synctera_client.apis.tags.admin_api import AdminApi
from synctera_client.apis.tags.api_keys_api import APIKeysApi
from synctera_client.apis.tags.ban_rules_api import BanRulesApi
from synctera_client.apis.tags.banks_api import BanksApi
from synctera_client.apis.tags.quickstart_api import QuickstartApi
from synctera_client.apis.tags.businesses_api import BusinessesApi
from synctera_client.apis.tags.cards_api import CardsApi
from synctera_client.apis.tags.external_cards_api import ExternalCardsApi
from synctera_client.apis.tags.cash_pickups_alpha_api import CashPickupsAlphaApi
from synctera_client.apis.tags.compliance_rules_api import ComplianceRulesApi
from synctera_client.apis.tags.compliance_searches_api import ComplianceSearchesApi
from synctera_client.apis.tags.customers_api import CustomersApi
from synctera_client.apis.tags.disclosures_api import DisclosuresApi
from synctera_client.apis.tags.disclosures_deprecated_api import DisclosuresDeprecatedApi
from synctera_client.apis.tags.documents_api import DocumentsApi
from synctera_client.apis.tags.stately_api import StatelyApi
from synctera_client.apis.tags.external_accounts_api import ExternalAccountsApi
from synctera_client.apis.tags.history_api import HistoryApi
from synctera_client.apis.tags.identity_api import IdentityApi
from synctera_client.apis.tags.internal_accounts_api import InternalAccountsApi
from synctera_client.apis.tags.kyc_verification_deprecated_api import KYCVerificationDeprecatedApi
from synctera_client.apis.tags.middesk_api import MiddeskApi
from synctera_client.apis.tags.monitoring_api import MonitoringApi
from synctera_client.apis.tags.notes_api import NotesApi
from synctera_client.apis.tags.partners_api import PartnersApi
from synctera_client.apis.tags.party_groups_api import PartyGroupsApi
from synctera_client.apis.tags.cronut_api import CronutApi
from synctera_client.apis.tags.persons_api import PersonsApi
from synctera_client.apis.tags.posting_dates_api import PostingDatesApi
from synctera_client.apis.tags.remote_check_deposit_api import RemoteCheckDepositApi
from synctera_client.apis.tags.rdc_config_api import RDCConfigApi
from synctera_client.apis.tags.relationships_api import RelationshipsApi
from synctera_client.apis.tags.roles_api import RolesApi
from synctera_client.apis.tags.spend_controls_beta_api import SpendControlsBetaApi
from synctera_client.apis.tags.tenant_configs_api import TenantConfigsApi
from synctera_client.apis.tags.card_transaction_simulations_api import CardTransactionSimulationsApi
from synctera_client.apis.tags.transaction_risk_api import TransactionRiskApi
from synctera_client.apis.tags.transactions_api import TransactionsApi
from synctera_client.apis.tags.users_api import UsersApi
from synctera_client.apis.tags.egress_gateway_vendor_secret_crudapi_api import EgressGatewayVendorSecretCRUDAPIApi
from synctera_client.apis.tags.kyckyb_verifications_api import KYCKYBVerificationsApi
from synctera_client.apis.tags.waitlist_api import WaitlistApi
from synctera_client.apis.tags.watchlist_deprecated_api import WatchlistDeprecatedApi
from synctera_client.apis.tags.egress_gateway_webhook_secret_crudapi_api import EgressGatewayWebhookSecretCRUDAPIApi
from synctera_client.apis.tags.card_webhook_simulations_api import CardWebhookSimulationsApi
from synctera_client.apis.tags.webhooks_api import WebhooksApi
from synctera_client.apis.tags.wires_alpha_api import WiresAlphaApi
from synctera_client.apis.tags.digital_wallet_tokens_api import DigitalWalletTokensApi
from synctera_client.apis.tags.internal_transfer_api import InternalTransferApi
from synctera_client.apis.tags.payment_schedules_api import PaymentSchedulesApi
from synctera_client.apis.tags.remote_check_deposit_beta_api import RemoteCheckDepositBetaApi
from synctera_client.apis.tags.sandbox_wipe_alpha_api import SandboxWipeAlphaApi
from synctera_client.apis.tags.statements_api import StatementsApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.ACCOUNT_PRODUCTS: AccountProductsApi,
        TagValues.ACCOUNTS: AccountsApi,
        TagValues.ACCOUNT_TEMPLATES: AccountTemplatesApi,
        TagValues.ACH: ACHApi,
        TagValues.ACH_TRANSACTION_SIMULATIONS: ACHTransactionSimulationsApi,
        TagValues.ADMIN: AdminApi,
        TagValues.API_KEYS: APIKeysApi,
        TagValues.BAN_RULES: BanRulesApi,
        TagValues.BANKS: BanksApi,
        TagValues.QUICKSTART: QuickstartApi,
        TagValues.BUSINESSES: BusinessesApi,
        TagValues.CARDS: CardsApi,
        TagValues.EXTERNAL_CARDS: ExternalCardsApi,
        TagValues.CASH_PICKUPS_ALPHA: CashPickupsAlphaApi,
        TagValues.COMPLIANCE_RULES: ComplianceRulesApi,
        TagValues.COMPLIANCE_SEARCHES: ComplianceSearchesApi,
        TagValues.CUSTOMERS: CustomersApi,
        TagValues.DISCLOSURES: DisclosuresApi,
        TagValues.DISCLOSURES_DEPRECATED: DisclosuresDeprecatedApi,
        TagValues.DOCUMENTS: DocumentsApi,
        TagValues.STATELY: StatelyApi,
        TagValues.EXTERNAL_ACCOUNTS: ExternalAccountsApi,
        TagValues.HISTORY: HistoryApi,
        TagValues.IDENTITY: IdentityApi,
        TagValues.INTERNAL_ACCOUNTS: InternalAccountsApi,
        TagValues.KYC_VERIFICATION_DEPRECATED: KYCVerificationDeprecatedApi,
        TagValues.MIDDESK: MiddeskApi,
        TagValues.MONITORING: MonitoringApi,
        TagValues.NOTES: NotesApi,
        TagValues.PARTNERS: PartnersApi,
        TagValues.PARTY_GROUPS: PartyGroupsApi,
        TagValues.CRONUT: CronutApi,
        TagValues.PERSONS: PersonsApi,
        TagValues.POSTING_DATES: PostingDatesApi,
        TagValues.REMOTE_CHECK_DEPOSIT: RemoteCheckDepositApi,
        TagValues.RDC_CONFIG: RDCConfigApi,
        TagValues.RELATIONSHIPS: RelationshipsApi,
        TagValues.ROLES: RolesApi,
        TagValues.SPEND_CONTROLS_BETA: SpendControlsBetaApi,
        TagValues.TENANT_CONFIGS: TenantConfigsApi,
        TagValues.CARD_TRANSACTION_SIMULATIONS: CardTransactionSimulationsApi,
        TagValues.TRANSACTION_RISK: TransactionRiskApi,
        TagValues.TRANSACTIONS: TransactionsApi,
        TagValues.USERS: UsersApi,
        TagValues.EGRESS_GATEWAY_VENDOR_SECRET_CRUD_API: EgressGatewayVendorSecretCRUDAPIApi,
        TagValues.KYC_KYB_VERIFICATIONS: KYCKYBVerificationsApi,
        TagValues.WAITLIST: WaitlistApi,
        TagValues.WATCHLIST_DEPRECATED: WatchlistDeprecatedApi,
        TagValues.EGRESS_GATEWAY_WEBHOOK_SECRET_CRUD_API: EgressGatewayWebhookSecretCRUDAPIApi,
        TagValues.CARD_WEBHOOK_SIMULATIONS: CardWebhookSimulationsApi,
        TagValues.WEBHOOKS: WebhooksApi,
        TagValues.WIRES_ALPHA: WiresAlphaApi,
        TagValues.DIGITAL_WALLET_TOKENS: DigitalWalletTokensApi,
        TagValues.INTERNAL_TRANSFER: InternalTransferApi,
        TagValues.PAYMENT_SCHEDULES: PaymentSchedulesApi,
        TagValues.REMOTE_CHECK_DEPOSIT_BETA: RemoteCheckDepositBetaApi,
        TagValues.SANDBOX_WIPE_ALPHA: SandboxWipeAlphaApi,
        TagValues.STATEMENTS: StatementsApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.ACCOUNT_PRODUCTS: AccountProductsApi,
        TagValues.ACCOUNTS: AccountsApi,
        TagValues.ACCOUNT_TEMPLATES: AccountTemplatesApi,
        TagValues.ACH: ACHApi,
        TagValues.ACH_TRANSACTION_SIMULATIONS: ACHTransactionSimulationsApi,
        TagValues.ADMIN: AdminApi,
        TagValues.API_KEYS: APIKeysApi,
        TagValues.BAN_RULES: BanRulesApi,
        TagValues.BANKS: BanksApi,
        TagValues.QUICKSTART: QuickstartApi,
        TagValues.BUSINESSES: BusinessesApi,
        TagValues.CARDS: CardsApi,
        TagValues.EXTERNAL_CARDS: ExternalCardsApi,
        TagValues.CASH_PICKUPS_ALPHA: CashPickupsAlphaApi,
        TagValues.COMPLIANCE_RULES: ComplianceRulesApi,
        TagValues.COMPLIANCE_SEARCHES: ComplianceSearchesApi,
        TagValues.CUSTOMERS: CustomersApi,
        TagValues.DISCLOSURES: DisclosuresApi,
        TagValues.DISCLOSURES_DEPRECATED: DisclosuresDeprecatedApi,
        TagValues.DOCUMENTS: DocumentsApi,
        TagValues.STATELY: StatelyApi,
        TagValues.EXTERNAL_ACCOUNTS: ExternalAccountsApi,
        TagValues.HISTORY: HistoryApi,
        TagValues.IDENTITY: IdentityApi,
        TagValues.INTERNAL_ACCOUNTS: InternalAccountsApi,
        TagValues.KYC_VERIFICATION_DEPRECATED: KYCVerificationDeprecatedApi,
        TagValues.MIDDESK: MiddeskApi,
        TagValues.MONITORING: MonitoringApi,
        TagValues.NOTES: NotesApi,
        TagValues.PARTNERS: PartnersApi,
        TagValues.PARTY_GROUPS: PartyGroupsApi,
        TagValues.CRONUT: CronutApi,
        TagValues.PERSONS: PersonsApi,
        TagValues.POSTING_DATES: PostingDatesApi,
        TagValues.REMOTE_CHECK_DEPOSIT: RemoteCheckDepositApi,
        TagValues.RDC_CONFIG: RDCConfigApi,
        TagValues.RELATIONSHIPS: RelationshipsApi,
        TagValues.ROLES: RolesApi,
        TagValues.SPEND_CONTROLS_BETA: SpendControlsBetaApi,
        TagValues.TENANT_CONFIGS: TenantConfigsApi,
        TagValues.CARD_TRANSACTION_SIMULATIONS: CardTransactionSimulationsApi,
        TagValues.TRANSACTION_RISK: TransactionRiskApi,
        TagValues.TRANSACTIONS: TransactionsApi,
        TagValues.USERS: UsersApi,
        TagValues.EGRESS_GATEWAY_VENDOR_SECRET_CRUD_API: EgressGatewayVendorSecretCRUDAPIApi,
        TagValues.KYC_KYB_VERIFICATIONS: KYCKYBVerificationsApi,
        TagValues.WAITLIST: WaitlistApi,
        TagValues.WATCHLIST_DEPRECATED: WatchlistDeprecatedApi,
        TagValues.EGRESS_GATEWAY_WEBHOOK_SECRET_CRUD_API: EgressGatewayWebhookSecretCRUDAPIApi,
        TagValues.CARD_WEBHOOK_SIMULATIONS: CardWebhookSimulationsApi,
        TagValues.WEBHOOKS: WebhooksApi,
        TagValues.WIRES_ALPHA: WiresAlphaApi,
        TagValues.DIGITAL_WALLET_TOKENS: DigitalWalletTokensApi,
        TagValues.INTERNAL_TRANSFER: InternalTransferApi,
        TagValues.PAYMENT_SCHEDULES: PaymentSchedulesApi,
        TagValues.REMOTE_CHECK_DEPOSIT_BETA: RemoteCheckDepositBetaApi,
        TagValues.SANDBOX_WIPE_ALPHA: SandboxWipeAlphaApi,
        TagValues.STATEMENTS: StatementsApi,
    }
)
