maple_guard
===========

为maple在worker层提供更灵活的抵御攻击的能力。

python2, python3 supported

### 注意

1. 记得添加IP白名单，比如机器人登录的源IP 。

2. 当gateway重启时，也有可能因为用户登录不进来而导致滚雪球，从而导致IP被封。所以如果gateway需要重启，建议先把maple_guard停掉，等用户在线恢复后再重新启动。
