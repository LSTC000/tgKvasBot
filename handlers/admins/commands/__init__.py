__all__ = ['register_admins_commands']


from .admin_commad import admin_command

from aiogram import Dispatcher


def register_admins_commands(dp: Dispatcher):
    dp.register_message_handler(admin_command)
