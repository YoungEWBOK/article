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





## **栈与递归**







## **队列的表示和操作的实现**

