rm -rf "python" && mkdir -p "python"

docker run --rm -v /"$PWD" -w /"$PWD" lambci/lambda:build-python3.7 pip install nltk --ignore-installed --no-deps --target="//python"
