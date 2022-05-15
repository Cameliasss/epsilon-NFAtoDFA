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
>>* state_change_table :dict类型的list,存放处理过后的NFA状态转移表,如[{'state':'q0', '0':{}, '1':{'q0','q1'}, 'epsilon':{'q2'}]
>>* states :str类型的list,存放NFA所有状态,如['q0','q1','q2']
>>* state_num :int类型,存放NFA状态数
>>* begin_state :str类型,存放NFA起始状态
>>* end_state :str类型,存放NFA接受状态
```
with open('ε-NFA.txt', 'r') as r:
    NFA = [line.rstrip('\n') for line in r.readlines()]
Move_NFA = NFA[1::]
alphabet=NFA[0].split()
state_change_table=[]
states=[]
for i in range(len(Move_NFA)):
    state_change_list=Move_NFA[i].split()
    dt=dict()
    dt['state']=state_change_list[0][-2:]
    states.append(state_change_list[0][-2:])
    for j in range(len(alphabet)):
        s=state_change_list[j+1][1:-1].split(',')
        dt[alphabet[j]]=s
    state_change_table.append(dt)
    state_num=len(states)
    if state_change_list[0][0]=='#':
        begin_state=state_change_list[0][1:]
    if state_change_list[0][0]=='*':
        end_state=state_change_list[0][1:]
```

>### 完成一次空闭包查找
>遍历所有状态,找到输入列表中状态,合并状态转移表中其epsilon对应项.返回项是合并列表closure_epsilon
```
def FindClosureEpsilonOnce(state_list):
    closure_epsilon=state_list
    for i in range(state_num):
        values=list(state_change_table[i].values())
        if values[0] in state_list:
            closure_epsilon=list(set(closure_epsilon+values[-1]))
    return closure_epsilon
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
>### 找到所有NFA状态读入除epsilon外任一字符后的空闭包集合
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
>### 将输出DFA写入txt文件
```
def text_create(DFA):
    file_path = 'DFA.txt'
    file = open(file_path, 'w')
    for i in range(len(states)+1):
        if i==0:
            for j in range(len(alphabet)):
                if j!=(len(alphabet)-1):
                    file.write(alphabet[j]+' ')
                else:
                    file.write('\n')
        else:
            for k in range(len(alphabet)):
                if k==0 and states[i-1]==begin_state:
                    file.write('#')
                    file.write(states[i-1])
                    file.write(' ')
                elif k==0 and states[i-1]==end_state:
                    file.write('*')
                    file.write(states[i - 1])
                    file.write(' ')
                elif k==0:
                    file.write(states[i - 1])
                    file.write(' ')
                elif k!=(len(alphabet)-1):
                    file.write('{')
                    for x in DFA[i-1][k-1]:
                        file.write(x)
                        if DFA[i-1][k-1].index(x)!=(len(DFA[i-1][k-1])-1):
                            file.write(',')
                    file.write('} ')
                else:
                    file.write('{')
                    for x in DFA[i - 1][k - 1]:
                        file.write(x)
                        if DFA[i - 1][k - 1].index(x) != (len(DFA[i - 1][k - 1]) - 1):
                            file.write(',')
                    file.write('}'+'\n')
    file.close()
```

测试样例

-------
