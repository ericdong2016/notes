## 1. 用途

- 缓存
- 持久存储

## 2. 用法

* 单机
* 单机 复制集群 Replication
* 分片 分布式集群 Partition

## 3. 数据类型

* string

  * 作为数值使用  decr、decrby、incr、incrby、incrbyfloat
  * **位图** bitop、bitcount、setbit等
  * users:status    b'0101010101011111111'
  * **分布式锁 setnx**-> set if not exists   'foo': 'bar' -> 1 0

* list

  * 构建消息队列

* set

  * 支持集合的交、差、并 运算，并且结果可以选择放到新的记录里

* sorted set  (zset)

  * **分数可以相同**
  * **分数支持incr 操作**
  * 如果分数全部为0，会按照字典序排序
  * 也支持集合的交、差、并 运算

* sort指令

  ![image-20190417192430307](/Users/delron/Library/Application Support/typora-user-images/image-20190417192430307.png)





原文地址：https://redis.io/topics/data-types

Strings类型：一个String类型的value最大可以存储**512M**

Lists类型：list的元素个数最多为2^32-1个，也就是4294967295个。

Sets类型：元素个数最多为2^32-1个，也就是4294967295个。

Hashes类型：键值对个数最多为2^32-1个，也就是4294967295个。

Sorted sets类型：跟Sets类型相似。



## 4. 事务 ACID

watch 'foo'

get 'foo'



multi

​	set

​	setex

​	hset

exec



单机支持 watch multi exec， redis cluster 不支持



## 5. Pipeline

pl = redis_client.pipeline()  # 流水线

pl.set()   A

pl.set()  B





pl.set()  A

pl.set()



pl.hset()

pl.execute()

* 在客户端统一收集指令
* 帮助补充上multi命令和exec命令





pl.set()   A

pl.set()  A



## 6. 有效期

expire foo 300

#### Redis的过期策略

过期策略通常有以下三种：

- 定时过期：每个设置过期时间的key都需要创建一个定时器，到过期时间就会立即清除。该策略可以立即清除过期的数据，对内存很友好；但是会占用大量的CPU资源去处理过期的数据，从而影响缓存的响应时间和吞吐量。

  ```python
  setex('a', 300, 'aval')
  setex('b', 600, 'bval')
  ```

  

- 惰性过期：只有当访问一个key时，才会判断该key是否已过期，过期则清除。该策略可以最大化地节省CPU资源，却对内存非常不友好。极端情况可能出现大量的过期key没有再次被访问，从而不会被清除，占用大量内存。

```python
get('a')
```



- 定期过期：每隔一定的时间，会扫描一定数量的数据库的expires字典中一定数量的key，并清除其中已过期的key。该策略是前两者的一个折中方案。通过调整定时扫描的时间间隔和每次扫描的限定耗时，可以在不同情况下使得CPU和内存资源达到最优的平衡效果。

- 

  (expires字典会保存所有设置了过期时间的key的过期时间数据，其中，key是指向键空间中的某个键的指针，value是该键的毫秒精度的UNIX时间戳表示的过期时间。键空间是指该Redis集群中保存的所有键。)

**Redis中同时使用了惰性过期和定期过期两种过期策略。**

Redis过期删除采用的是定期删除，默认是每100ms检测一次，遇到过期的key则进行删除，这里的检测并不是顺序检测，而是随机检测。那这样会不会有漏网之鱼？显然Redis也考虑到了这一点，当我们去读/写一个已经过期的key时，会触发Redis的惰性删除策略，直接回干掉过期的key

**为什么不用定时删除策略?**

定时删除,用一个定时器来负责监视key,过期则自动删除。虽然内存及时释放，但是十分消耗CPU资源。在大并发请求下，CPU要将时间应用在处理请求，而不是删除key,因此没有采用这一策略.

**定期删除+惰性删除是如何工作的呢?**

定期删除，redis默认每个100ms检查，是否有过期的key,有过期key则删除。需要说明的是，redis不是每个100ms将所有的key检查一次，而是随机抽取进行检查(如果每隔100ms,全部key进行检查，redis岂不是卡死)。因此，如果只采用定期删除策略，会导致很多key到时间没有删除。

于是，惰性删除派上用场。也就是说在你获取某个key的时候，redis会检查一下，这个key如果设置了过期时间那么是否过期了？如果过期了此时就会删除。

采用定期删除+惰性删除就没其他问题了么?

不是的，如果定期删除没删除key。然后你也没即时去请求key，也就是说惰性删除也没生效。这样，redis的内存会越来越高。那么就应该采用内存淘汰机制。

