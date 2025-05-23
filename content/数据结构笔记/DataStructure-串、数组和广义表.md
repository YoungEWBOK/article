---
title: 数据结构笔记③——串、数组和广义表
date: '2024-03-03'
summary: 代码来自B站视频：数据结构与算法基础（青岛大学-王卓）
tags:
  - 笔记
  - 数据结构
share: false
---

# 串、数组和广义表

## **串**

### 串的定义

零个或多个任意**字符组成的有限序列**

- **子串:** 串中任意个连续字符组成的子序列称为该串的子串
  - **真子串**是指不包含自身的所有子串
- **主串:** 包含子串的串相应地称为主串
- **字符位置:** 字符在**序列中的序号**为该字符在串中的位置
- **子串位置:** 子串**第一个字符**在主串中的位置
- **空格串:** 由一个或多个空格组成的串，**与空串不同**
- **串相等:** 两串长度相等并且各个对应位置上的字符都相同
  - 所有空串是相等的

### 串的类型定义、存储结构及运算

```
ADT String{
	数据对象:
    	D={ai|ai∈CharacterSet, i=1,2,···,n,n≥0}
    数据关系:
        R1={<ai-1,ai>|ai-1,ai∈D, i=2,···,n}
    基本操作:串赋值、串比较、求串长、串连结、查找子串的位置(字符串的匹配)等
}ADT String
```

串中元素逻辑关系与线性表的相同，串可以采用与线性表相同的存储结构

- 顺序存储结构：**顺序串**
- 链式存储结构：**链串**

#### 串的顺序存储结构

```c++
#define MAXLEN 255
typedef struct{
    char ch[MAXLEN+1];  //存储串的一维数组，下标从1号位置开始，0号位置闲置不用
    int length;  //串的当前长度
}SString;
```

#### 串的链式存储结构

**块链结构:** 可将多个字符存放在一个结点中，以克服其**存储密度较低**的缺点

```c++
#define CHUNKSIZE 80  //块的大小可由用户定义
typedef struct Chunk{
    char ch[CHUNKSIZE];
    struct Chunk *next;
}Chunk;

typedef struct{
    Chunk *head,*tail;  //串的头指针和尾指针
    int curlen;  //串的当前长度
}LString;  //字符串的块链结构
```

#### 串的模式匹配算法

**算法目的:** 确定主串中所含子串(模式串)第一次出现的位置(定位)

**算法种类:**

- BF算法（Brute-Force，又称古典的、经典的、朴素的、穷举的）
- KMP算法（特点：速度快）

##### BF算法

Brute-Force简称为BF算法，亦称简单匹配算法，采用穷举法的思路

算法思路：从S的每一个字符开始依次与T的字符进行匹配

匹配失败：

- i 回溯：i = i - j + 2，S当前位置是 i，移动长度是 j-1，当前位置 - 移动长度 + 1 = 下一次比较的起始位置
- j = 1（从头开始）

匹配成功：返回 i - t.length

```c++
int Index_BF(SString S,SString T){  //如果对开始查找的位置有要求，可增加参数int pos，将i初始化时赋值pos
    int i=1,j=1;
    while(i<=S.length&&j<=T.length){
        if(S.ch[i]==T.ch[j]){++i;++j;}  //主串和子串依次匹配下一个字符
        else {i=i-j+2;j=1;}  //主串、子串指针回溯重新开始下一次匹配
    }
    if(j>T.length) return i-T.length;  //返回匹配的第一个字符的下标
    else return 0;  //模式匹配不成功
}
```

时间复杂度：若n为主串长度，m为子串长度，最坏情况是

- 主串前面n-m个位置都部分匹配到子串的最后一位，即这n-m位各比较了m次
- 最后m位也各比较了1次

总次数为：(n-m)×m+m=(n-m+1)×m，若m<<n，则算法复杂度为O(n*m)（最坏情况和平均情况）

##### KMP算法

利用已经**部分匹配**的结果而加快模式串的滑动速度，且主串S的指针 i 不必回溯，可提速到O(n+m)

为此，定义next[j]函数，表明当模式中第 j 个字符与主串中相应字符"失配"时，在模式中需重新和主串中该字符进行比较的字符的位置

**next[j]=**

- max{k|1<k<j，且"p(1)···p(k-1)"="p(j-k+1)···p(j-1)"} **(从头开始的 k-1 个元素 = j 前面的 k-1 个元素，前缀=后缀)** 当此集合非空时
  - 前缀是向右移动，后缀是向左移动，因此即使当前不匹配仍然需要加长元素个数再次判断，属于此情况的值至少为2(因为k-1=1)
- 0    当 j=1 时
- 1    其他情况

```c++
int Index_KMP(SString S,SString T,int pos){
    i=pos,j=1;
    while(i<S.length&&j<T.length){
        if(j==0||S.ch[i]==T.ch[j]){i++;j++;}
        else
            j=next[j];  //i不变，j后退
    }
    if(j>T.length) return i-T.length;  //匹配成功
    else return 0;  //返回不匹配标志
}

void get_next(SString T,int &next[]){
    i=1;next[1]=0;j=0;
    while(i<T.length){
        if(j==0||T.ch[i]==T.ch[j]){
            ++i;++j;
            next[i]=j;
        }
        else
            j=next[j];
    }
}
/* 关于 j=next[j];这句：如果j被赋值为0(表明i在当前位置时，模式串先前的所有位置都无法与之匹配(即使从头开始也不匹配)，需要从下一个位置开始)，则会进入第15行的if语句内，让i++、j++，即j保持1不动，i向后移位一个元素，接下来模式串从头开始、主串从下一位置开始，再进行比较 */
```

**next函数的改进**

![](next.png)

![](nextval.png)

**大概理解(待确认):** j 位置和其next值对应的下标 i 位置进行字符的比较，字符相同则 j 位置nextval的值=下标 i 位置的next的值，不相同则 j 位置nextval的值=自身的next的值

```c++
void get_nextval(SString T,int &nextval[]){
    i=1;nextval[1]=0;j=0;
    while(i<T.length){
        if(j==0||T.ch[i]==T.ch[j]){
            ++i;++j;
            if(T.ch[i]!=T.ch[j])
                nextval[i]=j;
            else
                nextval[i]=nextval[j];
        }
        else
            j=nextval[j];
    }
}
```



## **数组**

## **广义表**



