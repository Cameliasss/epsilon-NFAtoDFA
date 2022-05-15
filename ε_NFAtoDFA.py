# 寻找一步epsilon
def FindClosureEpsilonOnce(state_list):
    closure_epsilon=state_list
    for i in range(state_num):
        values=list(state_change_table[i].values())
        if values[0] in state_list:
            closure_epsilon=list(set(closure_epsilon+values[-1]))
    return closure_epsilon

# 寻找epsilon闭包
def FindClosureEpsilon(state_list):
    _closure_epsilon=state_list
    while FindClosureEpsilonOnce(_closure_epsilon)!=_closure_epsilon:
        _closure_epsilon=FindClosureEpsilonOnce(_closure_epsilon)
    new_closure_epsilon = [i for i in _closure_epsilon if i != '']
    return new_closure_epsilon

# 寻找sigma2模式输入字符的转移结果
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

# DFA输出txt文件
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

# 读取NFA文件并进行数据处理
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


if __name__ == '__main__':
    # 创建结果状态转移表
    DFA=[[0 for i in range(len(alphabet))] for i in range(len(states))]
    for i in range(len(states)):
        now_state = []
        now_state.append(states[i])
        for j in range(len(alphabet)-1,-1,-1):
            if j==(len(alphabet)-1):
                DFA[i][j]=FindClosureEpsilon(now_state)
            else:
                tmp=FindClosureEpsilon(now_state)
                DFA[i][j]=FindClosureOther(tmp,alphabet[j])
    print('DFA=',DFA)
    text_create(DFA)

