# What is this?

Tinybird Analytics is a blazing fast analytics engine for your serverless applications.
Think of it as a set of next-generation lego pieces for building data workflows and applications which rely on real-time analytics.

## Developing tinybird.co?

### Installing the development environment

#### 1. Compile or install ClickHouse. Current productions versions are [23.3.1.2823](https://github.com/ClickHouse/ClickHouse/releases/tag/v23.3.1.2823-lts), [22.8.11.15](https://github.com/ClickHouse/ClickHouse/releases/tag/v22.8.11.15-lts) and [21.9.5.16](https://github.com/ClickHouse/ClickHouse/releases/tag/v21.9.5.16-stable).

To help you choose the right version of ClickHouse to install, [take a look at this section in the FAQ](#which-clickhouse-version-should-i-install)

* Downloading binaries.
This is the easiest way to have multiple ClickHouse versions locally is to use pre-built binaries.
Check out [how to install it from tgz archives](https://clickhouse.com/docs/en/getting-started/install/#from-tgz-archives) and [why you don't need to build ClickHouse](https://clickhouse.tech/docs/en/development/build/#you-dont-have-to-build-clickhouse).
[This is the current production version for Linux](https://packages.clickhouse.com/tgz/stable/clickhouse-common-static-22.8.11.15-amd64.tgz), while the rest can be found [in the stable dir of the tgz archive](https://packages.clickhouse.com/tgz/stable/).
(See FAQ: using native ClickHouse builds with macOS). You can download the `clickhouse-common-static` tgz for any stable released ClickHouse version. That contains the standalone binaries within its `usr/bin` directory. This way, you can have different portable versions of ClickHouse that you can use to test. Then, you simply set `PATH` env var as explained in the following sections to choose which version to use. e.g. of directory structure:

```bash
/home/Tinybird/ch-versions
├── 21.9.5.16/usr/bin/
│   ├── clickhouse
│   ├── clickhouse-extract-from-config -> clickhouse
│   ├── clickhouse-library-bridge
│   └── clickhouse-odbc-bridge
├── 22.8.11.15/usr/bin/
│   ├── clickhouse
│   ├── clickhouse-extract-from-config -> clickhouse
│   ├── clickhouse-library-bridge
│   └── clickhouse-odbc-bridge
```

* Local Installation on M1 Mac

OSX System Integrity will block the standard install procedure recommended in the [https://clickhouse.com/docs/en/install/#self-managed-install](Clickhouse Docs), therefore you must also use the binary-path flag during the install *and all subsequent calls to the clickhouse binary*

```bash
curl https://clickhouse.com/ | sh
sudo ./clickhouse install --binary-path=/usr/local/bin
```

* Compiling ClickHouse.
You'll need 70 GB of free disk space. It is recommended to use our production version (v22.8.11.15) following its compilation docs: [https://github.com/ClickHouse/ClickHouse/blob/v22.8.11.15-lts/docs/en/development/build.md](https://github.com/ClickHouse/ClickHouse/blob/v22.8.11.15-lts/docs/en/development/build.md). The final binary is generated at `[build_dir]/programs/clickhouse`. You can use this compiled version setting the `PATH` env var accordingly.

#### 2. Install and configure Redis

* On macOS:

    ```bash
    brew install redis
    ```

* On Ubuntu/Debian:

    ```bash
    sudo apt install redis-server
    ```

Install the redis-cell extension.

* On Linux:

    ```bash
    sudo cp deploy/files/redis-cell/redis-cell-v0.2.5-x86_64-unknown-linux-gnu/libredis_cell.so /var/lib/redis
    echo 'loadmodule /var/lib/redis/libredis_cell.so' | sudo tee -a /etc/redis/redis.conf
    ```

**Important note:**
    Then modify `/etc/redis/redis.conf` and change line `supervised no` to `supervised systemd`.
    Lastly, start the service with `sudo systemctl restart redis`. You can also enable it to be automatically
    started on boot: `sudo systemctl enable redis`. You can check that it is running by executing `redis-cli ping`.

#### 3. Install Zookeeper

```bash
# On Ubuntu:
sudo apt install zookeeperd
```

```bash
# On Mac:
brew install zookeeper
```

For better **ZooKeeper performance on macOS**, the recommended JDK/JRE version is Java 8. You can download it from https://www.oracle.com/java/technologies/downloads/#java8-mac.
You should be able to keep using your ZooKeeper's Homebrew service by setting the `JAVA_HOME` environment variable so the service picks your own Java installation instead of the one from Homebrew.
You can achieve that in different ways, either modifying the Homebrew's zkServer script (you can find it with `brew info zookeeper`) or by using `launchctl setenv JAVA_HOME $JAVA_HOME` in your shell rc script.

#### 4. Checkout this repo

#### 5. Install Python >= 3.11.2

* On Ubuntu

    ```bash
    wget -qO - https://packages.confluent.io/deb/7.3/archive.key | sudo apt-key add -
    sudo add-apt-repository "deb https://packages.confluent.io/clients/deb $(lsb_release -cs) main"
    sudo apt install python3-pip libcurl4-openssl-dev libsqlite3-dev liblzma-dev libssl-dev libbz2-dev libffi-dev librdkafka1
    ```

    Install pyenv to use the recommended python version (3.11.2), following [pyenv's installation guide](https://github.com/pyenv/pyenv-installer)

    Then install python 3.11.2 and set it as the default for our analytics directory:

    ```bash
    # analytics is this cloned repo path
    cd analytics/
    CONFIGURE_OPTS=--enable-shared pyenv install 3.11.2
    pyenv local 3.11.2
    ```

* On macOS 11.X

    Install [pyenv's system dependencies](https://github.com/pyenv/pyenv/wiki#troubleshooting--faq):

    If you haven't done so, install Xcode Command Line Tools (xcode-select --install) and Homebrew. Then:

    ```bash
    brew install openssl@1.1 readline sqlite3 xz zlib
    ```

    Install pyenv, following [pyenv's installation guide](https://github.com/pyenv/pyenv-installer)

    Install Python >= 3.11.2:

    ```bash
    pyenv install 3.11.2
    ```

    Set it as a global version if you want to always use this one:

    ```bash
    pyenv global 3.11.2
    ```

* On macOS with M1

    Note that the first native version is 3.9.1

    Install Python >= 3.11.2:

    ```bash
    pyenv install 3.11.2
    ```

    Set it as a global version if you want to always use this one:

    ```bash
    pyenv global 3.11.2
    ```

#### 6. Create your mvenv and install all dependencies:

* On Ubuntu

    ```bash
    pyenv exec python3 -m venv .e
    .e/bin/python3 -m pip install --upgrade pip
    . .e/bin/activate
    PYCURL_SSL_LIBRARY=openssl pip install --editable .
    ```

    (--editable option means you can change code inside tinybird folder). Note that you need, at least, ClickHouse headers in order to install python dependencies

    virtualenv alternative in case something goes wrong with pyenv:

    ```bash
    # analytics is this cloned repo path
    sudo apt-get install python3-dev
    pip3 install virtualenv
    virtualenv -p python3.11 .e
    . .e/bin/activate
    ```

    In case you have problems installing `confluent-kafka`, compile `librdkafka` and retry:

    ```bash
    git clone https://github.com/edenhill/librdkafka.git --depth=1 --branch=v1.9.2
    cd librdkafka
    ./configure --prefix=/usr
    make -j$(nproc) && sudo make install
    ```

* On macOS with M1

    ```bash
    brew install openssl@1.1 curl-openssl libffi librdkafka postgresql
    python3 -mvenv .e
    . .e/bin/activate

    # Needs the latest pip version to correctly install clickhouse-toolset
    pip install --upgrade pip

    # Uninstall pycurl in case you have a stale version
    pip uninstall -y pycurl

    # cffi needs to be installed separately because with the --editable option it fails
    pip install cffi==1.14.5

    export PYCURL_SSL_LIBRARY=openssl LDFLAGS="-L$(brew --prefix openssl)/lib" CPPFLAGS="-I$(brew --prefix openssl)/include"

    pip install --no-cache-dir --compile --install-option="--with-openssl" --install-option="--openssl-dir=/opt/homebrew/opt/openssl@1.1" pycurl==7.45.1

    # Compiling GRPC for Apple Silicon is a PITA, see https://github.com/pietrodn/grpcio-mac-arm-build
    PYTHON_VERSION=$(python -c 'import sys; print(f"{sys.version_info.major}{sys.version_info.minor}")')
    pip install https://github.com/pietrodn/grpcio-mac-arm-build/releases/download/1.51.1/grpcio-1.51.1-cp${PYTHON_VERSION}-cp${PYTHON_VERSION}-macosx_11_0_arm64.whl

    export CFLAGS="-I$HOMEBREW_PREFIX/include"
    pip install --editable .
    ```

* On macOS with Intel

    ```bash
    brew install openssl@1.1 curl-openssl libffi librdkafka postgresql
    python3 -mvenv .e
    . .e/bin/activate

    # Needs the latest pip version to correctly install clickhouse-toolset
    pip install --upgrade pip

    # Install pycurl with the correct openssl files. After this, to check if pycurl is correctly installed and configured,
    # executing "python -c 'import pycurl'" must return nothing.
    export PYCURL_SSL_LIBRARY=openssl
    export LDFLAGS='-L/usr/local/opt/openssl/lib -L/usr/local/opt/c-ares/lib -L/usr/local/opt/nghttp2/lib -L/usr/local/opt/libmetalink/lib -L/usr/local/opt/rtmpdump/lib -L/usr/local/opt/libssh2/lib -L/usr/local/opt/openldap/lib -L/usr/local/opt/brotli/lib'
    export CPPFLAGS=-I/usr/local/opt/openssl/include

    pip install pycurl==7.45.1 --compile --no-cache-dir

    # Finally install the rest of dependencies.
    pip install --editable .
    ```

#### 7. Config pre-commit to install a pre-commit hook to prevent lint errors:

```bash
pre-commit install
```

#### 8. Extra system-wide configuration

* On Linux, increase the max number of opened files:

    ```bash
    ulimit -n 8096
    ```

    To make that change persistent, you will need to add to your `/etc/security/limits.conf` the following:

    ```bash
    # Increase # of file descriptors
    *               hard    nofile          8096
    *               soft    nofile          8096
    ```

    **On macOS** you may have noticed that ClickHouse takes at least 5 seconds to do some operations. For instance,
    if you execute ClickHouse Local with a simple query, it may take more time than expected:

    ```bash
    time ./clickhouse local --query 'Select 1'
    1
    ./clickhouse local --query 'Select 1'  0.06s user 0.02s system 1% cpu 5.092 total
    ```

    This problem is related to how macOS [manages internally the DNS queries and the hostname](https://stackoverflow.com/questions/44760633/mac-os-x-slow-connections-mdns-4-5-seconds-bonjour-slow)

    To fix this, you need to add your laptop hostname to the `/etc/hosts` file. For example doing:

    ```bash
    sudo su
    echo 127.0.0.1 localhost $(hostname) >> /etc/hosts
    ```

    This should be enough to fix the problem.

    **In both platforms:**

    It is necessary to have `clickhouse` in your `$PATH` when running the application.
    You can set it up in your environment by altering the variable on your session or by
    adding it to your shell init scripts (likely `~/.bashrc` or `~/.zshrc`).
    This will be an example for a self-compiled installation:

    ```bash
    # On self-compiled installation (Ubuntu):
    export PATH=$PATH:/usr/local/bin/
    ```

#### 9. Install Kafka [optional]

Download Kafka:

```bash
curl 'https://archive.apache.org/dist/kafka/2.8.0/kafka_2.13-2.8.0.tgz' | tar xz
```

To avoid having to setup the KAFKA_PATH envvar, decompress it on the parent folder of analytics:

```bash
my/dir/analytics
my/dir/kafka_2.13-2.8.0
```
#### 10. Configure your ClickHouse

To configure your ClickHouse instances you need to know several things about production:

* The configuration is generated via ansible.
* All clusters use replication (but not all of them have more than 1 replica)
* The configuration changes based on customer settings and the ClickHouse version.

The CI, which is probably what you are most interested on, does the same thing and generates its config via ansible:
* The one and only source of truth about the configuration is [ci.yaml](./deploy/inventories/ci.yml)
* Currently (2023-04-04) all the CI (and you) need to run the tests are 2 ClickHouse instances.
* Instances are usually called `clickhouse-01` and `clickhouse-02` but the name is meaningless.
* Port numbers do not matter (you can use any), but there **must** be 877 difference (9000-8123) between the HTTP and TCP ports. This is due to a limitation in the app logic that will be removed in the future. The HTTP ports must later be passed to the Varnish config, and that's what the application will use.
* The CI expect you to have 2 clusters: tinybird and tinybird_b available.

**Important note:** on macOS you need to configure the TCP port to 9001 due to a bug in clickhouse-local that limits connections to the default port.

In order to get some complete configuration files (config.xml and users.xml) there are 2 ways:
* Go to any Gitlab CI pipeline. check the ch_config stages and download the artifacts. Beware that CI mixes CH versions, so for example you might get clickhouse-01 config with 22.8 and clickhouse-02 config for 23.3.
* Use the ones stored under test_ch_config/$version. These might not be up to date or available for all releases, so the getting them from the CI itself is prefered.

##### 1. Configure your ClickHouse (default)

You now need to prepare to run two ClickHouse 'Shards' locally - each requires separate data, logs and other directories and config files. For the following instructions, ensure any directory path that defaults to 'clickhouse' actually then points to either 'clickhouse-1' or 'clickhouse-2'.

1. Copy config from CI tests

    ```bash
    # On Linux:
    sudo su
    echo '127.0.0.1 redis clickhouse-01 clickhouse-02' >> /etc/hosts
    cp -r test_ch_config/23.3/* /etc
    ```

2. Path configuration:

You can either leave the CI paths `/builds/tinybird/analytics/ch-${replica_num}` or change them in /etc/clickhouse-server-1/config.xml` and `/etc/clickhouse-server-2/config.xml` (changes required under `LOGGING` and `PATHS`).

4. Ensure the directories exist with proper permissions:

Note that if you changed the paths in the previous step you'll need to create and chown those directories instead:

    ```bash
    sudo mkdir -p /builds/tinybird/analytics/ch-1/ /builds/tinybird/analytics/ch-2/ /builds/tinybird/analytics/clickhouse_logs_1/ /builds/tinybird/analytics/clickhouse_logs_2/
    sudo chown $(whoami) /builds/tinybird/analytics/
    ```

#### 11. Install and run Varnish as the ClickHouse LB
1. Install
    * On macOS:

        ```bash
        brew install varnish
        ```

    * On Ubuntu/Debian:

        ```bash
        sudo apt install varnish
        ```

2. Generate a configuration based on your ClickHouse installation/configuration:

    ```bash
    export CH_PORT_01=28123 CH_PORT_02=38123 CH_LB_HOST=ci_ch CH_LB_PORT=6081
    python3.11 gitlab/prepare_varnish_db_ci_config.py ${CH_LB_HOST} ${CH_LB_PORT} 127.0.0.1 ${CH_PORT_01} 127.0.0.1 ${CH_PORT_02} > ch_lb.vcl
    ```

3. Your system must be able to resolve the CH_LB_HOST host, you can add it to your hosts files with something like:

    ```bash
    echo "127.0.0.1 ${CH_LB_HOST}" | sudo tee -a /etc/hosts
    ```

4. You can run Varnish in the foreground with:

    ```bash
    varnishd -a :${CH_LB_PORT} -T 127.0.0.1:6082 -f $(pwd)/ch_lb.vcl -s malloc,32m -F -p max_retries=1
    ```

5. You can also run as a service with systemd or brew service.
    For systemd, you can [use and adapt the template from our own Varnish unit file](https://gitlab.com/tinybird/analytics/-/blob/master/deploy/roles/ansible-varnish/templates/varnish.service.j2).

Once the ClickHouse load balancer is running, you can change the database_server in your workspaces to be "http://ci_ch:6081".

You can verify what is happening with Varnish using `varnishlog`:

```bash
sudo varnishlog
```


### Start ClickHouse and Dependency services

#### On Mac M1

Your services, apart from Clickhouse, should all be in `brew services`, therefore you can start them all with brew commands.

```bash
brew services list
# Name      Status User File
# kafka     none
# redis     none
# varnish   none
# zookeeper none

brew services start --all
#==> Successfully started `kafka` (label: homebrew.mxcl.kafka)
#==> Successfully started `redis` (label: homebrew.mxcl.redis)
#==> Successfully started `varnish` (label: homebrew.mxcl.varnish)
#==> Successfully started `zookeeper` (label: homebrew.mxcl.zookeeper)
```

#### On Linux:
Leave opened the zookeeper service:

```bash
sudo /usr/share/zookeeper/bin/zkServer.sh start-foreground
```

#### Starting ClickHouse with Default single version

```bash
clickhouse server --config-file=/etc/clickhouse-server-1/config.xml
clickhouse server --config-file=/etc/clickhouse-server-2/config.xml
```

To change to a different clickhouse version use a different binary, for example:

```bash
/home/Tinybird/ch-versions/22.8.11.15/usr/bin/clickhouse server --config-file=/etc/clickhouse-server-1/config.xml
```


One good way to make things easier for you would be to use shell aliases instead:


### Access and test that ClickHouse has started correctly

You should have at least 2 ClickHouse instances. By default those are:
* clickhouse-01:29000
* clickhouse-02:39000

To access them you should use the `-h` and `--port` options of the ClickHouse client:

```
$ clickhouse client -h clickhouse-01 --port 29000
ClickHouse client version 23.3.1.2537.
Connecting to clickhouse-01:49000 as user default.
Connected to ClickHouse server version 23.3.1 revision 54462.

Warnings:
 * Linux transparent hugepages are set to "always". Check /sys/kernel/mm/transparent_hugepage/enabled

production-01 :)
```

One simple way to avoid needing to write host or port numbers is to use shell aliases:
```bash
alias ch_client_prod-01='clickhouse client -h clickhouse-01 --port 29000'
alias ch_client_prod-02='clickhouse client -h clickhouse-02 --port 39000'
```

```bash
$ ch_client_prod-01 --query "Select 1"
1
```

You can check if your clusters are correctly configured from the clickhouse console:

```sql
:) select cluster, shard_num, replica_num, host_name, host_address, port, is_local from system.clusters

┌─cluster────┬─shard_num─┬─replica_num─┬─host_name─────┬─host_address─┬──port─┬─is_local─┐
│ tinybird   │         1 │           1 │ clickhouse-01 │ 127.0.0.1    │ 49000 │        1 │
│ tinybird   │         1 │           2 │ clickhouse-02 │ 127.0.0.1    │ 59000 │        0 │
│ tinybird_b │         1 │           1 │ clickhouse-01 │ 127.0.0.1    │ 49000 │        1 │
│ tinybird_b │         1 │           2 │ clickhouse-02 │ 127.0.0.1    │ 59000 │        0 │
└────────────┴───────────┴─────────────┴───────────────┴──────────────┴───────┴──────────┘
```


### Testing Code locally

1. Install testing dependencies

    ```bash
    pip install -e ".[test]"
    ```

2. Run the tests with [pytest](https://docs.pytest.org/en/stable/usage.html):

   * To run all tests

   ```bash
   # Note that this is very intensive and not a good test for 'is my new install working'
   pytest tests
   ```

   * There are several options, for example, testing a single file:

   ```bash
   pytest tests/views/test_api_datasources.py -vv
   ```

   * Running a single test:

   ```bash
   pytest tests/views/test_api_datasources.py -k test_name
   ```

### Starting the development environment

> Note: remember about setting the $PATH correctly with the version you want to use in the app, as it's explained above
> Note: If you are using VSCode or Pycharm or some other IDE you may want to set tinybird.app up as a Run configuration

```bash
tinybird_server --port 8001
```

* Using the *advanced* configuration from above:

```bash
PATH=$PATH:/home/Tinybird/ch-versions/22.8.11.15/usr/bin tinybird_server --port 8001
```

**Important note:** on macOS add `OBJC_DISABLE_INITIALIZE_FORK_SAFETY` as follows

```bash
OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES tinybird_server --port 8001
```

To stop the server and kill the running process, we suggest adding the following aliases:

```sh
alias tinybird_stop="ps -ef | grep 'tinybird_server' | grep -v grep | awk '{print $2}' | xargs kill -9"
alias tinybird_stop_python="ps -ef | grep 'analytics/.e/bin/python' | grep -v grep | awk '{print $2}' | xargs kill -9"
```

To start HFI server:
```bash
uvicorn tinybird.hfi.hfi:app --port 8042
```

### Useful commands

If running CH with docker, you can do the following to connect to ClickHouse client

```bash
docker exec -it tt ClickHouse client
```

### Configuring the metrics

If you've configured your clickhouse environment following the *advanced* steps, you should be able to activate the metrics by changing the `default_secrets.py` file adding: `metrics_cluster="metrics"`

## Developing in the UI

We encourage you to use **node** version 16 to have the same version that we use in production builds. Then, in the root of the project:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
nvm install 16
nvm use 16
```

Once Node is installed, run the setup in the code directory

```bash
pnpm run setup
```

If you want to make changes and check how they look:

```bash
pnpm run dev:watch
```

Don't forget to test your changes:

```bash
pnpm run test
```

Or test + watch 🤗:

```bash
pnpm run test:watch
```

If you want to clean your environment:

```bash
pnpm run clean
```

You have more information about development [here](development.md).

## FAQ

### Which ClickHouse version should I install?

That depends on your role. As a rule of thumb:

* If you are not a developer or don't want to do backend-related work. Download the recommended prebuilt release.

* If you are doing backend work, you should have available several different releases available for testing.
  See the official [prebuilt binaries](https://clickhouse.com/docs/en/getting-started/install/#from-tgz-archives).
  You should also have your own build copy of ClickHouse for testing and debugging purposes as explained [here](#installing-the-development-environment)

Finally, ClickHouse/master should be considered to be stable and fully compatible with Analytics. All tests should pass and everything work as expected.
If you detect any issue, please open a ticket and tag it as `ClickHouse Team`

### What do I do to validate my development environment is working correctly?

Browse to [http://localhost:8001/dashboard](http://localhost:8001/dashboard). You'll be prompted to login with your gmail account. Go back to /dashboard once you do and try importing

### I can't connect to ClickHouse with tinybird configuration

```bash
clickhouse client -h clickhouse-01 --port 29000
```

### Where is the marketing website code?

It is in [webflow](https://webflow.com/)

### Where is the blog hosted?

It is generated with Jekyll, and it is located in other [repository](https://gitlab.com/tinybird/blog).

### How can I see the documentation?

There is an automatic deploy job created so every time you merge something in master, if everything goes OK, the latest version of the documentation will be available at [https://docs.tinybird.co](https://docs.tinybird.co)

## Using native ClickHouse builds with macOS

Downloading the latest version of ClickHouse already compiled:

```bash
curl https://clickhouse.com/ | sh
chmod a+x ./clickhouse
```

## Debugging problems in gitlab CI

You can use `gitlab-runner` to execute any `.gitlab-ci.yml` job locally. Follow these steps to debug any of those jobs:

* Modify the `.gitlab-ci.yml` file, including `tail -f /dev/null` in the script section of the job
* Run the job you need with gitlab-runner, for instance: `gitlab-runner exec docker tests_integration_ch_207_py38`
* Wait until the container stops in `tail -f /dev/null`
* `docker ps` to list the name of the Docker container
* Open a shell session inside the container `docker exec -it <docker_name_from_previous_step> /bin/bash`
* Now you can run anything you need to debug, including breakpoints with pdb, etc.
* Once you finish stop the container `docker stop <docker_name>`

Note: If you do any modification to a project file, you need to commit it in order to be available in the Docker container. Once you finish you can squash all the commits.

## Adding distributed metrics

Read the [metrics](METRICS.md) guide.

## Changelog

We have a `CHANGELOG.md` file in the root of the project to document notable changes.

This file uses the `union` git merge strategy to avoid conflicts by taking all available options when some conflict happens. To add a new entry to the changelog and avoid duplicates and bad formatting, you need to take into account the following:

* Maintain the branch up to date with master so you can use the latest version of the changelog.
* There should be one entry in the changelog for each week. If the current week is not present, it should be added. Take into account that the changelog is ordered by date, so the latest entry should be at the top. This can lead to duplicates if someone else has added an entry for the current week. Be sure to check the last changes in master branch.
* Avoid reordering the changelog entries. If someone else updates the same lines, it will lead to duplicates and strange formatting. We should follow the next order: `Added`, `Changed`, `Deprecated`, `Fixed`, `Released`, `Removed`, `Security`.
* The changelog should be written in a way that it can be understood by a non-technical person.
* With every MR, a job will trigger to check if the changelog was updated. If it is not the case, the job will fail. There are a couple of exceptions to avoid this by adding the label `[changelog_not_needed]`:
  - The issue is not product related, but it is a pure engineering task.
  - The incoming code is under a feature flag and is not visible to the users.
