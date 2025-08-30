# Makefile for ASCII Cam

# Default target: run the application with standard settings
.PHONY: default
default: run

# Install Python dependencies
.PHONY: install
install:
	@echo "Installing dependencies..."
	pip install opencv-python numpy pyvirtualcam

# Run the application with default settings
.PHONY: run
run:
	@echo "Running ASCII Cam with default settings..."
	python main.py

# Show all available command-line options
.PHONY: help
help:
	@python main.py --help

# Run with the default matrix mode (random characters)
.PHONY: matrix
matrix:
	@echo "Running in matrix mode..."
	python main.py --ascii-mode=matrix

# Run with the matrix mode using custom falling words
# You can change the words here.
.PHONY: matrix-words
matrix-words:
	@echo "Running in matrix mode with custom words..."
	python main.py --ascii-mode=matrix --rain-words NEO IS THE ONE

# Run with a sparse matrix rain effect
.PHONY: matrix-sparse
matrix-sparse:
	@echo "Running in matrix mode with sparse rain..."
	python main.py --ascii-mode=matrix --rain-cols=30

# Run in high resolution
.PHONY: high-res
high-res:
	@echo "Running in high resolution..."
	python main.py --cols=160 --rows=120

# Run without any ASCII art rendering (plain video)
.PHONY: no-ascii
no-ascii:
	@echo "Running with ASCII rendering disabled..."
	python main.py --no-ascii

# Run with the virtual camera output
# Note: Ensure the virtual camera backend (e.g., OBS) is running first.
.PHONY: virtual-cam
virtual-cam:
	@echo "Running with virtual camera output..."
	python main.py --mode=virtual

# A phony target to prevent conflicts with a file named 'clean'
.PHONY: clean
clean:
	@echo "Cleaning up..."
	@rm -f *.pyc
	@rm -rf __pycache__
