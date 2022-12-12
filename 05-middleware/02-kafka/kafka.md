


## 1. 基本概念及特性

**概念：**

```
Kafka最初是由LinkedIn公司采用Scala语言开发的一个多分区、多副本并且基于ZooKeeper协调的分布
式消息系统。目前Kafka已经定位为一个分布式流式处理平台，它以高吞吐、可持久化、可水平扩展、支持流处理等多种特性而被广泛应用。

Apache Kafka是一个分布式的发布-订阅消息系统，能够支撑海量数据的数据传递。在离线和实时的消
息处理业务系统中，Kafka都有广泛的应用。Kafka将消息持久化到磁盘中，并对消息创建了备份保证了
数据的安全。Kafka在保证了较高的处理速度的同时，又能保证数据处理的低延迟和数据的零丢失
```

**特性：**

```
（1）高吞吐量、低延迟：kafka每秒可以处理几十万条消息，它的延迟最低只有几毫秒，每个主题可以
分多个分区, 消费组对分区进行消费操作；
（2）可扩展性：kafka集群支持热扩展；
	1、Kafka 集群在运行期间可以轻松地扩展或收缩（可以添加或删除代理），而不会宕机。
    2、可以扩展一个 Kafka 主题来包含更多的分区。由于一个分区无法扩展到多个代理，所以它的容量受
    到代理磁盘空间的限制。能够增加分区和代理的数量意味着单个主题可以存储的数据量是没有限制的
（3）持久性、可靠性：消息被持久化到本地磁盘，并且支持数据备份防止数据丢失；
（4）容错性：允许集群中节点失败（若副本数量为n,则允许n-1个节点失败）；
（5）高并发：支持数千个客户端同时读写
```

## 2. 适用场景

```
（1）日志收集：一个公司可以用Kafka可以收集各种服务的log，通过kafka以统一接口服务的方式开放
给各种consumer，例如Hadoop、Hbase、Solr等；
（2）消息系统：解耦和生产者和消费者、缓存消息等；
（3）用户活动跟踪：Kafka经常被用来记录web用户或者app用户的各种活动，如浏览网页、搜索、点
击等活动，这些活动信息被各个服务器发布到kafka的topic中，然后订阅者通过订阅这些topic来做实时
的监控分析，或者装载到Hadoop、数据仓库中做离线分析和挖掘；
（4）运营指标：Kafka也经常用来记录运营监控数据。包括收集各种分布式应用的数据，生产各种操作
的集中反馈，比如报警和报告；
（5）流式处理：比如spark streaming和storm；
```

## 3. 常用术语

![](1-kafka架构图.png)

```
Producer
生产者即数据的发布者，该角色将消息发布到Kafka的topic中。broker接收到生产者发送的消息后，
broker将该消息追加到当前用于追加数据的segment文件中。生产者发送的消息，存储到一个partition
中，生产者也可以指定数据存储的partition。

Consumer
消费者可以从broker中读取数据。消费者可以消费多个topic中的数据。

Topic
在Kafka中，使用一个类别属性来划分数据的所属类，划分数据的这个类称为topic。如果把Kafka看做
为一个数据库，topic可以理解为数据库中的一张表，topic的名字即为表名。

Partition
topic中的数据分割为一个或多个partition。每个topic至少有一个partition。每个partition中的数据使
用多个segment文件存储。partition中的数据是有序的，partition间的数据丢失了数据的顺序。如果
topic有多个partition，消费数据时就不能保证数据的顺序。在需要严格保证消息的消费顺序的场景下，
需要将partition数目设为1。

Partition offset
每条消息都有一个当前Partition下唯一的64字节的offset，它指明了这条消息的起始位置。

Replicas of partition
副本是一个分区的备份。副本不会被消费者消费，副本只用于防止数据丢失，即消费者不从为follower
的partition中消费数据，而是从为leader的partition中读取数据。副本之间是一主多从的关系。

Broker
Kafka 集群包含一个或多个服务器，服务器节点称为broker。broker存储topic的数据。如果某topic有
N个partition，集群有N个broker，那么每个broker存储该topic的一个partition。如果某topic有N个
partition，集群有(N+M)个broker，那么其中有N个broker存储该topic的一个partition，剩下的M个
broker不存储该topic的partition数据。如果某topic有N个partition，集群中broker数目少于N个，那么
一个broker存储该topic的一个或多个partition。在实际生产环境中，尽量避免这种情况的发生，这种
情况容易导致Kafka集群数据不均衡。

leader


Follower
Follower跟随Leader，所有写请求都通过Leader路由，数据变更会广播给所有Follower，Follower与
Leader保持数据同步。如果Leader失效，则从Follower中选举出一个新的Leader。当Follower与
Leader挂掉、卡住或者同步太慢，leader会把这个follower从“in sync replicas”（ISR）列表中删除，重
新创建一个Follower。

Zookeeper
Zookeeper负责维护和协调broker。当Kafka系统中新增了broker或者某个broker发生故障失效时，由
ZooKeeper通知生产者和消费者。生产者和消费者依据Zookeeper的broker状态信息与broker协调数据
的发布和订阅任务。

AR(Assigned Replicas)
分区中所有的副本统称为AR。

ISR(In-Sync Replicas)
所有与Leader部分保持一定程度的副（包括Leader副本在内）本组成ISR。

OSR(Out-of-Sync-Replicas)
与Leader副本同步滞后过多的副本。


HW(High Watermark)
高水位，标识了一个特定的offset，消费者只能拉取到这个offset之前的消息。

LEO(Log End Offset)
即日志末端位移(log end offset)，记录了该副本底层日志(log)中下一条消息的位移值。注意是下一条消
息！也就是说，如果LEO=10，那么表示该副本保存了10条消息，位移值范围是[0, 9]。

```

![](2-leo.png)

## 4. 安装及配置

```
1. 下载jdk, 解压放到指定目录，配置环境变量
/etc/profile

export JAVA_HOME=/java/jdk-12.0.1
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib:$CLASSPATH
export PATH=.:$JAVA_HOME/bin:$JRE_HOME/bin:$KE_HOME/bin:${MAVEN_HOME}/bin:$PATH

java -version

2. 下载zookeeper, 解压放到指定目录
Zookeeper是安装Kafka集群的必要组件，Kafka通过Zookeeper来实施对元数据信息的管理，包括集
群、主题、分区等内容

修改 Zookeeper的配置文件，首先进入安装路径conf目录，并将zoo_sample.cfg文件修改为
zoo.cfg，并对核心参数进行配置
vim zoo.cfg
# The number of milliseconds of each tick
# zk服务器的心跳时间
tickTime=2000
# The number of ticks that the initial
# synchronization phase can take
# 投票选举新Leader的初始化时间
initLimit=10
# The number of ticks that can pass between
# sending a request and getting an acknowledgement
# do not use /tmp for storage, /tmp here is just
# example sakes.
# 数据目录
dataDir=temp/zookeeper/data
# 日志目录
dataLogDir=temp/zookeeper/log
# the port at which the clients will connect
# Zookeeper对外服务端口，保持默认
clientPort=2181

启动 Zookeeper命令：
bin/zkServer.sh start

3. Kafka的安装与配置
官网下载安装解压缩： http://kafka.apache.org/downloads
下载解压启动:       bin/kafka-server-start.sh config/server.properties

server.properties配置中需要关注以下几个参数：
broker.id=0 表示broker的编号，如果集群中有多个broker，则每个broker的编号需要设置
的不同
listeners=PLAINTEXT://:9092         brokder对外提供的服务入口地址
log.dirs=/tmp/kafka/log             设置存放消息日志文件的地址
zookeeper.connect=localhost:2181    Kafka所需Zookeeper集群地址


4. 测试
首先创建一个主题
bin/kafka-topics.sh --zookeeper zookeeper:2181 --create --topic heima --partitions 2 --replication-factor 1

展示所有主题
bin/kafka-topics.sh --zookeeper zookeeper:2181 --list

查看主题详情（--describe 查看详情动作指令）
bin/kafka-topics.sh --zookeeper zookeeper:2181 --describe --topic heima

启动一个消费者
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic heima

生产端发送消息
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic heima

查看groupId
bin/kafka-consumer-groups.sh --zookeeper zookeeper:2181 --group console-consumer-64116 --describe

查看消费
bin/kafka-consumer-groups.sh --zookeeper zookeeper:2181 --list

查看消费组信息
kafka-consumer-group.sh  xxx --describe --group xxx
 
current_offset: 最后被消费的消息的偏移量
leo: 消息总量， 最后一条消息的偏移量
lag: 积压了多少消息
```

## 5. 第一个kafka程序

> https://github.com/Shopify/sarama/blob/v1.33.0/README.md
>
> https://github.com/segmentio/kafka-go/blob/main/addoffsetstotxn.go
>
> https://github.com/zeromicro/go-queue
>
> https://github.com/yireyun/go-queue

```
// 创建生产者
// Kafka集群地址
 private static final String brokerList = "localhost:9092";
 // 主题名称-之前已经创建
 private static final String topic = "heima";
 public static void main(String[] args) {
   Properties properties = new Properties();
   // 设置key序列化器
   properties.put("key.serializer",
"org.apache.kafka.common.serialization.StringSerializer");
   //另外一种写法
   //properties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG,
StringSerializer.class.getName());
   // 设置重试次数
   properties.put(ProducerConfig.RETRIES_CONFIG, 10);
   // 设置值序列化器
   properties.put("value.serializer",
"org.apache.kafka.common.serialization.StringSerializer");
   // 设置集群地址
   properties.put("bootstrap.servers", brokerList);
   // KafkaProducer 线程安全
   KafkaProducer<String, String> producer = new KafkaProducer<>
(properties);
   ProducerRecord<String, String> record = new ProducerRecord<>(topic,
"Kafka-demo-001", "hello, Kafka!");
   try {
     producer.send(record);
   } catch (Exception e) {
     e.printStackTrace();
   }
   producer.close();
 }
```

```
// 创建消费者
public class ConsumerFastStart {
 // Kafka集群地址
 private static final String brokerList = "127.0.0.1:9092";
 // 主题名称-之前已经创建
 private static final String topic = "heima";
 // 消费组
 private static final String groupId = "group.demo";
 public static void main(String[] args) {
   Properties properties = new Properties();
   properties.put("key.deserializer",
       "org.apache.kafka.common.serialization.StringDeserializer");
   properties.put("bootstrap.servers", brokerList);
   properties.put("group.id", groupId);
   
   KafkaConsumer<String, String> consumer = new KafkaConsumer<>
(properties);
   consumer.subscribe(Collections.singletonList(topic));
   while (true) {
     ConsumerRecords<String, String> records =
         consumer.poll(Duration.ofMillis(1000));
     for (ConsumerRecord<String, String> record : records) {
       System.out.println(record.value());
     }
   }
 }
}
```

```
// 注意： 使用java连接linux下kafka集群需要设置hosts绑定；
// 启动  
先启动消费者，后启动生产者

```

## 6. 服务端常用配置

```
egrep 'zookeeper|listeners|broker.id|log.dir|log.dirs' config/server.properties

broker.id=0
listeners=PLAINTEXT://0.0.0.0:9092
#advertised.listeners=PLAINTEXT://your.host.name:9092
log.dirs=/tmp/kafka/log
zookeeper.connect=zookeeper:2181
zookeeper.connection.timeout.ms=6000



zookeeper.connect
指明Zookeeper主机地址，如果zookeeper是集群则以逗号隔开，如：
172.6.14.61:2181,172.6.14.62:2181,172.6.14.63:2181

listeners
监听列表，broker对外提供服务时绑定的IP和端口。多个以逗号隔开，如果监听器名称不是一个安全的
协议， listener.security.protocol.map也必须设置。主机名称设置0.0.0.0绑定所有的接口，主机名称为
空则绑定默认的接口。如：
PLAINTEXT://myhost:9092
SSL://:9091
CLIENT://0.0.0.0:9092
REPLICATION://localhost:9093

broker.id
broker的唯一标识符，如果不配置则自动生成，建议配置且一定要保证集群中必须唯一，默认-1

log.dirs
日志数据存放的目录，如果没有配置则使用log.dir，建议此项配置。

message.max.bytes
服务器接受单个消息的最大大小，默认1000012 约等于976.6KB。
```



## 7. 生产者

> 官网的example 和 mock 中代码

### 1. 发送类型

```
  发送即忘记
  	RequiredAcks: kafka.RequireNone,
  同步发送
  	  &kafka.Writer{
            // 有很多的配置
            Addr:     kafka.TCP(kafkaURL),
            Topic:    topic,
            Balancer: &kafka.LeastBytes{},
        }
  异步发送
  
      &kafka.Writer{
            // 有很多的配置
            Addr:     kafka.TCP(kafkaURL),
            Topic:    topic,
            //		RequiredAcks: kafka.RequireAll,
            //		Async:        true, // make the writer asynchronous
            //		Completion: func(messages []kafka.Message, err error) {
            //			...
            //		},
        }
```



### 2. 分区器

```
随机partitioner
手动partitioner
自定义
hash
自定义hash
```



### 3. 拦截器

```
使用场景
    1、按照某个规则过滤掉不符合要求的消息
    2、修改消息的内容
    3、统计类需求
    
type ProducerInterceptor interface {
	// OnSend is called when the producer message is intercepted. Please avoid
	// modifying the message until it's safe to do so, as this is _not_ a copy
	// of the message.
	OnSend(*ProducerMessage)
}
```

### 4. 发送流程 （java）

```
消息发送的过程中，涉及到两个线程协同工作，主线程首先将业务数据封装成 ProducerRecord对象，
之后调用send()方法将消息放入RecordAccumulator(消息收集器，也可以理解为主线程与Sender线程
直接的缓冲区)中暂存，Sender线程负责将消息信息构成请求，并最终执行网络I/O的线程，它从
RecordAccumulator中取出消息并批量发送出去，需要注意的是，KafkaProducer是线程安全的，多个
线程间可以共享使用同一个KafkaProducer对象
```

