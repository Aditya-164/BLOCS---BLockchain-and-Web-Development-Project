import json

class Message:
    @staticmethod
    def create_message(message_type, content, sender_ip, sender_port):
        return json.dumps({
            "type": message_type,
            "content": content,
            "sender_ip": sender_ip,
            "sender_port": sender_port
        })

    @staticmethod
    def parse_message(message_str):
        return json.loads(message_str)
