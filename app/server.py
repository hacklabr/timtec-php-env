from importd import d

import docker, redis, os, tarfile

d(DEBUG=True)

dock = docker.Client(base_url='unix://var/run/docker.sock',
                                    version='1.6',
                                    timeout=10)

red = redis.StrictRedis(host='localhost', port=6379, db=0)

@d("/")
def containers(request):
    return dock.containers()

@d("/<int:userid>/")
def info(request, userid):
    return dock.inspect_container("php%s" % userid)

@d("/<int:userid>/url/")
def url(request, userid):
    return {'url': "http://php%s.timtec.com.br/" % userid}

@d("/<int:userid>/start/")
def start(request, userid):
    try:
        running = dock.inspect_container("php%s" % userid)['State']['Running']
    except docker.client.APIError:
        running = False
        dock.create_container("hacklab/precise-php-fpm-nginx", detach=True,
                               volumes=['/var/www'], name="php%s" % userid)
    finally:
        if not running:
            if not os.path.exists("/var/www/containers/php%s" % userid):
                os.makedirs("/var/www/containers/php%s" % userid)
            dock.start("php%s" % userid, binds={'/var/www/containers/php%s' % userid: '/var/www'})
            f = open("/var/www/containers/php%s/info.php" % userid, 'w')
            f.write("<? phpinfo(); ?>")
            f.close()

    url = "php%s.timtec.com.br" % userid
    red.delete("dead:%s" % url)
    red.delete("frontend:%s" % url)
    container = dock.inspect_container("php%s" % userid)
    ip = container["NetworkSettings"]['IPAddress']
    red.sadd("frontend:%s" % url, "http://%s:80" % ip)
    return {'result': True}

@d("/<int:userid>/stop/")
def stop(request, userid):
    dock.stop("php%s" % userid)
    return {'result': True}

@d("/<int:userid>/restart/")
def restart(request, userid):
    dock.restart("php%s" % userid)
    return start(request, userid)

@d("/<int:userid>/rm/")
def rm(request, userid):
    dock.stop("php%s" % userid)
    dock.remove_container("php%s" % userid)
    return {'result': True}

@d("/<int:userid>/documents/")
def documents(request, userid):
    if request.method == 'GET':
        return d.render_to_response("form.html")
    tgz = request.FILES['tgz']
    tf = tarfile.open(fileobj=tgz, mode="r:gz")
    tf.extractall("/var/www/containers/php%s/" % userid)
    return {'result': True}

if __name__ == "__main__":
    d.main()
