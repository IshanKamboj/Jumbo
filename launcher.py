from bot import Jumbo

VERSION = '1.0.1'

def main():
    bot=Jumbo()
    bot.remove_command("help")
    @bot.check
    def check_commands(ctx):
        return ctx.guild is not None
    bot.run(VERSION)


if __name__ == "__main__":
    main()