### 5. 代码

> 默认，往哪个partion 里发送是 通过Key 算出来的； 也可通过指定来往某个分区上发送
>
> 同步发消息，生产者发送消息 没有收到ack , 生产者会阻塞，阻塞到3s, 如果还没有收到消息，会进行重试，重试3次
>
> 异步发消息： 会有回调

```
package main

import (
	"fmt"
	"github.com/Shopify/sarama"
)

// go连接Kafka报错kafka: client has run out of available brokers to talk to
// 1. 连接信息
//  listeners=PLAINTEXT://:9099
// advertised.listeners=PLAINTEXT://175.24.115.7:9099
// 2. Kafka 版本问题

func main() {
	config := sarama.NewConfig()
	// 应答
	/*
		c.Producer.MaxMessageBytes = 1000000
		c.Producer.RequiredAcks = WaitForLocal
		c.Producer.Timeout = 10 * time.Second
		c.Producer.Partitioner = NewHashPartitioner
		c.Producer.Retry.Max = 3
		c.Producer.Retry.Backoff = 100 * time.Millisecond
		c.Producer.Return.Errors = true
		c.Producer.CompressionLevel = CompressionLevelDefault

	*/
	config.Producer.RequiredAcks = sarama.WaitForAll // 发送完数据需要leader和follow都确认
	// 分区 有很多分区可以选
	config.Producer.Partitioner = sarama.NewRandomPartitioner // 新选出一个partition
	config.Producer.Return.Successes = true                   // 成功交付的消息将在success channel返回

	// addr
	addr := []string{"192.168.19.160:9092"}
	// 连接kafka, 发送类型为同步， 还有异步， client
	client, err := sarama.NewSyncProducer(addr, config)
	if err != nil {
		fmt.Println("producer closed, err:", err)
		return
	}
	defer client.Close()
	// 构造一个消息(序列化)
	/*
		topic
		key
		value
		offset
		Partition
		retries
		flag
	*/
	msg := &sarama.ProducerMessage{}
	msg.Topic = "web_log"
	msg.Value = sarama.StringEncoder("this is a test log")
	// 发送消息
	pid, offset, err := client.SendMessage(msg)
	if err != nil {
		fmt.Println("send msg failed, err:", err)
		return
	}
	fmt.Printf("pid:%v offset:%v\n", pid, offset)
}

```

### 6. 一些配置参数

```
c.Producer.MaxMessageBytes = 1000000
c.Producer.RequiredAcks = WaitForLocal
c.Producer.Timeout = 10 * time.Second
c.Producer.Partitioner = NewHashPartitioner
c.Producer.Retry.Max = 3
c.Producer.Retry.Backoff = 100 * time.Millisecond
c.Producer.Return.Errors = true
c.Producer.CompressionLevel = CompressionLevelDefault

1. acks
这个参数用来指定分区中必须有多少个副本收到这条消息，之后生产者才会认为这条消息时写入成功
的。acks是生产者客户端中非常重要的一个参数，它涉及到消息的可靠性和吞吐量之间的权衡。
ack=0 ， 生产者在成功写入消息之前不会等待任何来自服务器的相应。如果出现问题生产者是感知
不到的，消息就丢失了。不过因为生产者不需要等待服务器响应，所以它可以以网络能够支持的最
大速度发送消息，从而达到很高的吞吐量。
ack=1 ，默认值为1，只要集群的首领节点收到消息，生产这就会收到一个来自服务器的成功响
应。如果消息无法达到首领节点（比如首领节点崩溃，新的首领还没有被选举出来），生产者会收
到一个错误响应，为了避免数据丢失，生产者会重发消息。但是，这样还有可能会导致数据丢失，
如果收到写成功通知，此时首领节点还没来的及同步数据到follower节点，首领节点崩溃，就会导
致数据丢失。
ack=-1 ， 只有当所有参与复制的节点都收到消息时，生产这会收到一个来自服务器的成功响应，
这种模式是最安全的，它可以保证不止一个服务器收到消息。


2.retries
生产者从服务器收到的错误有可能是临时性的错误（比如分区找不到首领）。在这种情况下，如果达到
了 retires 设置的次数，生产者会放弃重试并返回错误。默认情况下，生产者会在每次重试之间等待
100ms，可以通过 retry.backoff.ms 参数来修改这个时间间隔。

3.batch.size(go kafka 里面暂时没有看到相关设置 )
当有多个消息要被发送到同一个分区时，生产者会把它们放在同一个批次里。该参数指定了一个批次可
以使用的内存大小，按照字节数计算，而不是消息个数。当批次被填满，批次里的所有消息会被发送出
去。不过生产者并不一定都会等到批次被填满才发送，半满的批次，甚至只包含一个消息的批次也可能
被发送。所以就算把 batch.size 设置的很大，也不会造成延迟，只会占用更多的内存而已，如果设置
的太小，生产者会因为频繁发送消息而增加一些额外的开销。

4.max.request.size
该参数用于控制生产者发送的请求大小，它可以指定能发送的单个消息的最大值，也可以指单个请求里
所有消息的总大小。 broker 对可接收的消息最大值也有自己的限制（ message.max.size ），所以两
边的配置最好匹配，避免生产者发送的消息被 broker 拒绝。


缓冲区机制
	先往缓冲区中写，写满16k, 发送，如果到了10s, 还是没满，也会发送
	buffer_memory_config
	batch_size_config
	linger_ms_config
```



## 8. 消费者

### 1.  消费者和消费组

```
Kafka消费者是消费组的一部分，当多个消费者形成一个消费组来消费主题时，每个消费者会收到不同
分区的消息。假设有一个T1主题，该主题有4个分区；同时我们有一个消费组G1，这个消费组只有一个
消费者C1。那么消费者C1将会收到这4个分区的消息

Kafka 一个很重要的特性就是，只需写入一次消息，可以支持任意多的应用读取这个消息。换句话说，
每个应用都可以读到全量的消息。为了使得每个应用都能读到全量消息，应用需要有不同的消费组。对
于上面的例子，假如我们新增了一个新的消费组G2，而这个消费组有两个消费者
```

### 2. 参数设置

```
c.Consumer.Fetch.Min = 1
c.Consumer.Fetch.Default = 1024 * 1024
c.Consumer.Fetch.Max = 1024 * 1024

c.Consumer.MaxWaitTime = 500 * time.Millisecond
c.Consumer.MaxProcessingTime = 100 * time.Millisecond

c.Consumer.Retry.Backoff = 2 * time.Second

c.Consumer.Return.Errors = false
c.Consumer.Offsets.AutoCommit.Enable = true
c.Consumer.Offsets.AutoCommit.Interval = 1 * time.Second
c.Consumer.Offsets.Initial = OffsetNewest
c.Consumer.Offsets.Retry.Max = 3

c.Consumer.Group.Session.Timeout = 10 * time.Second
c.Consumer.Group.Heartbeat.Interval = 3 * time.Second
c.Consumer.Group.Rebalance.Strategy = BalanceStrategyRange
c.Consumer.Group.Rebalance.Timeout = 60 * time.Second
c.Consumer.Group.Rebalance.Retry.Max = 4
c.Consumer.Group.Rebalance.Retry.Backoff = 2 * time.Second

c.ClientID = defaultClientID

在go中没看到设置
```

### 3. 订阅主题

```
1. 精准
2. 正则表达式
3. 指定订阅的分区   指定分区消费

Partitions(topic string) ([]int32, error)
// 指定分区消费
ConsumePartition(topic string, partition int32, offset int64) (PartitionConsumer, error)


kafka.NewReader(kafka.ReaderConfig{
		Brokers:  brokers,
		GroupID:  groupID,
		Topic:    topic,
		MinBytes: 10e3, // 10KB
		MaxBytes: 10e6, // 10MB
	})
```

### 4. 消费提交(***)

```
对于Kafka中的分区而言，它的每条消息都有唯一的offset，用来表示消息在分区中的位置。
当我们调用poll()时，该方法会返回我们没有消费的消息。当消息从broker返回消费者时，broker并不
跟踪这些消息是否被消费者接收到；Kafka让消费者自身来管理消费的位移，并向消费者提供更新位移
的接口，这种更新位移方式称为提交（commit）

重复消费

消息丢失

自动提交   poll 后直接commit 
    这种方式让消费者来管理位移，应用本身不需要显式操作。当我们将enable.auto.commit设置为true，
    那么消费者会在poll方法调用后每隔5秒（由auto.commit.interval.ms指定）自动提交一次位移。和很多其
    他操作一样，自动提交也是由poll()方法来驱动的；在调用poll()时，消费者判断是否到达提交时间，如
    果是则提交上一次poll返回的最大位移。
    
    需要注意到，这种方式可能会导致消息重复消费。假如，某个消费者poll消息后，应用正在处理消息，
    在3秒后Kafka进行了重平衡，那么由于没有更新位移导致重平衡后这部分消息重复消费；或者导致消费丢失，在commit后，消费者没有消费，挂了，新的消费者会从新的偏移量开始消费，导致前面的消费丢失。
    
    c.Consumer.Offsets.AutoCommit.Enable = true
    
同步提交(手动提交)
	消费消息后  commit
	// 手动提交有一个缺点，那就是当发起提交调用时应用会阻塞。当然我们可以减少手动提交的频率，但这
个会增加重复消息的概率（和自动提交一样）

	props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
	c.Consumer.Offsets.Initial = OffsetNewest
    // 手动提交开启
    c.Consumer.Offsets.AutoCommit.Enable = false
    
   /* java
       while (true) {
         ConsumerRecords<String, String> records = consumer.poll(1000);
         if (records.isEmpty()) {
           break;
         }
         List<ConsumerRecord<String, String>> partitionRecords = records.records(tp);
         lastConsumedOffset = partitionRecords.get(partitionRecords.size() -1).offset();
         consumer.commitSync();  // 同步提交消费位移
       }
   */
   
   

异步提交(手动提交)  消息重复消费
	消费消息后  commmit
	
	手动提交有一个缺点，那就是当发起提交调用时应用会阻塞。当然我们可以减少手动提交的频率，但这
个会增加消息重复的概率（和自动提交一样）。另外一个解决办法是，使用异步提交的API。
	但是异步提交也有个缺点，那就是如果服务器返回提交失败，异步提交不会进行重试。相比较起来，同
步提交会进行重试直到成功或者最后抛出异常给应用。异步提交没有实现重试是因为，如果同时存在多
个异步提交，进行重试可能会导致位移覆盖。举个例子，假如我们发起了一个异步提交commitA，此时
的提交位移为2000，随后又发起了一个异步提交commitB且位移为3000；commitA提交失败但
commitB提交成功，此时commitA进行重试并成功的话，会将实际上将已经提交的位移从3000回滚到
2000，导致消息重复消费。

	try {
     while (running.get()) {
       ConsumerRecords<String, String> records = consumer.poll(1000);
       for (ConsumerRecord<String, String> record : records) {
         //do some logical processing.
       }
       // 异步回调
       consumer.commitAsync(new OffsetCommitCallback() {
         @Override
         public void onComplete(Map<TopicPartition, OffsetAndMetadata> offsets,
         
         } else {
             log.error("fail to commit offsets {}", offsets, exception);
           }
         }
       });
     }
   } finally {
     consumer.close();
   }
   
   

poll消息细节：
max_poll_records_config 500
1. 当设定的容量未到，指定时间到了， 一次poll结束，无论拉取多少条,  中间可以多次Poll
2. 当设定的容量到了，去拉取
3. 如果两次poll 时间超过30s,  kafka会认为消费能力过弱，将其提出，max_poll_interval_ms_config 
	rebalance
	
消费者的健康检查：
消费者每隔1s向kafka集群发送心跳，集群发现如果有操作10s续约的消费者，将被提出消费组，触发该消费组的rebalance.

heatbeat_interval_ms_config 
session_timeout_ms_config 
```

### 5. 指定位移消费

```
1. 指定分区

2. 从头消费
	seek()方法正好提供了这个功能，让我们得以追踪以前的消费或者回溯消费

3. 指定offset
	consumer.seek(tp, 10);
	
for (TopicPartition tp : assignment) {
     // 参数partition表示分区，offset表示指定从分区的哪个位置开始消费
     consumer.seek(tp, 10);
     // consumer.seek(new TopicPartition(topic,0), 10)
   }
	
   // 指定分区末尾：
   Map<TopicPartition, Long> offsets = consumer.endOffsets(assignment);
   for (TopicPartition tp : assignment) {
     consumer.seek(tp, offsets.get(tp));
   }
   
4. 从指定时间点开始消费  如果已经消费完了，能拿到么
 
 
 一个小细节：
 新的消费组加入，从哪里开始消费：
 auto_offset_reset_config   earliest（包括之前的） / latest 只消费启动后的最新的
 
 
// go 
pc, err := consumer.ConsumePartition("web_log", int32(partition), sarama.OffsetNewest)
```



### 6. 再均衡监听器

