## Setup

Install apparmor and dependencies (see below about bug)
```
sudo apt-get install -y apparmor apparmor-utils
```

## Run

Apply the AppArmor policy (in the HOST(!) OS)
```
sudo apparmor_parser -r -W apparmor.config
```

Check that the AppArmor policy was applied
```
sudo aa-status
```
should see an entry for the AppArmor policy described in ``apparmor.config`` file

Start with docker-compose
```
docker-compose up --build
```

After run, check ``dmesg`` for log of things that were blocked by AppArmor

More reading

* https://docs.docker.com/engine/security/apparmor/
* https://github.com/docker/labs/tree/master/security/apparmor/wordpress
* man apparmor.d

## Bugs

Bug in apparmor in ubuntu 18.10, see https://raw.githubusercontent.com/zuazo/kitchen-in-travis/0.5.0/scripts/start_docker.sh
```
sudo apt-get -o Dpkg::Options::=--force-confnew -o Dpkg::Options::=--force-confmiss --reinstall install apparmor
```
