from dataclasses import dataclass

from dew.ext.command.decorators import command
from dew.ext.command import CommandClient, DI, Kwargs


@dataclass
class Database:
    data: str

    def fetch(self):
        return self.data


@command
def my_command(db: Database, kwargs: Kwargs):
    return db.fetch(), kwargs[0]


di = DI({})
di.set(Database, Database("some data here"))

client = CommandClient(di, {})
client.register(my_command)


command = "my_command some:input"
# some data here

print(client.execute(command))