```
再均衡是指分区的所属从一个消费者转移到另外一个消费者的行为，它为消费组具备了高可用性和伸缩
性提供了保障，使得我们既方便又安全地删除消费组内的消费者或者往消费组内添加消费者。不过再均
衡发生期间，消费者是无法拉取消息的

public static void main(String[] args) {
   Properties props = initConfig();
   KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
   Map<TopicPartition, OffsetAndMetadata> currentOffsets = new HashMap<>();
   
   consumer.subscribe(Arrays.asList(topic), new ConsumerRebalanceListener(){
     @Override
     public void onPartitionsRevoked(Collection<TopicPartition>
partitions) {
       // 尽量避免重复消费
       consumer.commitSync(currentOffsets);
     }
     @Override
     public void onPartitionsAssigned(Collection<TopicPartition>
partitions) {
       //do nothing.
     }
   });
   
   try {
     while (isRunning.get()) {
       ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(1000));
       for (ConsumerRecord<String, String> record : records) {
         System.out.println(record.offset() + ":" + record.value());
         // 异步提交消费位移，在发生再均衡动作之前可以通过再均衡监听器的onPartitionsRevoked回调执行commitSync方法同步提交位移。
         currentOffsets.put(new TopicPartition(record.topic(),
record.partition()), new OffsetAndMetadata(record.offset() + 1));
       }
       consumer.commitAsync(currentOffsets, null);
     }
   } finally {
     consumer.close();
   }
 }
 
 
 	c.Consumer.Group.Rebalance.Strategy = BalanceStrategyRange
	c.Consumer.Group.Rebalance.Timeout = 60 * time.Second
	c.Consumer.Group.Rebalance.Retry.Max = 4
	c.Consumer.Group.Rebalance.Retry.Backoff = 2 * time.Second

```



### 7. 拦截器

```
// ConsumerInterceptor allows you to intercept (and possibly mutate) the records
// received by the consumer before they are sent to the messages channel.
type ConsumerInterceptor interface {
	// OnConsume is called when the consumed message is intercepted. Please
	// avoid modifying the message until it's safe to do so, as this is _not_ a
	// copy of the message.
	OnConsume(*ConsumerMessage)
}
```



### 8. 元数据接口

```
func metadata_test() {
    fmt.Printf("metadata test\n")

    config := sarama.NewConfig()
    config.Version = sarama.V0_11_0_2

    client, err := sarama.NewClient([]string{"localhost:9092"}, config)
    if err != nil {
        fmt.Printf("metadata_test try create client err :%s\n", err.Error())
        return
    }

    defer client.Close()

    // get topic set
    topics, err := client.Topics()
    if err != nil {
        fmt.Printf("try get topics err %s\n", err.Error())
        return
    }

    fmt.Printf("topics(%d):\n", len(topics))

    for _, topic := range topics {
        fmt.Println(topic)
    }

    // get broker set
    brokers := client.Brokers()
    fmt.Printf("broker set(%d):\n", len(brokers))
    for _, broker := range brokers {
        fmt.Printf("%s\n", broker.Addr())
    }
}
```





## 9. 主题

```
1. 创建主题
bin/kafka-topics.sh --zookeeper zookeeper:2181 --create --topic heima --partitions 2 --replication-factor 1

2. 查看topic中元数据的信息  zookeeper
bin/zkCli.sh -server localhost:2181

get /brokers/topics/web_log

3. 查看主题
bin/kafka-topics.sh --list --zookeeper zookeeper:2181


// 通过 --describe查看某个特定主题信息,不指定topic则查询所有 
bin/kafka-topics.sh --describe --zookeeper zookeeper:2181 --topic web_log

//查看正在同步的主题
// 通过 --describe 和 under-replicated-partitions命令组合查看 under-replacation状态
bin/kafka-topics.sh --describe  under-replicated-partitions --zookeeper zookeeper:2181 --topic web_log

4. 修改主题
// 增加配置
bin/kafka-topics.sh --alter --zookeeper zookeeper:2181 --topic web_log --config flush.messages=1

// 删除配置
bin/kafka-topics.sh --alter --zookeeper zookeeper:2181 --topic web_log --delete-config flush.messages


5. 删除主题
若 delete.topic.enable=true  直接彻底删除该 Topic。 若 delete.topic.enable=false  如果当前
Topic 没有使用过即没有传输过信息：可以彻底删除。  如果当前 Topic 有使用过即有过传输过信息：
并没有真正删除 Topic 只是把这个 Topic 标记为删除(marked for deletion)，重启 Kafka Server 后删
除。

bin/kafka-topics.sh --delete --zookeeper zookeeper:2181 --topic web_log



6. 增加分区
bin/kafka-topics.sh --alter --zookeeper zookeeper:2181 --topic web_log --partitions 3

//修改分区数时，仅能增加分区个数。若是用其减少 partition 个数，则会报如下错误信息：
InvalidPartitionsException: The number of
partitions for a topic can only be increased. Topic heima currently has 3
partitions, 2 would not be an increase

7. 分区副本的配置
bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic my-
topic --partitions 1 --replication-factor 1 --config max.message.bytes=64000 --config
flush.messages=1

bin/kafka-configs.sh --zookeeper zookeeper:2181 --entity-type topics --entity-name my-topic 
--alter --add-config max.message.bytes=128000

bin/kafka-configs.sh --zookeeper localhost:2181 --entity-type topics --entity-name my-topic --describe

bin/kafka-configs.sh --zookeeper zookeeper:2181 --entity-type topics --
entity-name my-topic --alter --delete-config max.message.bytes


8. kafkaAdminClient
我们都习惯使用Kafka中bin目录下的脚本工具来管理查看Kafka，但是有些时候需要将某些管理查看的
功能集成到系统（比如Kafka Manager）中，那么就需要调用一些API来直接操作Kafka了

public class KafkaAdminConfigOperation {
 public static void main(String[] args) throws ExecutionException,
InterruptedException {
//    describeTopicConfig();
//    alterTopicConfig();
   addTopicPartitions();
   
   //Config(entries=[ConfigEntry(name=compression.type, value=producer,
source=DEFAULT_CONFIG, isSensitive=false, isReadOnly=false, synonyms=[]),
ConfigEntry(name=leader.replication.throttled.replicas, value=,
source=DEFAULT_CONFIG, isSensitive=false, isReadOnly=false, synonyms=[]),
ConfigEntry(name=message.downconversion.enable, value=true,
source=DEFAULT_CONFIG, isSensitive=false, isReadOnly=false, synonyms=[]),
ConfigEntry(name=min.insync.replicas, value=1, source=DEFAULT_CONFIG,
isSensitive=false, isReadOnly=false, synonyms=[]),
ConfigEntry(name=segment.jitter.ms, value=0, source=DEFAULT_CONFIG,
isSensitive=false, isReadOnly=false, synonyms=[]),
ConfigEntry(name=cleanup.policy, value=delete, source=DEFAULT_CONFIG,
isSensitive=false, isReadOnly=false, synonyms=[]), ConfigEntry(name=flush.ms,
value=9223372036854775807, source=DEFAULT_CONFIG, isSensitive=false,
isReadOnly=false, synonyms=[]),
ConfigEntry(name=follower.replication.throttled.replicas, value=,
source=DEFAULT_CONFIG, isSensitive=false, isReadOnly=false, synonyms=[]),
ConfigEntry(name=segment.bytes, value=1073741824, source=STATIC_BROKER_CONFIG,
isSensitive=false, isReadOnly=false, synonyms=[]),
ConfigEntry(name=retention.ms, value=604800000, source=DEFAULT_CONFIG,
isSensitive=false, isReadOnly=false, synonyms=[]),
ConfigEntry(name=flush.messages, value=9223372036854775807,
source=DEFAULT_CONFIG, isSensitive=false, isReadOnly=false, synonyms=[]),
ConfigEntry(name=message.format.version, value=2.0-IV1, source=DEFAULT_CONFIG,
isSensitive=false, isReadOnly=false, synonyms=[]),
ConfigEntry(name=file.delete.delay.ms, value=60000, source=DEFAULT_CONFIG,
isSensitive=false, isReadOnly=false, synonyms=[]),
ConfigEntry(name=max.message.bytes, value=1000012, source=DEFAULT_CONFIG,
isSensitive=false, isReadOnly=false, synonyms=[]),
ConfigEntry(name=min.compaction.lag.ms, value=0, source=DEFAULT_CONFIG,
isSensitive=false, isReadOnly=false, synonyms=[]),
ConfigEntry(name=message.timestamp.type, value=CreateTime,
source=DEFAULT_CONFIG, isSensitive=false, isReadOnly=false, synonyms=[]),
ConfigEntry(name=preallocate, value=false, source=DEFAULT_CONFIG,
isSensitive=false, isReadOnly=false, synonyms=[]),
ConfigEntry(name=min.cleanable.dirty.ratio, value=0.5, source=DEFAULT_CONFIG,
isSensitive=false, isReadOnly=false, synonyms=[]),
ConfigEntry(name=index.interval.bytes, value=4096, source=DEFAULT_CONFIG,
isSensitive=false, isReadOnly=false, synonyms=[]),
ConfigEntry(name=unclean.leader.election.enable, value=false,
source=DEFAULT_CONFIG, isSensitive=false, isReadOnly=false, synonyms=[]),
ConfigEntry(name=retention.bytes, value=-1, source=DEFAULT_CONFIG,
isSensitive=false, isReadOnly=false, synonyms=[]),
ConfigEntry(name=delete.retention.ms, value=86400000, source=DEFAULT_CONFIG,
isSensitive=false, isReadOnly=false, synonyms=[]), ConfigEntry(name=segment.ms,
value=604800000, source=DEFAULT_CONFIG, isSensitive=false, isReadOnly=false,
synonyms=[]), ConfigEntry(name=message.timestamp.difference.max.ms,
value=9223372036854775807, source=DEFAULT_CONFIG, isSensitive=false,
isReadOnly=false, synonyms=[]), ConfigEntry(name=segment.index.bytes,
value=10485760, source=DEFAULT_CONFIG, isSensitive=false, isReadOnly=false,
synonyms=[])])
 public static void describeTopicConfig() throws ExecutionException,
     InterruptedException {
   String brokerList = "localhost:9092";
   String topic = "heima";
   
AdminClient client = AdminClient.create(props);
   ConfigResource resource =
       new ConfigResource(ConfigResource.Type.TOPIC, topic);
   DescribeConfigsResult result =
       client.describeConfigs(Collections.singleton(resource));
   Config config = result.all().get().get(resource);
   System.out.println(config);
   client.close();
 }
 public static void alterTopicConfig() throws ExecutionException,
InterruptedException {
   String brokerList = "localhost:9092";
   String topic = "heima";
   Properties props = new Properties();
   props.put(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, brokerList);
   props.put(AdminClientConfig.REQUEST_TIMEOUT_MS_CONFIG, 30000);
   AdminClient client = AdminClient.create(props);
   ConfigResource resource =
       new ConfigResource(ConfigResource.Type.TOPIC, topic);
   ConfigEntry entry = new ConfigEntry("cleanup.policy", "compact");
   Config config = new Config(Collections.singleton(entry));
   Map<ConfigResource, Config> configs = new HashMap<>();
   configs.put(resource, config);
   AlterConfigsResult result = client.alterConfigs(configs);
   result.all().get();
   client.close();
 }
 public static void addTopicPartitions() throws ExecutionException,
InterruptedException {
   String brokerList = "localhost:9092";
   String topic = "heima";
   Properties props = new Properties();
   props.put(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, brokerList);
   props.put(AdminClientConfig.REQUEST_TIMEOUT_MS_CONFIG, 30000);
   AdminClient client = AdminClient.create(props);
   NewPartitions newPartitions = NewPartitions.increaseTo(5);
   Map<String, NewPartitions> newPartitionsMap = new HashMap<>();
   newPartitionsMap.put(topic, newPartitions);
   CreatePartitionsResult result =
client.createPartitions(newPartitionsMap);
   result.all().get();
   client.close();
 }
}

```





## 10. 分区

```
Kafka可以将主题划分为多个分区（Partition），会根据分区规则选择把消息存储到哪个分区中，只要
如果分区规则设置的合理，那么所有的消息将会被均匀的分布到不同的分区中，这样就实现了负载均衡
和水平扩展， 同时将大的文件存储分摊到小的分区中。 另外，多个订阅者可以从一个或者多个分区中同时消费数据，以支撑海量数据处理能力。
顺便说一句，由于消息是以追加到分区中的，多个分区顺序写磁盘的总效率要比随机写内存还要高（引
用Apache Kafka – A High Throughput Distributed Messaging System的观点），是Kafka高吞吐率的
重要保证之一
```

### 1. 副本机制

```
由于Producer和Consumer都只会与Leader角色的分区副本相连，所以kafka需要以集群的组织形式提
供主题下的消息高可用。kafka支持主备复制，所以消息具备高可用和持久性。

一个分区可以有多个副本，这些副本保存在不同的broker上。每个分区的副本中都会有一个作为
Leader。当一个broker失败时，Leader在这台broker上的分区都会变得不可用，kafka会自动移除
Leader，再其他副本中选一个作为新的Leader。

在通常情况下，增加分区可以提供kafka集群的吞吐量。然而，也应该意识到集群的总分区数或是单台
服务器上的分区数过多，会增加不可用及延迟的风险(延迟过高，会被踢掉)
```

### 2. 分区Leader选举

```
可以预见的是,如果某个分区的Leader挂了,那么其它跟随者将会进行选举产生一个新的leader,之后所有
的读写就会转移到这个新的Leader上,在kafka中,其不是采用常见的多数选举的方式进行副本的Leader
选举,而是会在Zookeeper上针对每个Topic维护一个称为ISR（in-sync replica，已同步的副本）的集合,
显然还有一些副本没有来得及同步。只有这个ISR列表里面的才有资格成为leader(先使用ISR里面的第一
个，如果不行依次类推，因为ISR里面的是同步副本，消息是最完整且各个节点都是一样的)。 通过
ISR, kafka需要的冗余度较低，可以容忍的失败数比较高。

假设某个topic有f+1个副本，kafka可以容忍f个不可用,当然,如果全部ISR里面的副本都不可用,也可以选择其他可用的副本,只是存在数据的不一致。   这种场景如何处理？

```

### 3. 分区rebalance

> 前提： 消费者没有指定分区消费，当消费组里消费者和分区关系发生变化，就会触发rebalance

