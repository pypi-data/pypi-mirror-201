from synctera_client.paths.external_cards_external_card_id.get import ApiForget
from synctera_client.paths.external_cards_external_card_id.delete import ApiFordelete
from synctera_client.paths.external_cards_external_card_id.patch import ApiForpatch


class ExternalCardsExternalCardId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
