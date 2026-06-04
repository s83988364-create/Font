#!/usr/bin/env python3
"""
FONT GENERATOR BOT - Text to Stylish Font Converter
Jaisa font user chaahe, waisa text convert karega
"""

import json
import urllib.request
import urllib.parse
import time
import os
from datetime import datetime
from flask import Flask, request
from threading import Thread

# ========== CONFIGURATION ==========
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
BOT_NAME = "Font Generator Bot"

# ========== FLASK APP ==========
app = Flask('')

@app.route('/')
def home():
    return f"🎨 {BOT_NAME} Active!"

@app.route(f'/webhook/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    try:
        update = json.loads(request.data)
        process_update(update)
        return 'OK', 200
    except Exception as e:
        print(f"Webhook error: {e}")
        return 'Error', 500

# ========== FONT STYLES MAPPING ==========
# Unicode characters for different font styles

FONTS = {
    # Normal Serif/Sans Styles
    "serif": {
        "name": "𝐒𝐞𝐫𝐢𝐟 𝐁𝐨𝐥𝐝",
        "desc": "Bold Serif style - 𝐓𝐡𝐢𝐬 𝐢𝐬 𝐞𝐱𝐚𝐦𝐩𝐥𝐞",
        "map": "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳"
    },
    "serif_italic": {
        "name": "𝑺𝒆𝒓𝒊𝒇 𝑰𝒕𝒂𝒍𝒊𝒄",
        "desc": "Italic Serif style - 𝑻𝒉𝒊𝒔 𝒊𝒔 𝒆𝒙𝒂𝒎𝒑𝒍𝒆",
        "map": "𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛"
    },
    "serif_bold_italic": {
        "name": "𝑺𝒆𝒓𝒊𝒇 𝑩𝒐𝒍𝒅 𝑰𝒕𝒂𝒍𝒊𝒄",
        "desc": "Bold Italic Serif - 𝑻𝒉𝒊𝒔 𝒊𝒔 𝒆𝒙𝒂𝒎𝒑𝒍𝒆",
        "map": "𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛"
    },
    
    # Script/Cursive Styles
    "script": {
        "name": "𝓢𝓬𝓻𝓲𝓹𝓽",
        "desc": "Cursive Script style - 𝓣𝓱𝓲𝓼 𝓲𝓼 𝓮𝔁𝓪𝓶𝓹𝓵𝓮",
        "map": "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃"
    },
    "script_bold": {
        "name": "𝓢𝓬𝓻𝓲𝓹𝓽 𝓑𝓸𝓵𝓭",
        "desc": "Bold Script style - 𝓣𝓱𝓲𝓼 𝓲𝓼 𝓮𝔁𝓪𝓶𝓹𝓵𝓮",
        "map": "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃"
    },
    
    # Double Struck (Mathematical)
    "double_struck": {
        "name": "𝔻𝕠𝕦𝕓𝕝𝕖 𝕊𝕥𝕣𝕦𝕔𝕜",
        "desc": "Double Struck style - 𝕋𝕙𝕚𝕤 𝕚𝕤 𝕖𝕩𝕒𝕞𝕡𝕝𝕖",
        "map": "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫"
    },
    
    # Fraktur (Gothic)
    "fraktur": {
        "name": "𝕱𝖗𝖆𝖐𝖙𝖚𝖗",
        "desc": "Gothic Fraktur style - 𝕿𝖍𝖎𝖘 𝖎𝖘 𝖊𝖝𝖆𝖒𝖕𝖑𝖊",
        "map": "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟"
    },
    "fraktur_bold": {
        "name": "𝖁𝖔𝖑𝖉 𝕱𝖗𝖆𝖐𝖙𝖚𝖗",
        "desc": "Bold Gothic style - 𝕿𝖍𝖎𝖘 𝖎𝖘 𝖊𝖝𝖆𝖒𝖕𝖑𝖊",
        "map": "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟"
    },
    
    # Monospace
    "monospace": {
        "name": "𝙼𝚘𝚗𝚘𝚜𝚙𝚊𝚌𝚎",
        "desc": "Monospace style - 𝚃𝚑𝚒𝚜 𝚒𝚜 𝚎𝚡𝚊𝚖𝚙𝚕𝚎",
        "map": "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣"
    },
    
    # Small Caps
    "smallcaps": {
        "name": "Sᴍᴀʟʟ Cᴀᴘs",
        "desc": "Small Caps style - Tʜɪs ɪs ᴇxᴀᴍᴘʟᴇ",
        "map": "ABCDEFGHIJKLMNOPQRSTUVWXYZᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
    },
    
    # Upside Down
    "upside": {
        "name": "Upside Down",
        "desc": "Upside Down style - ʇxǝɯɐdǝ sı ɥsı⊥",
        "map": "∀qɔpǝɟɓɥᴉɾʞlɯuodbɹsʇnʌʍxʎzɐqɔpǝɟɓɥᴉɾʞlɯuodbɹsʇnʌʍxʎz"
    },
    
    # Circle (Enclosed)
    "circle": {
        "name": "🅒🅘🅡🅒🅛🅔",
        "desc": "Circled style - 🅣🅗🅘🅢 🅘🅢 🅔🅧🅐🅜🅟🅛🅔",
        "map": "🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩"
    },
    
    # Parenthesis
    "parenthesis": {
        "name": "P⦅a⦆r⦅e⦆n⦅t⦆h⦅e⦆s⦅i⦆s",
        "desc": "Parenthesis style - ⦅T⦆h⦅i⦆s ⦅i⦆s ⦅e⦆x⦅a⦆m⦅p⦆l⦅e⦆",
        "map": "⦅A⦆⦅B⦆⦅C⦆⦅D⦆⦅E⦆⦅F⦆⦅G⦆⦅H⦆⦅I⦆⦅J⦆⦅K⦆⦅L⦆⦅M⦆⦅N⦆⦅O⦆⦅P⦆⦅Q⦆⦅R⦆⦅S⦆⦅T⦆⦅U⦆⦅V⦆⦅W⦆⦅X⦆⦅Y⦆⦅Z⦆⦅a⦆⦅b⦆⦅c⦆⦅d⦆⦅e⦆⦅f⦆⦅g⦆⦅h⦆⦅i⦆⦅j⦆⦅k⦆⦅l⦆⦅m⦆⦅n⦆⦅o⦆⦅p⦆⦅q⦆⦅r⦆⦅s⦆⦅t⦆⦅u⦆⦅v⦆⦅w⦆⦅x⦆⦅y⦆⦅z⦆"
    },
    
    # Squared
    "squared": {
        "name": "🄰🄱🄲🄳🄴",
        "desc": "Squared style - 🅃🄷🄸🅂 🄸🅂 🄴🅇🄰🄼🄿🄻🄴",
        "map": "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉"
    },
    
    # Bubble (Emoji style)
    "bubble": {
        "name": "Ⓑⓤⓑⓑⓛⓔ",
        "desc": "Bubble style - Ⓣⓗⓘⓢ ⓘⓢ ⓔⓧⓐⓜⓟⓛⓔ",
        "map": "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ"
    },
    
    # Strike-through
    "strike": {
        "name": "S̶t̶r̶i̶k̶e̶",
        "desc": "Strike-through style - T̶h̶i̶s̶ i̶s̶ e̶x̶a̶m̶p̶l̶e̶",
        "map": "A̶B̶C̶D̶E̶F̶G̶H̶I̶J̶K̶L̶M̶N̶O̶P̶Q̶R̶S̶T̶U̶V̶W̶X̶Y̶Z̶a̶b̶c̶d̶e̶f̶g̶h̶i̶j̶k̶l̶m̶n̶o̶p̶q̶r̶s̶t̶u̶v̶w̶x̶y̶z̶"
    },
    
    # Underline
    "underline": {
        "name": "U̲n̲d̲e̲r̲l̲i̲n̲e̲",
        "desc": "Underline style - T̲h̲i̲s̲ i̲s̲ e̲x̲a̲m̲p̲l̲e̲",
        "map": "A̲B̲C̲D̲E̲F̲G̲H̲I̲J̲K̲L̲M̲N̲O̲P̲Q̲R̲S̲T̲U̲V̲W̲X̲Y̲Z̲a̲b̲c̲d̲e̲f̲g̲h̲i̲j̲k̲l̲m̲n̲o̲p̲q̲r̲s̲t̲u̲v̲w̲x̲y̲z̲"
    },
    
    # Slanted
    "slanted": {
        "name": "S̸l̸a̸n̸t̸e̸d̸",
        "desc": "Slanted style - T̸h̸i̸s̸ i̸s̸ e̸x̸a̸m̸p̸l̸e̸",
        "map": "A̸B̸C̸D̸E̸F̸G̸H̸I̸J̸K̸L̸M̸N̸O̸P̸Q̸R̸S̸T̸U̸V̸W̸X̸Y̸Z̸a̸b̸c̸d̸e̸f̸g̸h̸i̸j̸k̸l̸m̸n̸o̸p̸q̸r̸s̸t̸u̸v̸w̸x̸y̸z̸"
    },
    
    # Bold Sans
    "bold_sans": {
        "name": "𝗕𝗼𝗹𝗱 𝗦𝗮𝗻𝘀",
        "desc": "Bold Sans style - 𝗧𝗵𝗶𝘀 𝗶𝘀 𝗲𝘅𝗮𝗺𝗽𝗹𝗲",
        "map": "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇"
    },
    
    # Sans Italic
    "sans_italic": {
        "name": "𝘚𝘢𝘯𝘴 𝘐𝘵𝘢𝘭𝘪𝘤",
        "desc": "Sans Italic style - 𝘛𝘩𝘪𝘴 𝘪𝘴 𝘦𝘹𝘢𝘮𝘱𝘭𝘦",
        "map": "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻"
    },
    
    # Bold Sans Italic
    "bold_sans_italic": {
        "name": "𝙎𝙖𝙣𝙨 𝘽𝙤𝙡𝙙 𝙄𝙩𝙖𝙡𝙞𝙘",
        "desc": "Bold Sans Italic - 𝙏𝙝𝙞𝙨 𝙞𝙨 𝙚𝙭𝙖𝙢𝙥𝙡𝙚",
        "map": "𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯"
    },
    
    # Typewriter
    "typewriter": {
        "name": "𝚃𝚢𝚙𝚎𝚠𝚛𝚒𝚝𝚎𝚛",
        "desc": "Typewriter style - 𝚃𝚑𝚒𝚜 𝚒𝚜 𝚎𝚡𝚊𝚖𝚙𝚕𝚎",
        "map": "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣"
    }
}

# ========== HELPER FUNCTIONS ==========
def convert_text(text, font_map):
    """Convert normal text to styled text"""
    result = []
    normal_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    normal_lower = "abcdefghijklmnopqrstuvwxyz"
    styled_chars = font_map
    
    for char in text:
        if char.isupper() and char in normal_upper:
            idx = normal_upper.index(char)
            result.append(styled_chars[idx] if idx < len(styled_chars) else char)
        elif char.islower() and char in normal_lower:
            idx = normal_lower.index(char)
            result.append(styled_chars[26 + idx] if 26 + idx < len(styled_chars) else char)
        else:
            result.append(char)
    return ''.join(result)

def get_inline_keyboard():
    """Create inline keyboard with all font styles"""
    keyboard = []
    row = []
    
    # Font list in rows of 2
    fonts = list(FONTS.keys())
    for i, font_key in enumerate(fonts):
        font_info = FONTS[font_key]
        row.append({"text": font_info["name"], "callback_data": f"font_{font_key}"})
        if len(row) == 2 or i == len(fonts) - 1:
            keyboard.append(row.copy())
            row.clear()
    
    # Add help button
    keyboard.append([{"text": "❓ How to Use", "callback_data": "help"}])
    
    return {"inline_keyboard": keyboard}

def get_back_keyboard():
    return {"inline_keyboard": [[{"text": "🔙 Back to Fonts", "callback_data": "back_to_fonts"}]]}

# ========== TELEGRAM API ==========
def telegram_api_call(method, params=None):
    if params is None:
        params = {}
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/{method}"
    data = json.dumps(params).encode('utf-8')
    try:
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"API error: {e}")
        return None