```
我们往已经部署好的Kafka集群里面添加机器是最正常不过的需求，而且添加起来非常地方便，

我们需要做的事是从已经部署好的Kafka节点中复制相应的配置文件，然后把里面的broker id修改成全局唯一
的，最后启动这个节点即可将它加入到现有Kafka集群中。但是问题来了，新添加的Kafka节点并不会自动地分配数据，所以无法分担集群的负载，除非我们新建一个topic。但是现在我们想手动将部分分区移到新添加的Kafka节点上，Kafka内部提供了相关的工具来重新分布某个topic的分区

第一步：我们创建一个有三个节点的集群
bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --topic heima-par --partitions 3 --replication-factor 3

bin/kafka-topics.sh --describe--zookeeper zookeeper:2181 --topic heima-par

第二步：主题 heima-par再添加一个分区
bin/kafka-topics.sh --alter --zookeeper zookeeper:2181 --topic heima-par --partitions 4

bin/kafka-topics.sh --describe--zookeeper zookeeper:2181 --topic heima-par

第三步：再添加一个 broker节点

第四步：重新分配
现在我们需要将原先分布在broker 1-3节点上的分区重新分布到broker 1-4节点上，借助kafka-
reassign-partitions.sh工具生成reassign plan，不过我们先得按照要求定义一个文件，里面说明哪些
topic需要重新分区，文件内容如下：
vim reassign.json
{"topics":[{"topic":"heima-par"}],
"version":1
}

然后使用 kafka -reassign-partitions.sh 工具生成reassign plan
bin/kafka-reassign-partitions.sh --zookeeper zookeeper:2181 --topics-to-move-json-file
reassign.json --broker-list "0,1,2,3" --generate

xx
xx

输出内容中包括当前的分布配置和即将改变后的分布配置。
将以上命令的输出内容保存为json文件。其中当前分布配置备份为backup.json，改变后的分布配置保存为expand-cluster-reassignment.json

bin/kafka-reassign-partitions.sh --zookeeper zookeeper:2181 --reassignment-json-file expand-cluster-reassignment.json --execute


校验：
bin/kafka-reassign-partitions.sh --zookeeper zookeeper:2181 --reassignment-json-file expand-cluster-reassignment.json --verify

bin/kafka-topics.sh --describe--zookeeper zookeeper:2181 --topic heima-par

手动再平衡
当以上迁移过程导致kafka的leader分布，不符preferred replica分布建议，则可以手动进行再平衡维护。
注：进行分区迁移时，最好先保留一个分区在原来的磁盘，这样不会影响正常的消费和生产。部分迁移则支持正常消费和生产
./kafka-preferred-replica-election.sh ip:port
```



### 4. 修改副本因子

```
实际项目中我们可能在创建topic时没有设置好正确的replication-factor，导致kafka集群虽然是高可用
的，但是该topic在有broker宕机时，可能发生无法使用的情况。topic一旦使用又不能轻易删除重建，
因此动态增加副本因子就成为最终的选择

说明：kafka 1.0版本配置文件默认没有default.replication.factor=x， 因此如果创建topic时，不指定–
replication-factor 想， 默认副本因子为1. 我们可以在自己的server.properties中配置上常用的副本因
子，省去手动调整。例如设置default.replication.factor=3

首先我们配置topic的副本，保存为replication-factor.json
	{
        "version":1,
        "partitions":[
            {"topic":"heima","partition":0,"replicas":[0,1,2]},
            {"topic":"heima","partition":1,"replicas":[0,1,2]},
            {"topic":"heima","partition":2,"replicas":[0,1,2]}
        ]
	}

然后执行脚本 
	bin/kafka-reassign-partitions.sh --zookeeper zookeeper:2181 --reassignment-json-file replication-factor.json --execute
	
	xxx > result.json

验证
 	bin/kafka-reassign-partitions.sh --zookeeper zookeeper:2181 --reassignment-json-file result.json --verify
 	
    Status of partition reassignment:
    Reassignment of partition heima-par-3 completed successfully
    Reassignment of partition heima-par-0 is still in progress
    Reassignment of partition heima-par-2 is still in progress
    Reassignment of partition heima-par-1 is still in progress
    {
    "version":1,
    "partitions":[
        {"topic":"heima","partition":0,"replicas":[0,1,2]},
        {"topic":"heima","partition":1,"replicas":[0,1,2]},
        {"topic":"heima","partition":2,"replicas":[0,1,2]}
    ]
    }
```

### 5. 分区分配策略

> sticky 很重要

```
按照Kafka默认的消费逻辑设定，一个分区只能被同一个消费组（ConsumerGroup）内的一个消费者
消费。假设目前某消费组内只有一个消费者C0，订阅了一个topic，这个topic包含7个分区，也就是说
这个消费者C0订阅了7个分区    0-7

此时消费组内又加入了一个新的消费者 C1，按照既定的逻辑需要将原来消费者C0的部分分区分配给消
费者C1消费，情形上图（2），消费者C0和C1各自负责消费所分配到的分区，相互之间并无实质性的干
扰。    0-4，5-7

接着消费组内又加入了一个新的消费者C2，如此消费者C0、C1和C2按照上图（3）中的方式各自负责
消费所分配到的分区   0-2  3-5  6-7 

如果消费者过多，出现了消费者的数量大于分区的数量的情况，就会有消费者分配不到任何分区。参考
下图，一共有8个消费者，7个分区，那么最后的消费者C7由于分配不到任何分区进而就无法消费任何
消息

RangeAssignor分配策略  通过公式计算， 如果挂了，重新来一遍
    RangeAssignor策略的原理是按照消费者总数和分区总数进行整除运算来获得一个跨度，然后将分区按
    照跨度进行平均分配，以保证分区尽可能均匀地分配给所有的消费者。对于每一个topic，
    RangeAssignor策略会将消费组内所有订阅这个topic的消费者按照名称的字典序排序，然后为每个消费
    者划分固定的分区范围，如果不够平均分配，那么字典序靠前的消费者会被多分配一个分区。
    
    假设n=分区数/消费者数量，m=分区数%消费者数量，那么前m个消费者每个分配n+1个分区，后面的
    （消费者数量-m）个消费者每个分配n个分区。
    
    假设消费组内有2个消费者C0和C1，都订阅了主题t0和t1，并且每个主题都有4个分区，那么所订阅的
    所有分区可以标识为：t0p0、t0p1、t0p2、t0p3、t1p0、t1p1、t1p2、t1p3。最终的分配结果为：
    消费者C0：t0p0、t0p1、t1p0、t1p1
	消费者C1：t0p2、t0p3、t1p2、t1p3
	
	假设上面例子中 2个主题都只有3个分区，那么所订阅的所有分区可以标识为：t0p0、t0p1、t0p2、
	t1p0、t1p1、t1p2。最终的分配结果为：
	消费者C0：t0p0、t0p1、t1p0、t1p1
	消费者C1：t0p2、t1p2
	
	可以明显的看到这样的分配并不均匀，如果将类似的情形扩大，有可能会出现部分消费者过载的情况


RoundRobinAssignor分配策略  轮训，如果挂了，重新来一遍
	RoundRobinAssignor策略的原理是将消费组内所有消费者以及消费者所订阅的所有topic的partition按
    照字典序排序，然后通过轮询方式逐个将分区以此分配给每个消费者。RoundRobinAssignor策略对应
    的partition.assignment.strategy参数值为：
    org.apache.kafka.clients.consumer.RoundRobinAssignor。
    
    假设消费组中有2个消费者C0和C1，都订阅了主题t0和t1，并且每个主题都有3个分区，那么所订阅的
    所有分区可以标识为：t0p0、t0p1、t0p2、t1p0、t1p1、t1p2。最终的分配结果为：
    消费者C0：t0p0、t0p2、t1p1
	消费者C1：t0p1、t1p0、t1p2
	
	如果同一个消费组内的消费者所订阅的信息是不相同的，那么在执行分区分配的时候就不是完全的轮询
    分配，有可能会导致分区分配的不均匀。如果某个消费者没有订阅消费组内的某个topic，那么在分配分
    区的时候此消费者将分配不到这个topic的任何分区。
    
    假设消费组内有3个消费者C0、C1和C2，它们共订阅了3个主题：t0、t1、t2，这3个主题分别有1、2、
    3个分区，即整个消费组订阅了t0p0、t1p0、t1p1、t2p0、t2p1、t2p2这6个分区。
    具体而言，消费者C0订阅的是主题t0，消费者C1订阅的是主题t0和t1，消费者C2订阅的是主题t0、t1和t2，那    么最终的分配结果为：
        
    	消费者C2：t1p1、t2p0、t2p1、t2p2
	可以看到 RoundRobinAssignor策略也不是十分完美，这样分配其实并不是最优解，因为完全可以将分区t1p1分配给消费者C1
	
	
StickyAssignor分配策略   在触发rebalance后，在消费者消费的原有基础上进行调整(如果挂了，原有不变）
	Kafka从0.11.x版本开始引入这种分配策略，它主要有两个目的：分区的分配要尽可能的均匀； 分区的分配尽可能的与上次分配的保持相同。当两者发生冲突时，第一个目标优先于第二个目标。鉴于这两个目标，StickyAssignor策略的具体实现要比RangeAssignor和RoundRobinAssignor这两种分配策略要复杂很多
	
	假设消费组内有3个消费者：C0、C1和C2，它们都订阅了4个主题：t0、t1、t2、t3，并且每个主题有2
个分区，也就是说整个消费组订阅了t0p0、t0p1、t1p0、t1p1、t2p0、t2p1、t3p0、t3p1这8个分
区。最终的分配结果如下：
	消费者C0：t0p0、t1p1、t3p0
    消费者C1：t0p1、t2p0、t3p1
    消费者C2：t1p0、t2p1
    
   假设此时消费者 C1脱离了消费组，那么消费组就会执行再平衡操作，进而消费分区会重新分配。如果采
用RoundRobinAssignor策略，那么此时的分配结果如下：
	消费者C0：t0p0、t1p0、t2p0、t3p0
	消费者C2：t0p1、t1p1、t2p1、t3p1
	
	如分配结果所示， RoundRobinAssignor策略会按照消费者C0和C2进行重新轮询分配。而如果此时使用
的是StickyAssignor策略，那么分配结果为：
	消费者C0：t0p0、t1p1、t3p0、t2p0
	消费者C2：t1p0、t2p1、t0p1、t3p1
	
	可以看到分配结果中保留了上一次分配中对于消费者 C0和C2的所有分配结果，并将原来消费者C1的“负
担”分配给了剩余的两个消费者C0和C2，最终C0和C2的分配还保持了均衡。


自定义分配
	需实现：org.apache.kafka.clients.consumer.internals.PartitionAssignor
	继承自：org.apache.kafka.clients.consumer.internals.AbstractPartitionAssignor
```





## 11. 存储

```
1. partition存储结构
        partition  100G
segment 500m      segment  500m

每一个 partion(文件夹)相当于一个巨型文件被平均分配到多个大小相等segment(段)数据文件里。
但每一个段segment file消息数量不一定相等，这样的特性方便old segment file高速被删除。
（默认情况下每一个文件大小为1G）
每一个 partiton仅仅须要支持顺序读写即可了。segment文件生命周期由服务端配置參数决定。

2. segment文件存储结构
egment file组成：由2大部分组成。分别为index file和data file，此2个文件一一相应，成对出现，后
缀”.index”和“.log”分别表示为segment索引文件、数据文件.
segment文件命名规则：partion全局的第一个segment从0开始，兴许每一个segment文件名称为上一
个segment文件最后一条消息的offset值。
数值最大为64位long大小。19位数字字符长度，没有数字用0填充。

ll /tmp/kafka/log/heima-0/
-rw-r--r-- 1 itcast sudo  10485760 Aug 29 09:38 00000000000000000000.index
-rw-r--r-- 1 itcast sudo     0 Aug 29 09:38     00000000000000000000.log
-rw-r--r-- 1 itcast sudo  10485756 Aug 29 09:38 00000000000000000000.timeindex
-rw-r--r-- 1 itcast sudo     8 Aug 29 09:38     leader-epoch-checkpoint
```



### 日志索引

```
1. 数据文件的分段
	数据文件以该段中最小的offset命名。这样在查找指定offset的Message的时候，用二分查找就可
以定位到该Message在哪个段中   offset(index) - > message(log) 

2. 偏移量索引
	数据文件分段使得可以在一个较小的数据文件中查找对应offset的Message了，但是这依然需要顺序扫
描才能找到对应offset的Message。为了进一步提高查找的效率，Kafka为每个分段后的数据文件建立了索引文件，文件名与数据文件的名字是一样的，只是文件扩展名为.index

比如：要查找绝对 offset为7 的Message：
首先是用二分查找确定它是在哪个Segment中，自然是在第一个Segment中。 打开这个Segment的
index文件，也是用二分查找找到offset小于或者等于指定offset的索引条目中最大的那个offset。自然
offset为6的那个索引是我们要找的，通过索引文件我们知道offset为6的Message在数据文件中的位置
为9807。
打开log数据文件，从位置为9807的那个地方开始顺序扫描直到找到offset为7的那条Message。
这套机制是建立在offset是有序的。索引文件被映射到内存中，所以查找的速度还是很快的。

总结：
	Kafka的Message存储采用了分区(partition)，分段(Segment)和稀疏索引这几个手段来达到了高效性
```

### 日志清理

