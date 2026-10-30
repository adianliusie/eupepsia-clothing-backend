layer:
	./build_layer.sh

up:
	sam local start-api -t template.yaml --skip-pull-image --warm-containers EAGER -p 8001

deploy:
	sam deploy --config-env dev

clean:
	rm -rf ./.aws-sam/
