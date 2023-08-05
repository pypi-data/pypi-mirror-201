'''
# pgSTAC CDK construct

## Published Packages

* https://pypi.org/project/cdk-pgstac/
* https://www.npmjs.com/package/cdk-pgstac/

## Release

Versioning is automatically handled via [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) and [Semantic Release](https://semantic-release.gitbook.io/semantic-release/).

*Warning*: If you rebase `main`, you must ensure that the commits referenced by tags point to commits that are within the `main` branch. If a commit references a commit that is no longer on the `main` branch, Semantic Release will fail to detect the correct version of the project. [More information](https://github.com/semantic-release/semantic-release/issues/1121#issuecomment-517945233).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk
import aws_cdk.aws_apigateway
import aws_cdk.aws_dynamodb
import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_logs
import aws_cdk.aws_rds
import aws_cdk.aws_s3
import aws_cdk.aws_secretsmanager
import constructs


@jsii.data_type(
    jsii_type="cdk-pgstac.ApiEntrypoint",
    jsii_struct_bases=[],
    name_mapping={"entry": "entry", "handler": "handler", "index": "index"},
)
class ApiEntrypoint:
    def __init__(
        self,
        *,
        entry: builtins.str,
        handler: typing.Optional[builtins.str] = None,
        index: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param entry: (experimental) Path to the source of the function or the location for dependencies.
        :param handler: (experimental) The name of the exported handler in the index file.
        :param index: (experimental) The path (relative to entry) to the index file containing the exported handler.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(ApiEntrypoint.__init__)
            check_type(argname="argument entry", value=entry, expected_type=type_hints["entry"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        self._values: typing.Dict[str, typing.Any] = {
            "entry": entry,
        }
        if handler is not None:
            self._values["handler"] = handler
        if index is not None:
            self._values["index"] = index

    @builtins.property
    def entry(self) -> builtins.str:
        '''(experimental) Path to the source of the function or the location for dependencies.

        :stability: experimental
        '''
        result = self._values.get("entry")
        assert result is not None, "Required property 'entry' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def handler(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the exported handler in the index file.

        :stability: experimental
        '''
        result = self._values.get("handler")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def index(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path (relative to entry) to the index file containing the exported handler.

        :stability: experimental
        '''
        result = self._values.get("index")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiEntrypoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BastionHost(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-pgstac.BastionHost",
):
    '''(experimental) The database is located in an isolated subnet, meaning that it is not accessible from the public internet.

    As such, to interact with the database directly, a user must tunnel through a bastion host.


    Configuring

    This codebase controls *who* is allowed to connect to the bastion host. This requires two steps:

    1. Adding the IP address from which you are connecting to the ``ipv4Allowlist`` array
    2. Creating a bastion host system user by adding the user's configuration inform to ``userdata.yaml``



    Adding an IP address to the ``ipv4Allowlist`` array

    The ``BastionHost`` construct takes in an ``ipv4Allowlist`` array as an argument. Find your IP address (eg ``curl api.ipify.org``) and add that to the array along with the trailing CIDR block (likely ``/32`` to indicate that you are adding a single IP address).


    Creating a user via ``userdata.yaml``

    Add an entry to the ``users`` array with a username (likely matching your local systems username, which you can get by running the ``whoami`` command in your terminal) and a public key (likely your default public key, which you can get by running ``cat ~/.ssh/id_*.pub`` in your terminal).


    Tips & Tricks when using the Bastion Host

    **Connecting to RDS Instance via SSM*::

       aws ssm start-session --target $INSTANCE_ID \\
       --document-name AWS-StartPortForwardingSessionToRemoteHost \\
       --parameters '{
       "host": [
       "example-db.c5abcdefghij.us-west-2.rds.amazonaws.com"
       ],
       "portNumber": [
       "5432"
       ],
       "localPortNumber": [
       "9999"
       ]
       }' \\
       --profile $AWS_PROFILE

    Example::

       psql -h localhost -p 9999 # continue adding username (-U) and db (-d) here...

    Connect directly to Bastion Host::

       aws ssm start-session --target $INSTANCE_ID --profile $AWS_PROFILE

    **Setting up an SSH tunnel**

    In your ``~/.ssh/config`` file, add an entry like::

       Host db-tunnel
       Hostname {the-bastion-host-address}
       LocalForward 54322 {the-db-hostname}:5432

    Then a tunnel can be opened via::

       ssh -N db-tunnel

    And a connection to the DB can be made via::

       psql -h 127.0.0.1 -p 5433 -U {username} -d {database}

    **Handling ``REMOTE HOST IDENTIFICATION HAS CHANGED!`` error**

    If you've redeployed a bastion host that you've previously connected to, you may see an error like::

    :stability: experimental
    ::

    IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
    Someone could be eavesdropping on you right now (man-in-the-middle attack)!
    It is also possible that a host key has just been changed.
    The fingerprint for the ECDSA key sent by the remote host is
    SHA256:mPnxAOXTpb06PFgI1Qc8TMQ2e9b7goU8y2NdS5hzIr8.
    Please contact your system administrator.
    Add correct host key in /Users/username/.ssh/known_hosts to get rid of this message.
    Offending ECDSA key in /Users/username/.ssh/known_hosts:28
    ECDSA host key for ec2-12-34-56-789.us-west-2.compute.amazonaws.com has changed and you have requested strict checking.
    Host key verification failed::


    This is due to the server's fingerprint changing. We can scrub the fingerprint from our system with a command like:

    ssh-keygen -R 12.34.56.789 Example::
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        db: aws_cdk.aws_rds.IDatabaseInstance,
        ipv4_allowlist: typing.Sequence[builtins.str],
        user_data: aws_cdk.aws_ec2.UserData,
        vpc: aws_cdk.aws_ec2.IVpc,
        create_elastic_ip: typing.Optional[builtins.bool] = None,
        ssh_port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param db: 
        :param ipv4_allowlist: 
        :param user_data: 
        :param vpc: 
        :param create_elastic_ip: (experimental) Whether or not an elastic IP should be created for the bastion host. Default: false
        :param ssh_port: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(BastionHost.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = BastionHostProps(
            db=db,
            ipv4_allowlist=ipv4_allowlist,
            user_data=user_data,
            vpc=vpc,
            create_elastic_ip=create_elastic_ip,
            ssh_port=ssh_port,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> aws_cdk.aws_ec2.Instance:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_ec2.Instance, jsii.get(self, "instance"))

    @instance.setter
    def instance(self, value: aws_cdk.aws_ec2.Instance) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(BastionHost, "instance").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instance", value)


@jsii.data_type(
    jsii_type="cdk-pgstac.BastionHostProps",
    jsii_struct_bases=[],
    name_mapping={
        "db": "db",
        "ipv4_allowlist": "ipv4Allowlist",
        "user_data": "userData",
        "vpc": "vpc",
        "create_elastic_ip": "createElasticIp",
        "ssh_port": "sshPort",
    },
)
class BastionHostProps:
    def __init__(
        self,
        *,
        db: aws_cdk.aws_rds.IDatabaseInstance,
        ipv4_allowlist: typing.Sequence[builtins.str],
        user_data: aws_cdk.aws_ec2.UserData,
        vpc: aws_cdk.aws_ec2.IVpc,
        create_elastic_ip: typing.Optional[builtins.bool] = None,
        ssh_port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param db: 
        :param ipv4_allowlist: 
        :param user_data: 
        :param vpc: 
        :param create_elastic_ip: (experimental) Whether or not an elastic IP should be created for the bastion host. Default: false
        :param ssh_port: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(BastionHostProps.__init__)
            check_type(argname="argument db", value=db, expected_type=type_hints["db"])
            check_type(argname="argument ipv4_allowlist", value=ipv4_allowlist, expected_type=type_hints["ipv4_allowlist"])
            check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument create_elastic_ip", value=create_elastic_ip, expected_type=type_hints["create_elastic_ip"])
            check_type(argname="argument ssh_port", value=ssh_port, expected_type=type_hints["ssh_port"])
        self._values: typing.Dict[str, typing.Any] = {
            "db": db,
            "ipv4_allowlist": ipv4_allowlist,
            "user_data": user_data,
            "vpc": vpc,
        }
        if create_elastic_ip is not None:
            self._values["create_elastic_ip"] = create_elastic_ip
        if ssh_port is not None:
            self._values["ssh_port"] = ssh_port

    @builtins.property
    def db(self) -> aws_cdk.aws_rds.IDatabaseInstance:
        '''
        :stability: experimental
        '''
        result = self._values.get("db")
        assert result is not None, "Required property 'db' is missing"
        return typing.cast(aws_cdk.aws_rds.IDatabaseInstance, result)

    @builtins.property
    def ipv4_allowlist(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("ipv4_allowlist")
        assert result is not None, "Required property 'ipv4_allowlist' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def user_data(self) -> aws_cdk.aws_ec2.UserData:
        '''
        :stability: experimental
        '''
        result = self._values.get("user_data")
        assert result is not None, "Required property 'user_data' is missing"
        return typing.cast(aws_cdk.aws_ec2.UserData, result)

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''
        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    @builtins.property
    def create_elastic_ip(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not an elastic IP should be created for the bastion host.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("create_elastic_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ssh_port(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("ssh_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BastionHostProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BootstrapPgStac(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-pgstac.BootstrapPgStac",
):
    '''(experimental) Bootstraps a database instance, installing pgSTAC onto the database.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        database: typing.Union[aws_cdk.aws_rds.IDatabaseInstance, aws_cdk.aws_rds.DatabaseInstance],
        db_secret: aws_cdk.aws_secretsmanager.ISecret,
        pgstac_db_name: typing.Optional[builtins.str] = None,
        pgstac_username: typing.Optional[builtins.str] = None,
        pgstac_version: typing.Optional[builtins.str] = None,
        secrets_prefix: typing.Optional[builtins.str] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param database: (experimental) Database onto which pgSTAC should be installed.
        :param db_secret: (experimental) Secret containing valid connection details for the database instance. Secret must conform to the format of CDK's ``DatabaseInstance`` (i.e. a JSON object containing a ``username``, ``password``, ``host``, ``port``, and optionally a ``dbname``). If a ``dbname`` property is not specified within the secret, the bootstrapper will attempt to connect to a database with the name of ``"postgres"``.
        :param pgstac_db_name: (experimental) Name of database that is to be created and onto which pgSTAC will be installed. Default: pgstac
        :param pgstac_username: (experimental) Name of user that will be generated for connecting to the pgSTAC database. Default: pgstac_user
        :param pgstac_version: (experimental) pgSTAC version to be installed. Default: 0.6.8
        :param secrets_prefix: (experimental) Prefix to assign to the generated ``secrets_manager.Secret``. Default: pgstac
        :param vpc: (experimental) VPC in which the database resides. Note - Must be explicitely set if the ``database`` only conforms to the ``aws_rds.IDatabaseInstace`` interface (ie it is a reference to a database instance rather than a database instance.) Default: - ``vpc`` property of the ``database`` instance provided.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(BootstrapPgStac.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = BootstrapPgStacProps(
            database=database,
            db_secret=db_secret,
            pgstac_db_name=pgstac_db_name,
            pgstac_username=pgstac_username,
            pgstac_version=pgstac_version,
            secrets_prefix=secrets_prefix,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, jsii.get(self, "secret"))

    @secret.setter
    def secret(self, value: aws_cdk.aws_secretsmanager.ISecret) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(BootstrapPgStac, "secret").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value)


@jsii.data_type(
    jsii_type="cdk-pgstac.BootstrapPgStacProps",
    jsii_struct_bases=[],
    name_mapping={
        "database": "database",
        "db_secret": "dbSecret",
        "pgstac_db_name": "pgstacDbName",
        "pgstac_username": "pgstacUsername",
        "pgstac_version": "pgstacVersion",
        "secrets_prefix": "secretsPrefix",
        "vpc": "vpc",
    },
)
class BootstrapPgStacProps:
    def __init__(
        self,
        *,
        database: typing.Union[aws_cdk.aws_rds.IDatabaseInstance, aws_cdk.aws_rds.DatabaseInstance],
        db_secret: aws_cdk.aws_secretsmanager.ISecret,
        pgstac_db_name: typing.Optional[builtins.str] = None,
        pgstac_username: typing.Optional[builtins.str] = None,
        pgstac_version: typing.Optional[builtins.str] = None,
        secrets_prefix: typing.Optional[builtins.str] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        '''
        :param database: (experimental) Database onto which pgSTAC should be installed.
        :param db_secret: (experimental) Secret containing valid connection details for the database instance. Secret must conform to the format of CDK's ``DatabaseInstance`` (i.e. a JSON object containing a ``username``, ``password``, ``host``, ``port``, and optionally a ``dbname``). If a ``dbname`` property is not specified within the secret, the bootstrapper will attempt to connect to a database with the name of ``"postgres"``.
        :param pgstac_db_name: (experimental) Name of database that is to be created and onto which pgSTAC will be installed. Default: pgstac
        :param pgstac_username: (experimental) Name of user that will be generated for connecting to the pgSTAC database. Default: pgstac_user
        :param pgstac_version: (experimental) pgSTAC version to be installed. Default: 0.6.8
        :param secrets_prefix: (experimental) Prefix to assign to the generated ``secrets_manager.Secret``. Default: pgstac
        :param vpc: (experimental) VPC in which the database resides. Note - Must be explicitely set if the ``database`` only conforms to the ``aws_rds.IDatabaseInstace`` interface (ie it is a reference to a database instance rather than a database instance.) Default: - ``vpc`` property of the ``database`` instance provided.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(BootstrapPgStacProps.__init__)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument db_secret", value=db_secret, expected_type=type_hints["db_secret"])
            check_type(argname="argument pgstac_db_name", value=pgstac_db_name, expected_type=type_hints["pgstac_db_name"])
            check_type(argname="argument pgstac_username", value=pgstac_username, expected_type=type_hints["pgstac_username"])
            check_type(argname="argument pgstac_version", value=pgstac_version, expected_type=type_hints["pgstac_version"])
            check_type(argname="argument secrets_prefix", value=secrets_prefix, expected_type=type_hints["secrets_prefix"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[str, typing.Any] = {
            "database": database,
            "db_secret": db_secret,
        }
        if pgstac_db_name is not None:
            self._values["pgstac_db_name"] = pgstac_db_name
        if pgstac_username is not None:
            self._values["pgstac_username"] = pgstac_username
        if pgstac_version is not None:
            self._values["pgstac_version"] = pgstac_version
        if secrets_prefix is not None:
            self._values["secrets_prefix"] = secrets_prefix
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def database(
        self,
    ) -> typing.Union[aws_cdk.aws_rds.IDatabaseInstance, aws_cdk.aws_rds.DatabaseInstance]:
        '''(experimental) Database onto which pgSTAC should be installed.

        :stability: experimental
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(typing.Union[aws_cdk.aws_rds.IDatabaseInstance, aws_cdk.aws_rds.DatabaseInstance], result)

    @builtins.property
    def db_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''(experimental) Secret containing valid connection details for the database instance.

        Secret must
        conform to the format of CDK's ``DatabaseInstance`` (i.e. a JSON object containing a
        ``username``, ``password``, ``host``, ``port``, and optionally a ``dbname``). If a ``dbname``
        property is not specified within the secret, the bootstrapper will attempt to
        connect to a database with the name of ``"postgres"``.

        :stability: experimental
        '''
        result = self._values.get("db_secret")
        assert result is not None, "Required property 'db_secret' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    @builtins.property
    def pgstac_db_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of database that is to be created and onto which pgSTAC will be installed.

        :default: pgstac

        :stability: experimental
        '''
        result = self._values.get("pgstac_db_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pgstac_username(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of user that will be generated for connecting to the pgSTAC database.

        :default: pgstac_user

        :stability: experimental
        '''
        result = self._values.get("pgstac_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pgstac_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) pgSTAC version to be installed.

        :default: 0.6.8

        :stability: experimental
        '''
        result = self._values.get("pgstac_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secrets_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Prefix to assign to the generated ``secrets_manager.Secret``.

        :default: pgstac

        :stability: experimental
        '''
        result = self._values.get("secrets_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        '''(experimental) VPC in which the database resides.

        Note - Must be explicitely set if the ``database`` only conforms to the
        ``aws_rds.IDatabaseInstace`` interface (ie it is a reference to a database instance
        rather than a database instance.)

        :default: - ``vpc`` property of the ``database`` instance provided.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BootstrapPgStacProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pgstac.DatabaseParameters",
    jsii_struct_bases=[],
    name_mapping={
        "effective_cache_size": "effectiveCacheSize",
        "maintenance_work_mem": "maintenanceWorkMem",
        "max_connections": "maxConnections",
        "max_locks_per_transaction": "maxLocksPerTransaction",
        "random_page_cost": "randomPageCost",
        "seq_page_cost": "seqPageCost",
        "shared_buffers": "sharedBuffers",
        "temp_buffers": "tempBuffers",
        "work_mem": "workMem",
    },
)
class DatabaseParameters:
    def __init__(
        self,
        *,
        effective_cache_size: builtins.str,
        maintenance_work_mem: builtins.str,
        max_connections: builtins.str,
        max_locks_per_transaction: builtins.str,
        random_page_cost: builtins.str,
        seq_page_cost: builtins.str,
        shared_buffers: builtins.str,
        temp_buffers: builtins.str,
        work_mem: builtins.str,
    ) -> None:
        '''
        :param effective_cache_size: Default: - 75% of instance memory
        :param maintenance_work_mem: Default: - 25% of shared buffers
        :param max_connections: Default: - LEAST({DBInstanceClassMemory/9531392}, 5000)
        :param max_locks_per_transaction: Default: 1024
        :param random_page_cost: Default: 1.1
        :param seq_page_cost: Default: 1
        :param shared_buffers: (experimental) Note: This value is measured in 8KB blocks. Default: '{DBInstanceClassMemory/32768}' 25% of instance memory, ie ``{(DBInstanceClassMemory/(1024*8)) * 0.25}``
        :param temp_buffers: Default: 131172 (128 * 1024)
        :param work_mem: Default: - shared buffers divided by max connections

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DatabaseParameters.__init__)
            check_type(argname="argument effective_cache_size", value=effective_cache_size, expected_type=type_hints["effective_cache_size"])
            check_type(argname="argument maintenance_work_mem", value=maintenance_work_mem, expected_type=type_hints["maintenance_work_mem"])
            check_type(argname="argument max_connections", value=max_connections, expected_type=type_hints["max_connections"])
            check_type(argname="argument max_locks_per_transaction", value=max_locks_per_transaction, expected_type=type_hints["max_locks_per_transaction"])
            check_type(argname="argument random_page_cost", value=random_page_cost, expected_type=type_hints["random_page_cost"])
            check_type(argname="argument seq_page_cost", value=seq_page_cost, expected_type=type_hints["seq_page_cost"])
            check_type(argname="argument shared_buffers", value=shared_buffers, expected_type=type_hints["shared_buffers"])
            check_type(argname="argument temp_buffers", value=temp_buffers, expected_type=type_hints["temp_buffers"])
            check_type(argname="argument work_mem", value=work_mem, expected_type=type_hints["work_mem"])
        self._values: typing.Dict[str, typing.Any] = {
            "effective_cache_size": effective_cache_size,
            "maintenance_work_mem": maintenance_work_mem,
            "max_connections": max_connections,
            "max_locks_per_transaction": max_locks_per_transaction,
            "random_page_cost": random_page_cost,
            "seq_page_cost": seq_page_cost,
            "shared_buffers": shared_buffers,
            "temp_buffers": temp_buffers,
            "work_mem": work_mem,
        }

    @builtins.property
    def effective_cache_size(self) -> builtins.str:
        '''
        :default: - 75% of instance memory

        :stability: experimental
        '''
        result = self._values.get("effective_cache_size")
        assert result is not None, "Required property 'effective_cache_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def maintenance_work_mem(self) -> builtins.str:
        '''
        :default: - 25% of shared buffers

        :stability: experimental
        '''
        result = self._values.get("maintenance_work_mem")
        assert result is not None, "Required property 'maintenance_work_mem' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_connections(self) -> builtins.str:
        '''
        :default: - LEAST({DBInstanceClassMemory/9531392}, 5000)

        :stability: experimental
        '''
        result = self._values.get("max_connections")
        assert result is not None, "Required property 'max_connections' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_locks_per_transaction(self) -> builtins.str:
        '''
        :default: 1024

        :stability: experimental
        '''
        result = self._values.get("max_locks_per_transaction")
        assert result is not None, "Required property 'max_locks_per_transaction' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def random_page_cost(self) -> builtins.str:
        '''
        :default: 1.1

        :stability: experimental
        '''
        result = self._values.get("random_page_cost")
        assert result is not None, "Required property 'random_page_cost' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def seq_page_cost(self) -> builtins.str:
        '''
        :default: 1

        :stability: experimental
        '''
        result = self._values.get("seq_page_cost")
        assert result is not None, "Required property 'seq_page_cost' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def shared_buffers(self) -> builtins.str:
        '''(experimental) Note: This value is measured in 8KB blocks.

        :default: '{DBInstanceClassMemory/32768}' 25% of instance memory, ie ``{(DBInstanceClassMemory/(1024*8)) * 0.25}``

        :stability: experimental
        '''
        result = self._values.get("shared_buffers")
        assert result is not None, "Required property 'shared_buffers' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def temp_buffers(self) -> builtins.str:
        '''
        :default: 131172 (128 * 1024)

        :stability: experimental
        '''
        result = self._values.get("temp_buffers")
        assert result is not None, "Required property 'temp_buffers' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def work_mem(self) -> builtins.str:
        '''
        :default: - shared buffers divided by max connections

        :stability: experimental
        '''
        result = self._values.get("work_mem")
        assert result is not None, "Required property 'work_mem' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PgStacApiLambda(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-pgstac.PgStacApiLambda",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        db: aws_cdk.aws_rds.IDatabaseInstance,
        db_secret: aws_cdk.aws_secretsmanager.ISecret,
        subnet_selection: typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]],
        vpc: aws_cdk.aws_ec2.IVpc,
        api_code: typing.Optional[typing.Union[ApiEntrypoint, typing.Dict[str, typing.Any]]] = None,
        api_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param db: (experimental) RDS Instance with installed pgSTAC.
        :param db_secret: (experimental) Secret containing connection information for pgSTAC database.
        :param subnet_selection: (experimental) Subnet into which the lambda should be deployed.
        :param vpc: (experimental) VPC into which the lambda should be deployed.
        :param api_code: (experimental) Custom code to run for fastapi-pgstac. Default: - simplified version of fastapi-pgstac
        :param api_env: (experimental) Customized environment variables to send to fastapi-pgstac runtime.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(PgStacApiLambda.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PgStacApiLambdaProps(
            db=db,
            db_secret=db_secret,
            subnet_selection=subnet_selection,
            vpc=vpc,
            api_code=api_code,
            api_env=api_env,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "url"))


@jsii.data_type(
    jsii_type="cdk-pgstac.PgStacApiLambdaProps",
    jsii_struct_bases=[],
    name_mapping={
        "db": "db",
        "db_secret": "dbSecret",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
        "api_code": "apiCode",
        "api_env": "apiEnv",
    },
)
class PgStacApiLambdaProps:
    def __init__(
        self,
        *,
        db: aws_cdk.aws_rds.IDatabaseInstance,
        db_secret: aws_cdk.aws_secretsmanager.ISecret,
        subnet_selection: typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]],
        vpc: aws_cdk.aws_ec2.IVpc,
        api_code: typing.Optional[typing.Union[ApiEntrypoint, typing.Dict[str, typing.Any]]] = None,
        api_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param db: (experimental) RDS Instance with installed pgSTAC.
        :param db_secret: (experimental) Secret containing connection information for pgSTAC database.
        :param subnet_selection: (experimental) Subnet into which the lambda should be deployed.
        :param vpc: (experimental) VPC into which the lambda should be deployed.
        :param api_code: (experimental) Custom code to run for fastapi-pgstac. Default: - simplified version of fastapi-pgstac
        :param api_env: (experimental) Customized environment variables to send to fastapi-pgstac runtime.

        :stability: experimental
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = aws_cdk.aws_ec2.SubnetSelection(**subnet_selection)
        if isinstance(api_code, dict):
            api_code = ApiEntrypoint(**api_code)
        if __debug__:
            type_hints = typing.get_type_hints(PgStacApiLambdaProps.__init__)
            check_type(argname="argument db", value=db, expected_type=type_hints["db"])
            check_type(argname="argument db_secret", value=db_secret, expected_type=type_hints["db_secret"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument api_code", value=api_code, expected_type=type_hints["api_code"])
            check_type(argname="argument api_env", value=api_env, expected_type=type_hints["api_env"])
        self._values: typing.Dict[str, typing.Any] = {
            "db": db,
            "db_secret": db_secret,
            "subnet_selection": subnet_selection,
            "vpc": vpc,
        }
        if api_code is not None:
            self._values["api_code"] = api_code
        if api_env is not None:
            self._values["api_env"] = api_env

    @builtins.property
    def db(self) -> aws_cdk.aws_rds.IDatabaseInstance:
        '''(experimental) RDS Instance with installed pgSTAC.

        :stability: experimental
        '''
        result = self._values.get("db")
        assert result is not None, "Required property 'db' is missing"
        return typing.cast(aws_cdk.aws_rds.IDatabaseInstance, result)

    @builtins.property
    def db_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''(experimental) Secret containing connection information for pgSTAC database.

        :stability: experimental
        '''
        result = self._values.get("db_secret")
        assert result is not None, "Required property 'db_secret' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    @builtins.property
    def subnet_selection(self) -> aws_cdk.aws_ec2.SubnetSelection:
        '''(experimental) Subnet into which the lambda should be deployed.

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        assert result is not None, "Required property 'subnet_selection' is missing"
        return typing.cast(aws_cdk.aws_ec2.SubnetSelection, result)

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''(experimental) VPC into which the lambda should be deployed.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    @builtins.property
    def api_code(self) -> typing.Optional[ApiEntrypoint]:
        '''(experimental) Custom code to run for fastapi-pgstac.

        :default: - simplified version of fastapi-pgstac

        :stability: experimental
        '''
        result = self._values.get("api_code")
        return typing.cast(typing.Optional[ApiEntrypoint], result)

    @builtins.property
    def api_env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Customized environment variables to send to fastapi-pgstac runtime.

        :stability: experimental
        '''
        result = self._values.get("api_env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PgStacApiLambdaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PgStacDatabase(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-pgstac.PgStacDatabase",
):
    '''(experimental) An RDS instance with pgSTAC installed.

    This is a wrapper around the
    ``rds.DatabaseInstance`` higher-level construct making use
    of the BootstrapPgStac construct.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        pgstac_db_name: typing.Optional[builtins.str] = None,
        pgstac_username: typing.Optional[builtins.str] = None,
        pgstac_version: typing.Optional[builtins.str] = None,
        secrets_prefix: typing.Optional[builtins.str] = None,
        character_set_name: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[aws_cdk.aws_rds.Credentials] = None,
        storage_encrypted: typing.Optional[builtins.bool] = None,
        storage_encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        engine: aws_cdk.aws_rds.IInstanceEngine,
        allocated_storage: typing.Optional[jsii.Number] = None,
        allow_major_version_upgrade: typing.Optional[builtins.bool] = None,
        database_name: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        license_model: typing.Optional[aws_cdk.aws_rds.LicenseModel] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timezone: typing.Optional[builtins.str] = None,
        vpc: aws_cdk.aws_ec2.IVpc,
        auto_minor_version_upgrade: typing.Optional[builtins.bool] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        backup_retention: typing.Optional[aws_cdk.Duration] = None,
        cloudwatch_logs_exports: typing.Optional[typing.Sequence[builtins.str]] = None,
        cloudwatch_logs_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
        cloudwatch_logs_retention_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        copy_tags_to_snapshot: typing.Optional[builtins.bool] = None,
        delete_automated_backups: typing.Optional[builtins.bool] = None,
        deletion_protection: typing.Optional[builtins.bool] = None,
        domain: typing.Optional[builtins.str] = None,
        domain_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        enable_performance_insights: typing.Optional[builtins.bool] = None,
        iam_authentication: typing.Optional[builtins.bool] = None,
        instance_identifier: typing.Optional[builtins.str] = None,
        iops: typing.Optional[jsii.Number] = None,
        max_allocated_storage: typing.Optional[jsii.Number] = None,
        monitoring_interval: typing.Optional[aws_cdk.Duration] = None,
        monitoring_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        multi_az: typing.Optional[builtins.bool] = None,
        option_group: typing.Optional[aws_cdk.aws_rds.IOptionGroup] = None,
        parameter_group: typing.Optional[aws_cdk.aws_rds.IParameterGroup] = None,
        performance_insight_encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        performance_insight_retention: typing.Optional[aws_cdk.aws_rds.PerformanceInsightRetention] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_backup_window: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        processor_features: typing.Optional[typing.Union[aws_cdk.aws_rds.ProcessorFeatures, typing.Dict[str, typing.Any]]] = None,
        publicly_accessible: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[aws_cdk.RemovalPolicy] = None,
        s3_export_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
        s3_export_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        s3_import_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
        s3_import_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        security_groups: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        storage_type: typing.Optional[aws_cdk.aws_rds.StorageType] = None,
        subnet_group: typing.Optional[aws_cdk.aws_rds.ISubnetGroup] = None,
        vpc_subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param pgstac_db_name: 
        :param pgstac_username: 
        :param pgstac_version: 
        :param secrets_prefix: 
        :param character_set_name: For supported engines, specifies the character set to associate with the DB instance. Default: - RDS default character set name
        :param credentials: Credentials for the administrative user. Default: - A username of 'admin' (or 'postgres' for PostgreSQL) and SecretsManager-generated password
        :param storage_encrypted: Indicates whether the DB instance is encrypted. Default: - true if storageEncryptionKey has been provided, false otherwise
        :param storage_encryption_key: The KMS key that's used to encrypt the DB instance. Default: - default master key if storageEncrypted is true, no key otherwise
        :param engine: The database engine.
        :param allocated_storage: The allocated storage size, specified in gibibytes (GiB). Default: 100
        :param allow_major_version_upgrade: Whether to allow major version upgrades. Default: false
        :param database_name: The name of the database. Default: - no name
        :param instance_type: The name of the compute and memory capacity for the instance. Default: - m5.large (or, more specifically, db.m5.large)
        :param license_model: The license model. Default: - RDS default license model
        :param parameters: The parameters in the DBParameterGroup to create automatically. You can only specify parameterGroup or parameters but not both. You need to use a versioned engine to auto-generate a DBParameterGroup. Default: - None
        :param timezone: The time zone of the instance. This is currently supported only by Microsoft Sql Server. Default: - RDS default timezone
        :param vpc: The VPC network where the DB subnet group should be created.
        :param auto_minor_version_upgrade: Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window. Default: true
        :param availability_zone: The name of the Availability Zone where the DB instance will be located. Default: - no preference
        :param backup_retention: The number of days during which automatic DB snapshots are retained. Set to zero to disable backups. When creating a read replica, you must enable automatic backups on the source database instance by setting the backup retention to a value other than zero. Default: - Duration.days(1) for source instances, disabled for read replicas
        :param cloudwatch_logs_exports: The list of log types that need to be enabled for exporting to CloudWatch Logs. Default: - no log exports
        :param cloudwatch_logs_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``Infinity``. Default: - logs never expire
        :param cloudwatch_logs_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - a new role is created.
        :param copy_tags_to_snapshot: Indicates whether to copy all of the user-defined tags from the DB instance to snapshots of the DB instance. Default: true
        :param delete_automated_backups: Indicates whether automated backups should be deleted or retained when you delete a DB instance. Default: false
        :param deletion_protection: Indicates whether the DB instance should have deletion protection enabled. Default: - true if ``removalPolicy`` is RETAIN, false otherwise
        :param domain: The Active Directory directory ID to create the DB instance in. Default: - Do not join domain
        :param domain_role: The IAM role to be used when making API calls to the Directory Service. The role needs the AWS-managed policy AmazonRDSDirectoryServiceAccess or equivalent. Default: - The role will be created for you if {@link DatabaseInstanceNewProps#domain} is specified
        :param enable_performance_insights: Whether to enable Performance Insights for the DB instance. Default: - false, unless ``performanceInsightRentention`` or ``performanceInsightEncryptionKey`` is set.
        :param iam_authentication: Whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts. Default: false
        :param instance_identifier: A name for the DB instance. If you specify a name, AWS CloudFormation converts it to lowercase. Default: - a CloudFormation generated name
        :param iops: The number of I/O operations per second (IOPS) that the database provisions. The value must be equal to or greater than 1000. Default: - no provisioned iops
        :param max_allocated_storage: Upper limit to which RDS can scale the storage in GiB(Gibibyte). Default: - No autoscaling of RDS instance
        :param monitoring_interval: The interval, in seconds, between points when Amazon RDS collects enhanced monitoring metrics for the DB instance. Default: - no enhanced monitoring
        :param monitoring_role: Role that will be used to manage DB instance monitoring. Default: - A role is automatically created for you
        :param multi_az: Specifies if the database instance is a multiple Availability Zone deployment. Default: false
        :param option_group: The option group to associate with the instance. Default: - no option group
        :param parameter_group: The DB parameter group to associate with the instance. Default: - no parameter group
        :param performance_insight_encryption_key: The AWS KMS key for encryption of Performance Insights data. Default: - default master key
        :param performance_insight_retention: The amount of time, in days, to retain Performance Insights data. Default: 7
        :param port: The port for the instance. Default: - the default port for the chosen engine.
        :param preferred_backup_window: The daily time range during which automated backups are performed. Constraints: - Must be in the format ``hh24:mi-hh24:mi``. - Must be in Universal Coordinated Time (UTC). - Must not conflict with the preferred maintenance window. - Must be at least 30 minutes. Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow
        :param preferred_maintenance_window: The weekly time range (in UTC) during which system maintenance can occur. Format: ``ddd:hh24:mi-ddd:hh24:mi`` Constraint: Minimum 30-minute window Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance
        :param processor_features: The number of CPU cores and the number of threads per core. Default: - the default number of CPU cores and threads per core for the chosen instance class. See https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html#USER_ConfigureProcessor
        :param publicly_accessible: Indicates whether the DB instance is an internet-facing instance. Default: - ``true`` if ``vpcSubnets`` is ``subnetType: SubnetType.PUBLIC``, ``false`` otherwise
        :param removal_policy: The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update. Default: - RemovalPolicy.SNAPSHOT (remove the resource, but retain a snapshot of the data)
        :param s3_export_buckets: S3 buckets that you want to load data into. This property must not be used if ``s3ExportRole`` is used. For Microsoft SQL Server: Default: - None
        :param s3_export_role: Role that will be associated with this DB instance to enable S3 export. This property must not be used if ``s3ExportBuckets`` is used. For Microsoft SQL Server: Default: - New role is created if ``s3ExportBuckets`` is set, no role is defined otherwise
        :param s3_import_buckets: S3 buckets that you want to load data from. This feature is only supported by the Microsoft SQL Server, Oracle, and PostgreSQL engines. This property must not be used if ``s3ImportRole`` is used. For Microsoft SQL Server: Default: - None
        :param s3_import_role: Role that will be associated with this DB instance to enable S3 import. This feature is only supported by the Microsoft SQL Server, Oracle, and PostgreSQL engines. This property must not be used if ``s3ImportBuckets`` is used. For Microsoft SQL Server: Default: - New role is created if ``s3ImportBuckets`` is set, no role is defined otherwise
        :param security_groups: The security groups to assign to the DB instance. Default: - a new security group is created
        :param storage_type: The storage type. Storage types supported are gp2, io1, standard. Default: GP2
        :param subnet_group: Existing subnet group for the instance. Default: - a new subnet group will be created.
        :param vpc_subnets: The type of subnets to add to the created DB subnet group. Default: - private subnets

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(PgStacDatabase.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PgStacDatabaseProps(
            pgstac_db_name=pgstac_db_name,
            pgstac_username=pgstac_username,
            pgstac_version=pgstac_version,
            secrets_prefix=secrets_prefix,
            character_set_name=character_set_name,
            credentials=credentials,
            storage_encrypted=storage_encrypted,
            storage_encryption_key=storage_encryption_key,
            engine=engine,
            allocated_storage=allocated_storage,
            allow_major_version_upgrade=allow_major_version_upgrade,
            database_name=database_name,
            instance_type=instance_type,
            license_model=license_model,
            parameters=parameters,
            timezone=timezone,
            vpc=vpc,
            auto_minor_version_upgrade=auto_minor_version_upgrade,
            availability_zone=availability_zone,
            backup_retention=backup_retention,
            cloudwatch_logs_exports=cloudwatch_logs_exports,
            cloudwatch_logs_retention=cloudwatch_logs_retention,
            cloudwatch_logs_retention_role=cloudwatch_logs_retention_role,
            copy_tags_to_snapshot=copy_tags_to_snapshot,
            delete_automated_backups=delete_automated_backups,
            deletion_protection=deletion_protection,
            domain=domain,
            domain_role=domain_role,
            enable_performance_insights=enable_performance_insights,
            iam_authentication=iam_authentication,
            instance_identifier=instance_identifier,
            iops=iops,
            max_allocated_storage=max_allocated_storage,
            monitoring_interval=monitoring_interval,
            monitoring_role=monitoring_role,
            multi_az=multi_az,
            option_group=option_group,
            parameter_group=parameter_group,
            performance_insight_encryption_key=performance_insight_encryption_key,
            performance_insight_retention=performance_insight_retention,
            port=port,
            preferred_backup_window=preferred_backup_window,
            preferred_maintenance_window=preferred_maintenance_window,
            processor_features=processor_features,
            publicly_accessible=publicly_accessible,
            removal_policy=removal_policy,
            s3_export_buckets=s3_export_buckets,
            s3_export_role=s3_export_role,
            s3_import_buckets=s3_import_buckets,
            s3_import_role=s3_import_role,
            security_groups=security_groups,
            storage_type=storage_type,
            subnet_group=subnet_group,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="getParameters")
    def get_parameters(
        self,
        instance_type: builtins.str,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> DatabaseParameters:
        '''
        :param instance_type: -
        :param parameters: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(PgStacDatabase.get_parameters)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        return typing.cast(DatabaseParameters, jsii.invoke(self, "getParameters", [instance_type, parameters]))

    @builtins.property
    @jsii.member(jsii_name="db")
    def db(self) -> aws_cdk.aws_rds.DatabaseInstance:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_rds.DatabaseInstance, jsii.get(self, "db"))

    @db.setter
    def db(self, value: aws_cdk.aws_rds.DatabaseInstance) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(PgStacDatabase, "db").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "db", value)

    @builtins.property
    @jsii.member(jsii_name="pgstacSecret")
    def pgstac_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, jsii.get(self, "pgstacSecret"))

    @pgstac_secret.setter
    def pgstac_secret(self, value: aws_cdk.aws_secretsmanager.ISecret) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(PgStacDatabase, "pgstac_secret").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pgstacSecret", value)


@jsii.data_type(
    jsii_type="cdk-pgstac.PgStacDatabaseProps",
    jsii_struct_bases=[aws_cdk.aws_rds.DatabaseInstanceProps],
    name_mapping={
        "vpc": "vpc",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "availability_zone": "availabilityZone",
        "backup_retention": "backupRetention",
        "cloudwatch_logs_exports": "cloudwatchLogsExports",
        "cloudwatch_logs_retention": "cloudwatchLogsRetention",
        "cloudwatch_logs_retention_role": "cloudwatchLogsRetentionRole",
        "copy_tags_to_snapshot": "copyTagsToSnapshot",
        "delete_automated_backups": "deleteAutomatedBackups",
        "deletion_protection": "deletionProtection",
        "domain": "domain",
        "domain_role": "domainRole",
        "enable_performance_insights": "enablePerformanceInsights",
        "iam_authentication": "iamAuthentication",
        "instance_identifier": "instanceIdentifier",
        "iops": "iops",
        "max_allocated_storage": "maxAllocatedStorage",
        "monitoring_interval": "monitoringInterval",
        "monitoring_role": "monitoringRole",
        "multi_az": "multiAz",
        "option_group": "optionGroup",
        "parameter_group": "parameterGroup",
        "performance_insight_encryption_key": "performanceInsightEncryptionKey",
        "performance_insight_retention": "performanceInsightRetention",
        "port": "port",
        "preferred_backup_window": "preferredBackupWindow",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "processor_features": "processorFeatures",
        "publicly_accessible": "publiclyAccessible",
        "removal_policy": "removalPolicy",
        "s3_export_buckets": "s3ExportBuckets",
        "s3_export_role": "s3ExportRole",
        "s3_import_buckets": "s3ImportBuckets",
        "s3_import_role": "s3ImportRole",
        "security_groups": "securityGroups",
        "storage_type": "storageType",
        "subnet_group": "subnetGroup",
        "vpc_subnets": "vpcSubnets",
        "engine": "engine",
        "allocated_storage": "allocatedStorage",
        "allow_major_version_upgrade": "allowMajorVersionUpgrade",
        "database_name": "databaseName",
        "instance_type": "instanceType",
        "license_model": "licenseModel",
        "parameters": "parameters",
        "timezone": "timezone",
        "character_set_name": "characterSetName",
        "credentials": "credentials",
        "storage_encrypted": "storageEncrypted",
        "storage_encryption_key": "storageEncryptionKey",
        "pgstac_db_name": "pgstacDbName",
        "pgstac_username": "pgstacUsername",
        "pgstac_version": "pgstacVersion",
        "secrets_prefix": "secretsPrefix",
    },
)
class PgStacDatabaseProps(aws_cdk.aws_rds.DatabaseInstanceProps):
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        auto_minor_version_upgrade: typing.Optional[builtins.bool] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        backup_retention: typing.Optional[aws_cdk.Duration] = None,
        cloudwatch_logs_exports: typing.Optional[typing.Sequence[builtins.str]] = None,
        cloudwatch_logs_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
        cloudwatch_logs_retention_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        copy_tags_to_snapshot: typing.Optional[builtins.bool] = None,
        delete_automated_backups: typing.Optional[builtins.bool] = None,
        deletion_protection: typing.Optional[builtins.bool] = None,
        domain: typing.Optional[builtins.str] = None,
        domain_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        enable_performance_insights: typing.Optional[builtins.bool] = None,
        iam_authentication: typing.Optional[builtins.bool] = None,
        instance_identifier: typing.Optional[builtins.str] = None,
        iops: typing.Optional[jsii.Number] = None,
        max_allocated_storage: typing.Optional[jsii.Number] = None,
        monitoring_interval: typing.Optional[aws_cdk.Duration] = None,
        monitoring_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        multi_az: typing.Optional[builtins.bool] = None,
        option_group: typing.Optional[aws_cdk.aws_rds.IOptionGroup] = None,
        parameter_group: typing.Optional[aws_cdk.aws_rds.IParameterGroup] = None,
        performance_insight_encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        performance_insight_retention: typing.Optional[aws_cdk.aws_rds.PerformanceInsightRetention] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_backup_window: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        processor_features: typing.Optional[typing.Union[aws_cdk.aws_rds.ProcessorFeatures, typing.Dict[str, typing.Any]]] = None,
        publicly_accessible: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[aws_cdk.RemovalPolicy] = None,
        s3_export_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
        s3_export_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        s3_import_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
        s3_import_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        security_groups: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        storage_type: typing.Optional[aws_cdk.aws_rds.StorageType] = None,
        subnet_group: typing.Optional[aws_cdk.aws_rds.ISubnetGroup] = None,
        vpc_subnets: typing.Optional[typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]]] = None,
        engine: aws_cdk.aws_rds.IInstanceEngine,
        allocated_storage: typing.Optional[jsii.Number] = None,
        allow_major_version_upgrade: typing.Optional[builtins.bool] = None,
        database_name: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        license_model: typing.Optional[aws_cdk.aws_rds.LicenseModel] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timezone: typing.Optional[builtins.str] = None,
        character_set_name: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[aws_cdk.aws_rds.Credentials] = None,
        storage_encrypted: typing.Optional[builtins.bool] = None,
        storage_encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        pgstac_db_name: typing.Optional[builtins.str] = None,
        pgstac_username: typing.Optional[builtins.str] = None,
        pgstac_version: typing.Optional[builtins.str] = None,
        secrets_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param vpc: The VPC network where the DB subnet group should be created.
        :param auto_minor_version_upgrade: Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window. Default: true
        :param availability_zone: The name of the Availability Zone where the DB instance will be located. Default: - no preference
        :param backup_retention: The number of days during which automatic DB snapshots are retained. Set to zero to disable backups. When creating a read replica, you must enable automatic backups on the source database instance by setting the backup retention to a value other than zero. Default: - Duration.days(1) for source instances, disabled for read replicas
        :param cloudwatch_logs_exports: The list of log types that need to be enabled for exporting to CloudWatch Logs. Default: - no log exports
        :param cloudwatch_logs_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``Infinity``. Default: - logs never expire
        :param cloudwatch_logs_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - a new role is created.
        :param copy_tags_to_snapshot: Indicates whether to copy all of the user-defined tags from the DB instance to snapshots of the DB instance. Default: true
        :param delete_automated_backups: Indicates whether automated backups should be deleted or retained when you delete a DB instance. Default: false
        :param deletion_protection: Indicates whether the DB instance should have deletion protection enabled. Default: - true if ``removalPolicy`` is RETAIN, false otherwise
        :param domain: The Active Directory directory ID to create the DB instance in. Default: - Do not join domain
        :param domain_role: The IAM role to be used when making API calls to the Directory Service. The role needs the AWS-managed policy AmazonRDSDirectoryServiceAccess or equivalent. Default: - The role will be created for you if {@link DatabaseInstanceNewProps#domain} is specified
        :param enable_performance_insights: Whether to enable Performance Insights for the DB instance. Default: - false, unless ``performanceInsightRentention`` or ``performanceInsightEncryptionKey`` is set.
        :param iam_authentication: Whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts. Default: false
        :param instance_identifier: A name for the DB instance. If you specify a name, AWS CloudFormation converts it to lowercase. Default: - a CloudFormation generated name
        :param iops: The number of I/O operations per second (IOPS) that the database provisions. The value must be equal to or greater than 1000. Default: - no provisioned iops
        :param max_allocated_storage: Upper limit to which RDS can scale the storage in GiB(Gibibyte). Default: - No autoscaling of RDS instance
        :param monitoring_interval: The interval, in seconds, between points when Amazon RDS collects enhanced monitoring metrics for the DB instance. Default: - no enhanced monitoring
        :param monitoring_role: Role that will be used to manage DB instance monitoring. Default: - A role is automatically created for you
        :param multi_az: Specifies if the database instance is a multiple Availability Zone deployment. Default: false
        :param option_group: The option group to associate with the instance. Default: - no option group
        :param parameter_group: The DB parameter group to associate with the instance. Default: - no parameter group
        :param performance_insight_encryption_key: The AWS KMS key for encryption of Performance Insights data. Default: - default master key
        :param performance_insight_retention: The amount of time, in days, to retain Performance Insights data. Default: 7
        :param port: The port for the instance. Default: - the default port for the chosen engine.
        :param preferred_backup_window: The daily time range during which automated backups are performed. Constraints: - Must be in the format ``hh24:mi-hh24:mi``. - Must be in Universal Coordinated Time (UTC). - Must not conflict with the preferred maintenance window. - Must be at least 30 minutes. Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow
        :param preferred_maintenance_window: The weekly time range (in UTC) during which system maintenance can occur. Format: ``ddd:hh24:mi-ddd:hh24:mi`` Constraint: Minimum 30-minute window Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance
        :param processor_features: The number of CPU cores and the number of threads per core. Default: - the default number of CPU cores and threads per core for the chosen instance class. See https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html#USER_ConfigureProcessor
        :param publicly_accessible: Indicates whether the DB instance is an internet-facing instance. Default: - ``true`` if ``vpcSubnets`` is ``subnetType: SubnetType.PUBLIC``, ``false`` otherwise
        :param removal_policy: The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update. Default: - RemovalPolicy.SNAPSHOT (remove the resource, but retain a snapshot of the data)
        :param s3_export_buckets: S3 buckets that you want to load data into. This property must not be used if ``s3ExportRole`` is used. For Microsoft SQL Server: Default: - None
        :param s3_export_role: Role that will be associated with this DB instance to enable S3 export. This property must not be used if ``s3ExportBuckets`` is used. For Microsoft SQL Server: Default: - New role is created if ``s3ExportBuckets`` is set, no role is defined otherwise
        :param s3_import_buckets: S3 buckets that you want to load data from. This feature is only supported by the Microsoft SQL Server, Oracle, and PostgreSQL engines. This property must not be used if ``s3ImportRole`` is used. For Microsoft SQL Server: Default: - None
        :param s3_import_role: Role that will be associated with this DB instance to enable S3 import. This feature is only supported by the Microsoft SQL Server, Oracle, and PostgreSQL engines. This property must not be used if ``s3ImportBuckets`` is used. For Microsoft SQL Server: Default: - New role is created if ``s3ImportBuckets`` is set, no role is defined otherwise
        :param security_groups: The security groups to assign to the DB instance. Default: - a new security group is created
        :param storage_type: The storage type. Storage types supported are gp2, io1, standard. Default: GP2
        :param subnet_group: Existing subnet group for the instance. Default: - a new subnet group will be created.
        :param vpc_subnets: The type of subnets to add to the created DB subnet group. Default: - private subnets
        :param engine: The database engine.
        :param allocated_storage: The allocated storage size, specified in gibibytes (GiB). Default: 100
        :param allow_major_version_upgrade: Whether to allow major version upgrades. Default: false
        :param database_name: The name of the database. Default: - no name
        :param instance_type: The name of the compute and memory capacity for the instance. Default: - m5.large (or, more specifically, db.m5.large)
        :param license_model: The license model. Default: - RDS default license model
        :param parameters: The parameters in the DBParameterGroup to create automatically. You can only specify parameterGroup or parameters but not both. You need to use a versioned engine to auto-generate a DBParameterGroup. Default: - None
        :param timezone: The time zone of the instance. This is currently supported only by Microsoft Sql Server. Default: - RDS default timezone
        :param character_set_name: For supported engines, specifies the character set to associate with the DB instance. Default: - RDS default character set name
        :param credentials: Credentials for the administrative user. Default: - A username of 'admin' (or 'postgres' for PostgreSQL) and SecretsManager-generated password
        :param storage_encrypted: Indicates whether the DB instance is encrypted. Default: - true if storageEncryptionKey has been provided, false otherwise
        :param storage_encryption_key: The KMS key that's used to encrypt the DB instance. Default: - default master key if storageEncrypted is true, no key otherwise
        :param pgstac_db_name: 
        :param pgstac_username: 
        :param pgstac_version: 
        :param secrets_prefix: 

        :stability: experimental
        '''
        if isinstance(processor_features, dict):
            processor_features = aws_cdk.aws_rds.ProcessorFeatures(**processor_features)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(PgStacDatabaseProps.__init__)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument auto_minor_version_upgrade", value=auto_minor_version_upgrade, expected_type=type_hints["auto_minor_version_upgrade"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument backup_retention", value=backup_retention, expected_type=type_hints["backup_retention"])
            check_type(argname="argument cloudwatch_logs_exports", value=cloudwatch_logs_exports, expected_type=type_hints["cloudwatch_logs_exports"])
            check_type(argname="argument cloudwatch_logs_retention", value=cloudwatch_logs_retention, expected_type=type_hints["cloudwatch_logs_retention"])
            check_type(argname="argument cloudwatch_logs_retention_role", value=cloudwatch_logs_retention_role, expected_type=type_hints["cloudwatch_logs_retention_role"])
            check_type(argname="argument copy_tags_to_snapshot", value=copy_tags_to_snapshot, expected_type=type_hints["copy_tags_to_snapshot"])
            check_type(argname="argument delete_automated_backups", value=delete_automated_backups, expected_type=type_hints["delete_automated_backups"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument domain_role", value=domain_role, expected_type=type_hints["domain_role"])
            check_type(argname="argument enable_performance_insights", value=enable_performance_insights, expected_type=type_hints["enable_performance_insights"])
            check_type(argname="argument iam_authentication", value=iam_authentication, expected_type=type_hints["iam_authentication"])
            check_type(argname="argument instance_identifier", value=instance_identifier, expected_type=type_hints["instance_identifier"])
            check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
            check_type(argname="argument max_allocated_storage", value=max_allocated_storage, expected_type=type_hints["max_allocated_storage"])
            check_type(argname="argument monitoring_interval", value=monitoring_interval, expected_type=type_hints["monitoring_interval"])
            check_type(argname="argument monitoring_role", value=monitoring_role, expected_type=type_hints["monitoring_role"])
            check_type(argname="argument multi_az", value=multi_az, expected_type=type_hints["multi_az"])
            check_type(argname="argument option_group", value=option_group, expected_type=type_hints["option_group"])
            check_type(argname="argument parameter_group", value=parameter_group, expected_type=type_hints["parameter_group"])
            check_type(argname="argument performance_insight_encryption_key", value=performance_insight_encryption_key, expected_type=type_hints["performance_insight_encryption_key"])
            check_type(argname="argument performance_insight_retention", value=performance_insight_retention, expected_type=type_hints["performance_insight_retention"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument preferred_backup_window", value=preferred_backup_window, expected_type=type_hints["preferred_backup_window"])
            check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
            check_type(argname="argument processor_features", value=processor_features, expected_type=type_hints["processor_features"])
            check_type(argname="argument publicly_accessible", value=publicly_accessible, expected_type=type_hints["publicly_accessible"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument s3_export_buckets", value=s3_export_buckets, expected_type=type_hints["s3_export_buckets"])
            check_type(argname="argument s3_export_role", value=s3_export_role, expected_type=type_hints["s3_export_role"])
            check_type(argname="argument s3_import_buckets", value=s3_import_buckets, expected_type=type_hints["s3_import_buckets"])
            check_type(argname="argument s3_import_role", value=s3_import_role, expected_type=type_hints["s3_import_role"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument storage_type", value=storage_type, expected_type=type_hints["storage_type"])
            check_type(argname="argument subnet_group", value=subnet_group, expected_type=type_hints["subnet_group"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument allocated_storage", value=allocated_storage, expected_type=type_hints["allocated_storage"])
            check_type(argname="argument allow_major_version_upgrade", value=allow_major_version_upgrade, expected_type=type_hints["allow_major_version_upgrade"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument license_model", value=license_model, expected_type=type_hints["license_model"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
            check_type(argname="argument character_set_name", value=character_set_name, expected_type=type_hints["character_set_name"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument storage_encrypted", value=storage_encrypted, expected_type=type_hints["storage_encrypted"])
            check_type(argname="argument storage_encryption_key", value=storage_encryption_key, expected_type=type_hints["storage_encryption_key"])
            check_type(argname="argument pgstac_db_name", value=pgstac_db_name, expected_type=type_hints["pgstac_db_name"])
            check_type(argname="argument pgstac_username", value=pgstac_username, expected_type=type_hints["pgstac_username"])
            check_type(argname="argument pgstac_version", value=pgstac_version, expected_type=type_hints["pgstac_version"])
            check_type(argname="argument secrets_prefix", value=secrets_prefix, expected_type=type_hints["secrets_prefix"])
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
            "engine": engine,
        }
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if backup_retention is not None:
            self._values["backup_retention"] = backup_retention
        if cloudwatch_logs_exports is not None:
            self._values["cloudwatch_logs_exports"] = cloudwatch_logs_exports
        if cloudwatch_logs_retention is not None:
            self._values["cloudwatch_logs_retention"] = cloudwatch_logs_retention
        if cloudwatch_logs_retention_role is not None:
            self._values["cloudwatch_logs_retention_role"] = cloudwatch_logs_retention_role
        if copy_tags_to_snapshot is not None:
            self._values["copy_tags_to_snapshot"] = copy_tags_to_snapshot
        if delete_automated_backups is not None:
            self._values["delete_automated_backups"] = delete_automated_backups
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if domain is not None:
            self._values["domain"] = domain
        if domain_role is not None:
            self._values["domain_role"] = domain_role
        if enable_performance_insights is not None:
            self._values["enable_performance_insights"] = enable_performance_insights
        if iam_authentication is not None:
            self._values["iam_authentication"] = iam_authentication
        if instance_identifier is not None:
            self._values["instance_identifier"] = instance_identifier
        if iops is not None:
            self._values["iops"] = iops
        if max_allocated_storage is not None:
            self._values["max_allocated_storage"] = max_allocated_storage
        if monitoring_interval is not None:
            self._values["monitoring_interval"] = monitoring_interval
        if monitoring_role is not None:
            self._values["monitoring_role"] = monitoring_role
        if multi_az is not None:
            self._values["multi_az"] = multi_az
        if option_group is not None:
            self._values["option_group"] = option_group
        if parameter_group is not None:
            self._values["parameter_group"] = parameter_group
        if performance_insight_encryption_key is not None:
            self._values["performance_insight_encryption_key"] = performance_insight_encryption_key
        if performance_insight_retention is not None:
            self._values["performance_insight_retention"] = performance_insight_retention
        if port is not None:
            self._values["port"] = port
        if preferred_backup_window is not None:
            self._values["preferred_backup_window"] = preferred_backup_window
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if processor_features is not None:
            self._values["processor_features"] = processor_features
        if publicly_accessible is not None:
            self._values["publicly_accessible"] = publicly_accessible
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if s3_export_buckets is not None:
            self._values["s3_export_buckets"] = s3_export_buckets
        if s3_export_role is not None:
            self._values["s3_export_role"] = s3_export_role
        if s3_import_buckets is not None:
            self._values["s3_import_buckets"] = s3_import_buckets
        if s3_import_role is not None:
            self._values["s3_import_role"] = s3_import_role
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if storage_type is not None:
            self._values["storage_type"] = storage_type
        if subnet_group is not None:
            self._values["subnet_group"] = subnet_group
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if allocated_storage is not None:
            self._values["allocated_storage"] = allocated_storage
        if allow_major_version_upgrade is not None:
            self._values["allow_major_version_upgrade"] = allow_major_version_upgrade
        if database_name is not None:
            self._values["database_name"] = database_name
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if license_model is not None:
            self._values["license_model"] = license_model
        if parameters is not None:
            self._values["parameters"] = parameters
        if timezone is not None:
            self._values["timezone"] = timezone
        if character_set_name is not None:
            self._values["character_set_name"] = character_set_name
        if credentials is not None:
            self._values["credentials"] = credentials
        if storage_encrypted is not None:
            self._values["storage_encrypted"] = storage_encrypted
        if storage_encryption_key is not None:
            self._values["storage_encryption_key"] = storage_encryption_key
        if pgstac_db_name is not None:
            self._values["pgstac_db_name"] = pgstac_db_name
        if pgstac_username is not None:
            self._values["pgstac_username"] = pgstac_username
        if pgstac_version is not None:
            self._values["pgstac_version"] = pgstac_version
        if secrets_prefix is not None:
            self._values["secrets_prefix"] = secrets_prefix

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''The VPC network where the DB subnet group should be created.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    @builtins.property
    def auto_minor_version_upgrade(self) -> typing.Optional[builtins.bool]:
        '''Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window.

        :default: true
        '''
        result = self._values.get("auto_minor_version_upgrade")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The name of the Availability Zone where the DB instance will be located.

        :default: - no preference
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup_retention(self) -> typing.Optional[aws_cdk.Duration]:
        '''The number of days during which automatic DB snapshots are retained.

        Set to zero to disable backups.
        When creating a read replica, you must enable automatic backups on the source
        database instance by setting the backup retention to a value other than zero.

        :default: - Duration.days(1) for source instances, disabled for read replicas
        '''
        result = self._values.get("backup_retention")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def cloudwatch_logs_exports(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of log types that need to be enabled for exporting to CloudWatch Logs.

        :default: - no log exports
        '''
        result = self._values.get("cloudwatch_logs_exports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cloudwatch_logs_retention(
        self,
    ) -> typing.Optional[aws_cdk.aws_logs.RetentionDays]:
        '''The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``Infinity``.

        :default: - logs never expire
        '''
        result = self._values.get("cloudwatch_logs_retention")
        return typing.cast(typing.Optional[aws_cdk.aws_logs.RetentionDays], result)

    @builtins.property
    def cloudwatch_logs_retention_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        :default: - a new role is created.
        '''
        result = self._values.get("cloudwatch_logs_retention_role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    @builtins.property
    def copy_tags_to_snapshot(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether to copy all of the user-defined tags from the DB instance to snapshots of the DB instance.

        :default: true
        '''
        result = self._values.get("copy_tags_to_snapshot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def delete_automated_backups(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether automated backups should be deleted or retained when you delete a DB instance.

        :default: false
        '''
        result = self._values.get("delete_automated_backups")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def deletion_protection(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the DB instance should have deletion protection enabled.

        :default: - true if ``removalPolicy`` is RETAIN, false otherwise
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''The Active Directory directory ID to create the DB instance in.

        :default: - Do not join domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''The IAM role to be used when making API calls to the Directory Service.

        The role needs the AWS-managed policy
        AmazonRDSDirectoryServiceAccess or equivalent.

        :default: - The role will be created for you if {@link DatabaseInstanceNewProps#domain} is specified
        '''
        result = self._values.get("domain_role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    @builtins.property
    def enable_performance_insights(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable Performance Insights for the DB instance.

        :default: - false, unless ``performanceInsightRentention`` or ``performanceInsightEncryptionKey`` is set.
        '''
        result = self._values.get("enable_performance_insights")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def iam_authentication(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts.

        :default: false
        '''
        result = self._values.get("iam_authentication")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def instance_identifier(self) -> typing.Optional[builtins.str]:
        '''A name for the DB instance.

        If you specify a name, AWS CloudFormation
        converts it to lowercase.

        :default: - a CloudFormation generated name
        '''
        result = self._values.get("instance_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        '''The number of I/O operations per second (IOPS) that the database provisions.

        The value must be equal to or greater than 1000.

        :default: - no provisioned iops
        '''
        result = self._values.get("iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_allocated_storage(self) -> typing.Optional[jsii.Number]:
        '''Upper limit to which RDS can scale the storage in GiB(Gibibyte).

        :default: - No autoscaling of RDS instance

        :see: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIOPS.StorageTypes.html#USER_PIOPS.Autoscaling
        '''
        result = self._values.get("max_allocated_storage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def monitoring_interval(self) -> typing.Optional[aws_cdk.Duration]:
        '''The interval, in seconds, between points when Amazon RDS collects enhanced monitoring metrics for the DB instance.

        :default: - no enhanced monitoring
        '''
        result = self._values.get("monitoring_interval")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def monitoring_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''Role that will be used to manage DB instance monitoring.

        :default: - A role is automatically created for you
        '''
        result = self._values.get("monitoring_role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    @builtins.property
    def multi_az(self) -> typing.Optional[builtins.bool]:
        '''Specifies if the database instance is a multiple Availability Zone deployment.

        :default: false
        '''
        result = self._values.get("multi_az")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def option_group(self) -> typing.Optional[aws_cdk.aws_rds.IOptionGroup]:
        '''The option group to associate with the instance.

        :default: - no option group
        '''
        result = self._values.get("option_group")
        return typing.cast(typing.Optional[aws_cdk.aws_rds.IOptionGroup], result)

    @builtins.property
    def parameter_group(self) -> typing.Optional[aws_cdk.aws_rds.IParameterGroup]:
        '''The DB parameter group to associate with the instance.

        :default: - no parameter group
        '''
        result = self._values.get("parameter_group")
        return typing.cast(typing.Optional[aws_cdk.aws_rds.IParameterGroup], result)

    @builtins.property
    def performance_insight_encryption_key(
        self,
    ) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        '''The AWS KMS key for encryption of Performance Insights data.

        :default: - default master key
        '''
        result = self._values.get("performance_insight_encryption_key")
        return typing.cast(typing.Optional[aws_cdk.aws_kms.IKey], result)

    @builtins.property
    def performance_insight_retention(
        self,
    ) -> typing.Optional[aws_cdk.aws_rds.PerformanceInsightRetention]:
        '''The amount of time, in days, to retain Performance Insights data.

        :default: 7
        '''
        result = self._values.get("performance_insight_retention")
        return typing.cast(typing.Optional[aws_cdk.aws_rds.PerformanceInsightRetention], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port for the instance.

        :default: - the default port for the chosen engine.
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preferred_backup_window(self) -> typing.Optional[builtins.str]:
        '''The daily time range during which automated backups are performed.

        Constraints:

        - Must be in the format ``hh24:mi-hh24:mi``.
        - Must be in Universal Coordinated Time (UTC).
        - Must not conflict with the preferred maintenance window.
        - Must be at least 30 minutes.

        :default:

        - a 30-minute window selected at random from an 8-hour block of
        time for each AWS Region. To see the time blocks available, see
        https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow
        '''
        result = self._values.get("preferred_backup_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''The weekly time range (in UTC) during which system maintenance can occur.

        Format: ``ddd:hh24:mi-ddd:hh24:mi``
        Constraint: Minimum 30-minute window

        :default:

        - a 30-minute window selected at random from an 8-hour block of
        time for each AWS Region, occurring on a random day of the week. To see
        the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def processor_features(self) -> typing.Optional[aws_cdk.aws_rds.ProcessorFeatures]:
        '''The number of CPU cores and the number of threads per core.

        :default:

        - the default number of CPU cores and threads per core for the
        chosen instance class.

        See https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html#USER_ConfigureProcessor
        '''
        result = self._values.get("processor_features")
        return typing.cast(typing.Optional[aws_cdk.aws_rds.ProcessorFeatures], result)

    @builtins.property
    def publicly_accessible(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the DB instance is an internet-facing instance.

        :default: - ``true`` if ``vpcSubnets`` is ``subnetType: SubnetType.PUBLIC``, ``false`` otherwise
        '''
        result = self._values.get("publicly_accessible")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[aws_cdk.RemovalPolicy]:
        '''The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update.

        :default: - RemovalPolicy.SNAPSHOT (remove the resource, but retain a snapshot of the data)
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[aws_cdk.RemovalPolicy], result)

    @builtins.property
    def s3_export_buckets(self) -> typing.Optional[typing.List[aws_cdk.aws_s3.IBucket]]:
        '''S3 buckets that you want to load data into.

        This property must not be used if ``s3ExportRole`` is used.

        For Microsoft SQL Server:

        :default: - None

        :see: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/oracle-s3-integration.html
        '''
        result = self._values.get("s3_export_buckets")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_s3.IBucket]], result)

    @builtins.property
    def s3_export_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''Role that will be associated with this DB instance to enable S3 export.

        This property must not be used if ``s3ExportBuckets`` is used.

        For Microsoft SQL Server:

        :default: - New role is created if ``s3ExportBuckets`` is set, no role is defined otherwise

        :see: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/oracle-s3-integration.html
        '''
        result = self._values.get("s3_export_role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    @builtins.property
    def s3_import_buckets(self) -> typing.Optional[typing.List[aws_cdk.aws_s3.IBucket]]:
        '''S3 buckets that you want to load data from.

        This feature is only supported by the Microsoft SQL Server, Oracle, and PostgreSQL engines.

        This property must not be used if ``s3ImportRole`` is used.

        For Microsoft SQL Server:

        :default: - None

        :see: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Procedural.Importing.html
        '''
        result = self._values.get("s3_import_buckets")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_s3.IBucket]], result)

    @builtins.property
    def s3_import_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''Role that will be associated with this DB instance to enable S3 import.

        This feature is only supported by the Microsoft SQL Server, Oracle, and PostgreSQL engines.

        This property must not be used if ``s3ImportBuckets`` is used.

        For Microsoft SQL Server:

        :default: - New role is created if ``s3ImportBuckets`` is set, no role is defined otherwise

        :see: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Procedural.Importing.html
        '''
        result = self._values.get("s3_import_role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        '''The security groups to assign to the DB instance.

        :default: - a new security group is created
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]], result)

    @builtins.property
    def storage_type(self) -> typing.Optional[aws_cdk.aws_rds.StorageType]:
        '''The storage type.

        Storage types supported are gp2, io1, standard.

        :default: GP2

        :see: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Storage.html#Concepts.Storage.GeneralSSD
        '''
        result = self._values.get("storage_type")
        return typing.cast(typing.Optional[aws_cdk.aws_rds.StorageType], result)

    @builtins.property
    def subnet_group(self) -> typing.Optional[aws_cdk.aws_rds.ISubnetGroup]:
        '''Existing subnet group for the instance.

        :default: - a new subnet group will be created.
        '''
        result = self._values.get("subnet_group")
        return typing.cast(typing.Optional[aws_cdk.aws_rds.ISubnetGroup], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        '''The type of subnets to add to the created DB subnet group.

        :default: - private subnets
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], result)

    @builtins.property
    def engine(self) -> aws_cdk.aws_rds.IInstanceEngine:
        '''The database engine.'''
        result = self._values.get("engine")
        assert result is not None, "Required property 'engine' is missing"
        return typing.cast(aws_cdk.aws_rds.IInstanceEngine, result)

    @builtins.property
    def allocated_storage(self) -> typing.Optional[jsii.Number]:
        '''The allocated storage size, specified in gibibytes (GiB).

        :default: 100
        '''
        result = self._values.get("allocated_storage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def allow_major_version_upgrade(self) -> typing.Optional[builtins.bool]:
        '''Whether to allow major version upgrades.

        :default: false
        '''
        result = self._values.get("allow_major_version_upgrade")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''The name of the database.

        :default: - no name
        '''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        '''The name of the compute and memory capacity for the instance.

        :default: - m5.large (or, more specifically, db.m5.large)
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.InstanceType], result)

    @builtins.property
    def license_model(self) -> typing.Optional[aws_cdk.aws_rds.LicenseModel]:
        '''The license model.

        :default: - RDS default license model
        '''
        result = self._values.get("license_model")
        return typing.cast(typing.Optional[aws_cdk.aws_rds.LicenseModel], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The parameters in the DBParameterGroup to create automatically.

        You can only specify parameterGroup or parameters but not both.
        You need to use a versioned engine to auto-generate a DBParameterGroup.

        :default: - None
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''The time zone of the instance.

        This is currently supported only by Microsoft Sql Server.

        :default: - RDS default timezone
        '''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def character_set_name(self) -> typing.Optional[builtins.str]:
        '''For supported engines, specifies the character set to associate with the DB instance.

        :default: - RDS default character set name
        '''
        result = self._values.get("character_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def credentials(self) -> typing.Optional[aws_cdk.aws_rds.Credentials]:
        '''Credentials for the administrative user.

        :default: - A username of 'admin' (or 'postgres' for PostgreSQL) and SecretsManager-generated password
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional[aws_cdk.aws_rds.Credentials], result)

    @builtins.property
    def storage_encrypted(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the DB instance is encrypted.

        :default: - true if storageEncryptionKey has been provided, false otherwise
        '''
        result = self._values.get("storage_encrypted")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def storage_encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        '''The KMS key that's used to encrypt the DB instance.

        :default: - default master key if storageEncrypted is true, no key otherwise
        '''
        result = self._values.get("storage_encryption_key")
        return typing.cast(typing.Optional[aws_cdk.aws_kms.IKey], result)

    @builtins.property
    def pgstac_db_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("pgstac_db_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pgstac_username(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("pgstac_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pgstac_version(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("pgstac_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secrets_prefix(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("secrets_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PgStacDatabaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StacIngestor(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-pgstac.StacIngestor",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        data_access_role: aws_cdk.aws_iam.IRole,
        stac_db_secret: aws_cdk.aws_secretsmanager.ISecret,
        stac_db_security_group: aws_cdk.aws_ec2.ISecurityGroup,
        stac_url: builtins.str,
        stage: builtins.str,
        subnet_selection: typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]],
        vpc: aws_cdk.aws_ec2.IVpc,
        api_endpoint_configuration: typing.Optional[typing.Union[aws_cdk.aws_apigateway.EndpointConfiguration, typing.Dict[str, typing.Any]]] = None,
        api_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        api_policy: typing.Optional[aws_cdk.aws_iam.PolicyDocument] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param data_access_role: (experimental) ARN of AWS Role used to validate access to S3 data.
        :param stac_db_secret: (experimental) Secret containing pgSTAC DB connection information.
        :param stac_db_security_group: (experimental) Security Group used by pgSTAC DB.
        :param stac_url: (experimental) URL of STAC API.
        :param stage: (experimental) Stage of deployment (e.g. ``dev``, ``prod``).
        :param subnet_selection: (experimental) Boolean indicating whether or not pgSTAC DB is in a public subnet.
        :param vpc: (experimental) VPC running pgSTAC DB.
        :param api_endpoint_configuration: (experimental) API Endpoint Configuration, useful for creating private APIs.
        :param api_env: (experimental) Environment variables to be sent to Lambda.
        :param api_policy: (experimental) API Policy Document, useful for creating private APIs.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(StacIngestor.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StacIngestorProps(
            data_access_role=data_access_role,
            stac_db_secret=stac_db_secret,
            stac_db_security_group=stac_db_security_group,
            stac_url=stac_url,
            stage=stage,
            subnet_selection=subnet_selection,
            vpc=vpc,
            api_endpoint_configuration=api_endpoint_configuration,
            api_env=api_env,
            api_policy=api_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> aws_cdk.aws_dynamodb.Table:
        '''
        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_dynamodb.Table, jsii.get(self, "table"))

    @table.setter
    def table(self, value: aws_cdk.aws_dynamodb.Table) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(getattr(StacIngestor, "table").fset)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "table", value)


@jsii.data_type(
    jsii_type="cdk-pgstac.StacIngestorProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_access_role": "dataAccessRole",
        "stac_db_secret": "stacDbSecret",
        "stac_db_security_group": "stacDbSecurityGroup",
        "stac_url": "stacUrl",
        "stage": "stage",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
        "api_endpoint_configuration": "apiEndpointConfiguration",
        "api_env": "apiEnv",
        "api_policy": "apiPolicy",
    },
)
class StacIngestorProps:
    def __init__(
        self,
        *,
        data_access_role: aws_cdk.aws_iam.IRole,
        stac_db_secret: aws_cdk.aws_secretsmanager.ISecret,
        stac_db_security_group: aws_cdk.aws_ec2.ISecurityGroup,
        stac_url: builtins.str,
        stage: builtins.str,
        subnet_selection: typing.Union[aws_cdk.aws_ec2.SubnetSelection, typing.Dict[str, typing.Any]],
        vpc: aws_cdk.aws_ec2.IVpc,
        api_endpoint_configuration: typing.Optional[typing.Union[aws_cdk.aws_apigateway.EndpointConfiguration, typing.Dict[str, typing.Any]]] = None,
        api_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        api_policy: typing.Optional[aws_cdk.aws_iam.PolicyDocument] = None,
    ) -> None:
        '''
        :param data_access_role: (experimental) ARN of AWS Role used to validate access to S3 data.
        :param stac_db_secret: (experimental) Secret containing pgSTAC DB connection information.
        :param stac_db_security_group: (experimental) Security Group used by pgSTAC DB.
        :param stac_url: (experimental) URL of STAC API.
        :param stage: (experimental) Stage of deployment (e.g. ``dev``, ``prod``).
        :param subnet_selection: (experimental) Boolean indicating whether or not pgSTAC DB is in a public subnet.
        :param vpc: (experimental) VPC running pgSTAC DB.
        :param api_endpoint_configuration: (experimental) API Endpoint Configuration, useful for creating private APIs.
        :param api_env: (experimental) Environment variables to be sent to Lambda.
        :param api_policy: (experimental) API Policy Document, useful for creating private APIs.

        :stability: experimental
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = aws_cdk.aws_ec2.SubnetSelection(**subnet_selection)
        if isinstance(api_endpoint_configuration, dict):
            api_endpoint_configuration = aws_cdk.aws_apigateway.EndpointConfiguration(**api_endpoint_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(StacIngestorProps.__init__)
            check_type(argname="argument data_access_role", value=data_access_role, expected_type=type_hints["data_access_role"])
            check_type(argname="argument stac_db_secret", value=stac_db_secret, expected_type=type_hints["stac_db_secret"])
            check_type(argname="argument stac_db_security_group", value=stac_db_security_group, expected_type=type_hints["stac_db_security_group"])
            check_type(argname="argument stac_url", value=stac_url, expected_type=type_hints["stac_url"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument api_endpoint_configuration", value=api_endpoint_configuration, expected_type=type_hints["api_endpoint_configuration"])
            check_type(argname="argument api_env", value=api_env, expected_type=type_hints["api_env"])
            check_type(argname="argument api_policy", value=api_policy, expected_type=type_hints["api_policy"])
        self._values: typing.Dict[str, typing.Any] = {
            "data_access_role": data_access_role,
            "stac_db_secret": stac_db_secret,
            "stac_db_security_group": stac_db_security_group,
            "stac_url": stac_url,
            "stage": stage,
            "subnet_selection": subnet_selection,
            "vpc": vpc,
        }
        if api_endpoint_configuration is not None:
            self._values["api_endpoint_configuration"] = api_endpoint_configuration
        if api_env is not None:
            self._values["api_env"] = api_env
        if api_policy is not None:
            self._values["api_policy"] = api_policy

    @builtins.property
    def data_access_role(self) -> aws_cdk.aws_iam.IRole:
        '''(experimental) ARN of AWS Role used to validate access to S3 data.

        :stability: experimental
        '''
        result = self._values.get("data_access_role")
        assert result is not None, "Required property 'data_access_role' is missing"
        return typing.cast(aws_cdk.aws_iam.IRole, result)

    @builtins.property
    def stac_db_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''(experimental) Secret containing pgSTAC DB connection information.

        :stability: experimental
        '''
        result = self._values.get("stac_db_secret")
        assert result is not None, "Required property 'stac_db_secret' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    @builtins.property
    def stac_db_security_group(self) -> aws_cdk.aws_ec2.ISecurityGroup:
        '''(experimental) Security Group used by pgSTAC DB.

        :stability: experimental
        '''
        result = self._values.get("stac_db_security_group")
        assert result is not None, "Required property 'stac_db_security_group' is missing"
        return typing.cast(aws_cdk.aws_ec2.ISecurityGroup, result)

    @builtins.property
    def stac_url(self) -> builtins.str:
        '''(experimental) URL of STAC API.

        :stability: experimental
        '''
        result = self._values.get("stac_url")
        assert result is not None, "Required property 'stac_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stage(self) -> builtins.str:
        '''(experimental) Stage of deployment (e.g. ``dev``, ``prod``).

        :stability: experimental
        '''
        result = self._values.get("stage")
        assert result is not None, "Required property 'stage' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_selection(self) -> aws_cdk.aws_ec2.SubnetSelection:
        '''(experimental) Boolean indicating whether or not pgSTAC DB is in a public subnet.

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        assert result is not None, "Required property 'subnet_selection' is missing"
        return typing.cast(aws_cdk.aws_ec2.SubnetSelection, result)

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''(experimental) VPC running pgSTAC DB.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    @builtins.property
    def api_endpoint_configuration(
        self,
    ) -> typing.Optional[aws_cdk.aws_apigateway.EndpointConfiguration]:
        '''(experimental) API Endpoint Configuration, useful for creating private APIs.

        :stability: experimental
        '''
        result = self._values.get("api_endpoint_configuration")
        return typing.cast(typing.Optional[aws_cdk.aws_apigateway.EndpointConfiguration], result)

    @builtins.property
    def api_env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables to be sent to Lambda.

        :stability: experimental
        '''
        result = self._values.get("api_env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def api_policy(self) -> typing.Optional[aws_cdk.aws_iam.PolicyDocument]:
        '''(experimental) API Policy Document, useful for creating private APIs.

        :stability: experimental
        '''
        result = self._values.get("api_policy")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.PolicyDocument], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StacIngestorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ApiEntrypoint",
    "BastionHost",
    "BastionHostProps",
    "BootstrapPgStac",
    "BootstrapPgStacProps",
    "DatabaseParameters",
    "PgStacApiLambda",
    "PgStacApiLambdaProps",
    "PgStacDatabase",
    "PgStacDatabaseProps",
    "StacIngestor",
    "StacIngestorProps",
]

publication.publish()