```
1. 日志删除
默认是7天，Kafka日志管理器允许定制删除策略。  
目前的策略是 删除修改时间在N天之前的日志（按时间删除），也可以使用另外一个策略：保留最后的N GB数据的策略(按大小删除)。
	//1.清理超过指定时间清理：
	log.retention.hours=16
	//2. 超过指定大小后，删除旧的消息：
	log.retention.bytes=1073741824

为了避免在删除时阻塞读操作，采用了copy-on-write形式的实现，删除操作进行时，读取操作的二分查找功能实际是在一个静态的快照副本上进行的，这类似于Java的CopyOnWriteArrayList。 

Kafka消费日志删除思想：Kafka把topic中一个parition大文件分成多个小文件段，通过多个小文件段，就容易定期清除或删除已经消费完文件，减少磁盘占用

2. 日志压缩
将数据压缩，只保留每个key最后一个版本的数据。
首先在broker的配置中设置log.cleaner.enable=true启用cleaner，这个默认是关闭的。
在Topic的配置中设置 log.cleanup.policy=compact启用压缩策略

压缩后的offset可能是不连续的，比如上图中没有5和7，因为这些offset的消息被merge了，当从这些
offset消费消息时，将会拿到比这个offset大的offset对应的消息，比如，当试图获取offset为5的消息
时，实际上会拿到offset为6的消息，并从这个位置开始消费。
这种策略只适合特俗场景，比如消息的key是用户ID，消息体是用户的资料，通过这种压缩策略，整个
消息集里就保存了所有用户最新的资料。
压缩策略支持删除，当某个Key的最新版本的消息没有内容时，这个Key将被删除
```

### 存储优势

> 消息顺序追加，页缓存,   零拷贝技术

```
Kafka在设计的时候，采用了文件追加的方式来写入消息，即只能在日志文件的尾部追加新的消息，并
且不允许修改已经写入的消息，这种方式属于典型的顺序写入此判断的操作，所以就算是Kafka使用磁
盘作为存储介质，所能实现的额吞吐量也非常可观

Kafka中大量使用页缓存(pagecache)，这页是Kafka实现高吞吐的重要因素之一。
```



![](3-传统方式.png)





```
除了消息顺序追加，页缓存等技术, Kafka还使用了零拷贝技术来进一步提升性能。“零拷贝技术”只用将
磁盘文件的数据复制到页面缓存中一次，然后将数据从页面缓存直接发送到网络中（发送给不同的订阅
者时，都可以使用同一个页面缓存），避免了重复复制操作。如果有10个消费者，传统方式下，数据复
制次数为4*10=40次，而使用“零拷贝技术”只需要1+10=11次，一次为从磁盘复制到页面缓存，10次表
示10个消费者各自读取一次页面缓存
```



![](4-kafka零拷贝.png)





## 12. 稳定性

> 高可用
>
> Kafka通过controller_epoch来保证控制器的唯一性，进而保证相关操作的一致性

```
因为网络问题而造成通信中断，那producer就无法判断该条消息是否已经提交（commit）。虽然Kafka无法
确定网络故障期间发生了什么，但是producer可以retry多次，确保消息已经正确传输到broker中，所
以目前Kafka实现的是at least once
```

### 幂等性

```
所谓幂等性，就是对接口的多次调用所产生的结果和调用一次是一致的。
生产者在进行重试的时候有可能会重复写入消息，使用Kafka的幂等性功能就可以避免这种情况。

但是幂等性是有条件的：
1. 只能保证 Producer 在单个会话内不丟不重，如果 Producer 出现意外挂掉再重启是无法保证的
（幂等性情况下，是无法获取之前的状态信息，因此是无法做到跨会话级别的不丢不重）;
2. 幂等性不能跨多个 Topic-Partition，只能保证单个 partition 内的幂等性，当涉及多个 Topic-
Partition 时，这中间的状态并没有同步。

Producer 使用幂等性的示例非常简单，与正常情况下 Producer 使用相比变化不大，只需要把
Producer 的配置 enable.idempotence 设置为 true 即可


生产：
1. mysql 插入业务id 作为主键，主键是唯一的，所以一次只能插入一次
2. 用redis， zk的分布式锁




Properties props = new Properties();

props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, "true");
props.put("acks", "all");   // 当 enable.idempotence 为 true，这里默认为 all
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer","org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer","org.apache.kafka.common.serialization.StringSerializer");

KafkaProducer producer = new KafkaProducer(props);
producer.send(new ProducerRecord(topic, "test");
```

### 事务

```
幂等性并不能跨多个分区运作，而事务可以弥补这个缺憾，事务可以保证对多个分区写入操作的原子
性。操作的原子性是指多个操作要么全部成功，要么全部失败，不存在部分成功部分失败的可能。
为了实现事务，应用程序必须提供唯一的transactionalId，这个参数通过客户端程序来进行设定

properties.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, transactionId);

事务要求生产者开启幂等特性，因此通过将transactional.id参数设置为非空从而开启事务特性的同时
需要将ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG设置为true（默认值为true），如果显示设
置为false，则会抛出异常。

//初始化事务
public void initTransactions();
//开启事务
public void beginTransaction()
//为消费者提供事务内的位移提交操作
public void sendOffsetsToTransaction(Map<TopicPartition, OffsetAndMetadata>offsets, String consumerGroupId)
//提交事务
public void commitTransaction()
//终止事务，类似于回滚
public void abortTransaction()


生产者代码：
public class ProducerTransactionSend {
 public static final String topic = "topic-transaction";
 public static final String brokerList = "localhost:9092";
 public static final String transactionId = "transactionId";
 
 public static void main(String[] args) {
   Properties properties = new Properties();
   properties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG,
       StringSerializer.class.getName());
   properties.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG,
       StringSerializer.class.getName());
   properties.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, brokerList);
   //
   properties.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, transactionId);
   // 
   KafkaProducer<String, String> producer = new KafkaProducer<>(properties);
   // 初始化及开始
   producer.initTransactions();
   producer.beginTransaction();
   
   try {
     //处理业务逻辑并创建ProducerRecord
     ProducerRecord<String, String> record1 = new ProducerRecord<>(topic,
"msg1");
     producer.send(record1);
     ProducerRecord<String, String> record2 = new ProducerRecord<>(topic,
"msg2");
     producer.send(record2);
     ProducerRecord<String, String> record3 = new ProducerRecord<>(topic,
"msg3");
     producer.send(record3);
	// 提交
     producer.commitTransaction();
   } catch (ProducerFencedException e) {
     producer.abortTransaction();
   }
}


模拟事务回滚案例
try {
     //处理业务逻辑并创建ProducerRecord
     ProducerRecord<String, String> record1 = new ProducerRecord<>(topic,
"msg1");
     producer.send(record1);
     //模拟事务回滚案例
     System.out.println(1/0);
     ProducerRecord<String, String> record2 = new ProducerRecord<>(topic,
"msg2");
     producer.send(record2);
     ProducerRecord<String, String> record3 = new ProducerRecord<>(topic,
"msg3");
     producer.send(record3);
     //处理一些其它逻辑
     producer.commitTransaction();
   } catch (ProducerFencedException e) {
     producer.abortTransaction();
   }
   
 msg1发送成功之后，出现了异常事务进行了回滚，则msg1消费端也收不到消息
```

### controller

> controller_epoch

```
在Kafka集群中会有一个或者多个broker，其中有一个broker会被选举为控制器（Kafka Controller），
它负责管理整个集群中 所有分区和副本的状态。
主要作用：
1.当某个分区的leader副本出现故障时，由控制器负责为该分区选举新的leader副本。
2.当检测到某个分区的ISR集合发生变化时，由控制器负责通知所有broker更新其元数据信息。
3.当使用kafka-topics.sh脚本为某个topic增加分区数量时，同样还是由控制器负责分区的重新分配。


Kafka中的控制器选举的工作依赖于Zookeeper，成功竞选为控制器的broker会在Zookeeper中创
建/controller这个临时（EPHEMERAL）节点

使用 zookeeper图形化的客户端工具(ZooInspector)提供的jar来进行管理，启动如下：
1、定位到jar所在目录
2、运行jar文件 java -jar zookeeper-dev-ZooInspector.jar
3、连接Zookeeper

其中 version在目前版本中固定为1，brokerid表示称为控制器的broker的id编号，timestamp表示竞选
称为控制器时的时间戳。
在任意时刻，集群中有且仅有一个控制器。每个broker启动的时候会去尝试去读取/controller节点的
brokerid的值，如果读取到brokerid的值不为-1，则表示已经有其它broker节点成功竞选为控制器，所
以当前broker就会放弃竞选；如果Zookeeper中不存在/controller这个节点，或者这个节点中的数据异
常，那么就会尝试去创建/controller这个节点，当前broker去创建节点的时候，也有可能其他broker同
时去尝试创建这个节点，只有创建成功的那个broker才会成为控制器，而创建失败的broker则表示竞选
失败。每个broker都会在内存中保存当前控制器的brokerid值，这个值可以标识为activeControllerId。
Zookeeper中还有一个与控制器有关的/controller_epoch节点，这个节点是持久（PERSISTENT）节
点，节点中存放的是一个整型的controller_epoch值。controller_epoch用于记录控制器发生变更的次
数，即记录当前的控制器是第几代控制器，我们也可以称之为“控制器的纪元”。

controller_epoch 的初始值为1，即集群中第一个控制器的纪元为1，当控制器发生变更时，每选出一个
新的控制器就将该字段值加1。每个和控制器交互的请求都会携带上controller_epoch这个字段，如果
请求的controller_epoch值小于内存中的controller_epoch值，则认为这个请求是向已经过期的控制器
所发送的请求，那么这个请求会被认定为无效的请求。如果请求的controller_epoch值大于内存中的
controller_epoch值，那么则说明已经有新的控制器当选了。由此可见，Kafka通过controller_epoch来
保证控制器的唯一性，进而保证相关操作的一致性。

具备控制器身份的broker需要比其他普通的broker多一份职责，具体细节如下：
1、监听partition相关的变化。
2、监听topic相关的变化。
3、监听broker相关的变化
```

### 可靠性

```
1. 可靠性保证：确保系统在各种不同的环境下能够发生一致的行为
2. Kafka的保证
	a）保证分区消息的顺序
        如果使用 同一个生产者往同一个分区写入消息，而且消息B在消息A之后写入
        那么Kafka可以保证消息B的偏移量比消息A的偏移量大，而且消费者会先读取消息A再
        读取消息B   (追加  日志结构)
	b)只有当消息被写入分区的所有同步副本时（文件系统缓存），它才被认为是已提交
		生产者可以选择接收不同类型的确认，控制参数 acks
	c)只要还有一个副本是活跃的，那么 已提交的消息就不会丢失
	d)消费者只能读取已经提交的消息

3. 失效副本
	怎么样判定一个分区是否有副本是处于同步失效状态的呢？从Kafka 0.9.x版本开始通过唯一的一个参数
replica.lag.time.max.ms（默认大小为10,000）来控制，当ISR中的一个follower副本滞后leader副本
的时间超过参数replica.lag.time.max.ms指定的值时即判定为副本失效，需要将此follower副本剔出除
ISR之外。
	具体实现原理很简单，当follower副本将leader副本的LEO（Log End Offset，每个分区最后
一条消息的位置）之前的日志全部同步时，则认为该follower副本已经追赶上leader副本，此时更新该
副本的lastCaughtUpTimeMs标识。Kafka的副本管理器（ReplicaManager）启动时会启动一个副本过
期检测的定时任务，而这个定时任务会定时检查当前时间与副本的lastCaughtUpTimeMs差值是否大于
参数replica.lag.time.max.ms指定的值。千万不要错误的认为follower副本只要拉取leader副本的数据
就会更新lastCaughtUpTimeMs，试想当leader副本的消息流入速度大于follower副本的拉取速度时，
follower副本一直不断的拉取leader副本的消息也不能与leader副本同步，如果还将此follower副本置
于ISR中，那么当leader副本失效，而选取此follower副本为新的leader副本，那么就会有严重的消息丢
失。

4. 副本复制
	Kafka 中的每个主题分区都被复制了 n 次，其中的 n 是主题的复制因子（replication factor）。这允许
Kafka 在集群服务器发生故障时自动切换到这些副本，以便在出现故障时消息仍然可用。Kafka 的复制
是以分区为粒度的，分区的预写日志被复制到 n 个服务器。 在 n 个副本中，一个副本作为 leader，其
他副本成为 followers。顾名思义，producer 只能往 leader 分区上写数据（读也只能从 leader 分区上
进行），followers 只按顺序从 leader 上复制日志。

一个副本可以不同步Leader有如下几个原因 
	慢副本：在一定周期时间内follower不能追赶上leader。最常见的原因之一是I / O瓶颈导致follower追加复制消息速度慢于从leader拉取速度。 
	卡住副本：在一定周期时间内follower停止从leader拉取请求。follower replica卡住了是由于GC暂停或follower失效或死亡。
	新启动副本：当用户给主题增加副本因子时，新的follower不在同步副本列表中，直到他们完全赶上了
leader日志

	在服务端现在只有一个参数需要配置 replica.lag.time.max.ms。这个参数解释replicas响应partition leader的最长等待时间。
	检测卡住或失败副本的探测——如果一个replica失败导致发送拉取请求时间间隔replica.lag.time.max.ms。Kafka会认为此replica已经死亡会从同步副本列表从移除。
	检测慢副本机制发生了变化——如果一个replica开始落后leader超过replica.lag.time.max.ms。Kafka会认为太缓慢并且会从同步副本列表中移除。除非replica请求leader时间间隔大于replica.lag.time.max.ms，因
此即使leader使流量激增和大批量写消息。Kafka也不会从同步副本列表从移除该副本
```

### 一致性

> leader epoch
>
> hw
>
> leo

