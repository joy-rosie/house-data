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