def send_message(chat_id, text, parse_mode=None, reply_markup=None, reply_to=None):
    params = {'chat_id': chat_id, 'text': text}
    if parse_mode:
        params['parse_mode'] = parse_mode
    if reply_markup:
        params['reply_markup'] = reply_markup
    if reply_to:
        params['reply_to_message_id'] = reply_to
    telegram_api_call('sendMessage', params)

def edit_message(chat_id, message_id, text, parse_mode=None, reply_markup=None):
    params = {
        'chat_id': chat_id,
        'message_id': message_id,
        'text': text
    }
    if parse_mode:
        params['parse_mode'] = parse_mode
    if reply_markup:
        params['reply_markup'] = reply_markup
    telegram_api_call('editMessageText', params)

def answer_callback(callback_id, text=None):
    params = {'callback_query_id': callback_id}
    if text:
        params['text'] = text
    telegram_api_call('answerCallbackQuery', params)

def send_typing(chat_id):
    telegram_api_call('sendChatAction', {'chat_id': chat_id, 'action': 'typing'})

def get_bot_info():
    result = telegram_api_call('getMe')
    return result.get('ok', False) if result else False

def set_webhook():
    render_url = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")
    if render_url:
        webhook_url = f"https://{render_url}/webhook/{TELEGRAM_TOKEN}"
        telegram_api_call('setWebhook', {'url': webhook_url})

