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
    return dock.inspect_container(userid)

@d("/<int:userid>/url/")
def url(request, userid):
    return {'url': "http://php%s.timtec.com.br/" % userid}

@d("/<int:userid>/start/")
def start(request, userid):
    try:
        running = dock.inspect_container(userid)['State']['Running']
    except docker.client.APIError:
        running = False
        dock.create_container("hacklab/precise-php-fpm-nginx", detach=True,
                               volumes=['/var/www'], name="%s" % userid)
    finally:
        if not running:
            if not os.path.exists("/var/www/containers/%s" % userid):
                os.makedirs("/var/www/containers/%s" % userid)
            dock.start(userid, binds={'/var/www/containers/%s' % userid: '/var/www'})
            f = open("/var/www/containers/%s/info.php" % userid, 'w')
            f.write("<? phpinfo(); ?>")
            f.close()

    url = "php%s.timtec.com.br" % userid
    if not red.sdiff("frontend:%s" % userid, "dead:%s" % userid):
        red.spop("dead:%s" % url)
        container = dock.inspect_container(userid)
        ip = container["NetworkSettings"]['IPAddress']
        red.sadd("frontend:%s" % url, "http://%s:80" % ip)
    return {'result': True}

@d("/<int:userid>/stop/")
def stop(request, userid):
    dock.stop(userid)
    return {'result': True}

@d("/<int:userid>/restart/")
def restart(request, userid):
    dock.restart(userid)
    return start(request, userid)

@d("/<int:userid>/rm/")
def rm(request, userid):
    dock.stop(userid)
    dock.remove_container(userid)
    return {'result': True}

@d("/<int:userid>/documents/")
def documents(request, userid):
    if request.method == 'GET':
        return d.render_to_response("form.html")
    tgz = request.FILES['tgz']
    tf = tarfile.open(fileobj=tgz, mode="r:gz")
    tf.extractall("/var/www/containers/%s/" % userid)
    return {'result': True}

if __name__ == "__main__":
    d.main()
