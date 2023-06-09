from starter import get_today


def lambda_handler(event, context):
    """Lambda handler for orchestrator starter.

    param event: Event data passed to this handler.
    type event: dict
    param context: Context object passed to this handler.
    type context: dict

    return: Event dict containing status and today's date in mm/dd/yyyy format. 
    rtype: dict
    """

    today = get_today()

    return {
        'status': 'success',
        'today': today
    }
