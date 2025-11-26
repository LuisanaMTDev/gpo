#!/usr/bin/zsh

tailwindcss --input tailwind-input.css --output static/styles.css && docker-compose start && uv run -- flask --debug run