## 7. 缓存淘汰

Redis自身实现了缓存淘汰



LRU  LFU  页面缓存淘汰

Least Recently Use  时间

[a, b, c, d, e, f,  g]   h

[a, b, c, d, e, f,  h]   

[d, h, a, b, c, , e, k]   k



LFU

Least  Frequency Use  频率  记录使用此时

[(a, 10000), (b, 9900), (c, 8000) ]  d

[(a, 10000), (b, 9900), (d, 1) ]  e   定期衰减

[(a, 5000), (b, 4995),]



Redis的内存淘汰策略是指在Redis的用于缓存的内存不足时，怎么处理需要新写入且需要申请额外空间的数据。

- noeviction：当内存不足以容纳新写入数据时，新写入操作会报错。
- allkeys-lru：当内存不足以容纳新写入数据时，在键空间中，移除最近最少使用的key。
- allkeys-random：当内存不足以容纳新写入数据时，在键空间中，随机移除某个key。
- **volatile-lru：当内存不足以容纳新写入数据时，在设置了过期时间的键空间中，移除最近最少使用的key。**
- volatile-random：当内存不足以容纳新写入数据时，在设置了过期时间的键空间中，随机移除某个key。
- volatile-ttl：当内存不足以容纳新写入数据时，在设置了过期时间的键空间中，有更早过期时间的key优先移除。

#### redis 4.x 后支持LFU策略，最少频率使用

allkeys-lfu

volatile-lfu



maxmemory <bytes>

maxmemory-policy noeviction

**面试题：mySQL里有2000w数据，redis中只存20w的数据，如何保证redis中的数据都是热点数据**

**maxmemory   268435456 bytes /256m**

**maxmemory-policy volatile-lru**



## 8. Redis 持久化

* RDB 快照持久化      dump.db
  * 定期触发    
  * BGSAVE
  * SHUTDOWN
  * 创建子进程执行  停顿时长
* AOF 追加文件
  * 文件体积增大

## 9. Redis复制集

* 只能一主 多从     

  ```
                  master  127.0.0.1:8360
                     |
            slave1   maseter   slave2  127.0.0.1:8361
               |
          slave3  slave 4
            
              
  ```

  

* slaveof
* info Replication

## 10. Sentinel 哨兵  高可用 HA

- **Monitoring**. Sentinel constantly checks if your master and slave instances are working as expected.
- **Notification**. Sentinel can notify the system administrator, another computer programs, via an API, that something is wrong with one of the monitored Redis instances.
- **Automatic failover**. If a master is not working as expected, Sentinel can start a failover process where a slave is promoted to master, the other additional slaves are reconfigured to use the new master, and the applications using the Redis server informed about the new address to use when connecting.
- **Configuration provider**. Sentinel acts as a source of authority for clients service discovery: clients connect to Sentinels in order to ask for the address of the current Redis master responsible for a given service. If a failover occurs, Sentinels will report the new address

* 看管redis主从，进行故障转移 failover  高可用
* 至少三个以上 ，决定master是否宕机



redis 6380 6381 6382

sentienl  26380 26381 ..

<https://redis.io/topics/sentinel>

## 11. Redis集群

<https://redis.io/topics/partitioning>

* Redis Cluster   不支持事务 不支持mset('a', 'b', 'c')
* Twemproxy
* codis

相关补充阅读

* <https://redis.io/documentation>
* 《Redis实践》 （Redis in action)

## 12. Redis python使用的注意

python 操作redis的库

```python
redis-py 单机
* 2.10.6

* 3.*

redis-cluster-py   集群
依赖redis-py 2.10.6版本
```

- redis-py 2.10.6

  - zset

    ```python
    zadd(key, *args, **kwargs)
    
    val1 = 'python', score1=100
    val2 = 'cpp', score2=99
    
    zadd(key, score1, val1, score2, val2)
    zadd(key, python=100, cpp=99)
    ```

    

  - Redis

    - 指令的参数顺序未严格按照redis官方指令

    - ```
      setex(self, name, value，time)
      ```

  - StrictRedis

    - 指令的参数顺序严格按照redis官方指令

    - ```
      setex(self, name, time, value)
      ```

- redis-py 3.x

  - 只提供Redis  Redis=StrictRedis

  - zset

  - ```python
    zadd(key, kwargs)
    
    val1 = 'python', score1=100
    val2 = 'cpp', score2=99
    
    zadd(key, {'python':100, 'cpp':99})
    ```

    redis-cluster-py



