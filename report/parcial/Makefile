.PHONY: all
ML = pdflatex -shell-escape -interaction=nonstopmode -output-directory=aux

all: create move

create:
	@echo "Making latex pdf"
	mkdir aux || ${ML} *.tex

move:
	@echo "Moving pdf file to main folder"
	mv aux/*.pdf .
