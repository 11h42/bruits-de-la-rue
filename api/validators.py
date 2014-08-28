from core.models import User


def json_bid_is_valid(bid):
    # One of the required fields are empty
    if not 'title' in bid or not 'creator' in bid or not 'description' in bid:
        return False

    #The given creator does not exist
    if not User.objects.filter(id=bid['creator'])[:1]:
        return False

    return True
