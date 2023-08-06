from .clientSubscriber import subscribe 


def launchMqttService( topic = "ssop/SSOPCloud"):

    subscribe(topic)

