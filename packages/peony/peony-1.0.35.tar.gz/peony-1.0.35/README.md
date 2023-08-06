# peony

### 一. 概述

peony是专为maple的broker-server架构而设计，可以看作是maple.worker的官方扩展包。

```
gateway/ws_gateway -> broker -> peony
      ^                           |
      |                           |
      +-------- forwarder --------+
```

peony的特点:

1. 支持对worker分组和自定义路由

2. 启动速度更快

    worker使用multiprocessing.Process启动，比burst速度更快，但是无法支持worker的热重启

3. 获取task的速度更快

    不对连接到peony的client做直接响应，全部通过trigger对gateway发送消息

4. 代码更简洁

    proxy合并到了master进程中，worker与master的通信使用multiprocessing.Queue

5. 与maple的结合更好

    不需要编写代码就可以像在maple.worker中一样获取request.cmd, request.task等等
    如果需要实现request.write_to_client，可以继承request进行增加功能。

### 二. 适用场景

1. 需要将请求将peony当作分组后的maple.worker使用，实现分业务处理

2. 需要将数据read到内存来实现复杂业务

    - 单人联网的逻辑复杂游戏
    - 玩家间的交互非常少

    比如修仙模拟器，其计算逻辑非常复杂，计算依赖的数据量也很大，比如进入副本之后的战斗。
    如果每次客户端请求都先加载一遍数据，计算完再返回给客户端，对性能的消耗太大了。

    如果使用peony的话，就可以让某个玩家固定路由到某台peony.worker上，其数据在第一次请求的时候加载进入worker内存中，之后的请求就不用再加载了。
    然后定时将内存的数据写入到 leveldb/ssdb/redis 中。
    其中leveldb由于只能单进程访问，而redis对内存大小有限制，而我们的场景是读少写多，所以使用本地启动的ssdb是个不错的选择。

    peony中还自带了定时器功能，所以可以很方便的实现定时处理的事件。如定时获得资源，或者定时写入磁盘等。

3. 非关键路径的业务处理

    比如客户端的统计和异常上报。
    可以开启UDP协议，让broker使用UDP转发


### 三. 最佳实践

1. 修真类游戏的实现方案

    这类游戏的特点是: 一个把存档放在了服务器上的单机游戏。
    其每一步的操作逻辑都很复杂，并且可能有一些复杂的定时操作，但是与其它玩家的交互较少。

    解决方案如下:

    由于worker是单进程单线程的，为了消息处理及时，worker的所有操作不能是阻塞的，比如读取数据应该从磁盘/内存读取。
    从redis读取虽然也很快，但是毕竟走了网络会有速度的问题。

    由于对于一个用户只有第一次时会读取磁盘，所以读取的频率还是很低的，大部分都是cpu计算，而python的多线程又是用不了多核的，所以直接使用一个单进程就足够了。

    数据写回磁盘有几种方式:

    1. 内存修改完之后立即写入
    2. 通过schedule定时写入
    3. 通过新线程定时写入

    第1种方案的磁盘压力最大，但是可以比较简单支持服务器重启不丢失数据。
    另外两种方案则需要在stop_worker的事件中做好数据写入的处理。

    所以存储方案使用LevelDb/RocksDB。

    至于性能对比上，网上这么说的：

    > LevelDB is the winner on disk space utilization, RocksDB is the winner on reads and deletes, and HyperLevelDB is the winner on writes.

    RocksDB编译实在太麻烦了，而且我们的方案也用不到那么高频率的读写，还是用LevelDB吧

    那么LevelDB中value的数据大小怎么设计呢:

    > no limitation on value size, but benchmark is better for small size, and in our case, limit value size to 1MB, and usually under 10KB.

    10K也够了，大不了分成: profile:1, bag:1

2. 合服后的数据迁移问题

    数据不合并，仅peony server共用即可。

    即原本一个region对应一个peony server，合服后两个region共用一个peony server。

    但是region的user数据还是存储在原来的地方，所以该去哪里读还是在哪里。

    这样既不会浪费服务器资源，也没有增加维护成本。

### 四. 设计说明

1. 配置要求

    group_id务必为数字类型，否则peonyctl无法正确处理。另外数字的查找性能也会高一点。

2. 热重启服务器问题

    不同于burst的实现，peony的worker是通过multiprocessing.Process来启动的。

    所以无法做到通过kill -HUP来实现热重启。

    原因有几个:

    - peony.worker的使用场景通常会将数据read到内存中，定时写入，所以worker直接支持热重启也不是很好的方案。
    - burst.worker的启动方式机器缓慢，所以当时burst为了支持reload，使用了极其复杂的逻辑。
    - proxy丢失数据其实没那么重要。burst之所以要支持reload，其实是希望proxy层不丢失已经接收的任务，同时也是因为起worker启动机器缓慢，所以restart的代价极高。

    但是仔细想想，在我们的业务里，如果restart的足够快的话，这些消息真的不能丢失吗？我觉得是可以的。

    如果想要支持热重启，可能最好的解决方案就是 worker 第一次请求uid时read一次，之后都不需要再read，只是写入即可。
    当然还是要加一下timeout，或者监听玩家掉线的事件，及时把read进来的数据释放掉。

3. 为什么要单独写个peony，通过burst在worker上开新线程实现定时器不行吗？
    burst更加重量级一些，其满足了很多大而全的功能，不是专为maple架构设计的。
    burst为了支持maple的broker-server架构需要做不少hack，很不优雅。

    而peony是专门配合maple来使用的。

    以peony来说:

    - 优点:
        1. 真实的pending_tasks统计
        2. 无需ask_for_task进行通信确认，速度更快，性能更高

    - 缺点:
        1. 无法进行热重启。更新代码后必须强制restart
            当然，这个缺点要看怎么想，前面的热重启服务器问题已经说的很清楚了。

4. 为什么不把request.write_to_client这样的功能也直接实现？

    因为需要额外配置一个trigger_address，但是并不是所有的使用场景都需要，比如如果只是想拿来做统计的话，就不需要。

    反正业务可以定义，所以其实也还好了。

5. worker直接kill -9会导致queue死锁，怎么解决？

    经过测试发现了这个问题，所以不要用kill -9去杀死进程。

    而后又测试了在代码中os.exit(-1)或者触发work_timeout，发现都不会死锁。

6. 关于worker与master的通信方案选择

    目前选择的是multiprocessing.Queue。

    原因如下：

    1. 方便在master上统计pending_tasks和discard_tasks
    2. 如果使用pipe的话，其recv函数是阻塞的，所以每次pool之后只能处理一个task，导致clock的计算次数大量增加。
    3. 如果使用文件socket+select的话，会有connect阻塞的问题，这里的代码实现会非常复杂。

    另外如果想要在master上统计pending_tasks和discard_tasks，就需要类似burst的响应方案，但是性能下降，或者就是不统计。

    当然，使用Queue也有缺点，就是比pipe性能低一点，毕竟为了支持多对多而加了锁。

### 五. 待处理

1. <del>性能测试</del>

2. <del>测试业务复杂之后，restart的速度</del>
