from databases.database import get_clients


class History:
    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.array = []

    def add(self, group_message_id, channel_message_id):
        if len(self.array) >= 5:
            self.array.pop(0)
        self.array.append((group_message_id, channel_message_id))

    def delete(self, group_message_id):
        for i in self.array:
            if i[0] == group_message_id:
                self.array.remove(i)
                return

    def search(self, group_message_id):
        for i in self.array:
            if i[0] == group_message_id:
                return i

    def __contains__(self, obj):
        if isinstance(obj, int):
            for i in self.array:
                if i[0] == obj:
                    return True
            return False
        return NotImplemented


history_dict: dict[int, History] = {}
for group_id, channel_id in get_clients():
    history_dict[group_id] = History(channel_id)
