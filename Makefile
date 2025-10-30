.PHONY: help start capture capture-discord capture-gif create-gif create-webm epd-preview epd-debug test

help:
	@echo "Available targets:"
	@echo "  start           - run the main timelapse script"
	@echo "  capture         - take a single photo via CLI"
	@echo "  capture-discord - take a photo and send Discord notification (if configured)"
	@echo "  capture-gif     - take a photo and prepare GIF (use --gif in CLI)"
	@echo "  create-gif      - create animated GIF from captured photos"
	@echo "  create-webm     - create animated WebM from captured photos"
	@echo "  epd-preview     - render a preview image for e-paper helper"
	@echo "  epd-debug       - run an epd debug invocation (writes /tmp/epd_debug.log)"

start:
	python3 timelapse.py

capture:
	python3 timelapse_lib/cli.py

capture-discord:
	python3 timelapse_lib/cli.py --discord

capture-gif:
	python3 timelapse_lib/cli.py --gif

create-gif:
	python3 -c "from timelapse_lib.create_animation import create_gif; print(create_gif())"

create-webm:
	python3 -c "from timelapse_lib.create_animation import create_webm; print(create_webm())"

test:
	pytest -q
