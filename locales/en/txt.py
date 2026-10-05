EN: dict[str, str] = {
    "/start": "Hello!\n\nI am the echo bot to demonstrate the work of a relational "
              "database <b>PostgreSQL</b> in conjunction with <code>aiogram</code>!\n\n"
              "If you want, you can send me something or send a command /help",
    "/help": "I am a bot that was created to demonstrate the collaboration of a relational "
             "database <b>PostgreSQL</b> and the library <code>aiogram</code>. I can save the "
             "selected interface language, as well as send you back your messages!\n\n"
             "Available Commands:\n\n"
             "/start - restarting the bot\n"
             "/lang - set the interface language\n"
             "/help - view this help\n",
    "/help_admin": "I am a bot that was created to demonstrate the collaboration of a relational "
                   "database <b>PostgreSQL</b> and the library <code>aiogram</code>. I can save the "
                   "selected interface language, as well as send you back your messages!\n\n"
                   "Your role in the system is <code>ADMIN</code> and therefore an extended "
                   "list of commands is available:\n\n"
                   "/start - restarting the bot\n"
                   "/lang - set the interface language\n"
                   "/help - view this help\n"
                   "/ban - ban the user\n"
                   "/unban - unban the user\n"
                   "/statistics - view user activity statistics",
    "/lang": "Select a language",
    "no_echo": "This type of update is not supported by the send_copy method.",
    "ru": "🇷🇺 Russian",
    "en": "🇬🇧 English",
    "save_lang_button_text": "✅ Save",
    "cancel_lang_button_text": "Cancel",
    "lang_saved": "The language has been successfully installed and will continue "
                  "to be used to display the bot interface!\n\nYou can send me something or "
                  "send a command /help",
    "lang_cancelled": "OK, your language is still: {}.\n\nYou can send me something or "
                      "send a command /help",
    "/start_description": "Restart the bot",
    "/lang_description": "Configure the interface language",
    "/help_description": "View the help for the bot",
    "/ban_description": "Ban a user (requires user_id or username)",
    "/unban_description": "Unban the user (requires user_id or username)",
    "/statistics_description": "View user activity statistics",
    "empty_ban_answer": "❗ Please specify the user's ID or @username.",
    "incorrect_ban_arg": "⚠️ <b>Incorrect format.</b>\n\nUse /ban <code>ID</code> "
                         "or /ban <code>@username</code>",
    "already_banned": "❗ The user is already banned!",
    "succesfully_banned": "⚠️ The user has been successfully banned!",
    "no_user": "❗ There is no such user in the database!",
    "empty_unban_answer": "❗ Please specify the user's ID or @username.",
    "incorrect_unban_arg": "⚠️ <b>Incorrect format.</b>\n\nUse /unban <code>ID</code> "
                           "or /unban <code>@username</code>",
    "not_banned": "❗ The user was not banned anyway!",
    "succesfully_unbanned": "⚠️ The user has been successfully unbanned!",
    "statistics": "📊 <b>Statistics on user actions:</b>\n\n{}",
}