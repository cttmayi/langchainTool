import chatGPT

context = '''
你是Android的专家， 请阅读下面材料， 按步骤总结如何分析Android Log

例如： 
步骤1： 查找Exception的关键字
步骤2： 分析CallStack

开始

如何收集崩溃日志的总结
收集崩溃时的基本信息

进程（前台进程还是后台进程）
线程（是否是 UI 线程）
崩溃堆栈（具体崩溃在系统的代码，还是我们自己的代码里面）
崩溃堆栈类型（Java 崩溃、Native 崩溃 or ANR）
收集崩溃时的系统信息

机型、系统、厂商、CPU、ABI、Linux 版本等。（寻找共性）
Logcat。（包括应用、系统的运行日志，其中会记录 App 运行的一些基本情况）
收集崩溃时的内存信息（OOM、ANR、虚拟内存耗尽等，很多崩溃都跟内存有直接关系）

系统剩余内存。（系统可用内存很小 – 低于 MemTotal 的 10%时，OOM、大量 GC、系统频繁自杀拉起等问题都非常容易出现）
虚拟内存（但是很多类似OOM、tgkill 等问题都是虚拟内存不足导致的）
应用使用内存（得出应用本身内存的占用大小和分布）
线程数（）
收集崩溃时的应用信息

崩溃场景（崩溃发生在哪个 Activity 或 Fragment，发生在哪个业务中）
关键操作路径（记录关键的用户操作路径，这对我们复现崩溃会有比较大的帮助）
其他自定义信息（不同应用关心的重点不一样。例如运行时间、是否加载了补丁、是否是全新安装或升级等）
如何分析崩溃日志的总结
确认重点（内存 & 线程 需特别注意，很多崩溃都是由于它们使用不当造成的）

确认严重程度
崩溃基本信息
Java 崩溃（比如 NullPPointerException 是空指针，OutOfMemoryError 是资源不足）
Native 崩溃（比较常见的是有 SIGSEGV 和 SIGABRT）
ANR（先看看主线程的堆栈，是否是因为锁等待导致。接着看看 ANR 日志中 iowait、CPU、GC、system server 等信息，进一步确定是 I/O 问题，或是 CPU 竞争问题，还是由于大量 GC 导致卡死）
Logcat。从 Logcat 中我们可以看到当时系统的一些行为跟手机的状态，当从一条崩溃日志中无法看出问题的原因，或者得不到有用信息时，不要放弃，建议查看相同崩溃点下的更多崩溃日志。
查找共性（机型、系统、ROM、厂商、ABI）

复现问题

针对系统崩溃
eg:

java.util.concurrent.TimeoutException: 
         android.os.BinderProxy.finalize() timed out after 10 seconds
at android.os.BinderProxy.destroy(Native Method)
at android.os.BinderProxy.finalize(Binder.java:459)

查找可能的原因。（但通过操作路径和日志，我们可以找到一些怀疑的点）
尝试规避（查看可疑的代码调用，是否使用了不恰当的 API，是否可以更换其他的实现方式规避）
Hook 解决（ Java Hook 和 Native Hook）
'''


context = '''

从哪收集 Crash 信息？
崩溃现场是我们的“第一案发现场”，它保留着很多有价值的线索。在这里我们挖掘到的信息越多，下一步分析的方向就越清晰。

操作系统是整个崩溃过程的“旁观者”，也是我们最重要的“证人”，也是我们最重要的“证人”。

一个好的崩溃捕获工具知道应该采集哪些系统信息，也知道在什么场景要深入挖掘哪些内容。

1.1 崩溃信息
从崩溃的基本信息，我们可以对崩溃有初步的判断。

进程名、线程名。崩溃的进程是前台进程还是后台进程，崩溃是不是发生在 UI 线程。
崩溃堆栈和类型。崩溃是属于 Java 崩溃、Native 崩溃，还是 ANR，对于不同类型的崩溃我们关注的点也不太一样。特别需要看崩溃堆栈的栈顶，看具体崩溃在系统的代码，还是我们自己的代码里面。
Process Name: 'com.sample.crash'
Thread Name: 'MyThread'

java.lang.NullPointerException
    at ...TestsActivity.crashInJava(TestsActivity.java:275)

1.2 系统信息
Logcat。这里包括应用、系统的运行日志。由于系统权限问题，获取到的 Logcat可能只包含与当前 App 相关的。其中系统的 event logcat 会记录 App 运行的一些基本情况，记录在文件 /system/etc/event-log-tags 中。
system logcat:
10-25 17:13:47.788 21430 21430 D dalvikvm: Trying to load lib ... 
event logcat:
10-25 17:13:47.788 21430 21430 I am_on_resume_called: 生命周期
10-25 17:13:47.788 21430 21430 I am_low_memory: 系统内存不足
10-25 17:13:47.788 21430 21430 I am_destroy_activity: 销毁 Activty
10-25 17:13:47.888 21430 21430 I am_anr: ANR 以及原因
10-25 17:13:47.888 21430 21430 I am_kill: APP 被杀以及原因

机型、系统、厂商、CPU、ABI、Linux 版本等。–> 寻找共性
设备状态：是否 root、是否是模拟器。一些问题是由 Xposed 或多开软件造成，对这部分问题我们要区别对待。
'''

prompt = f"Write questions based on the text below\n\nText: {context}\n\nQuestions:\n1."

if __name__ == '__main__':
    ret = chatGPT.chat(prompt)
    print(ret)
