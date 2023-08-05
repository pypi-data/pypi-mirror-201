import discord


class RizthmeException(Exception):
    pass


class DuplicateGuildPlayerThreadError(RizthmeException):
    def __init__(self, guild: discord.Guild):
        self.guild = guild

    def __str__(self):
        return f"You try to create a 2nd Player for the guild {self.guild}"


class BadLinkError(RizthmeException):
    def __init__(self, link: str):
        self.link = link

    def __str__(self):
        return f"Bad link: {self.link}"
