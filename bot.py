from twitchio.ext import commands
import py2snes
import asyncio

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token='', client_id='',
                         nick='', prefix='!',
                         initial_channels=[''])

    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)

    @commands.command(name='test')
    async def my_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')

	# An example command is "!snes 0x7E0DBE 0x07" to give Mario a cape powerup instantly
    @commands.command(name='snes')
    async def snesram(self, message):
        parts = message.content.split(' ')
        address = int(parts[1], 16)
        amount = int(parts[2], 16)
        snes = py2snes.snes()
        await snes.connect()
        devices = await snes.DeviceList()
        await snes.Attach(devices[0])
        print(await snes.Info())
        await snes.PutAddress(
            [
                [address - 0x7E0000 + 0xF50000, [amount]]
            ]
        )
        print(await snes.Info())


bot = Bot()
bot.run()