```
hw: 取一个分区对应的isr中最小的 leo 作为hw, consumer最多只能消费到hw的位置，另外每个replica都有hw, leader 和 follower 各自负责更新自己的hw状态，对于Leader新写入的消息，consumer不能立刻消费，leader会等待该消费被所有isr中的replica 更新Hw, 此时消息才能被consumer消费，这样既保证了如果leader所在的broker失效，消息依然能从新的leader中获取

1. 在 leader宕机后，只能从ISR列表中选取新的leader，无论ISR中哪个副本被选为新的leader，它都
知道HW之前的数据，可以保证在切换了leader后，消费者可以继续看到HW之前已经提交的数据。
2. HW的截断机制：选出了新的leader，而新的leader并不能保证已经完全同步了之前leader的所有
数据，只能保证HW之前的数据是同步过的，此时所有的follower都要将数据截断到HW的位置，
再和新的leader同步数据，来保证数据一致。 当宕机的leader恢复，发现新的leader中的数据和
自己持有的数据不一致，此时宕机的leader会将自己的数据截断到宕机之前的hw位置，然后同步
新leader的数据。宕机的leader活过来也像follower一样同步数据，来保证数据的一致性

数据丢失场景
数据出现不一致场景


Kafka 0.11.0. 版本解决方案
	造成上述两个问题的根本原因在于HW值被用于衡量副本备份的成功与否以及在出现failture时作为日志
截断的依据，但HW值的更新是异步延迟的，特别是需要额外的FETCH请求处理流程才能更新，故这中
间发生的任何崩溃都可能导致HW值的过期。鉴于这些原因，Kafka 0.11引入了leader epoch来取代HW
值。Leader端多开辟一段内存区域专门保存leader的epoch信息，这样即使出现上面的两个场景也能很
好地规避这些问题。
	所谓leader epoch实际上是一对值：（epoch，offset）。epoch表示leader的版本号，从0开始，当
leader变更过1次时epoch就会+1，而offset则对应于该epoch版本的leader写入第一条消息的位移。因
此假设有两对值：
	(0, 0)
	(1, 120)
	则表示第一个leader从位移0开始写入消息；共写了120条[0, 119]；而第二个leader版本号是1，从位移
120处开始写入消息。
	leader broker中会保存这样的一个缓存，并定期地写入到一个checkpoint文件中。
```



### 重复消费

```
1. 生产者
	产生原因：
		生产发送的消息没有收到正确的broke响应，导致producer重试。producer发出一条消息，broke落盘以后因为网络等种种原因发送端得到一个发送失败的响应或者网络中断，然后producer收到一个可恢复的Exception重试消息导致消息重复。
	解决方案：
        1、启动kafka的幂等性
        要启动kafka的幂等性，无需修改代码，默认为关闭，需要修改配置文件:
        enable.idempotence=true 同时要求 ack= all 且 retries > 1。
        2、ack=0，不重试。
        
    //  RequireNone (0)  fire-and-forget, do not wait for acknowledgements from the
	//  RequireOne  (1)  wait for the leader to acknowledge the writes
	//  RequireAll  (-1) wait for the full ISR to acknowledge the writes

2. 消费者
	根本原因：
		数据消费完没有及时提交offset到broker。
	解决方案：
        1、取消自动自动提交
        	每次消费完或者程序退出时手动提交。这可能也没法保证一条重复。
        2、下游做幂等
        	一般的解决方案是让下游做幂等或者尽量每消费一条消息都记录offset，对于少数严格的场景可能需要把offset或唯一ID,例如订单ID和下游状态更新放在同一个数据库里面做事务来保证精确的一次更新或者在下游数据表里面同时记录消费offset，然后更新下游数据的时候用消费位点做 乐观锁 拒绝掉旧位点的数据更新。
	
```



### _consumer_offsets

> log_dir 中可以看到，还有其他的主题-分区文件夹

```
_consumer_offsets是一个内部topic，对用户而言是透明的，除了它的数据文件以及偶尔在日志中出现
这两点之外，用户一般是感觉不到这个topic的。不过我们的确知道它保存的是Kafka新版本consumer
的位移信息。

何时创建:
一般情况下，当集群中第一有消费者消费消息时会自动创建主题__consumer_offsets，分区数可以通过
offsets.topic.num.partitions参数设定，默认值为50

有设么用：
   一个消费组中的某个消费者挂了，其他消费者是如何顺序消费的，而且不重复消费
  每个消费者消费完，需要提交偏移量 给broker 里面的leader , 保存在consumer_offset 主题中
  key 是 groupid + topic + 分区 ， value 是offset, kafka 会定期清理topic里的消息，保持最新的
  一个挂了，另一个会去先读取这个offset , 然后找到自己的位置
  
  hash(consumerGroupId) % _consumer_offset 主题的分区数
  
  consumer_offser 通过加机器的方式实现更高的并发
```



## 13.  监控

```
1. jmx
在实现Kafka监控系统的过程中，首先我们要知道监控的数据从哪来，Kafka自身提供的监控指标（包括
broker和主题的指标，集群层面的指标通过各个broker的指标累加来获取）都可以通过JMX（Java
Managent Extension）来进行获取。在使用JMX之前首先要确保Kafka开启了JMX的功能（默认是关闭
的）

在使用jmx之前需要确保kafka开启了jmx监控，kafka启动时要添加JMX_PORT=9999这一项，也就是
JMX_PORT=9999 bin/kafka-server-start.sh config/server.properties

2. JConsole
在开启JMX之后最简单的监控指标的方式就是使用JConsole，可以通过jconsole连接
service:jmx:rmi:///jndi/rmi://localhost:9999/jmxrmi或者localhost:9999来查看相应的数据值

3. 编程手段来获取监控指标


4. broker监控
活跃控制器
	该指标表示 broker 是否就是当前的集群控制器，其值可以是 0 或 l。如果是 1 ，表示 broker 就是当前
的控制器。任何时候，都应该只有一个 broker 是控制器，而且这个 broker 必须一直是集群控制器。如
果出现了两个控制器，说明有一个本该退出的控制器线程被阻 塞了，这会导致管理任务无陆正常执行，
比如移动分区。为了解决这个问题，需要将这两 个 broker 重启，而且不能通过正常的方式重启，因为
此时它们无陆被正常关闭。
	kafka.controller:type=KafkaController,name=ActiveControllerCount
	
	值区间： 0或1
	
请求处理器空闲率
	Kafka 使用了两个线程地来处理客户端的请求：网络处理器线程池和请求处理器线程池。 网络处理器线
程地负责通过网络读入和写出数据。这里没有太多的工作要做， 也就是说，不用太过担心这些线程会
出现问题。请求处理器线程地负责处理来自客户端的请求，包括 从磁盘读取消息和往磁盘写入消息。因
此， broker 负载的增长对这个线程池有很大的影响。
	kafka.server:type=KafkaRequestHandlerPool,name=RequestHandlerAvgIdlePercent
	
主题流入字节
	用于评估一个 broker 是否比集群里的其他 broker 接收了更多的流 量， 如果出现了这种情况，就需要
对分区进行再均衡
	kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec
	
	RateUni.t  这是速率的时间段，在这里是“秒＼ 这两个属性表明，速率是通过 bis 来表示的，不管它的值
是基于多长的时间段算出的平均 值。速率还有其他 4 个不同粒度的属性。 OneMi.nuteRate 前 1 分钟
的平均值。 Fi.ve问i.nuteRate 前 5 分钟的平均值。 Fi.fteenMi.nuteRate 前 15 分钟的平均值。
MeanRate 从 broker 启动到目前为止的平均值


主题流出字节
	主题流出字节速率与流入字节速率类似，是另一个与规模增长有关的度量指标。流出字节速 率显示的是
悄费者从 broker读取消息的速率。流出速率与流入速率的伸缩方式是不一样的， 这要归功于 Kafka 对
多消费者客户端的支持
	kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec

主题流入的消息
	之前介绍的字节速率以字节的方式来表示 broker 的流量， 而消息速率则以每秒生成消息个 数的方式来
表示流量，而且不考虑消息的大小。这也是一个很有用的生产者流量增长规模 度量指标。它也可以与字
节速率一起用于计算消息的平均大小
	kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec

分区数量
 	broker 的分区数量一般不会经常发生改变，它是指分配给 broker 的分区总数。它包括 broker 的每一
个分区副本，不管是首领还是跟随者
	kafka.server:type=ReplicaManager,name=PartitionCount
	
首领数量
 	该度量指标表示 broker 拥有的首领分区数量。与 broker 的其他度量一样，该度量指标也应 该在整个
集群的 broker 上保持均等。我们需要对该指析J进行周期性地检查，井适时地发出 告警，即使在副本的
数量和大小看起来都很完美的时候，它仍然能够显示出集群的不均衡 问题。因为 broker 有可能出于各
种原因释放掉一个分区的首领身份，比如 Zookeeper 会话 过期，而在会话恢复之后，这个分区并不会
自动拿回首领身份（除非启用了自动首领再均 衡功能）。在这些情况下，该度量指标会显示较少的首领
分区数，或者直接显示为零。这 个时候需要运行一个默认的副本选举，重新均衡集群的首领
	kafka.server:type=ReplicaManager,name=LeaderCount
	
	

5. 主题分区
	主题实例的度量指标
		主题的数量，而且用户极有可能不会监控这些度量指标或设置告 警。 它们一般提供给客户端使用，客
户端依此评估它们对 Kafka 的使用情况，并进行问题 调试。

	分区实例的度量指标
		分区实例的度量指标不如主题实例的度量指标那样有用。另外，它们的数量会更加庞大， 因为几百个主
题就可能包含数千个分区。不过不管怎样，在某些情况下，它们还是有一定用处的。 Partition size 度
量指标表示分区当前在磁盘上保留的数据量。如 果把它们组合在一起，就可以表示单个主题保留的数据
量，作为客户端配额的依据。同一 个主题的两个不同分区之间的数据量如果存在差异，说明消息并没有
按照生产消息的键 进行均句分布。 Log segment count 指标表示保存在磁盘上的日志片段的文件数
量，可以与 Partition size 指标结合起来，用于跟踪资糠的使用情况 


6. 生产者监控指标
	新版本 Kafka 生产者客户端的度量指标经过调整变得更加简洁，只用了少量的 MBean。相 反，之前版
本的客户端（不再受支持的版本） 使用了大量的 MBean，而且度量指标包含了 大量的细节（提供了大
量的百分位和各种移动平均数）。这些度量指标提供了很大的覆盖 面，但这样会让跟踪异常情况变得更
加困难。 生产者度盐指标的 MBean 名字里都包含了生产者的客户端 ID。在下面的示例里，客户端 ID
使用 CLIENTID 表示， broker ID 使用 BROKERID 表示， 主题的名字使用 TOPICNAME 表示
	kafka.server:type=BrokerTopicMetrics,name=ProduceMessageConversionsPerSec
	kafka.server:type=BrokerTopicMetrics,name=TotalProduceRequestsPerSec

7.  消费者监控指标
	kafka. consumer:type=consumer-metrics,client-id=CLIENTID
	kafka. consumer:type=consumer-fetch-manager-metrics,client-id=CLIENTID
	




8. kafka Eagle  
	在开发工作当中，消费 Kafka 集群中的消息时，数据的变动是我们所关心的，当业务并不复杂的前提
下，我们可以使用 Kafka 提供的命令工具，配合 Zookeeper 客户端工具，可以很方便的完成我们的工
作。随着业务的复杂化，Group 和 Topic 的增加，此时我们使用 Kafka 提供的命令工具，已预感到力不
从心，这时候 Kafka 的监控系统此刻便尤为显得重要，我们需要观察消费应用的详情。 监控系统业界
有很多杰出的开源监控系统。我们在早期，有使用 KafkaMonitor 和 Kafka Manager 等，不过随着业
务的快速发展，以及互联网公司特有的一些需求，现有的开源的监控系统在性能、扩展性、和 DEVS 的
使用效率方面，已经无法满足了。 因此，我们在过去的时间里，从互联网公司的一些需求出发，从各位
DEVS 的使用经验和反馈出发，结合业界的一些开源的 Kafka 消息监控，用监控的一些思考出发，设计
开发了现在 Kafka 集群消息监控系统：Kafka Eagle。

	Kafka Eagle 用于监控 Kafka 集群中 Topic 被消费的情况。 consumer 包含 Lag 的产生，Offset 的变动，Partition 的分布，Owner，Topic 被创建的时间和修改的时间等信息.

	
一些配置：
D:\kafka-eagle-web-1.3.6\conf\system-config.properties

######################################
# multi zookeeper&kafka cluster list
######################################
#如果只有一个集群的话，就写一个cluster1就行了
kafka.eagle.zk.cluster.alias=cluster1
#这里填上刚才上准备工作中的zookeeper.connect地址
cluster1.zk.list=localhost:2181
#如果多个集群，继续写，如果没有注释掉
#cluster2.zk.list=xdn10:2181,xdn11:2181,xdn12:2181
######################################
# zk client thread limit
######################################
kafka.zk.limit.size=25
######################################
# kafka eagle webui port
######################################
###web界面地址端口
kafka.eagle.webui.port=8048
######################################
# kafka offset storage
######################################
cluster1.kafka.eagle.offset.storage=kafka


######################################
# enable kafka metrics
######################################
kafka.eagle.metrics.charts=false
kafka.eagle.sql.fix.error=false
######################################
# kafka sql topic records max
######################################
kafka.eagle.sql.topic.records.max=5000
######################################
# alarm email configure
######################################
#kafka.eagle.mail.enable=false
#kafka.eagle.mail.sa=alert_sa@163.com
#kafka.eagle.mail.username=alert_sa@163.com
#kafka.eagle.mail.password=mqslimczkdqabbbh
#kafka.eagle.mail.server.host=smtp.163.com
#kafka.eagle.mail.server.port=25
######################################
# alarm im configure
######################################
#kafka.eagle.im.dingding.enable=true
#kafka.eagle.im.dingding.url=https://oapi.dingtalk.com/robot/send?access_token=
#kafka.eagle.im.wechat.enable=true
#kafka.eagle.im.wechat.token=https://qyapi.weixin.qq.com/cgi-bin/gettoken?
corpid=xxx&corpsecret=xxx
#kafka.eagle.im.wechat.url=https://qyapi.weixin.qq.com/cgi-bin/message/send?
access_token=
#kafka.eagle.im.wechat.touser=
#kafka.eagle.im.wechat.toparty=
#kafka.eagle.im.wechat.totag=
#kafka.eagle.im.wechat.agentid=
######################################
# delete kafka topic token
######################################
kafka.eagle.topic.token=keadmin
######################################
# kafka sasl authenticate
######################################
#cluster1.kafka.eagle.sasl.enable=false
#cluster1.kafka.eagle.sasl.protocol=SASL_PLAINTEXT
#cluster1.kafka.eagle.sasl.mechanism=PLAIN
#cluster2.kafka.eagle.sasl.enable=false
#cluster2.kafka.eagle.sasl.protocol=SASL_PLAINTEXT
#cluster2.kafka.eagle.sasl.mechanism=PLAIN
#cluster1.kafka.eagle.sasl.client=/mnt/d/kafka-eagle-web-
1.3.6/conf/kafka_client_jaas.conf
######################################

#这个地址，按照安装目录进行配置
kafka.eagle.url=jdbc:sqlite:D:/kafka-eagle-web-1.3.6/db/ke.db
kafka.eagle.username=root
kafka.eagle.password=123456


环境变量： KE_HOME D:\kafka-eagle-web-1.3.6
启动命令： D:\kafka-eagle-web-1.3.6\bin\ke.bat
访问地址： http://localhost:8048/ke 默认用户名：admin 密码：admin
```



