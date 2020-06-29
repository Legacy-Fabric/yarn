.PHONY: run

run: 
    $(shell ./gradlew yarn)

prerequisites: run

target: prerequisites 