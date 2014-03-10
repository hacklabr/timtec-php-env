all: setup_py

clean:
	find . -type f -name '*.py[co]' -exec rm {} \;

setup_py:
	pip install -q -r requirements.txt --use-mirrors

install: all
	cp -r hipache-nginx/* /etc/nginx/
	cp timtec-php-env.conf /etc/init/
        docker build -t hacklab/precise-php-fpm-nginx .
