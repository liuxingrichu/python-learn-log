#ifconfig



【1】增加账户
#useradd username


【2】删除账户
#userdel [-r] username

‘-r’ 选项的作用只有一个，就是删除账户的时候连带账户的家目录一起删除。

【3】配置centos网络

参看https://www.apelearn.com/study_v2/chapter6.html#linuxip

【注1】网络适配器为桥接模式（自动）
【注2】dhclient可以生效的前提是“编辑-》虚拟网络编辑器—》使用本地DHCP服务将IP地址分配给虚拟机（D）为选中状态”

 vi /etc/sysconfig/network-scripts/ifcfg-eth0

IPADDR=10.72.137.85
NETMASK=255.255.255.0
GATEWAY=10.72.137.1
ONBOOT=yes
BOOTPROTO=none



【4】出现Bringing up interface eth0:  Device eth0 does not seem to be present,delaying initialization.                    [FAILED]

解决办法：

参看http://www.linuxidc.com/Linux/2012-12/76248.htm

【注】dhclient生成的eth（num）一样


首先，打开/etc/udev/rules.d/70-persistent-net.rules内容如下面例子所示：
记录下，eth1网卡的mac地址00:0c:29:50:bd:17

接下来，打开/etc/sysconfig/network-scripts/ifcfg-eth0

# vi /etc/sysconfig/network-scripts/ifcfg-eth0

将 DEVICE="eth0"  改成  DEVICE="eth1"  ,
将 HWADDR="00:0c:29:8f:89:97" 改成上面的mac地址  HWADDR="00:0c:29:50:bd:17"

最后，重启网络

#service network restart
或者

#/etc/init.d/network restart

正常了。

【5】查看主机名
$hostname

【6】无密码登陆
$ssh-keygen
$ssh-copy-id "-p52113 root@10.0.0.31"
$ssh-copy-id "root@10.0.0.31"

【7】修改用户密码
#passwd username

【8】关机
#shutdown -h now
#poweroff

【9】重启
#reboot