# ========== MESSAGE PROCESSING ==========
def process_update(update):
    # Handle callback queries (button clicks)
    if 'callback_query' in update:
        callback = update['callback_query']
        callback_id = callback.get('id')
        message = callback.get('message', {})
        chat_id = message.get('chat', {}).get('id')
        message_id = message.get('message_id')
        data = callback.get('data', '')
        
        answer_callback(callback_id)
        
        if data == "back_to_fonts":
            edit_message(chat_id, message_id, 
                        f"🎨 *{BOT_NAME}*\n\nChoose a font style from below:",
                        parse_mode='Markdown',
                        reply_markup=get_inline_keyboard())
        
        elif data == "help":
            help_text = f"""❓ *How to Use {BOT_NAME}*

1. Click on any font button
2. Send me your text
3. I'll convert it to that font!

*Commands:*
/start - Show all fonts
/fonts - List all fonts

*Example:*
Click "𝐒𝐞𝐫𝐢𝐟 𝐁𝐨𝐥𝐝" then send "Hello"
→ Output: "𝐇𝐞𝐥𝐥𝐨"

*Tip:* You can forward the styled text anywhere!"""
            
            edit_message(chat_id, message_id, help_text, parse_mode='Markdown', reply_markup=get_back_keyboard())
        
        elif data.startswith("font_"):
            font_key = data.replace("font_", "")
            font_info = FONTS.get(font_key, {})
            
            # Store selected font in memory (simplified - use user context)
            # For simplicity, we'll just instruct user
            text = f"🎨 *{font_info.get('name', 'Font')} Selected*\n\n{font_info.get('desc', '')}\n\n✨ *Now send me your text!*\n\nI'll convert it to {font_info.get('name', 'this font')} style.\n\n💡 Example: Send \"Hello World\""
            
            # Store font preference (in a real bot, you'd store in DB)
            # Here we'll just edit message and expect next message
            edit_message(chat_id, message_id, text, parse_mode='Markdown', reply_markup=get_back_keyboard())
            
            # Store user's selected font (in memory)
            # Since we don't have DB, we'll use a global dict
            if not hasattr(process_update, 'user_fonts'):
                process_update.user_fonts = {}
            process_update.user_fonts[chat_id] = font_key
    
    # Handle normal messages
    elif 'message' in update:
        message = update['message']
        chat_id = message.get('chat', {}).get('id')
        user_name = message.get('from', {}).get('first_name', 'User')
        message_text = message.get('text', '')
        message_id = message.get('message_id')
        
        if not chat_id or not message_text:
            return
        
        # Handle commands
        if message_text.startswith('/'):
            cmd = message_text.lower()
            
            if cmd == '/start':
                welcome = f"""🎨 *Welcome to {BOT_NAME}!* ✨

Convert your text into *stylish fonts*!

*How to use:*
1️⃣ Click any font button below
2️⃣ Send me your text
3️⃣ Get stylish text instantly!

*Available Fonts:*
• Bold, Italic, Script
• Gothic, Monospace
• Bubble, Circle, Square
• And many more!

Click a font to get started! 🚀"""
                
                send_message(chat_id, welcome, parse_mode='Markdown', reply_markup=get_inline_keyboard())
                return
            
            elif cmd == '/fonts':
                send_message(chat_id, "🎨 *Available Fonts:*\n\nClick the buttons below!", 
                           parse_mode='Markdown', reply_markup=get_inline_keyboard())
                return
            
            else:
                send_message(chat_id, "❓ Unknown command.\nUse /start to see all fonts!", 
                           parse_mode='Markdown', reply_markup=get_inline_keyboard())
                return
        
        # Check if user has selected a font
        if hasattr(process_update, 'user_fonts') and chat_id in process_update.user_fonts:
            font_key = process_update.user_fonts[chat_id]
            font_info = FONTS.get(font_key, {})
            
            if font_info and 'map' in font_info:
                send_typing(chat_id)
                converted = convert_text(message_text, font_info['map'])
                
                result = f"*{font_info['name']} Style:*\n`{converted}`\n\n✨ Here's your stylish text!"
                send_message(chat_id, result, parse_mode='Markdown', reply_markup=get_back_keyboard())
                
                # Keep font selected for next conversion
                return
        
        # If no font selected, show error
        send_message(chat_id, f"❌ *No font selected!*\n\nPlease select a font first using /start or /fonts", 
                    parse_mode='Markdown', reply_markup=get_inline_keyboard())

# ========== MAIN ==========
if __name__ == "__main__":
    print("=" * 50)
    print(f"🎨 {BOT_NAME} Starting...")
    print("=" * 50)
    
    if not TELEGRAM_TOKEN:
        print("❌ ERROR: TELEGRAM_TOKEN not set!")
        print("Please add TELEGRAM_TOKEN in environment variables")
    else:
        print(f"✅ Bot Token: {TELEGRAM_TOKEN[:10]}...")
        
        if get_bot_info():
            print(f"✅ Bot connected successfully!")
            set_webhook()
            print(f"✅ Webhook set!")
        else:
            print(f"❌ Failed to connect to Telegram!")
    
    print("=" * 50)
    print(f"🎨 Fonts available: {len(FONTS)}")
    print("=" * 50)
    
    # Start Flask server
    app.run(host='0.0.0.0', port=8080)
