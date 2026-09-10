class MessageEventType:
    SEND = "message.send"
    RECEIVE = "message.receive"
    ACK = "message.ack"
    READ = "message.read"

    VALUES = (
        SEND,
        RECEIVE,
        ACK,
        READ,
    )