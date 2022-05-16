# epsilon-NFAtoDFA
形式语言实验：带空移动的不确定状态机转化为确定状态机

环境配置
-------
### python3.9+pycharm

代码解释
--------
>### txt文件处理
>>#### 数据结构
>>* Move_NFA :list类型的list,存放NFA状态转移表.
>>* alphabet :str类型的list,存放所有读入字符,如['0', '1', 'epsilon']
>>* alphabet_num ：int类型, 存放除epsilon的条件个数
>>* state_change_table :dict类型的list,存放处理过后的NFA状态转移表,如[{'state':'q0', '0':{}, '1':{'q0','q1'}, 'epsilon':{'q2'}]
>>* states :str类型的list,存放NFA所有状态,如['q0','q1','q2']
>>* state_num :int类型,存放NFA状态数
>>* begin_state :str类型,存放起始状态
>>* end_state :str类型的list,存放接受状态
>>* zhuanyi_state :str类型的list,存放所有非陷阱状态
>>* xianjing_state :str类型的list,存放陷阱状态
```
with open('ε-NFA.txt', 'r') as r:
    epsilon_NFA = [line.rstrip('\n') for line in r.readlines()]
Move_NFA = epsilon_NFA[1::]
alphabet=epsilon_NFA[0].split()
alphabet_num=len(alphabet)-1
state_change_table=[]
states=[]
zhuanyi_states=[]
xianjing_state=[]
for i in range(len(Move_NFA)):
    state_change_list=Move_NFA[i].split()
    dt=dict()
    if len(state_change_list[0]) > 3:
        print('len=',len(state_change_list[0]))
        dt['state']=state_change_list[0][1:]
        states.append(state_change_list[0][1:])
    else:
        dt['state'] = state_change_list[0][-2:]
        states.append(state_change_list[0][-2:])
    for j in range(len(alphabet)):
        s=state_change_list[j+1][1:-1].split(',')
        zhuanyi_states.extend(s)
        dt[alphabet[j]]=s
    state_change_table.append(dt)
    state_num=len(states)
    end_state=[]
    if state_change_list[0][0]=='#':
        begin_state=state_change_list[0][1:]
        zhuanyi_states.append(begin_state)
    if state_change_list[0][0]=='*':
        end_state.append(state_change_list[0][1:])
print('epsilonNFA=',state_change_table)
```

>### 完成一次空闭包查找
>遍历所有状态,找到输入列表中状态,合并状态转移表中其epsilon对应项.closure_epsilon是合并列表,返回项new_closure_epsilon是排序后结果
```
def FindClosureEpsilonOnce(state_list):
    closure_epsilon=state_list
    for i in range(state_num):
        values=list(state_change_table[i].values())
        if values[0] in state_list:
            closure_epsilon=list(set(closure_epsilon+values[-1]))
    new_closure_epsilon = [i for i in closure_epsilon if i != '']
    new_closure_epsilon.sort(key=lambda x:x[1])
    return new_closure_epsilon
```
>### 找到所有NFA状态的空闭包集合
>求出_closure_epsilon, _closure_epsilon(s)表示由状态s经由条件ε可以到达的所有状态的集合.处理其中空项后返回new_closure_epsilon
```
def FindClosureEpsilon(state_list):
    _closure_epsilon=state_list
    while FindClosureEpsilonOnce(_closure_epsilon)!=_closure_epsilon:
        _closure_epsilon=FindClosureEpsilonOnce(_closure_epsilon)
    new_closure_epsilon = [i for i in _closure_epsilon if i != '']
    return new_closure_epsilon
```
>### 找到所有ε-NFA状态读入除epsilon外任一字符后的空闭包集合
>求出_closure, _closure(s)表示由状态s经由条件x(不包括epsilon)可以到达的所有状态的集合.处理其中空项后返回new_closure
```
def FindClosureOther(state_list,character):
    _closure_epsilon = FindClosureEpsilon(state_list)
    _closure=[]
    for i in range(state_num):
        values=list(state_change_table[i].values())
        keys=list(state_change_table[i].keys())
        j=keys.index(character)
        if values[0] in _closure_epsilon:
            _closure=list(set(_closure+values[j]))
    _closure = FindClosureEpsilon(_closure)
    new_closure=[i for i in _closure if i!='']
    return new_closure
```
>### NFA转化为DFA
>采用子集构造法
```
def ConvertToDfa(NFA):
    DFA = [[] for i in range(len(alphabet))]
    begin_index = states.index(begin_state)
    begin_list = [begin_state]
    DFA[0].append(begin_list)
    for i in range(alphabet_num):
        DFA[i + 1].append(NFA[begin_index][i])
        if NFA[begin_index][i] not in DFA[0] and NFA[begin_index][i]!=[]:
            DFA[0].append(NFA[begin_index][i])
    states_len = 1
    start_zhuangtai=len(DFA[0])-1
    while True:
        length=len(DFA[0])
        for s in DFA[0][length-start_zhuangtai::]:
            for i in range(alphabet_num):
                tmp=FindClosureOther(s,alphabet[i])
                DFA[i + 1].append(tmp)
                if tmp not in DFA[0] and tmp!=[]:
                    DFA[0].append(tmp)
        if len(DFA[0])==states_len:
            break
        else:
            states_len=len(DFA[0])
            start_zhuangtai=states_len-length
    print('test=',DFA)
```
>### 格式转化
>合并NFA状态为新状态
```
q=[]
    end_states=[]
    global end_list
    for s in DFA[0]:
        q.append(s)
    for l in DFA:
        for i in range(len(DFA[0])):
            if l[i] !=[]:
                if set(l[i])&set(end_state)!=set():
                    end_states.append(l[i])
                index = q.index(l[i])
                l[i] = 'q' + str(index)
    end_states = list(set([tuple(t) for t in end_states]))
    end_states = [list(v) for v in end_states]
    end_list=end_states
    for i in range(len(end_list)):
        index=q.index(end_list[i])
        end_list[i]='q'+str(index)
```

>### 将输出DFA写入txt文件
>判断初始状态和接受状态，是否需要换行
```
def text_create(DFA):
    file_path = 'DFA.txt'
    file = open(file_path, 'w')
    row_num=len(DFA[0])
    for i in range(row_num+1):
        if i==0:
            for j in alphabet:
                if j!='epsilon':
                    file.write(j+' ')
                else:
                    file.write('\n')
        else:
            for k in range(len(alphabet)):
                if k==0 and DFA[k][i-1]==begin_state:
                    file.write('#')
                    file.write(DFA[k][i-1])
                    file.write(' ')
                elif k==0 and DFA[k][i-1] in end_list:
                    file.write('*')
                    file.write(DFA[k][i-1])
                    file.write(' ')
                elif k==0:
                    file.write(DFA[k][i-1])
                    file.write(' ')
                elif k!=(alphabet_num):
                    if DFA[k][i-1]!=[]:
                        file.write(DFA[k][i-1])
                        file.write(' ')
                    else:
                        file.write('epsilon')
                        file.write(' ')
                else:
                    if DFA[k][i- 1] != []:
                        file.write(DFA[k][i- 1])
                        file.write('\n')
                    else:
                        file.write('epsilon')
                        file.write('\n')
    file.close()
```
