import os
import glob
import re

fpath = os.path.abspath(__file__)
dirname = os.path.dirname(fpath)
files = glob.glob(dirname+"/*.cc")

all_src = ""
for f in files:
    if "obfuse" in f: continue
    if "ob_kernel" in f: continue
    if "all.cc" in f: continue
    # if "atomic" not in f: continue
    with open(f, 'r') as ff:
        all_src += ff.read()
        all_src += '\n'

#with open("/home/cjld/tmp/data.cc", "w") as f:
#    f.write(all_src)
#exit(0)

# move #include
incs = []
new_src = ""
for l in all_src.splitlines():
    if l.startswith("#inc"):
        incs.append(l)
        # print(l)
    else:
        new_src += l + '\n'
all_src = new_src

# remove // comments
all_src = re.sub("[^\"]//.*\n", "\n", all_src)


# string sub
new_src = ""
in_str = False
i = 0
while i < len(all_src):
    c = all_src[i]
    i += 1
    # print(i, len(all_src))
    if in_str and c==in_str:
        new_src += c
        in_str = False
        continue
    if in_str:
        if c == '\\':
            new_src += c + all_src[i]
            i += 1
            continue
        else:
            new_src += "\\x" + hex(ord(c))[2:]
    elif c == '"' or c == "'":
        in_str = c
        new_src += c
        continue
    else:
        new_src += c

all_src = new_src


# remove // comments
all_src = re.sub("//.*\n", "\n", all_src)

# remove /* */ comments
all_src = re.sub("/\\*.*?\\*/", "\n", all_src, flags=re.S)
# token replace
tokens = {"_inputs":1, "_outputs":1, "_stop_fuse":1, "_force_fuse":1}
token = ""
in_str = False
i = 0
while i < len(all_src):
    c = all_src[i]
    i += 1
    if in_str and c==in_str:
        in_str = False
        continue
    if in_str:
        if c == '\\':
            i += 1
            continue
        else:
            pass
    elif c == '"' or c == "'":
        in_str = c
        continue
    else:
        if (c>='a' and c<='z') or (c>='A' and c<='Z') or (c=='_'):
            token += c
        elif len(token) and ((c>='0' and c<='9')):
            token += c
        else:
            if len(token):
                tokens[token] = 1
            token = ""

def scan_no_str(all_src, func):
    new_src = ""
    no_str = ""
    in_str = False
    i = 0
    while i < len(all_src):
        c = all_src[i]
        i += 1
        # print(i, len(all_src))
        if in_str and c==in_str:
            new_src += c
            in_str = False
            no_str = ""
            continue
        if in_str:
            if c == '\\':
                new_src += c + all_src[i]
                i += 1
                continue
            else:
                new_src += c
        elif c == '"' or c == "'":
            # print(len(no_str), len(new_src))
            # print(no_str[:100], new_src[-100:])
            no_str = func(no_str)
            new_src += no_str
            # print(len(no_str))
            # print(no_str)
            no_str = ""
            in_str = c
            new_src += c
            continue
        else:
            no_str += c
    no_str = func(no_str)
    new_src += no_str
    return new_src


# print(','.join(tokens.keys()))
# 全局token
ex = "namespace,jittor,define,void,int64_t,int,const,vector,Op,ops,Var,father,size,auto,while,return,bool,if,flags,get,NodeFlags,stop_fuse,false,custom_data,type,OpType,other,force_fuse,true,reduce,broadcast,element,else,ifdef,outputs,endif,func,for,inputs,node,var,op,back,std,prev,end,begin,next,tflag,index,input,reserve,uint,push_back,V_ON,LOGvvvv,ASSERTop,continue,dtype,ns_bool,front,DECLARE_FLAG,para_opt_level,static,KernelIR,map,push_front,before,expr,make,attrs,to_string,dfs,Expr,is_sym,ir,find_define,str,nullptr,count,string,split,name_ex,ASSERT,OpCompiler,precompile,to_cstring,Pass,children,clear,unique_ptr,find,has_attr,break,get_attr,check_attr,swap,substr,unordered_map,at,after,pm,oc,get_op_var_by_name,length,LOGvvv,LOGf,AtomicTunerPass,run,get_loop_option,npos,this,S,rebuild_scope,startswith,insert,remove_all_unused,Node,tflag_count,nt,int64,lived_nodes,total_node,free_buffer,inline,free_var,mem_ptr,allocator,free,allocation,number_of_lived_vars,pop,CHECK_EXIST,is_var,backward_liveness,erase,is_stop_grad,release_backward_liveness,pending_liveness,is_finished,release_pending_liveness,forward_liveness,release_forward_liveness,need_free,release,number_of_lived_ops,memcheck_all_exist,NODE_MEMCHECK,CHECK_NODE_EXIST,own_pending_liveness,own_forward_liveness,own_backward_liveness,own_both_liveness,release_both_liveness,SetupFreeBuffer,setup_free_buffer,finish_pending_liveness,set,finished,need_release,release_inputs,set_inputs,list,size_t,emplace_back,add_inputs,set_stop_grad,stop_grad,ostream,operator,move_out,match,extern,EXTERN_LIB,_inputs,_outputs,_stop_fuse,_force_fuse,flist,inner,try_parse_define,max,min,clone,function,simplify,move,is,make_op,assign_symbol,LoopVarAnalyzePass,ParallelPass,loop_options,name,_number,get_pass,number_of_ranges,omp_get_max_threads,_cuda,_cpu,char,NanoVector,_stop_grad,_finished,get_nbits,__release,count_fuse,sizeof,_malloca,_freea,_WIN32,STACK_ALLOC,cuda_archs,replace,shape"
ex += ",_out_hint,_needed_by_backward"
ex += ",lived_nodes_id"
ex += ",num"
ex += ",ReduceOp,SharedReducePass,dynamic_cast,reduce_mask,stoi,pair,make_pair,FusedOp,empty,first,second,rfind,typedef,tuple,make_tuple"
ex += ",free_var_mem"
ex = set(ex.split(','))


