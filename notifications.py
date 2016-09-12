def notify_pushover(config, message, title):
    from pushover import Client
    client = Client(config['Notifications']['user_key'], api_token=config['Notifications']['api_key'])
    client.send_message(message, title=title)


def notify_pushbullet(config, message, title):
    from pushbullet import Pushbullet
    pb = Pushbullet(config['Notifications']['api_key'])
    pb.push_note(title, message)


notify_handlers = {
    'pushover': notify_pushover,
    'pushbullet': notify_pushbullet
}


def notify(config, message, title="PASS Monitor"):
    notify_handlers[config['Notifications']['client']](config, message, title)
