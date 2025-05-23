---
title: 数据结构笔记②——栈和队列
date: '2024-02-29'
summary: 代码来自B站视频：数据结构与算法基础（青岛大学-王卓）
tags:
  - 笔记
  - 数据结构
share: false
---

# **栈和队列**

## **定义和特点**

栈和队列是限定插入和删除只能在表的“端点”进行的<u>**线性表**</u>，是线性表的子集（插入和删除位置受限的线性表）

**栈:** 后进先出  <u>VS</u>  **队列:** 先进先出

- **插入:** 栈和队列只能在第n+1个位置插入元素

- **删除:** 栈只能在第n个位置删除元素；队列只能在第1个位置删除元素

- **栈可用于改变顺序，队列可用于维持顺序**

### 栈 stack

**LIFO结构：Last In First Out**

表尾称为**栈顶**Top；表头称为**栈底**Base

插入元素到栈顶(即表尾)的操作，称为**入栈**(PUSH)

从栈顶(即表尾)删除最后一个元素的操作，称为**出栈**(POP)

逻辑结构：与线性表相同，仍为一对一关系

存储结构：用顺序栈或链栈存储均可，但顺序栈更常见

运算规则：只能在栈顶运算，且访问结点时依照LIFO原则

与一般线性表的区别：仅在于**运算规则**不同(随机存取VS后进先出)

【思考】假设有3个元素a，b，c，入栈顺序是a，b，c，则出栈顺序可能出现cab的情况吗？**<u>NO</u>**

### 队列 queue

**FIFO结构：First In First Out**

在表一端插入(表尾)，在另一端(表头)删除

逻辑结构：与线性表相同，仍为一对一关系

存储结构：顺序队或链队，以循环顺序队列更常见

运算规则：只能在队首和队尾运算，且访问结点时依照FIFO原则

## **栈的表示和操作的实现**

```
ADT Stack{
    数据对象:
    	D={ai|ai∈ElemSet, i=1,2,···,n,n≥0}
    数据关系:
        R1={<ai-1,ai>|ai-1,ai∈D, i=2,···,n}
    	约定an端为栈顶，ai端为栈底
    基本操作:初始化、进栈、出栈、取栈顶元素等
}ADT Stack
```

### 顺序栈的表示和实现

利用一组地址连续的存储单元依次存放自栈底到栈顶的数据元素。栈底一般在低地址端。

- 附设**top**指针，指示栈顶元素在顺序栈中的位置
  - 但是为了方便操作，通常top指示真正的栈顶元素之上的下标地址
- 另设**base**指针，指示栈底元素在顺序栈中的位置
- 另外，用**stacksize**表示栈可使用的最大容量

空栈：**base == top** 是栈空标志

栈满：**top - base == stacksize**

- 处理方法：**报错**，返回操作系统 / **分配更大的空间**，将原栈的内容移入新栈

溢出：(数组大小固定)

- **上溢**(overflow): 栈已经满，又要压入元素
- **下溢**(underflow): 栈已经空，还要弹出元素
- **注:** 上溢是一种错误，使问题的处理无法进行；而下溢一般认为是一种结束条件，即问题结束处理

#### 顺序栈的表示

```c++
#define MAXSIZE 100
typedef struct{
    SElemType *base;  //栈底指针
    SElemType *top;  //栈顶指针
    int stacksize;  //栈可用最大容量
}SqStack;
```

#### 顺序栈的初始化

```c++
Status InitStack(SqStack &S){  //构造一个空栈
    S.base=new SElemType[MAXSIZE];
    if(!S.base)
        exit(OVERFLOW);  //存储分配失败
    S.top=S.base;  //栈顶指针等于栈底指针
    S.stacksize=MAXSIZE;
    return OK;
}
```

#### 判断顺序栈是否为空

```c++
Status StackEmpty(SqStack S){  //若栈为空，返回TRUE；否则返回FALSE
    if(S.top==S.base)
        return TRUE;
    else
        return FALSE;
}
```

#### 求顺序栈长度

```c++
int StackLength(SqStack S){
    return S.top - S.base;
}
```

#### 清空顺序栈

