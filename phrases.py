url = 'https://wwi.mp3-tut.online/search?query='

track_form = '''
<b>### Track {} / {} ###</b>\n
<b>Performer:</b> <code>{}</code>
<b>Title:</b> <code>{}</code>
<b>Duration:</b> <code>{}</code>'''

start_phrase = '<b>Hello, stranger!</b>\n\nThis bot\'s sole purpose is to download <code>.mp3\'s</code> for you.' \
               ' And nothing else.\nJust send performer, title or both and it will try to find needed track.' \
               '\n\n<code>Also check out other bots written by </code>@Lor3m<code>:</code>\n - @GetAltsBot\n' \
               ' - @HeyTacoBot'

no_results_phrase = '<b>Sorry, but there are no results.</b>'

searching_phrase = '<code>Searching, please wait...</code>'

download_started_phrase = 'Started downloading...'

file_too_large_phrase = 'Track is too big, cant download it \U0001F614'

error_occurred_phrase = 'Sorry, an error occurred while uploading track \U0001F97A'

