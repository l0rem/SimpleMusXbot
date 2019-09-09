# SimpleMusXbot

This is a simplified version of MusXbot, that has much less abilities, but is also cleaner and more understandable (in terms of code).

## Installation

This project requires a [Heroku](https://www.heroku.com/) -ish environment. You can also self-host using [Dokku](http://dokku.viewdocs.io/dokku/).

Assuming Dokku, SSH into your _VPS with DOKKU installed_ on it and:
1. `dokku apps:create [APP-NAME]`
2. `dokku config:set --no-restart [APP-NAME] BOT_TOKEN=[YOUR-BOT-TOKEN]`
3. `dokku config:set --no-restart [APP-NAME] WEBHOOK_URL=[YOUR-WEBHOOK-URL]`
4. `dokku config:set --no-restart [APP-NAME] ENV=PROD`


From _local machine_:</br>
5. `git init`</br>
6. `git clone git@github.com:l0rem/SimpleMusXbot.git`</br>
7. `git remote add dokku dokku@dokku.me:[APP-NAME]`</br>
8. `git push dokku master`


Again _on VPS_:</br>
9. `dokku config:set --no-restart [APP-NAME] DOKKU_LETSENCRYPT_EMAIL=[E-MAIL]`</br>
10. `dokku letsencrypt [APP-NAME]` (requires [letsencrypt plugin](https://github.com/dokku/dokku-letsencrypt))</br>
11. `dokku proxy:ports-set [APP-NAME] https:443:8080`

## Usage

Send /start to bot.

In order to see list of parsed tracks send your query as a text message to bot.

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Credits

python-telegram-bot 
DOKKU 