```c++
Status ClearStack(SqStack S){
    if(S.base)
        S.top=S.base;
    return OK;
}
```

#### 销毁顺序栈

```c++
Status DestroyStack(SqStack &S){
    if(S.base){
        delete S.base;
        S.stacksize=0;
        S.base=S.top=NULL;
    }
    return OK;
}
```

#### 顺序栈的入栈

1. 判断是否栈满，若满则出错(上溢)
2. 元素e压入栈顶
3. 栈顶指针加1

```c++
Status Push(SqStack &S,SElemType e){
    if(S.top-S.base==S.stacksize)  //栈满
        return ERROR;
    *S.top++ = e;//相当于 *S.top=e; S.top++;
    return OK;
}
```

#### 顺序栈的出栈

1. 判断是否栈空，若空则出错(下溢)
2. 获取栈顶元素e
3. 栈顶指针减1

```c++
Status Pop(SqStack &S,SElemType &e){  //若栈不空，则删除S的栈顶元素，用e返回其值；并返回OK；否则返回ERROR
    if(S.top==S.base)  //等价于if(StackEmpty(S))
        return ERROR;
    e = *--S.top;  //指针先下移再取值，相当于 --S.top; e=*S.top;
    return OK;
}
```

### 链栈的表示和实现

#### 链栈的表示

链栈是运算受限的单链表，只能在链表头部进行操作

```c++
typedef struct StackNode{
    SElemType data;
    struct StackNode *next;
}StackNode,*LinkStack;
```

**注意：链栈中指针的方向是后继元素指向前驱元素**

- 链表的头指针就是栈顶
- 不需要头结点
- 基本不存在栈满的情况
- 空栈相当于头指针指向空
- 插入和删除仅在栈顶处执行

#### 链栈的初始化

```c++
void InitStack(LinkStack &S){
    //构造一个空栈，栈顶指针置为空
    S=NULL;
    return OK;
}
```

#### 判断链栈是否为空

```c++
Status StackEmpty(LinkStack S){
    if(S==NULL)
        return TRUE;
    else
        return FALSE;
}
```

#### 链栈的入栈

```c++
Status Push(LinkStack &S,SElemType e){
    p=new StackNode;  //生成新结点p
    p->data=e;  //将新结点数据域置为e
    p->next=S;  //将新结点插入栈顶，原先的栈顶元素作为其后继元素
    S=p;  //修改栈顶指针，S指向新结点
    return OK;
}
```

#### 链栈的出栈

```c++
Status Pop(LinkStack &S,SElemType &e){
    if(S==NULL)
        return ERROR;
    e=S->data;
    p=S;
    S=S->next;
    delete p;
    return OK;
}
```

#### 取栈顶元素

```c++
SElemType GetTop(LinkStack S){
    if(S!=NULL)
        return S->data;
}
```

## **栈与递归**

**注意点：必须有一个明确的递归出口，或称递归的边界**

函数嵌套调用遵循**后调用的先返回** => 用**栈**实现

## **队列的表示和操作的实现**

```
ADT Queue{
    数据对象:
    	D={ai|ai∈ElemSet, i=1,2,···,n,n≥0}
    数据关系:
        R1={<ai-1,ai>|ai-1,ai∈D, i=2,···,n}
    	约定其中a1端为队列头，an端为队列尾
    基本操作:初始化、入队、出队、取队头元素等
}ADT Queue
```

### 队列的顺序表示和实现(循环队列)

#### 循环队列的类型定义

**使用一维数组base[MAXQSIZE]**

```c++
#define MAXQSIZE 100  //最大队列长度
typedef struct{
    QElemType *base;  //初始化的动态分配存储空间
    int front;  //头指针，若队列不空，指向队列头元素
    int rear;  //尾指针，若队列不空，指向队列尾元素的下一个位置
}SqQueue;  //SqQueue不是指针类型，引用成员用.号  //front和rear并非指针变量，只是用以表示数组当中元素的下标位置
```

- 真溢出：front=0，rear=MAXQSIZE
- 假溢出：front≠0，rear=MAXQSIZE

**解决假上溢的方法**——引入**循环队列**