## 14. 调优

```
1、网络和io操作线程配置优化
broker处理消息的最大线程数（默认为3）
num.network.threads=cpu核数+1
broker处理磁盘IO的线程数
num.io.threads=cpu核数*2

2、log数据文件刷盘策略
每当producer写入10000条消息时，刷数据到磁盘
log.flush.interval.messages=10000
每间隔1秒钟时间，刷数据到磁盘
log.flush.interval.ms=1000

3、日志保留策略配置
保留三天，也可以更短 （log.cleaner.delete.retention.ms）
log.retention.hours=72
段文件配置1GB，有利于快速回收磁盘空间，重启kafka加载也会加快(如果文件过小，则文件数量比较
多，kafka启动时是单线程扫描目录(log.dir)下所有数据文件
log.segment.bytes=1073741824

4. 
这个参数指新创建一个topic时，默认的Replica数量,Replica过少会影响数据的可用性，太多则会白白浪
费存储资源，一般建议在2~3为宜。

5、调优vm.max_map_count参数。
主要适用于Kafka broker上的主题数超多的情况。Kafka日志段的索引文件是用映射文件的机制来做
的，故如果有超多日志段的话，这种索引文件数必然是很多的，极易打爆这个资源限制，所以对于这种
情况一般要适当调大这个参数。

6、JVM堆大小
首先鉴于目前Kafka新版本已经不支持Java7了，而Java 8本身不更新了，甚至Java9其实都不做了，直接
做Java10了，所以我建议Kafka至少搭配Java8来搭建。至于堆的大小，个人认为6-10G足矣。如果出现
了堆溢出，就提issure给社区，让他们看到底是怎样的问题。因为这种情况下即使用户调大heap size，也
只是延缓OOM而已，不太可能从根本上解决问题。
```



## docker-compose

> sarama kafka  官方文档

```
version: '3.7'
services:
  zookeeper-1:
    image: 'docker.io/library/zookeeper:3.6.3'
    restart: always
    environment:
      ZOO_MY_ID: '1'
      ZOO_SERVERS: 'server.1=zookeeper-1:2888:3888 server.2=zookeeper-2:2888:3888 server.3=zookeeper-3:2888:3888'
      ZOO_CFG_EXTRA: 'clientPort=2181 peerPort=2888 leaderPort=3888'
      ZOO_INIT_LIMIT: '10'
      ZOO_SYNC_LIMIT: '5'
      ZOO_MAX_CLIENT_CNXNS: '0'
      ZOO_4LW_COMMANDS_WHITELIST: 'mntr,conf,ruok'
  zookeeper-2:
    image: 'docker.io/library/zookeeper:3.6.3'
    restart: always
    environment:
      ZOO_MY_ID: '2'
      ZOO_SERVERS: 'server.1=zookeeper-1:2888:3888 server.2=zookeeper-2:2888:3888 server.3=zookeeper-3:2888:3888'
      ZOO_CFG_EXTRA: 'clientPort=2181 peerPort=2888 leaderPort=3888'
      ZOO_INIT_LIMIT: '10'
      ZOO_SYNC_LIMIT: '5'
      ZOO_MAX_CLIENT_CNXNS: '0'
      ZOO_4LW_COMMANDS_WHITELIST: 'mntr,conf,ruok'
  zookeeper-3:
    image: 'docker.io/library/zookeeper:3.6.3'
    restart: always
    environment:
      ZOO_MY_ID: '3'
      ZOO_SERVERS: 'server.1=zookeeper-1:2888:3888 server.2=zookeeper-2:2888:3888 server.3=zookeeper-3:2888:3888'
      ZOO_CFG_EXTRA: 'clientPort=2181 peerPort=2888 leaderPort=3888'
      ZOO_INIT_LIMIT: '10'
      ZOO_SYNC_LIMIT: '5'
      ZOO_MAX_CLIENT_CNXNS: '0'
      ZOO_4LW_COMMANDS_WHITELIST: 'mntr,conf,ruok'
  kafka-1:
    image: 'sarama/fv-kafka'
    build:
      context: .
      dockerfile: Dockerfile.kafka
    restart: always
    environment:
      KAFKA_VERSION: ${KAFKA_VERSION:-3.1.0}
      KAFKA_CFG_ZOOKEEPER_CONNECT: 'zookeeper-1:2181,zookeeper-2:2181,zookeeper-3:2181'
      KAFKA_CFG_LISTENERS: 'LISTENER_INTERNAL://:9091,LISTENER_LOCAL://:29091'
      KAFKA_CFG_ADVERTISED_LISTENERS: 'LISTENER_INTERNAL://kafka-1:9091,LISTENER_LOCAL://localhost:29091'
      KAFKA_CFG_INTER_BROKER_LISTENER_NAME: 'LISTENER_INTERNAL'
      KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP: 'LISTENER_INTERNAL:PLAINTEXT,LISTENER_LOCAL:PLAINTEXT'
      KAFKA_CFG_DEFAULT_REPLICATION_FACTOR: '2'
      KAFKA_CFG_BROKER_ID: '1'
      KAFKA_CFG_BROKER_RACK: '1'
      KAFKA_CFG_ZOOKEEPER_SESSION_TIMEOUT_MS: '6000'
      KAFKA_CFG_ZOOKEEPER_CONNECTION_TIMEOUT_MS: '6000'
      KAFKA_CFG_REPLICA_SELECTOR_CLASS: 'org.apache.kafka.common.replica.RackAwareReplicaSelector'
      KAFKA_CFG_DELETE_TOPIC_ENABLE: 'true'
      KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE: 'false'
  kafka-2:
    image: 'sarama/fv-kafka'
    build:
      context: .
      dockerfile: Dockerfile.kafka
    restart: always
    environment:
      KAFKA_VERSION: ${KAFKA_VERSION:-3.1.0}
      KAFKA_CFG_ZOOKEEPER_CONNECT: 'zookeeper-1:2181,zookeeper-2:2181,zookeeper-3:2181'
      KAFKA_CFG_LISTENERS: 'LISTENER_INTERNAL://:9091,LISTENER_LOCAL://:29092'
      KAFKA_CFG_ADVERTISED_LISTENERS: 'LISTENER_INTERNAL://kafka-2:9091,LISTENER_LOCAL://localhost:29092'
      KAFKA_CFG_INTER_BROKER_LISTENER_NAME: 'LISTENER_INTERNAL'
      KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP: 'LISTENER_INTERNAL:PLAINTEXT,LISTENER_LOCAL:PLAINTEXT'
      KAFKA_CFG_DEFAULT_REPLICATION_FACTOR: '2'
      KAFKA_CFG_BROKER_ID: '2'
      KAFKA_CFG_BROKER_RACK: '2'
      KAFKA_CFG_ZOOKEEPER_SESSION_TIMEOUT_MS: '6000'
      KAFKA_CFG_ZOOKEEPER_CONNECTION_TIMEOUT_MS: '6000'
      KAFKA_CFG_REPLICA_SELECTOR_CLASS: 'org.apache.kafka.common.replica.RackAwareReplicaSelector'
      KAFKA_CFG_DELETE_TOPIC_ENABLE: 'true'
      KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE: 'false'
  kafka-3:
    image: 'sarama/fv-kafka'
    build:
      context: .
      dockerfile: Dockerfile.kafka
    restart: always
    environment:
      KAFKA_VERSION: ${KAFKA_VERSION:-3.1.0}
      KAFKA_CFG_ZOOKEEPER_CONNECT: 'zookeeper-1:2181,zookeeper-2:2181,zookeeper-3:2181'
      KAFKA_CFG_LISTENERS: 'LISTENER_INTERNAL://:9091,LISTENER_LOCAL://:29093'
      KAFKA_CFG_ADVERTISED_LISTENERS: 'LISTENER_INTERNAL://kafka-3:9091,LISTENER_LOCAL://localhost:29093'
      KAFKA_CFG_INTER_BROKER_LISTENER_NAME: 'LISTENER_INTERNAL'
      KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP: 'LISTENER_INTERNAL:PLAINTEXT,LISTENER_LOCAL:PLAINTEXT'
      KAFKA_CFG_DEFAULT_REPLICATION_FACTOR: '2'
      KAFKA_CFG_BROKER_ID: '3'
      KAFKA_CFG_BROKER_RACK: '3'
      KAFKA_CFG_ZOOKEEPER_SESSION_TIMEOUT_MS: '6000'
      KAFKA_CFG_ZOOKEEPER_CONNECTION_TIMEOUT_MS: '6000'
      KAFKA_CFG_REPLICA_SELECTOR_CLASS: 'org.apache.kafka.common.replica.RackAwareReplicaSelector'
      KAFKA_CFG_DELETE_TOPIC_ENABLE: 'true'
      KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE: 'false'
  kafka-4:
    image: 'sarama/fv-kafka'
    build:
      context: .
      dockerfile: Dockerfile.kafka
    restart: always
    environment:
      KAFKA_VERSION: ${KAFKA_VERSION:-3.1.0}
      KAFKA_CFG_ZOOKEEPER_CONNECT: 'zookeeper-1:2181,zookeeper-2:2181,zookeeper-3:2181'
      KAFKA_CFG_LISTENERS: 'LISTENER_INTERNAL://:9091,LISTENER_LOCAL://:29094'
      KAFKA_CFG_ADVERTISED_LISTENERS: 'LISTENER_INTERNAL://kafka-4:9091,LISTENER_LOCAL://localhost:29094'
      KAFKA_CFG_INTER_BROKER_LISTENER_NAME: 'LISTENER_INTERNAL'
      KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP: 'LISTENER_INTERNAL:PLAINTEXT,LISTENER_LOCAL:PLAINTEXT'
      KAFKA_CFG_DEFAULT_REPLICATION_FACTOR: '2'
      KAFKA_CFG_BROKER_ID: '4'
      KAFKA_CFG_BROKER_RACK: '4'
      KAFKA_CFG_ZOOKEEPER_SESSION_TIMEOUT_MS: '6000'
      KAFKA_CFG_ZOOKEEPER_CONNECTION_TIMEOUT_MS: '6000'
      KAFKA_CFG_REPLICA_SELECTOR_CLASS: 'org.apache.kafka.common.replica.RackAwareReplicaSelector'
      KAFKA_CFG_DELETE_TOPIC_ENABLE: 'true'
      KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE: 'false'
  kafka-5:
    image: 'sarama/fv-kafka'
    build:
      context: .
      dockerfile: Dockerfile.kafka
    restart: always
    environment:
      KAFKA_VERSION: ${KAFKA_VERSION:-3.1.0}
      KAFKA_CFG_ZOOKEEPER_CONNECT: 'zookeeper-1:2181,zookeeper-2:2181,zookeeper-3:2181'
      KAFKA_CFG_LISTENERS: 'LISTENER_INTERNAL://:9091,LISTENER_LOCAL://:29095'
      KAFKA_CFG_ADVERTISED_LISTENERS: 'LISTENER_INTERNAL://kafka-5:9091,LISTENER_LOCAL://localhost:29095'
      KAFKA_CFG_INTER_BROKER_LISTENER_NAME: 'LISTENER_INTERNAL'
      KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP: 'LISTENER_INTERNAL:PLAINTEXT,LISTENER_LOCAL:PLAINTEXT'
      KAFKA_CFG_DEFAULT_REPLICATION_FACTOR: '2'
      KAFKA_CFG_BROKER_ID: '5'
      KAFKA_CFG_BROKER_RACK: '5'
      KAFKA_CFG_ZOOKEEPER_SESSION_TIMEOUT_MS: '6000'
      KAFKA_CFG_ZOOKEEPER_CONNECTION_TIMEOUT_MS: '6000'
      KAFKA_CFG_REPLICA_SELECTOR_CLASS: 'org.apache.kafka.common.replica.RackAwareReplicaSelector'
      KAFKA_CFG_DELETE_TOPIC_ENABLE: 'true'
      KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE: 'false'
  toxiproxy:
    image: 'ghcr.io/shopify/toxiproxy:2.3.0'
    ports:
      # The tests themselves actually start the proxies on these ports
      - '29091:29091'
      - '29092:29092'
      - '29093:29093'
      - '29094:29094'
      - '29095:29095'
      # This is the toxiproxy API port
      - '8474:8474'

```

kafka-go 

