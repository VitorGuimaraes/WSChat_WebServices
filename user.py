class User():
    def __init__(self, name):
        self.name = name
        self.status = True
        self.received_msgs = []

    def add_msg(self, sender, msg, time):
        self.messages.append([sender, msg, time])
    
    