OUTPUT_NAME=animego
BUILD_DIR=./build
LIB_DIR=./lib

build:
	gopy build -output=$(BUILD_DIR) ./$(OUTPUT_NAME)
	mkdir -p $(LIB_DIR)
	cp $(BUILD_DIR)/$(OUTPUT_NAME).py $(LIB_DIR)
	cp $(BUILD_DIR)/_$(OUTPUT_NAME).*.so $(LIB_DIR)
	cp $(BUILD_DIR)/go.py $(LIB_DIR)

clean:
	rm -rf ./build