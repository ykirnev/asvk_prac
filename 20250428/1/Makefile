# Makefile для автоматизации сборки MUD

# Переменные
PYTHON := pipenv run python
PYBABEL := pipenv run pybabel
SPHINX_BUILD := pipenv run make
TESTS := pipenv run pytest
LOCALE_DIR := mood/server/locale
POT_FILE := $(LOCALE_DIR)/messages.pot
PO_FILES := $(LOCALE_DIR)/ru_RU/LC_MESSAGES/messages.po $(LOCALE_DIR)/en_US/LC_MESSAGES/messages.po
MO_FILES := $(LOCALE_DIR)/ru_RU/LC_MESSAGES/messages.mo $(LOCALE_DIR)/en_US/LC_MESSAGES/messages.mo
DOCS_DIR := docs/source
BUILD_DIR := $(DOCS_DIR)/_build
CACHE_DIR := .pytest_cache

# Цель по умолчанию
.DEFAULT_GOAL := html

# Цель i18n: генерация переводов
.PHONY: i18n
i18n: compile
	@echo "Translations generated"

# Шаг init: создание .po файлов, если отсутствуют
.PHONY: init
init:
	@if [ ! -f $(LOCALE_DIR)/ru_RU/LC_MESSAGES/messages.po ]; then \
		$(PYBABEL) init -i $(POT_FILE) -d $(LOCALE_DIR) -l ru_RU; \
		echo "Created ru_RU messages.po"; \
	fi
	@if [ ! -f $(LOCALE_DIR)/en_US/LC_MESSAGES/messages.po ]; then \
		$(PYBABEL) init -i $(POT_FILE) -d $(LOCALE_DIR) -l en_US; \
		echo "Created en_US messages.po"; \
	fi

# Шаг extract: извлечение строк
.PHONY: extract
extract:
	$(PYBABEL) extract -F babel.cfg -o $(POT_FILE) mood/
	@echo "Extracted strings to $(POT_FILE)"

# Шаг update: обновление .po файлов
.PHONY: update
update: extract init
	$(PYBABEL) update -i $(POT_FILE) -d $(LOCALE_DIR) -l ru_RU
	$(PYBABEL) update -i $(POT_FILE) -d $(LOCALE_DIR) -l en_US
	@echo "Updated .po files"

# Шаг compile: компиляция .mo файлов
.PHONY: compile
compile: update
	$(PYBABEL) compile -d $(LOCALE_DIR) -l ru_RU
	$(PYBABEL) compile -d $(LOCALE_DIR) -l en_US
	@echo "Compiled .mo files"

# Цель html: генерация HTML-документации
.PHONY: html
html:
	cd $(DOCS_DIR) && $(SPHINX_BUILD) html
	@echo "HTML documentation generated in $(BUILD_DIR)"

# Цель test: запуск тестов клиент+сервер
.PHONY: test
test: i18n
	$(TESTS) tests/test_server_client.py -v
	@echo "Tests completed"

# Очистка i18n
.PHONY: clean-i18n
clean-i18n:
	rm -f $(POT_FILE) $(PO_FILES) $(MO_FILES)
	@echo "Cleaned i18n files"

# Очистка html
.PHONY: clean-html
clean-html:
	$(PYTHON) -c "import shutil; shutil.rmtree('$(BUILD_DIR)', ignore_errors=True)"
	@echo "Cleaned HTML documentation"

# Очистка test
.PHONY: clean-test
clean-test:
	$(PYTHON) -c "import shutil; shutil.rmtree('$(CACHE_DIR)', ignore_errors=True)"
	@echo "Cleaned test cache"

# Полная очистка
.PHONY: clean
clean: clean-i18n clean-html clean-test
	@echo "All generated files cleaned"