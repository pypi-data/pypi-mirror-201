#coding:utf-8
#!/usr/bin/python3
import os
import sys
import logging
import signal
import time
'''
from whole.Run import R,Start,Stop,Restart

pid_file = "/var/run/r.pid"
log_file = "/var/log/r.log"

R("spr","r")
Start(pid_file, log_file):#启动软件
Stop(pid_file):#停止软件运行
Restart(pid_file, log_file):#重新启动软件
'''

def write_pid_file(pid_file, pid):
    import fcntl
    import stat
    try:
        fd = os.open(pid_file, os.O_RDWR | os.O_CREAT, stat.S_IRUSR | stat.S_IWUSR)
    except OSError as e:
        return -1
    flags = fcntl.fcntl(fd, fcntl.F_GETFD)
    assert flags != -1
    flags |= fcntl.FD_CLOEXEC
    r = fcntl.fcntl(fd, fcntl.F_SETFD, flags)
    assert r != -1
    # There is no platform independent way to implement fcntl(fd, F_SETLK, &fl)
    # via fcntl.fcntl. So use lockf instead
    try:
        fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB, 0, 0, os.SEEK_SET)
    except IOError:
        r = os.read(fd, 32)
        if r:
            logging.error('already started at pid %s' % to_str(r))
        else:
            logging.error('already started')
        os.close(fd)
        return -1
    os.ftruncate(fd, 0)
    os.write(fd, to_bytes(str(pid)))
    return 0

def freopen(f, mode, stream):
    oldf = open(f, mode)
    oldfd = oldf.fileno()
    newfd = stream.fileno()
    os.close(newfd)
    os.dup2(oldfd, newfd)

def Start(pid_file, log_file):#启动软件
    def handle_exit(signum, _):
        if signum == signal.SIGTERM:
            sys.exit(0)
        sys.exit(1)
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    # fork only once because we are sure parent will exit
    pid = os.fork()
    assert pid != -1
    if pid > 0:
        # parent waits for its child
        time.sleep(5)
        sys.exit(0)
    # child signals its parent to exit
    ppid = os.getppid()
    pid = os.getpid()
    if write_pid_file(pid_file, pid) != 0:
        os.kill(ppid, signal.SIGINT)
        sys.exit(1)
    os.setsid()
    signal.signal(signal.SIG_IGN, signal.SIGHUP)
    print("启动："+pid_file)
    os.kill(ppid, signal.SIGTERM)
    sys.stdin.close()
    try:
        freopen(log_file, 'a', sys.stdout)
        freopen(log_file, 'a', sys.stderr)
    except IOError as e:
        sys.exit(1)

def Stop(pid_file):#停止软件运行
    import errno
    try:
        with open(pid_file) as f:
            buf = f.read()
            pid = to_str(buf)
            if not buf:
                logging.error('not running')
    except IOError as e:
        if e.errno == errno.ENOENT:
            # always exit 0 if we are sure daemon is not running
            logging.error('not running')
            return
        sys.exit(1)
    pid = int(pid)
    if pid > 0:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError as e:
            if e.errno == errno.ESRCH:
                logging.error('not running')
                # always exit 0 if we are sure daemon is not running
                return
            sys.exit(1)
    else:
        logging.error('pid is not positive: %d', pid)
    # sleep for maximum 10s
    for i in range(0, 200):
        try:
            # query for the pid
            os.kill(pid, 0)
        except OSError as e:
            if e.errno == errno.ESRCH:
                break
        time.sleep(0.05)
    else:
        logging.error('timed out when stopping pid %d', pid)
        sys.exit(1)
    print("停止:"+pid_file)
    os.unlink(pid_file)

def to_str(s):
    if bytes != str:
        if type(s) == bytes:
            return s.decode('utf-8')
    return s

def to_bytes(s):
    if bytes != str:
        if type(s) == str:
            return s.encode('utf-8')
    return s

def Restart(pid_file, log_file):#重新启动软件
    Stop(pid_file)
    Start(pid_file, log_file)

def R(t,n):
    pid="/var/run/"+n+".pid"
    log="/var/log/"+n+".log"
    if t == 's':##启动软件
        Start(pid, log)
    elif t == 'p':#停止软件运行
        Stop(pid)
        sys.exit(0)
    elif t == 'r':#重新启动软件
        Restart(pid, log)
    else:
        print("输入错误:"+t)
        sys.exit(0)