```
version: '2.3'
services:

  zookeeper:
    hostname: zookeeper
    image: wurstmeister/zookeeper:3.4.6
    expose:
    - "2181"
    ports:
    - "2181:2181"
  
  kafka:
    image: wurstmeister/kafka
    env_file:
    - kafka/kafka-variables.env
    depends_on:
    - zookeeper
    ports:
    - '9092:9092'
    - '8082:8082'
    - '8083:8083'

  mongo-db:
    image: mongo:4.0
    expose:
    - "27017"
    ports:
    - "27017:27017"
    environment:
      MONGO_DATA_DIR: /data/db
      MONGO_LOG_DIR: /dev/null

  consumer-mongo-db:
    build:
      context: consumer-mongo-db
    environment:
      mongoURL: mongodb://mongo-db:27017
      dbName: example_db
      collectionName: example_coll
      kafkaURL: kafka:9092
      topic: topic1
      GroupID: mongo-group
    depends_on: 
    - kafka
    - mongo-db

  consumer-logger:
    build:
      context: consumer-logger
    environment:
      kafkaURL: kafka:9092
      topic: topic1
      GroupID: logger-group
    depends_on: 
    - kafka

  producer-random:
    build:
      context: producer-random
    environment:
      kafkaURL: kafka:9092
      topic: topic1
    depends_on: 
    - kafka

  producer-api:
    build:
      context: producer-api
    environment:
      kafkaURL: kafka:9092
      topic: topic1
    expose:
    - "8080"
    ports:
    - "8080:8080"
    depends_on: 
    - kafka
```



## 问题

```
1. 一个生产者， 两个消费者，能消费到同一条消息么？
不能， 一个消费组里只有一个消费者能消费                                         单播
如果是不同的消费组订阅同一个topic， 每个消费组只有一个消费者能消费到消息        多播

同一个分区的消费顺序，不能保证总的顺序，一个消费者能消费多个分区

2. 一个消费组中的某个消费者挂了，其他消费者是如何顺序消费的，而且不重复消费
  每个消费者消费完，需要提交偏移量 给broker 里面的leader , 保存在consumer_offset 主题中
  key 是 groupid + topic + 分区 ， value 是offset, kafka 会定期清理topic里的消息，保持最新的
  
  一个挂了，另一个会去先读取这个offset , 然后找到自己的位置
  
  consumer_offser 通过加机器的方式实现更高的并发


幂等         参数设置
消息重试     参数设置

顺序消费     物理层面：同一生产者同一分区
		    代码层面：
		    	发送方： ack不能为0，使用同步发送，发送成功再发送下一条
		    	接受方： 一个分区只能有一个消费组的消费者来接受消息	
		    	顺序消费牺牲掉性能， 适用场景： 下单
		    	
消息不丢失   物理层面：只要有一个副本存在就不会丢失，
		    代码层面：但是要考虑到commit的几种可能(消息丢失，重复消费，同时考虑效率)
		   			发送方： ack =1 (leader)或者 -1(isr) , 99.99999% 要设置成-1， min.insync.replica设置成分区备份数， 同步，重试
		   			消费方： 自动提交改成手动提交(同步和异步)  ??? 还有重复消费的可能
		   			
重复消费     生产者和消费者
 		   通过幂等性保证(kafka本身有一定幂等性保证)
                1. mysql 插入业务id(uuid) 作为联合主键，主键是唯一的，所以一次只能插入一次
                2. 用redis， zk的分布式锁 业务id 作为锁	
                
             网络抖动，生产者没有收到ack, 生产者重试导致消费者收到2条消息


延时队列    kafka不擅长   
	适用场景：在订单创建超过30分钟后没有支付，则取消订单
	1. 创建多个topic, 每个topic表示延时的时间
		topic_5s
		topic_1m
		topic_30m
	2. 发送者发送到相应的topic, 并带上消息的发送时间
	3. 消费者订阅相应的topic, 轮训 消费整个topic中的消息
		如果消息的发送时间和消费的当前时间超过预设的值，比如 30分钟， 数据库把订单状态取消.
		如果消息的发送时间和消费的当前时间没有超过预设值，则不消费当前offset.
		下次继续消费该offset处的消息，判断时间是否已满足预设值.
		

死性队列     
	https://learnku.com/articles/60991
	https://blog.csdn.net/qq_43426271/article/details/114942881
	
	为什么不使用 kafka？
        考虑过类似基于 kafka/rocketmq 等消息队列作为存储的方案，最后从存储设计模型放弃了这类选择。

        举个例子，假设以 Kafka 这种消息队列存储来实现延时功能，每个队列的时间都需要创建一个单独的 topic (如: Q1-1s, Q1-2s..)。这种设计在延时时间比较固定的场景下问题不太大，但如果是延时时间变化比较大会导致 topic 数目过多，会把磁盘从顺序读写会变成随机读写从导致性能衰减，同时也会带来其他类似重启或者恢复时间过长的问题。

        topic 过多 → 存储压力
        topic 存储的是现实时间，在调度时对不同时间 (topic) 的读取，顺序读 → 随机读
        同理，写入的时候顺序写 → 随机写


***消息积压***    
消息中的内容呢？？？  补数据如何补？？？
1. 在这个消费中，使用多线程，充分利用机器的性能进行消费
2. 创建多个消费组，多个消费者，部署到其他机器上，一起消费
3. 创建一个消费者，该消费者在kafka另建一个主题，配上多个分区，多个分区配上多个消费者，该消费者poll下的消息不进行消费，直接转发到新建的主题上。 此时，新的主题的多个分区的多个消费者就一起消费了

	https://blog.csdn.net/loongshawn/article/details/119388712       // 典型架构
	https://blog.csdn.net/weixin_42322206/article/details/121848854  // 
	https://blog.csdn.net/qq_36268452/article/details/113242510      
	https://blog.csdn.net/qq_16681169/article/details/101081656   // 典型排错
	https://juejin.cn/post/7029608548942233636
	
	应急处理：
	几千万条数据在MQ里积压了七八个小时，从下午4点多，积压到了晚上很晚，10点多，11点多。线上故障了，这个时候要不然就是修复consumer的问题，让他恢复消费速度，然后傻傻的等待几个小时消费完毕。这个肯定不行。一个消费者一秒是1000条，一秒3个消费者是3000条，一分钟是18万条，1000多万条。 所以如果你积压了几百万到上千万的数据，即使消费者恢复了，也需要大概1小时的时间才能恢复过来。 解决方案：这种时候只能操作临时扩容，以更快的速度去消费数据了。
	具体操作步骤和思路如下： 
    ①先修复consumer的问题，确保其恢复消费速度，然后将现有consumer都停掉。
    ②临时建立好原先10倍或者20倍的queue数量(新建一个topic，partition是原来的10倍)。
    ③然后写一个临时分发消息的consumer程序，这个程序部署上去消费积压的消息，消费之后不做耗时处理，直接均匀轮询写入临时建好10倍数量的queue里面。
    ④紧接着征用10倍的机器来部署consumer，每一批consumer消费一个临时queue的消息。
    ⑤这种做法相当于临时将queue资源和consumer资源扩大10倍，以正常速度的10倍来消费消息。
    ⑥等快速消费完了之后，恢复原来的部署架构，重新用原来的consumer机器来消费消息。
********************************************************************************************
1、consumer导致kafka积压了大量消息

方法：
    1 增大partion数量，
    2 消费者加了并发，扩大消费线程，增加拉取条数，同时注意日志空间大小限制和拉取时间过长等问题。
    3 增加消费组数量
    4 kafka单机升级成了集群
    5 避免消费者消费消息时间过长，导致超时
        消费者每次poll的数据业务处理时间不能超过kafka的max.poll.interval.ms，可以考虑调大超时时间或者调小每次poll的数据量。
            增加max.poll.interval.ms处理时长(默认间隔300ms)
            max.poll.interval.ms=300

            修改分区拉取阈值(默认50s,建议压测评估调小)
            max.poll.records = 50
            


    6 使Kafka分区之间的数据均匀分布，在Kafka producer处，给key加随机后缀，使其均衡 
    	    batch_size = 16k 
            缓冲区大小 32m-64m
 
场景：
1 如果是Kafka消费能力不足，则可以考虑增加 topic 的 partition 的个数，
同时提升消费者组的消费者数量，消费数 = 分区数 （二者缺一不可）
2 若是下游数据处理不及时，则提高每批次拉取的数量。批次拉取数量过少
（拉取数据/处理时间 < 生产速度），使处理的数据小于生产的数据，也会造成数据积压

2、消息过期失效
产生消息堆积，消费不及时，kafka数据有过期时间，一些数据就丢失了，主要是消费不及时
 
经验:
1、消费kafka消息时，应该尽量减少每次消费时间，可通过减少调用三方接口、读库等操作，
   从而减少消息堆积的可能性。
2、如果消息来不及消费，可以先存在数据库中，然后逐条消费
  （还可以保存消费记录，方便定位问题）
3、每次接受kafka消息时，先打印出日志，包括消息产生的时间戳。
4、kafka消息保留时间（修改kafka配置文件， 默认7天）
5、任务启动从上次提交offset处开始消费处理

3 综上使用kafka注意事项
    1 由于Kafka消息key设置,在Kafka producer处，给key加随机后缀，使其均衡
    2 数据量很大，合理的增加Kafka分区数是关键。
       Kafka分区数是Kafka并行度调优的最小单元，如果Kafka分区数设置的太少，
       会影响Kafka consumer消费的吞吐量. 如果利用的是Spark流和Kafka direct approach方式，
       也可以对KafkaRDD进行repartition重分区，增加并行度处理
```



## 其他

```
参考：
    D:\百度云下载\分布式系统开发必会的技术-Kafka深入探秘者来了
	https://www.bilibili.com/video/BV1a4411B7V9?from=search&seid=17094196394904149225
	https://www.bilibili.com/video/BV1JX4y1N7Ya?p=12
	
安装：
    https://www.cnblogs.com/linjiqin/p/11891776.html (其中的参数配置横重要)
    
    https://cloud.tencent.com/developer/article/1436734
    
基本概念：
    https://www.cnblogs.com/qingyunzong/p/9004509.html#_label3_0
    
参数解释：
    https://www.cnblogs.com/happydreamzjl/p/12206997.html
    
常用命令：
    https://www.cnblogs.com/liyuanhong/p/12345751.html

底层原理：
    https://www.cnblogs.com/bainianminguo/p/12247158.html
    
python中使用kafka:
    https://blog.csdn.net/learn_tech/article/details/81115996
    
    https://blog.csdn.net/see_you_see_me/article/details/78468421
    
    https://blog.csdn.net/weixin_42357472/article/details/89242049
    
    https://blog.csdn.net/ywdhzxf/article/details/83185828?utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-1.control&dist_request_id=&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-1.control
    
    
    kafka-python使用的人多是比较成熟的库，kafka-python并没有zk的支持。pykafka是Samsa的升级版本，使用samsa连接zookeeper，生产者直接连接kafka服务器列表，消费者才用zookeeper
    
    pykafka
    
    kafka-python
    

web界面：
    https://blog.csdn.net/qq_41497111/article/details/89552733
    https://www.fengpt.cn/archives/kafka%E7%9A%84%E5%BC%80%E6%BA%90webui%E5%8F%AF%E8%A7%86%E5%8C%96%E7%95%8C%E9%9D%A2kafdrop
    
    kafka-manager
    
    Kafdrop
    
    Kafka Eagle  // 数据的变动
    
    

# https://www.cnblogs.com/linjiqin/p/11891776.html  很有用
# docker-compose.yml

version: '2'
services:
  zookeeper:
    image: wurstmeister/zookeeper
    ports:
      - "2181:2181"
    volumes:
      - ./data:/data
  kafka:
    image: wurstmeister/kafka:2.11-0.11.0.3
    ports:
      - "9092:9092"
    environment:
      #KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://192.168.19.160:9092
      #KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092
      #KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181

      KAFKA_ADVERTISED_HOST_NAME: 192.168.19.160    ## 修改:宿主机IP
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181       ## 卡夫卡运行是基于zookeeper的
      KAFKA_ADVERTISED_PORT: 9092
      KAFKA_LOG_RETENTION_HOURS: 120
      KAFKA_MESSAGE_MAX_BYTES: 10000000
      KAFKA_REPLICA_FETCH_MAX_BYTES: 10000000
      KAFKA_GROUP_MAX_SESSION_TIMEOUT_MS: 60000
      KAFKA_NUM_PARTITIONS: 3
      KAFKA_DELETE_RETENTION_MS: 1000
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./kafka-logs:/kafka
      - /etc/localtime:/etc/localtime

  kafka-manager:
    #image: obsidiandynamics/kafdrop
    image: sheepkiller/kafka-manager
    #restart: "no"
    ports:
      - "9000:9000"
    environment:
      ZK_HOSTS: 192.168.19.160


# kafka-manager 镜像地址
https://registry.hub.docker.com/r/kafkamanager/kafka-manager
https://registry.hub.docker.com/r/hlebalbau/kafka-manager
https://registry.hub.docker.com/r/sheepkiller/kafka-manager





生产者：***
	broker
	序列化器
	分区器
	拦截器
	
	其他生产者参数：acks, retries, batch.size, max.request.size
	
消费者：***
	消费者，消费组
	心跳机制
	必要参数设置
	订阅 主题和分区
	反序列化
	位移提交： 重复消费，消息丢失，自动提交，同步提交，异步提交
	再均衡
	消费者拦截器
	
	其他消费者参数： fetch.min.bytes, fetch.max.wait.ms, max.partition.fetch.bytes,  max.poll.records

主题：
	crud
	增加分区
	副本
	偏移量
	
分区：
	副本机制
	leader
	分区重新分配
	分区再平衡
	分配策略: rangeAssignor, RoundRobin, sticky
	
稳定性：***
	幂等性  enable.idempotence 设置为 true
	事务    幂等性并不能跨多个分区运作，而事务可以弥补这个缺憾，事务可以保证对多个分区写入操作的原子性。操作的原子性是指多个操作要么全部成功，要么全部失败，不存在部分成功部分失败的可能
			ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG设置为true（默认值为true） ； properties.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, transactionId);
			
	可靠性  失效副本, 副本复制
	一致性  leader epoch
	消费重复： 生产者重复，消费者重复
	

高级：***
	延时队列
	重试队列
	流式处理
	
# todo
缺少python，go代码使用
```


