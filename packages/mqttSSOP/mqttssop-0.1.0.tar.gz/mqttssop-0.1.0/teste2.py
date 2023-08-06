import mqtt_SSOP.clientSubscriber as Sub

information = {
    'lastMessage' : '',
    'id' : '',
}

Sub.subscribe("ssop/123",information,"Pedro")