base[0]接在base[MAXQSIZE-1]之后，若rear+1==M，则令rear=0

实现方法：利用**模(mod，C语言中: %)运算**

**解决队空or队满的判断方法**

- 另设标志区别队空/队满
- 另设变量记录元素个数
- 少用一个元素空间
  - 队空：front==rear
  - 队满：(rear+1)%MAXQSIZE==front

#### 循环队列的初始化

```c++
Status InitQueue(SqQueue &Q){
    Q.base=new QElemType[MAXQSIZE];  //分配数组空间
    if(!Q.base)
        exit(OVERFLOW);  //存储分配失败
    Q.front=Q.rear=0;  //头指针、尾指针置为0，队列为空
	return OK;
}
```

#### 求循环队列的长度

```c++
int QueueLength(SqQueue Q){
    return ((Q.rear-Q.front+MAXQSIZE)%MAXQSIZE);
}
```

#### 循环队列的入队

```c++
Status EnQueue(SqQueue &Q,QElemType e){
    if((Q.rear+1)%MAXQSIZE==Q.front)
        return ERROR;  //队满
    Q.base[Q.rear]=e;  //新元素加入队尾
    Q.rear=(Q.rear+1)%MAXQSIZE;  //队尾指针+1
    return OK;
}
```

#### 循环队列的出队

```c++
Status DeQueue(SqQueue &Q,QElemType &e){
    if(Q.front==Q.rear)
        return ERROR;  //队空
    e=Q.base[Q.front];  //保存队头元素
    Q.front=(Q.front+1)%MAXQSIZE;  //队头指针+1
    return OK;
}
```

#### 取循环队列的队头元素

```c++
SElemType GetHead(SqQueue Q){
    if(Q.front!=Q.rear)  //队列不为空
        return Q.base[Q.front];  //返回队头指针元素的值，队头指针不变
}
```

### 队列的链式表示和实现

链式队列带有头结点，头指针Q.front指向头结点，尾指针Q.rear指向尾结点

#### 链式队列的类型定义

```c++
#define MAXQSIZE 100  //最大队列长度
typedef struct Qnode{
    QElemType data;
    struct Qnode *next;
}QNode,*QueuePtr;

typedef struct{
    QueuePtr front;  //队头指针
    QueuePtr rear;  //队尾指针
}LinkQueue;  //LinkQueue不是指针类型，引用成员用.号
```

#### 链式队列的初始化

```c++
Status InitQueue(LinkQueue &Q){
    Q.front=Q.rear=(QueuePtr)malloc(sizeof(QNode));  //Q.front=Q.rear=new QNode;
    if(!Q.front)
        exit(OVERFLOW);
    Q.front->next=NULL;
    return OK;
}
```

#### 销毁链式队列

```c++
Status DestroyQueue(LinkQueue &Q){
    while(Q.front){
        p=Q.front->next;
        free(Q.front);  //delete Q.front
        Q.front=p;
    }  //Q.rear=Q.front->next; free(Q.front); Q.front=Q.rear;
    return OK;
}
```

#### 链式队列的入队

```c++
Status EnQueue(LinkQueue &Q,QElemType e){
    p=(QueuePtr)malloc(sizeof(QNode));  //p=new QNode;
    if(!p) exit(OVERFLOW);
    p->data=e;
    p->next=NULL;
    Q.rear->next=p;
    Q.rear=p;
    return OK;
}
```

#### 链式队列的出队

```c++
Status DeQueue(LinkQueue &Q,QElemType &e){
    if(Q.front==Q.rear)
        return ERROR;
    p=Q.front->next;
    e=p->data;
    Q.front->next=p->next;
    if(Q.rear==p)
        Q.rear=Q.front;  //如果删除的正好是尾结点(头结点的下一结点就是尾结点时)，那么还需要修改尾指针指向头结点
    delete p;
    return OK;
}
```

#### 取链式队列的队头元素

```c++
Status GetHead(LinkQueue Q,QElemType &e){
    if(Q.front==Q.rear)
        return ERROR;
    e=Q.front->next->data;
    return OK;
}
```

