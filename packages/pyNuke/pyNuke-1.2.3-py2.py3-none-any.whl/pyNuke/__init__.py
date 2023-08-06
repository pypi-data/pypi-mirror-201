__description__ = "A Discord Nuke. Meant to be used with good intent for testing purposes."
__version__ = "1.2.3"
__author__ = 'Tiago Coelho'
__status__ = "Beta"
__license__ = "The Unlicense  ||  Feel free to use this software however you want."
__how__ = "First, import pyNuke using `import pyNuke` and import discordNuke using `from pyNuke import discordNuke`.                                                        Make a command using, for example, @bot.tree.command().                                                                                                           At the end of the command, add the following function call: await discordNuke.nukeactivate(interaction=interaction, bot=bot).                                     Now, everytime someone uses that command, you will be able to use the discord nuke on the console."