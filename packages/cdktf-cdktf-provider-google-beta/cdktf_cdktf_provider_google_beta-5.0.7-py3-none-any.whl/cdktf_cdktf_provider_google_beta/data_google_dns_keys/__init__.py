'''
# `data_google_dns_keys`

Refer to the Terraform Registory for docs: [`data_google_dns_keys`](https://www.terraform.io/docs/providers/google-beta/d/google_dns_keys).
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


class DataGoogleDnsKeys(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.dataGoogleDnsKeys.DataGoogleDnsKeys",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google-beta/d/google_dns_keys google_dns_keys}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        managed_zone: builtins.str,
        key_signing_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataGoogleDnsKeysKeySigningKeys", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        zone_signing_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataGoogleDnsKeysZoneSigningKeys", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google-beta/d/google_dns_keys google_dns_keys} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param managed_zone: The Name of the zone. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/d/google_dns_keys#managed_zone DataGoogleDnsKeys#managed_zone}
        :param key_signing_keys: key_signing_keys block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/d/google_dns_keys#key_signing_keys DataGoogleDnsKeys#key_signing_keys}
        :param project: The ID of the project for the Google Cloud. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/d/google_dns_keys#project DataGoogleDnsKeys#project}
        :param zone_signing_keys: zone_signing_keys block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/d/google_dns_keys#zone_signing_keys DataGoogleDnsKeys#zone_signing_keys}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a301e23986428a24662d13489b12ce29002f9e404efa51d8f62ecba06a26df2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataGoogleDnsKeysConfig(
            managed_zone=managed_zone,
            key_signing_keys=key_signing_keys,
            project=project,
            zone_signing_keys=zone_signing_keys,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="putKeySigningKeys")
    def put_key_signing_keys(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataGoogleDnsKeysKeySigningKeys", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06d7c3910b5730f03ac18b21178d5c537a084a345e2c6bbf618ba091d4fc9b2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putKeySigningKeys", [value]))

    @jsii.member(jsii_name="putZoneSigningKeys")
    def put_zone_signing_keys(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataGoogleDnsKeysZoneSigningKeys", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__125c0507dd0576894f92568c8063669399f411f7a33125c2050fa8470705dc4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putZoneSigningKeys", [value]))

    @jsii.member(jsii_name="resetKeySigningKeys")
    def reset_key_signing_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeySigningKeys", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetZoneSigningKeys")
    def reset_zone_signing_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZoneSigningKeys", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="keySigningKeys")
    def key_signing_keys(self) -> "DataGoogleDnsKeysKeySigningKeysList":
        return typing.cast("DataGoogleDnsKeysKeySigningKeysList", jsii.get(self, "keySigningKeys"))

    @builtins.property
    @jsii.member(jsii_name="zoneSigningKeys")
    def zone_signing_keys(self) -> "DataGoogleDnsKeysZoneSigningKeysList":
        return typing.cast("DataGoogleDnsKeysZoneSigningKeysList", jsii.get(self, "zoneSigningKeys"))

    @builtins.property
    @jsii.member(jsii_name="keySigningKeysInput")
    def key_signing_keys_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataGoogleDnsKeysKeySigningKeys"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataGoogleDnsKeysKeySigningKeys"]]], jsii.get(self, "keySigningKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="managedZoneInput")
    def managed_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneSigningKeysInput")
    def zone_signing_keys_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataGoogleDnsKeysZoneSigningKeys"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataGoogleDnsKeysZoneSigningKeys"]]], jsii.get(self, "zoneSigningKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="managedZone")
    def managed_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedZone"))

    @managed_zone.setter
    def managed_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9568217bc120057d5a6b69b3e3d454c538ca170106ce859d49fcbac529a1a25d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedZone", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56acb169be0328209994d7dfdd0a6861c7633cacc70eaa7e5201c515f548fa95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.dataGoogleDnsKeys.DataGoogleDnsKeysConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "managed_zone": "managedZone",
        "key_signing_keys": "keySigningKeys",
        "project": "project",
        "zone_signing_keys": "zoneSigningKeys",
    },
)
class DataGoogleDnsKeysConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        managed_zone: builtins.str,
        key_signing_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataGoogleDnsKeysKeySigningKeys", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        zone_signing_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataGoogleDnsKeysZoneSigningKeys", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param managed_zone: The Name of the zone. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/d/google_dns_keys#managed_zone DataGoogleDnsKeys#managed_zone}
        :param key_signing_keys: key_signing_keys block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/d/google_dns_keys#key_signing_keys DataGoogleDnsKeys#key_signing_keys}
        :param project: The ID of the project for the Google Cloud. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/d/google_dns_keys#project DataGoogleDnsKeys#project}
        :param zone_signing_keys: zone_signing_keys block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/d/google_dns_keys#zone_signing_keys DataGoogleDnsKeys#zone_signing_keys}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61204949151abb629d180aa5f5bc5043e923d0df26086f8a0ce78c182c9bbf7e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument managed_zone", value=managed_zone, expected_type=type_hints["managed_zone"])
            check_type(argname="argument key_signing_keys", value=key_signing_keys, expected_type=type_hints["key_signing_keys"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument zone_signing_keys", value=zone_signing_keys, expected_type=type_hints["zone_signing_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "managed_zone": managed_zone,
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
        if key_signing_keys is not None:
            self._values["key_signing_keys"] = key_signing_keys
        if project is not None:
            self._values["project"] = project
        if zone_signing_keys is not None:
            self._values["zone_signing_keys"] = zone_signing_keys

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
    def managed_zone(self) -> builtins.str:
        '''The Name of the zone.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/d/google_dns_keys#managed_zone DataGoogleDnsKeys#managed_zone}
        '''
        result = self._values.get("managed_zone")
        assert result is not None, "Required property 'managed_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key_signing_keys(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataGoogleDnsKeysKeySigningKeys"]]]:
        '''key_signing_keys block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/d/google_dns_keys#key_signing_keys DataGoogleDnsKeys#key_signing_keys}
        '''
        result = self._values.get("key_signing_keys")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataGoogleDnsKeysKeySigningKeys"]]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The ID of the project for the Google Cloud.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/d/google_dns_keys#project DataGoogleDnsKeys#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone_signing_keys(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataGoogleDnsKeysZoneSigningKeys"]]]:
        '''zone_signing_keys block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/d/google_dns_keys#zone_signing_keys DataGoogleDnsKeys#zone_signing_keys}
        '''
        result = self._values.get("zone_signing_keys")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataGoogleDnsKeysZoneSigningKeys"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleDnsKeysConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.dataGoogleDnsKeys.DataGoogleDnsKeysKeySigningKeys",
    jsii_struct_bases=[],
    name_mapping={"digests": "digests"},
)
class DataGoogleDnsKeysKeySigningKeys:
    def __init__(
        self,
        *,
        digests: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataGoogleDnsKeysKeySigningKeysDigests", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param digests: digests block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/d/google_dns_keys#digests DataGoogleDnsKeys#digests}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__655f4b0254dedb3172c9ae5c5d728ce6591ab854a8f0bb6cab1592f2adc9cb88)
            check_type(argname="argument digests", value=digests, expected_type=type_hints["digests"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if digests is not None:
            self._values["digests"] = digests

    @builtins.property
    def digests(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataGoogleDnsKeysKeySigningKeysDigests"]]]:
        '''digests block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/d/google_dns_keys#digests DataGoogleDnsKeys#digests}
        '''
        result = self._values.get("digests")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataGoogleDnsKeysKeySigningKeysDigests"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleDnsKeysKeySigningKeys(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.dataGoogleDnsKeys.DataGoogleDnsKeysKeySigningKeysDigests",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleDnsKeysKeySigningKeysDigests:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleDnsKeysKeySigningKeysDigests(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleDnsKeysKeySigningKeysDigestsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.dataGoogleDnsKeys.DataGoogleDnsKeysKeySigningKeysDigestsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e81d1a5cf7586169ec765e3acbddeda5d8832dfcce94b51f095d5713d5e31b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleDnsKeysKeySigningKeysDigestsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cef0e7ac1232af3e318c28ca19623328c8d390e974593c64a5b3483c1c75cfc0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleDnsKeysKeySigningKeysDigestsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62087e699a2643f07f7bbf3603545133c5ac7786cc16913ce9767c811546cd4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e6c6e82b54b567426426a718c80610a193d107a1cf9b1b25b897ba77fedaca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d350ca4f2138351d55e62c7587edbeae86c4e7e4b32be55b258264c086f03be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataGoogleDnsKeysKeySigningKeysDigests]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataGoogleDnsKeysKeySigningKeysDigests]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataGoogleDnsKeysKeySigningKeysDigests]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cca8607e0554950a0f2c6ff963c0f03cec5873aa633fe1001d384d28cbd5f525)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataGoogleDnsKeysKeySigningKeysDigestsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.dataGoogleDnsKeys.DataGoogleDnsKeysKeySigningKeysDigestsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17ddf317489f8871d42c1e6ea1ab29f7184cd54cd70ad3bdeb541d371bee135f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="digest")
    def digest(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "digest"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataGoogleDnsKeysKeySigningKeysDigests, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataGoogleDnsKeysKeySigningKeysDigests, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataGoogleDnsKeysKeySigningKeysDigests, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48211eeb3906977aca70c3c1f64b95242a22409bf36cb3ec6d912f8ca5f0352f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataGoogleDnsKeysKeySigningKeysList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.dataGoogleDnsKeys.DataGoogleDnsKeysKeySigningKeysList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3e4fef18ef3e4c458f7e04bddce1d6a6bd49c2de749297783ee815f846ca8ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleDnsKeysKeySigningKeysOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07ef1fef2479183f360a6ae487884b0805111451013191e6364b65afd79950da)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleDnsKeysKeySigningKeysOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6086822831d2f72f072f528921e92732f55b9f92640492e76eaab22a5a5d2be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__725e6cc37875d224d72856b97424aed640f4c82dedbf9d12262fdda374d532f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__211c94885b741170e6565f067ddc2a06284aa702f792588759ef9a8cae9db363)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataGoogleDnsKeysKeySigningKeys]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataGoogleDnsKeysKeySigningKeys]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataGoogleDnsKeysKeySigningKeys]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25fca3dc33b0d7e56b0f3392e92b93e11efac860d6757cd8921337ca8aa91012)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataGoogleDnsKeysKeySigningKeysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.dataGoogleDnsKeys.DataGoogleDnsKeysKeySigningKeysOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0ae90a70b28dc8416dc45ef4cb444c92850d6892cb67013f5c6a347d49bd8c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDigests")
    def put_digests(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataGoogleDnsKeysKeySigningKeysDigests, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06a3db4d894b1773ce6fd5167f0f120b07b298e37aee75993c156f2229c09071)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDigests", [value]))

    @jsii.member(jsii_name="resetDigests")
    def reset_digests(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDigests", []))

    @builtins.property
    @jsii.member(jsii_name="algorithm")
    def algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "algorithm"))

    @builtins.property
    @jsii.member(jsii_name="creationTime")
    def creation_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTime"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="digests")
    def digests(self) -> DataGoogleDnsKeysKeySigningKeysDigestsList:
        return typing.cast(DataGoogleDnsKeysKeySigningKeysDigestsList, jsii.get(self, "digests"))

    @builtins.property
    @jsii.member(jsii_name="dsRecord")
    def ds_record(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dsRecord"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="isActive")
    def is_active(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isActive"))

    @builtins.property
    @jsii.member(jsii_name="keyLength")
    def key_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keyLength"))

    @builtins.property
    @jsii.member(jsii_name="keyTag")
    def key_tag(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keyTag"))

    @builtins.property
    @jsii.member(jsii_name="publicKey")
    def public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicKey"))

    @builtins.property
    @jsii.member(jsii_name="digestsInput")
    def digests_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataGoogleDnsKeysKeySigningKeysDigests]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataGoogleDnsKeysKeySigningKeysDigests]]], jsii.get(self, "digestsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataGoogleDnsKeysKeySigningKeys, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataGoogleDnsKeysKeySigningKeys, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataGoogleDnsKeysKeySigningKeys, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa5d3cc4e46f2b05f82c12470ff3cdb569b7f35daaa14bdefbd1f8be5ef022aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.dataGoogleDnsKeys.DataGoogleDnsKeysZoneSigningKeys",
    jsii_struct_bases=[],
    name_mapping={"digests": "digests"},
)
class DataGoogleDnsKeysZoneSigningKeys:
    def __init__(
        self,
        *,
        digests: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataGoogleDnsKeysZoneSigningKeysDigests", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param digests: digests block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/d/google_dns_keys#digests DataGoogleDnsKeys#digests}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__593801d03088851191220e792ffa4b0d6efba180b48b5b792571edd016cedf06)
            check_type(argname="argument digests", value=digests, expected_type=type_hints["digests"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if digests is not None:
            self._values["digests"] = digests

    @builtins.property
    def digests(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataGoogleDnsKeysZoneSigningKeysDigests"]]]:
        '''digests block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google-beta/d/google_dns_keys#digests DataGoogleDnsKeys#digests}
        '''
        result = self._values.get("digests")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataGoogleDnsKeysZoneSigningKeysDigests"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleDnsKeysZoneSigningKeys(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.dataGoogleDnsKeys.DataGoogleDnsKeysZoneSigningKeysDigests",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataGoogleDnsKeysZoneSigningKeysDigests:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataGoogleDnsKeysZoneSigningKeysDigests(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataGoogleDnsKeysZoneSigningKeysDigestsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.dataGoogleDnsKeys.DataGoogleDnsKeysZoneSigningKeysDigestsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e52b04ced022006b7fcd1ee8608c40425bc8718f1d606d12cb1ecda492fcd7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleDnsKeysZoneSigningKeysDigestsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b76d8209919a2f248fd90d6a4abb64a26e171ffeb80cba1a461d8e2c98695079)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleDnsKeysZoneSigningKeysDigestsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__942377fe0e16459d474d161bdf16629c3ecdd205f8a0fcb8182a64676478d240)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8c69e9534a6c7cf93e2f71b94d76bcd6a91f9d1803cd4841a06179e2a8a9858)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5624dcd553d73e725827ab6291fc5ea4489ac0cfbf10129f1145a612d783ba91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataGoogleDnsKeysZoneSigningKeysDigests]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataGoogleDnsKeysZoneSigningKeysDigests]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataGoogleDnsKeysZoneSigningKeysDigests]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9718ba1fdd289b36d71a49ccb6469dca7a7be97264df7389d78f5ee46edc5278)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataGoogleDnsKeysZoneSigningKeysDigestsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.dataGoogleDnsKeys.DataGoogleDnsKeysZoneSigningKeysDigestsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dafceff29254c7f780b67c7d819d9129ef411b3a07819993a9b3c80e6782628d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="digest")
    def digest(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "digest"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataGoogleDnsKeysZoneSigningKeysDigests, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataGoogleDnsKeysZoneSigningKeysDigests, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataGoogleDnsKeysZoneSigningKeysDigests, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd97ccf5691d269c40ea473fe7315a6664086487573bbc57a4ac3f5885d4f194)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataGoogleDnsKeysZoneSigningKeysList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.dataGoogleDnsKeys.DataGoogleDnsKeysZoneSigningKeysList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43f46a1264bc4dde56678a4cd32ad18f27b0d70772cedeafdb878fcd1649c212)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataGoogleDnsKeysZoneSigningKeysOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a711af1b193053aa9d78e6560192b10b02c17d9920d03835e7ed552b5a526ed9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataGoogleDnsKeysZoneSigningKeysOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09e5b97c282627312dc84f106319d2b52adf58cb5567619eb674411c8a34a234)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4218ef51612ccf722b7a85e11a45f1884e99183b993d0869acba57f67a233adf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__320abc86afa1506424021444090935cdc067cc3d3a7ebd6f83bb2c6ccf9a74f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataGoogleDnsKeysZoneSigningKeys]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataGoogleDnsKeysZoneSigningKeys]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataGoogleDnsKeysZoneSigningKeys]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7a48a97a7356904c859a49f65499a66833d9fd474490a4712f25d5450e8af0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataGoogleDnsKeysZoneSigningKeysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.dataGoogleDnsKeys.DataGoogleDnsKeysZoneSigningKeysOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f6d91767d9fabba19cf73d0d7133d502134d0b72e90a4d2501a5e2a852de518)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDigests")
    def put_digests(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataGoogleDnsKeysZoneSigningKeysDigests, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__135f2583432f4f8dc7c0d341080048a9006c765f056e66aa1b2cf45babcd6ffe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDigests", [value]))

    @jsii.member(jsii_name="resetDigests")
    def reset_digests(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDigests", []))

    @builtins.property
    @jsii.member(jsii_name="algorithm")
    def algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "algorithm"))

    @builtins.property
    @jsii.member(jsii_name="creationTime")
    def creation_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTime"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="digests")
    def digests(self) -> DataGoogleDnsKeysZoneSigningKeysDigestsList:
        return typing.cast(DataGoogleDnsKeysZoneSigningKeysDigestsList, jsii.get(self, "digests"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="isActive")
    def is_active(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isActive"))

    @builtins.property
    @jsii.member(jsii_name="keyLength")
    def key_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keyLength"))

    @builtins.property
    @jsii.member(jsii_name="keyTag")
    def key_tag(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keyTag"))

    @builtins.property
    @jsii.member(jsii_name="publicKey")
    def public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicKey"))

    @builtins.property
    @jsii.member(jsii_name="digestsInput")
    def digests_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataGoogleDnsKeysZoneSigningKeysDigests]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataGoogleDnsKeysZoneSigningKeysDigests]]], jsii.get(self, "digestsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataGoogleDnsKeysZoneSigningKeys, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataGoogleDnsKeysZoneSigningKeys, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataGoogleDnsKeysZoneSigningKeys, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd230623818f90b824de2d4a73dbe2b12cd3cdb11444a10a02b8d08256d97ca6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataGoogleDnsKeys",
    "DataGoogleDnsKeysConfig",
    "DataGoogleDnsKeysKeySigningKeys",
    "DataGoogleDnsKeysKeySigningKeysDigests",
    "DataGoogleDnsKeysKeySigningKeysDigestsList",
    "DataGoogleDnsKeysKeySigningKeysDigestsOutputReference",
    "DataGoogleDnsKeysKeySigningKeysList",
    "DataGoogleDnsKeysKeySigningKeysOutputReference",
    "DataGoogleDnsKeysZoneSigningKeys",
    "DataGoogleDnsKeysZoneSigningKeysDigests",
    "DataGoogleDnsKeysZoneSigningKeysDigestsList",
    "DataGoogleDnsKeysZoneSigningKeysDigestsOutputReference",
    "DataGoogleDnsKeysZoneSigningKeysList",
    "DataGoogleDnsKeysZoneSigningKeysOutputReference",
]

publication.publish()

def _typecheckingstub__3a301e23986428a24662d13489b12ce29002f9e404efa51d8f62ecba06a26df2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    managed_zone: builtins.str,
    key_signing_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataGoogleDnsKeysKeySigningKeys, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    zone_signing_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataGoogleDnsKeysZoneSigningKeys, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__06d7c3910b5730f03ac18b21178d5c537a084a345e2c6bbf618ba091d4fc9b2c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataGoogleDnsKeysKeySigningKeys, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125c0507dd0576894f92568c8063669399f411f7a33125c2050fa8470705dc4a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataGoogleDnsKeysZoneSigningKeys, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9568217bc120057d5a6b69b3e3d454c538ca170106ce859d49fcbac529a1a25d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56acb169be0328209994d7dfdd0a6861c7633cacc70eaa7e5201c515f548fa95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61204949151abb629d180aa5f5bc5043e923d0df26086f8a0ce78c182c9bbf7e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    managed_zone: builtins.str,
    key_signing_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataGoogleDnsKeysKeySigningKeys, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    zone_signing_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataGoogleDnsKeysZoneSigningKeys, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__655f4b0254dedb3172c9ae5c5d728ce6591ab854a8f0bb6cab1592f2adc9cb88(
    *,
    digests: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataGoogleDnsKeysKeySigningKeysDigests, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e81d1a5cf7586169ec765e3acbddeda5d8832dfcce94b51f095d5713d5e31b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef0e7ac1232af3e318c28ca19623328c8d390e974593c64a5b3483c1c75cfc0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62087e699a2643f07f7bbf3603545133c5ac7786cc16913ce9767c811546cd4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e6c6e82b54b567426426a718c80610a193d107a1cf9b1b25b897ba77fedaca9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d350ca4f2138351d55e62c7587edbeae86c4e7e4b32be55b258264c086f03be(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cca8607e0554950a0f2c6ff963c0f03cec5873aa633fe1001d384d28cbd5f525(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataGoogleDnsKeysKeySigningKeysDigests]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17ddf317489f8871d42c1e6ea1ab29f7184cd54cd70ad3bdeb541d371bee135f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48211eeb3906977aca70c3c1f64b95242a22409bf36cb3ec6d912f8ca5f0352f(
    value: typing.Optional[typing.Union[DataGoogleDnsKeysKeySigningKeysDigests, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e4fef18ef3e4c458f7e04bddce1d6a6bd49c2de749297783ee815f846ca8ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07ef1fef2479183f360a6ae487884b0805111451013191e6364b65afd79950da(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6086822831d2f72f072f528921e92732f55b9f92640492e76eaab22a5a5d2be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__725e6cc37875d224d72856b97424aed640f4c82dedbf9d12262fdda374d532f9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211c94885b741170e6565f067ddc2a06284aa702f792588759ef9a8cae9db363(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25fca3dc33b0d7e56b0f3392e92b93e11efac860d6757cd8921337ca8aa91012(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataGoogleDnsKeysKeySigningKeys]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0ae90a70b28dc8416dc45ef4cb444c92850d6892cb67013f5c6a347d49bd8c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06a3db4d894b1773ce6fd5167f0f120b07b298e37aee75993c156f2229c09071(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataGoogleDnsKeysKeySigningKeysDigests, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa5d3cc4e46f2b05f82c12470ff3cdb569b7f35daaa14bdefbd1f8be5ef022aa(
    value: typing.Optional[typing.Union[DataGoogleDnsKeysKeySigningKeys, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__593801d03088851191220e792ffa4b0d6efba180b48b5b792571edd016cedf06(
    *,
    digests: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataGoogleDnsKeysZoneSigningKeysDigests, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e52b04ced022006b7fcd1ee8608c40425bc8718f1d606d12cb1ecda492fcd7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b76d8209919a2f248fd90d6a4abb64a26e171ffeb80cba1a461d8e2c98695079(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__942377fe0e16459d474d161bdf16629c3ecdd205f8a0fcb8182a64676478d240(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8c69e9534a6c7cf93e2f71b94d76bcd6a91f9d1803cd4841a06179e2a8a9858(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5624dcd553d73e725827ab6291fc5ea4489ac0cfbf10129f1145a612d783ba91(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9718ba1fdd289b36d71a49ccb6469dca7a7be97264df7389d78f5ee46edc5278(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataGoogleDnsKeysZoneSigningKeysDigests]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dafceff29254c7f780b67c7d819d9129ef411b3a07819993a9b3c80e6782628d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd97ccf5691d269c40ea473fe7315a6664086487573bbc57a4ac3f5885d4f194(
    value: typing.Optional[typing.Union[DataGoogleDnsKeysZoneSigningKeysDigests, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43f46a1264bc4dde56678a4cd32ad18f27b0d70772cedeafdb878fcd1649c212(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a711af1b193053aa9d78e6560192b10b02c17d9920d03835e7ed552b5a526ed9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09e5b97c282627312dc84f106319d2b52adf58cb5567619eb674411c8a34a234(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4218ef51612ccf722b7a85e11a45f1884e99183b993d0869acba57f67a233adf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__320abc86afa1506424021444090935cdc067cc3d3a7ebd6f83bb2c6ccf9a74f8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7a48a97a7356904c859a49f65499a66833d9fd474490a4712f25d5450e8af0d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataGoogleDnsKeysZoneSigningKeys]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f6d91767d9fabba19cf73d0d7133d502134d0b72e90a4d2501a5e2a852de518(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__135f2583432f4f8dc7c0d341080048a9006c765f056e66aa1b2cf45babcd6ffe(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataGoogleDnsKeysZoneSigningKeysDigests, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd230623818f90b824de2d4a73dbe2b12cd3cdb11444a10a02b8d08256d97ca6(
    value: typing.Optional[typing.Union[DataGoogleDnsKeysZoneSigningKeys, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
