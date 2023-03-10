1. Following instructions from links below:
    - https://unix.stackexchange.com/questions/421325/wake-on-lan-via-ssh
    - https://necromuralist.github.io/posts/enabling-wake-on-lan/
1. Running the following gives me all the network connections:
    ```sh
    ip a
    ```
1. From there we pick the correct network connection that we want to work with, e.g. `enp2s0`
1. Then we need to find the current `Wake-on` settings by running:
    ```sh
    sudo ethtool enp2s0 | grep Wake-on
    ```
1. It is likely to output `Wake-on: d` which means disabled. To enable it to wake on ssh we need to turn it to `u`:
    ```sh
    sudo ethtool --change enp2s0 wol u
    ```
1. You can check that the settings have change by rerunning `sudo ethtool enp2s0 | grep Wake-on`
1. Now, you should be able to run the following to sleep/suspend (`exit` is there to shut down ssh straight away):
    ```sh
    sudo systemctl suspend && exit
    ```
1. And you should be able to ssh to wake up the computer
1. However, all of the above only does a temporary job, therefore we add the following into `/etc/systemd/system/wol.service` using `sudo`:
    ```
    [Unit]
    Description=Enable Wake On Lan

    [Service]
    Type=oneshot
    ExecStart = /sbin/ethtool --change enp4s0 wol g

    [Install]
    WantedBy=basic.target
    ```
1. And run the following:
    ```sh
    sudo systemctl daemon-reload
    sudo systemctl enable wol.service
    ```
1. Now, it should work after restart
1. More links:
  - https://bharath.lohray.com/weblog/suspending-a-computer-over-ssh/
  - https://askubuntu.com/questions/893056/logout-of-ssh-and-then-suspend-machine
  - https://askubuntu.com/questions/35719/how-do-i-suspend-over-ssh