values = set()
import random
random.seed(0)
max_len = 0
for k in list(tokens.keys()):
    max_len = max(max_len, len(k))
    while 1:
        v = "x"+str(random.randint(0,100000))
        if v not in values: break
    values.add(v)
    tokens[k] = v
    if k not in ex:
        print(k, '->', v)
        all_src = scan_no_str(all_src, lambda s: re.sub("\\b"+k+"\\b", v, s))
        # print(len(all_src))
        # all_src = re.sub("\\b"+k+"\\b", v, all_src)
    else:
        pass

# replace other
ss = "_"
for i in range(ord("a"), ord("z")+1): ss += chr(i)
for i in range(ord("A"), ord("Z")+1): ss += chr(i)
for i in range(ord("0"), ord("9")+1): ss += chr(i)
defs = ""
for k in ss:
    while 1:
        v = "x"+str(random.randint(0,100000))
        if v not in values: break
    values.add(v)
    tokens[k] = v
    defs += f"#define {v} {k}\n"

for i in range(2, max_len+1):
    args = [ f"x{j}" for j in range(i) ]
    defs += f"#define XX{i}(" + ",".join(args) + f") _XX{i}(" + ",".join(args) + ")\n"
    defs += f"#define _XX{i}(" + ",".join(args) + f") " + "##".join(args) + "\n"

for k in list(tokens.keys()):
    if k in ["define", "ifdef", "endif", "else", "NODE_MEMCHECK", "_WIN32"]: continue
    if k not in ex: continue
    v = tokens[k]
    if len(k)>1:
        v = f"XX{len(k)}("
        for i in range(len(k)):
            if i: v += ","
            v += tokens[k[i]]
        v += ")"
    print(k, '->', v)
    all_src = scan_no_str(all_src, lambda s: re.sub("\\b"+k+"\\b", v, s))

# replace simbol
sim_token = ["<<=", ">>=", "->", "==", "!=", "<=", ">=", "||", ">>", "<<", "&&", "&=", "^=", "|=", "+=", "-=", "*=", "/=", "&=", "|=", "++", "--", "::", "<>", "[]", "()", "{}", "!", "~", "*", "/", "%", ".", "&", "^", "[", "]", "{", "}", "=", "?", ":", "=", ";", "|", "<", ">"]
for k in sim_token:
    while 1:
        v = "x"+str(random.randint(0,100000))
        if v not in values: break
    values.add(v)
    defs += f"#define {v} {k}\n"
    v = " " + v + " "
    print(k, '->', v)
    all_src = scan_no_str(all_src, lambda s: s.replace(k, v))

# remove space
new_src = ""
i = 0
for a in all_src.splitlines():
    i += 1
    a = a.strip()
    if a.startswith("#"):
        new_src += "\n"+a+"\n"
    else:
        for j in range(10):
            a = a.replace("  ", " ")
        if i>=0:
            new_src += a + " "
        else:
            new_src += a + "\n"
for j in range(10):
    new_src = new_src.replace("  ", " ")
all_src = new_src

# random change line
def is_var(c):
    return c=='_' or (c>='A' and c<='Z') or (c>='a' and c<='z') or (c>='0' and c<='9')
cnt = 0
def scan(all_src):
    global cnt
    new_src = ""
    pc = "a"
    for c in all_src:
        if c == '\n':
            cnt = 0
        if cnt > 1000:
            if is_var(pc) != is_var(c):
                new_src += '\n'
                cnt = 0
        cnt += 1
        pc = c
        new_src += c
    return new_src
all_src = scan_no_str(all_src, scan)

# ob defs
defs = "\n".join(incs) + '\n' + defs
new_defs = ""
vs = list(values)
p = random.choices(vs, k=3000)
p += random.choices("[],", k=1000)
random.shuffle(p)
new_defs += "_P(" + " ".join(p) + ")\n"
for d in defs.splitlines():
    p = random.choices(vs, k=1000)
    p += random.choices("[],", k=50)
    random.shuffle(p)
    new_defs += "_P(" + " ".join(p) + ")\n"
    new_defs += d + "\n"


# add include
all_src = new_defs + all_src

with open("/tmp/all.cc", "w") as f:
    f.write(all_src)

import os
os.system(r"/usr/bin/g++ /tmp/all.cc  -Wno-unknown-pragmas -D_P\(...\)= -std=c++14 -fPIC  -march=native  -fdiagnostics-color=always  -I/home/lxl/workspace/test/jittor/python/jittor/src -I/usr/include/python3.8 -I/usr/include/python3.8 -I/home/lxl/.cache/jittor/master/g++  -O2  -c  -o /tmp/all.o")

import gzip

with gzip.open(dirname+'/../../../utils/data.gz', 'wb') as f:
    f.write(all_src.encode("utf8"))

