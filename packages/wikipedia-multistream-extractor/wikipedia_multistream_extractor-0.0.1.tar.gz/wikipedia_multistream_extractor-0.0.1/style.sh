#!/bin/bash

isort .
black --exclude='.*\/*(venv|.venv|test-results)\/*.*' .