#from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from maxapi.types.attachments.attachment import ButtonsPayload
from maxapi.types.attachments.buttons import (
    ClipboardButton,
    LinkButton,
    CallbackButton,
)


def get_lang_settings_kb(i18n: dict, locales: list[str], checked: str) -> ButtonsPayload:
    buttons = []
    for locale in sorted(locales):
        if locale == "default":
            continue
        if locale == checked:
            buttons.append(
                [
                    CallbackButton(
                        text=f"🔘 {i18n.get(locale)}", payload=locale
                    )
                ]
            )
        else:
            buttons.append(
                [
                    CallbackButton(
                        text=f"⚪️ {i18n.get(locale)}", payload=locale
                    )
                ]
            )
    buttons.append(
        [
            CallbackButton(
                text=i18n.get("cancel_lang_button_text"), 
                payload="cancel_lang_button_data"
            ),
            CallbackButton(
                text=i18n.get("save_lang_button_text"), 
                payload="save_lang_button_data"
            ),
        ]
    )
    return ButtonsPayload(buttons=buttons).pack()