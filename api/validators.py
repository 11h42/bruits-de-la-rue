from core.models import User


def json_bid_is_valid(bid):
    """
    Json bid values integrity test
    :param bid:
    :return: True if all the rules are respected. False instead.
    """

    if not 'title' in bid or not 'creator' in bid or not 'description' in bid or len(bid['title']) is 0 or len(
            bid['description']) is 0 or type(bid['creator']) is not int:
        return False

    if not User.objects.filter(id=bid['creator'])[:1]:
        return False

    return True
