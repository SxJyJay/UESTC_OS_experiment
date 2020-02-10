class PCB(object):
    def __init__(self):
        self.PID=''
        self.status=''
        self.child=[]
        self.parent='null'
        self.priority=0 #0-init,1-user,2-system
        self.resource_occupied=[0,0,0,0]    #当前占有四类资源数
        self.blocked_resource_type=0    #引起阻塞资源的种类

class RCB(object):
    def __init__(self):
        self.RID=0
        self.Init_num=0
        self.Ava_num=0

global Resource_List
global Ready_List
global Running
global Process_List
global Blocked_List

Resource_List=[]
Ready_List=[]
Blocked_List=[]
Process_List=[] #记录所有的进程信息
Running='null'

def init_resource_list():#初始化资源队列
    global  Resource_List
    for i in range(4):
        rcb=RCB()
        rcb.RID=(i+1)
        rcb.Ava_num=rcb.Init_num=(i+1)
        Resource_List.append(rcb)

def Create(PID,parent,child,priority):
    global Running
    global Ready_List
    global Process_List
    new=PCB()
    new.PID=PID
    if parent!="null":
        new.parent=parent.PID
    else:
        new.parent=parent
    if child!="null":
        new.child.append(child)
    new.priority=priority

    for item in Process_List:
        if new.PID==item.PID:
            print("该名字的进程已存在，不可再次创建")
            return
    if Ready_List==[]:
        if Running=='null':
            Running=new.PID
            new.status='running'
        else:
            new.status='ready'
            Ready_List.append(new)
    else:
        new.status='ready'
        Ready_List.append(new)

    Process_List.append(new)
    sort_ready_list()

def sort_ready_list():  #对就绪队列按优先级排序
    global Ready_List
    temp=[]
    for item in Ready_List:
        if(item.priority==2):
            temp.append(item)
    for item in Ready_List:
        if(item.priority==1):
            temp.append(item)
    for item in Ready_List:
        if(item.priority==0):
            temp.append(item)
    Ready_List=temp

def sort_blocked_list():  #对阻塞队列按优先级排序
    global Blocked_List
    temp=[]
    for item in Blocked_List:
        if(item.priority==2):
            temp.append(item)
    for item in Blocked_List:
        if(item.priority==1):
            temp.append(item)
    for item in Blocked_List:
        if(item.priority==0):
            temp.append(item)
    Blocked_List=temp

def Release(PID):
    global Process_List
    global Resource_List
    global Running
    global Ready_List
    global Blocked_List

    for item in Process_List:
        if item.PID==PID:
            temp=item
            Resource_List[0].Ava_num+=item.resource_occupied[0]
            item.resource_occupied[0]=0
            Resource_List[1].Ava_num+=item.resource_occupied[1]
            item.resource_occupied[1]=0
            Resource_List[2].Ava_num+=item.resource_occupied[2]
            item.resource_occupied[2]=0
            Resource_List[3].Ava_num+=item.resource_occupied[3]
            item.resource_occupied[3]=0
            break

    #检查阻塞队列中的进程，看是否有可唤醒的进程
    for item in Blocked_List:
        if item.blocked_resource_type==0:
            continue
        else:
            block_resource_type=item.blocked_resource_type
            if item.resource_occupied[block_resource_type-1]<=Resource_List[block_resource_type-1].Ava_num:
                item.status="ready"
                Resource_List[block_resource_type].Ava_num-=item.resource_occupied[block_resource_type-1]
                Blocked_List.remove(item)
                Ready_List.append(item)
                sort_blocked_list()
                sort_ready_list()
                break
            else:
                continue
    return temp


def Destroy(PID):
    global Process_List
    global Resource_List
    global Running
    global Ready_List
    global Blocked_List

    temp=Release(PID)

    for i in range(len(Blocked_List)):
        if Blocked_List[i].PID==PID:
            del Blocked_List[i]
            break

    for i in range(len(Ready_List)):
        if Ready_List[i].PID==PID:
            del Ready_List[i]
            break

    if(Running==PID):
        Running='null'

    Process_List.remove(temp)

    #递归调用删除该PCB的子进程PCB
    for child in temp.child:
        if(child=='null'):
            return
        else:
            Destroy(child)



def Request(RID,num):#只有可能是正在运行的进程可能做申请资源的操作
    global Running
    global Ready_List
    global Blocked_List
    global Resource_List
    global Process_List

    if(Running=='null'):
        print("无正在运行的进程，请求资源操作不成立")
        return

    if(Resource_List[RID-1].Ava_num-num<0):
        print("无足够资源分配")
        for item in Process_List:
            if item.PID==Running:
                temp=item
                break
        temp.blocked_resource_type=RID
        temp.resource_occupied[RID - 1] += num
        temp.status='blocked'
        Blocked_List.append(temp)
        if len(Ready_List)==0:
            Running="null"
        else:
            Running=Ready_List[0].PID
            Ready_List[0].status='running'
            Ready_List.pop(0)

    else:
        for item in Process_List:
            if item.PID==Running:
                item.resource_occupied[RID-1]+=num
                Resource_List[RID-1].Ava_num-=num

    sort_blocked_list()

def time_out():
    global Ready_List
    global Running
    for item in Process_List:
        if item.PID==Running:
            break
    Ready_List.append(item)
    item.status="ready"
    Running=Ready_List[0].PID
    Ready_List[0].status="running"
    Ready_List.pop(0)

    sort_ready_list()

def list_all_process_and_status():
    global Process_List
    for item in Process_List:
        print(item.__dict__)

def list_all_resource_and_status():
    global Resource_List
    for item in Resource_List:
        print(item.__dict__)

def check_process_info(PID):
    global Process_List
    for item in Process_List:
        if item.PID==PID:
            print(item.__dict__)
            break

def search_process_info(PID):
    global Process_List
    for item in Process_List:
        if item.PID==PID:
            return item
    return "null"

if __name__=='__main__':
    init_resource_list()
    while(True):
        Running_PCB = search_process_info(Running)  #用于记录正在运行的PCB，从而确定新创建进程与正在运行进程的父子关系
        command=[]
        command=input("shell>").split()

        if command[0]=='cr':
            Create(PID=command[1],parent=Running_PCB,child="null",priority=int(command[2]))
            new_PCB=search_process_info(command[1])
            if Running_PCB=="null":
                pass
            else:
                Running_PCB.child.append(new_PCB.PID)
            # print(len(Ready_List))

        elif command[0]=='de':
            Destroy(command[1])
            # print(len(Ready_List))

        elif command[0]=='to':
            time_out()

        elif command[0]=='req':
            if command[1]=='R1':
                Request(1, int(command[2]))
            elif command[1]=='R2':
                Request(2, int(command[2]))
            elif command[1]=='R3':
                Request(3, int(command[2]))
            elif command[1]=='R4':
                Request(4, int(command[2]))

        elif command[0]=='rel': #rel:release
            Release(Running)

        elif command[0]=='lsp': #lsp:list all process
            list_all_process_and_status()

        elif command[0]=='lsr': #lsr:list all resource
            list_all_resource_and_status()

        elif command[0]=='cp':  #cp:check process
            check_process_info(command[1])

        print("{} is running".format(Running))

