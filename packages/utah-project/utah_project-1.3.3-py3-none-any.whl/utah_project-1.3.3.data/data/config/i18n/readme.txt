
# To extract strings that need translation
pybabel extract -F babel.cfg -o ./config/i18n/messages.pot .

# Initialize a new language
pybabel init -i messages.pot -d ./config/i18n -l <LOCALE>

# Update existing
pybabel update -i ./config/i18n/messages.pot -d ./config/i18n

# to compile
pybabel compile -f -d ./config/i18n