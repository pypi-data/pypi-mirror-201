from synctera_client.paths.webhook_secrets.put import ApiForput
from synctera_client.paths.webhook_secrets.post import ApiForpost
from synctera_client.paths.webhook_secrets.delete import ApiFordelete


class WebhookSecrets(
    ApiForput,
    ApiForpost,
    ApiFordelete,
):
    pass
