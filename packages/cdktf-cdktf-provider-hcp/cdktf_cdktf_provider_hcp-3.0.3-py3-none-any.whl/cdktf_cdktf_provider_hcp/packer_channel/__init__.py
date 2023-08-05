'''
# `hcp_packer_channel`

Refer to the Terraform Registory for docs: [`hcp_packer_channel`](https://www.terraform.io/docs/providers/hcp/r/packer_channel).
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

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class PackerChannel(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.packerChannel.PackerChannel",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel hcp_packer_channel}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        bucket_name: builtins.str,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        iteration: typing.Optional[typing.Union["PackerChannelIteration", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["PackerChannelTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel hcp_packer_channel} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bucket_name: The slug of the HCP Packer Registry image bucket where the channel should be created in. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#bucket_name PackerChannel#bucket_name}
        :param name: The name of the channel being managed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#name PackerChannel#name}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#id PackerChannel#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param iteration: iteration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#iteration PackerChannel#iteration}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#timeouts PackerChannel#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b24ebdef9824e51075b15bdba17e99f222afe0721eae6700b19b7fb5386e23c1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PackerChannelConfig(
            bucket_name=bucket_name,
            name=name,
            id=id,
            iteration=iteration,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putIteration")
    def put_iteration(
        self,
        *,
        fingerprint: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        incremental_version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fingerprint: The fingerprint of the iteration assigned to the channel. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#fingerprint PackerChannel#fingerprint}
        :param id: The ID of the iteration assigned to the channel. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#id PackerChannel#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param incremental_version: The incremental_version of the iteration assigned to the channel. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#incremental_version PackerChannel#incremental_version}
        '''
        value = PackerChannelIteration(
            fingerprint=fingerprint, id=id, incremental_version=incremental_version
        )

        return typing.cast(None, jsii.invoke(self, "putIteration", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        default: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#create PackerChannel#create}.
        :param default: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#default PackerChannel#default}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#delete PackerChannel#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#update PackerChannel#update}.
        '''
        value = PackerChannelTimeouts(
            create=create, default=default, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIteration")
    def reset_iteration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIteration", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="authorId")
    def author_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorId"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="iteration")
    def iteration(self) -> "PackerChannelIterationOutputReference":
        return typing.cast("PackerChannelIterationOutputReference", jsii.get(self, "iteration"))

    @builtins.property
    @jsii.member(jsii_name="organizationId")
    def organization_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationId"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "PackerChannelTimeoutsOutputReference":
        return typing.cast("PackerChannelTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="iterationInput")
    def iteration_input(self) -> typing.Optional["PackerChannelIteration"]:
        return typing.cast(typing.Optional["PackerChannelIteration"], jsii.get(self, "iterationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["PackerChannelTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["PackerChannelTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6af7d3dfe20c5786c26da1fb0ada9f38d6b66fb842c2418851f5cfbe83f84ecd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ad4e12fe8ee303d1bdede4fdb0de36ff40976c11130fbdbe626c3c557534d6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__110c630d73cf0d9073f9d58d52f4fe8cad3870fc539c26ce25e58adad7b4ee70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.packerChannel.PackerChannelConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "bucket_name": "bucketName",
        "name": "name",
        "id": "id",
        "iteration": "iteration",
        "timeouts": "timeouts",
    },
)
class PackerChannelConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        bucket_name: builtins.str,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        iteration: typing.Optional[typing.Union["PackerChannelIteration", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["PackerChannelTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bucket_name: The slug of the HCP Packer Registry image bucket where the channel should be created in. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#bucket_name PackerChannel#bucket_name}
        :param name: The name of the channel being managed. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#name PackerChannel#name}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#id PackerChannel#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param iteration: iteration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#iteration PackerChannel#iteration}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#timeouts PackerChannel#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(iteration, dict):
            iteration = PackerChannelIteration(**iteration)
        if isinstance(timeouts, dict):
            timeouts = PackerChannelTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d477df52b7c60b14dc1bee079bed7a6b984f2086c59e5444cea18401d935f420)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument iteration", value=iteration, expected_type=type_hints["iteration"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
            "name": name,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if id is not None:
            self._values["id"] = id
        if iteration is not None:
            self._values["iteration"] = iteration
        if timeouts is not None:
            self._values["timeouts"] = timeouts

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''The slug of the HCP Packer Registry image bucket where the channel should be created in.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#bucket_name PackerChannel#bucket_name}
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the channel being managed.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#name PackerChannel#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#id PackerChannel#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iteration(self) -> typing.Optional["PackerChannelIteration"]:
        '''iteration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#iteration PackerChannel#iteration}
        '''
        result = self._values.get("iteration")
        return typing.cast(typing.Optional["PackerChannelIteration"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["PackerChannelTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#timeouts PackerChannel#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["PackerChannelTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PackerChannelConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.packerChannel.PackerChannelIteration",
    jsii_struct_bases=[],
    name_mapping={
        "fingerprint": "fingerprint",
        "id": "id",
        "incremental_version": "incrementalVersion",
    },
)
class PackerChannelIteration:
    def __init__(
        self,
        *,
        fingerprint: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        incremental_version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fingerprint: The fingerprint of the iteration assigned to the channel. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#fingerprint PackerChannel#fingerprint}
        :param id: The ID of the iteration assigned to the channel. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#id PackerChannel#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param incremental_version: The incremental_version of the iteration assigned to the channel. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#incremental_version PackerChannel#incremental_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab35d949073c20a9975f8d59dbcea56f6019586d8d17c87198ed9b73d8da416c)
            check_type(argname="argument fingerprint", value=fingerprint, expected_type=type_hints["fingerprint"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument incremental_version", value=incremental_version, expected_type=type_hints["incremental_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fingerprint is not None:
            self._values["fingerprint"] = fingerprint
        if id is not None:
            self._values["id"] = id
        if incremental_version is not None:
            self._values["incremental_version"] = incremental_version

    @builtins.property
    def fingerprint(self) -> typing.Optional[builtins.str]:
        '''The fingerprint of the iteration assigned to the channel.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#fingerprint PackerChannel#fingerprint}
        '''
        result = self._values.get("fingerprint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''The ID of the iteration assigned to the channel.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#id PackerChannel#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def incremental_version(self) -> typing.Optional[jsii.Number]:
        '''The incremental_version of the iteration assigned to the channel.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#incremental_version PackerChannel#incremental_version}
        '''
        result = self._values.get("incremental_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PackerChannelIteration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PackerChannelIterationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.packerChannel.PackerChannelIterationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8b9020611378575f041f88feac6fb375bec3d00efb0babcb87e2e12e0b0f181)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFingerprint")
    def reset_fingerprint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFingerprint", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIncrementalVersion")
    def reset_incremental_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncrementalVersion", []))

    @builtins.property
    @jsii.member(jsii_name="fingerprintInput")
    def fingerprint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fingerprintInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="incrementalVersionInput")
    def incremental_version_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "incrementalVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="fingerprint")
    def fingerprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fingerprint"))

    @fingerprint.setter
    def fingerprint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2de661dc22816f56dfee4e02c6b98a5473e69dc76324a166bb141d03dca87210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fingerprint", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fccde95d201ed12605607f93795c7d850c80d58fdf3285ab835945621b03b772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="incrementalVersion")
    def incremental_version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "incrementalVersion"))

    @incremental_version.setter
    def incremental_version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff8ce9e5dfcd8c9fce1a3208853ea728e08a756adb09128871cd956a5716211f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "incrementalVersion", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PackerChannelIteration]:
        return typing.cast(typing.Optional[PackerChannelIteration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[PackerChannelIteration]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc7bba7485169f61cb14f0d20aca1fb346888aa6523c132a830880f3b0db7303)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-hcp.packerChannel.PackerChannelTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "default": "default",
        "delete": "delete",
        "update": "update",
    },
)
class PackerChannelTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        default: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#create PackerChannel#create}.
        :param default: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#default PackerChannel#default}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#delete PackerChannel#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#update PackerChannel#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe787a15b951abd7c6a540834a0577806e60d41fed9c893cef64fa1dabed3638)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if default is not None:
            self._values["default"] = default
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#create PackerChannel#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#default PackerChannel#default}.'''
        result = self._values.get("default")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#delete PackerChannel#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/hcp/r/packer_channel#update PackerChannel#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PackerChannelTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PackerChannelTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-hcp.packerChannel.PackerChannelTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2e308ee1121442b524285ab62aa38d58a73278d49c333bd552e9ce698ad74cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDefault")
    def reset_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefault", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultInput")
    def default_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b17112e670e34175a296659ff07f4a0a0a32edd9604362f0da9961791498cc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @default.setter
    def default(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01777a67db8f2a922d2508900bc89f9481d19737bbfa898029f7384a9ddd298b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "default", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5905ca6eee60c9c416f55d6ac774408b11b2b8ee64a9fc06831accb4709655e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec81a6428baeb9dff7ec5c088737f5140e703236cb48e2144b77c6c9a1a80201)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[PackerChannelTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[PackerChannelTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[PackerChannelTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff1acde2245501fbd7e8c340078bb1568c00dae40940df6469dea8e6ab06c023)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "PackerChannel",
    "PackerChannelConfig",
    "PackerChannelIteration",
    "PackerChannelIterationOutputReference",
    "PackerChannelTimeouts",
    "PackerChannelTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b24ebdef9824e51075b15bdba17e99f222afe0721eae6700b19b7fb5386e23c1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    bucket_name: builtins.str,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    iteration: typing.Optional[typing.Union[PackerChannelIteration, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[PackerChannelTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6af7d3dfe20c5786c26da1fb0ada9f38d6b66fb842c2418851f5cfbe83f84ecd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ad4e12fe8ee303d1bdede4fdb0de36ff40976c11130fbdbe626c3c557534d6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__110c630d73cf0d9073f9d58d52f4fe8cad3870fc539c26ce25e58adad7b4ee70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d477df52b7c60b14dc1bee079bed7a6b984f2086c59e5444cea18401d935f420(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bucket_name: builtins.str,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    iteration: typing.Optional[typing.Union[PackerChannelIteration, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[PackerChannelTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab35d949073c20a9975f8d59dbcea56f6019586d8d17c87198ed9b73d8da416c(
    *,
    fingerprint: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    incremental_version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b9020611378575f041f88feac6fb375bec3d00efb0babcb87e2e12e0b0f181(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de661dc22816f56dfee4e02c6b98a5473e69dc76324a166bb141d03dca87210(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fccde95d201ed12605607f93795c7d850c80d58fdf3285ab835945621b03b772(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff8ce9e5dfcd8c9fce1a3208853ea728e08a756adb09128871cd956a5716211f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc7bba7485169f61cb14f0d20aca1fb346888aa6523c132a830880f3b0db7303(
    value: typing.Optional[PackerChannelIteration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe787a15b951abd7c6a540834a0577806e60d41fed9c893cef64fa1dabed3638(
    *,
    create: typing.Optional[builtins.str] = None,
    default: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2e308ee1121442b524285ab62aa38d58a73278d49c333bd552e9ce698ad74cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b17112e670e34175a296659ff07f4a0a0a32edd9604362f0da9961791498cc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01777a67db8f2a922d2508900bc89f9481d19737bbfa898029f7384a9ddd298b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5905ca6eee60c9c416f55d6ac774408b11b2b8ee64a9fc06831accb4709655e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec81a6428baeb9dff7ec5c088737f5140e703236cb48e2144b77c6c9a1a80201(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff1acde2245501fbd7e8c340078bb1568c00dae40940df6469dea8e6ab06c023(
    value: typing.Optional[typing.Union[PackerChannelTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
