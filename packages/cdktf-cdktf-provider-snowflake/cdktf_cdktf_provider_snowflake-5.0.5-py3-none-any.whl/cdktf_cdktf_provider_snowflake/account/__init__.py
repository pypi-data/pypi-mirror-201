'''
# `snowflake_account`

Refer to the Terraform Registory for docs: [`snowflake_account`](https://www.terraform.io/docs/providers/snowflake/r/account).
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


class Account(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.account.Account",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/snowflake/r/account snowflake_account}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        admin_name: builtins.str,
        edition: builtins.str,
        email: builtins.str,
        name: builtins.str,
        admin_password: typing.Optional[builtins.str] = None,
        admin_rsa_public_key: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        first_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        must_change_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        region_group: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/snowflake/r/account snowflake_account} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param admin_name: Login name of the initial administrative user of the account. A new user is created in the new account with this name and password and granted the ACCOUNTADMIN role in the account. A login name can be any string consisting of letters, numbers, and underscores. Login names are always case-insensitive. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#admin_name Account#admin_name}
        :param edition: `Snowflake Edition <https://docs.snowflake.com/en/user-guide/intro-editions.html>`_ of the account. Valid values are: STANDARD | ENTERPRISE | BUSINESS_CRITICAL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#edition Account#edition}
        :param email: Email address of the initial administrative user of the account. This email address is used to send any notifications about the account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#email Account#email}
        :param name: Specifies the identifier (i.e. name) for the account; must be unique within an organization, regardless of which Snowflake Region the account is in. In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters except for underscores (_). Note that if the account name includes underscores, features that do not accept account names with underscores (e.g. Okta SSO or SCIM) can reference a version of the account name that substitutes hyphens (-) for the underscores. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#name Account#name}
        :param admin_password: Password for the initial administrative user of the account. Optional if the ``ADMIN_RSA_PUBLIC_KEY`` parameter is specified. For more information about passwords in Snowflake, see `Snowflake-provided Password Policy <https://docs.snowflake.com/en/sql-reference/sql/create-account.html#:~:text=Snowflake%2Dprovided%20Password%20Policy>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#admin_password Account#admin_password}
        :param admin_rsa_public_key: Assigns a public key to the initial administrative user of the account in order to implement `key pair authentication <https://docs.snowflake.com/en/sql-reference/sql/create-account.html#:~:text=key%20pair%20authentication>`_ for the user. Optional if the ``ADMIN_PASSWORD`` parameter is specified. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#admin_rsa_public_key Account#admin_rsa_public_key}
        :param comment: Specifies a comment for the account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#comment Account#comment}
        :param first_name: First name of the initial administrative user of the account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#first_name Account#first_name}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#id Account#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param last_name: Last name of the initial administrative user of the account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#last_name Account#last_name}
        :param must_change_password: Specifies whether the new user created to administer the account is forced to change their password upon first login into the account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#must_change_password Account#must_change_password}
        :param region: ID of the Snowflake Region where the account is created. If no value is provided, Snowflake creates the account in the same Snowflake Region as the current account (i.e. the account in which the CREATE ACCOUNT statement is executed.) Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#region Account#region}
        :param region_group: ID of the Snowflake Region where the account is created. If no value is provided, Snowflake creates the account in the same Snowflake Region as the current account (i.e. the account in which the CREATE ACCOUNT statement is executed.) Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#region_group Account#region_group}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a29373c62148b7ac2a789ffbf18a14e4d195a99589893aeffac7dc5a22d115b9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AccountConfig(
            admin_name=admin_name,
            edition=edition,
            email=email,
            name=name,
            admin_password=admin_password,
            admin_rsa_public_key=admin_rsa_public_key,
            comment=comment,
            first_name=first_name,
            id=id,
            last_name=last_name,
            must_change_password=must_change_password,
            region=region,
            region_group=region_group,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetAdminPassword")
    def reset_admin_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminPassword", []))

    @jsii.member(jsii_name="resetAdminRsaPublicKey")
    def reset_admin_rsa_public_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminRsaPublicKey", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetFirstName")
    def reset_first_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirstName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLastName")
    def reset_last_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastName", []))

    @jsii.member(jsii_name="resetMustChangePassword")
    def reset_must_change_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMustChangePassword", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRegionGroup")
    def reset_region_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegionGroup", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="isOrgAdmin")
    def is_org_admin(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isOrgAdmin"))

    @builtins.property
    @jsii.member(jsii_name="adminNameInput")
    def admin_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminNameInput"))

    @builtins.property
    @jsii.member(jsii_name="adminPasswordInput")
    def admin_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="adminRsaPublicKeyInput")
    def admin_rsa_public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminRsaPublicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="editionInput")
    def edition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "editionInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="firstNameInput")
    def first_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firstNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="lastNameInput")
    def last_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastNameInput"))

    @builtins.property
    @jsii.member(jsii_name="mustChangePasswordInput")
    def must_change_password_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mustChangePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionGroupInput")
    def region_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="adminName")
    def admin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminName"))

    @admin_name.setter
    def admin_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b6163896dcab16fd16710ad2a40753a473079e78d9b67ce04bf4dbed3a726f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminName", value)

    @builtins.property
    @jsii.member(jsii_name="adminPassword")
    def admin_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminPassword"))

    @admin_password.setter
    def admin_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ee2b0b668d131877584b9b9f9bd9da91a8ac0eca865697428e50b2b89506a12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminPassword", value)

    @builtins.property
    @jsii.member(jsii_name="adminRsaPublicKey")
    def admin_rsa_public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "adminRsaPublicKey"))

    @admin_rsa_public_key.setter
    def admin_rsa_public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d11a9794d08aae08f0874f8bb161a0d04cb2000de018e83ae779ea9a9c22e016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminRsaPublicKey", value)

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2a94eae3c2f6cd2ca32ce95ce2a6580cc790172582322a761973d10bdc00dbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value)

    @builtins.property
    @jsii.member(jsii_name="edition")
    def edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edition"))

    @edition.setter
    def edition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b9d86cbfe589f174d83611b9465f4e6f97436bd46332f4671738317c42e443)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edition", value)

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4846ef9e4d5a8ef166e502a46f05815a04fc0e6104db37c342759fa565ee3ee1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value)

    @builtins.property
    @jsii.member(jsii_name="firstName")
    def first_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firstName"))

    @first_name.setter
    def first_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbd203ab91e49886cb22a6a9cf5ffd1227a7766264ff521c812715aeb5a4e66e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firstName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55b05546c806723aa39bfad5745dceca46c711b42c16da6a1db578590683d3e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="lastName")
    def last_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastName"))

    @last_name.setter
    def last_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77031a3ec032fc044313626f58e6a8bd2d831b0009f7d0c082026edbbf1d3e73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastName", value)

    @builtins.property
    @jsii.member(jsii_name="mustChangePassword")
    def must_change_password(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mustChangePassword"))

    @must_change_password.setter
    def must_change_password(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36f8af34993e19c693a1b86d42507c5976d12738fdac85ef4a1db7b55cab0ca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mustChangePassword", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__130b2230470ce387b43ae3af7d427b002bd349da116bdc4a39bb859343f7bb22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f04cdb119dfe3481568784effa2b7792d51e15551c3ab67e3ade1bac345caab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="regionGroup")
    def region_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionGroup"))

    @region_group.setter
    def region_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f239fabc136776fcbdb4e1b736f0f2f370000b96e28fb0e1c0d458365ad1c1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionGroup", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.account.AccountConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "admin_name": "adminName",
        "edition": "edition",
        "email": "email",
        "name": "name",
        "admin_password": "adminPassword",
        "admin_rsa_public_key": "adminRsaPublicKey",
        "comment": "comment",
        "first_name": "firstName",
        "id": "id",
        "last_name": "lastName",
        "must_change_password": "mustChangePassword",
        "region": "region",
        "region_group": "regionGroup",
    },
)
class AccountConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        admin_name: builtins.str,
        edition: builtins.str,
        email: builtins.str,
        name: builtins.str,
        admin_password: typing.Optional[builtins.str] = None,
        admin_rsa_public_key: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        first_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        last_name: typing.Optional[builtins.str] = None,
        must_change_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        region_group: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param admin_name: Login name of the initial administrative user of the account. A new user is created in the new account with this name and password and granted the ACCOUNTADMIN role in the account. A login name can be any string consisting of letters, numbers, and underscores. Login names are always case-insensitive. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#admin_name Account#admin_name}
        :param edition: `Snowflake Edition <https://docs.snowflake.com/en/user-guide/intro-editions.html>`_ of the account. Valid values are: STANDARD | ENTERPRISE | BUSINESS_CRITICAL. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#edition Account#edition}
        :param email: Email address of the initial administrative user of the account. This email address is used to send any notifications about the account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#email Account#email}
        :param name: Specifies the identifier (i.e. name) for the account; must be unique within an organization, regardless of which Snowflake Region the account is in. In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters except for underscores (_). Note that if the account name includes underscores, features that do not accept account names with underscores (e.g. Okta SSO or SCIM) can reference a version of the account name that substitutes hyphens (-) for the underscores. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#name Account#name}
        :param admin_password: Password for the initial administrative user of the account. Optional if the ``ADMIN_RSA_PUBLIC_KEY`` parameter is specified. For more information about passwords in Snowflake, see `Snowflake-provided Password Policy <https://docs.snowflake.com/en/sql-reference/sql/create-account.html#:~:text=Snowflake%2Dprovided%20Password%20Policy>`_. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#admin_password Account#admin_password}
        :param admin_rsa_public_key: Assigns a public key to the initial administrative user of the account in order to implement `key pair authentication <https://docs.snowflake.com/en/sql-reference/sql/create-account.html#:~:text=key%20pair%20authentication>`_ for the user. Optional if the ``ADMIN_PASSWORD`` parameter is specified. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#admin_rsa_public_key Account#admin_rsa_public_key}
        :param comment: Specifies a comment for the account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#comment Account#comment}
        :param first_name: First name of the initial administrative user of the account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#first_name Account#first_name}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#id Account#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param last_name: Last name of the initial administrative user of the account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#last_name Account#last_name}
        :param must_change_password: Specifies whether the new user created to administer the account is forced to change their password upon first login into the account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#must_change_password Account#must_change_password}
        :param region: ID of the Snowflake Region where the account is created. If no value is provided, Snowflake creates the account in the same Snowflake Region as the current account (i.e. the account in which the CREATE ACCOUNT statement is executed.) Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#region Account#region}
        :param region_group: ID of the Snowflake Region where the account is created. If no value is provided, Snowflake creates the account in the same Snowflake Region as the current account (i.e. the account in which the CREATE ACCOUNT statement is executed.) Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#region_group Account#region_group}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b266165bc094077007b82aaae53c2057678021a29a5a57ee79781990bc91348)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument admin_name", value=admin_name, expected_type=type_hints["admin_name"])
            check_type(argname="argument edition", value=edition, expected_type=type_hints["edition"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument admin_password", value=admin_password, expected_type=type_hints["admin_password"])
            check_type(argname="argument admin_rsa_public_key", value=admin_rsa_public_key, expected_type=type_hints["admin_rsa_public_key"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument first_name", value=first_name, expected_type=type_hints["first_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument last_name", value=last_name, expected_type=type_hints["last_name"])
            check_type(argname="argument must_change_password", value=must_change_password, expected_type=type_hints["must_change_password"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument region_group", value=region_group, expected_type=type_hints["region_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_name": admin_name,
            "edition": edition,
            "email": email,
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
        if admin_password is not None:
            self._values["admin_password"] = admin_password
        if admin_rsa_public_key is not None:
            self._values["admin_rsa_public_key"] = admin_rsa_public_key
        if comment is not None:
            self._values["comment"] = comment
        if first_name is not None:
            self._values["first_name"] = first_name
        if id is not None:
            self._values["id"] = id
        if last_name is not None:
            self._values["last_name"] = last_name
        if must_change_password is not None:
            self._values["must_change_password"] = must_change_password
        if region is not None:
            self._values["region"] = region
        if region_group is not None:
            self._values["region_group"] = region_group

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
    def admin_name(self) -> builtins.str:
        '''Login name of the initial administrative user of the account.

        A new user is created in the new account with this name and password and granted the ACCOUNTADMIN role in the account. A login name can be any string consisting of letters, numbers, and underscores. Login names are always case-insensitive.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#admin_name Account#admin_name}
        '''
        result = self._values.get("admin_name")
        assert result is not None, "Required property 'admin_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def edition(self) -> builtins.str:
        '''`Snowflake Edition <https://docs.snowflake.com/en/user-guide/intro-editions.html>`_ of the account. Valid values are: STANDARD | ENTERPRISE | BUSINESS_CRITICAL.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#edition Account#edition}
        '''
        result = self._values.get("edition")
        assert result is not None, "Required property 'edition' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def email(self) -> builtins.str:
        '''Email address of the initial administrative user of the account.

        This email address is used to send any notifications about the account.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#email Account#email}
        '''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the identifier (i.e. name) for the account; must be unique within an organization, regardless of which Snowflake Region the account is in. In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters except for underscores (_). Note that if the account name includes underscores, features that do not accept account names with underscores (e.g. Okta SSO or SCIM) can reference a version of the account name that substitutes hyphens (-) for the underscores.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#name Account#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def admin_password(self) -> typing.Optional[builtins.str]:
        '''Password for the initial administrative user of the account.

        Optional if the ``ADMIN_RSA_PUBLIC_KEY`` parameter is specified. For more information about passwords in Snowflake, see `Snowflake-provided Password Policy <https://docs.snowflake.com/en/sql-reference/sql/create-account.html#:~:text=Snowflake%2Dprovided%20Password%20Policy>`_.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#admin_password Account#admin_password}
        '''
        result = self._values.get("admin_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def admin_rsa_public_key(self) -> typing.Optional[builtins.str]:
        '''Assigns a public key to the initial administrative user of the account in order to implement `key pair authentication <https://docs.snowflake.com/en/sql-reference/sql/create-account.html#:~:text=key%20pair%20authentication>`_ for the user. Optional if the ``ADMIN_PASSWORD`` parameter is specified.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#admin_rsa_public_key Account#admin_rsa_public_key}
        '''
        result = self._values.get("admin_rsa_public_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the account.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#comment Account#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def first_name(self) -> typing.Optional[builtins.str]:
        '''First name of the initial administrative user of the account.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#first_name Account#first_name}
        '''
        result = self._values.get("first_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#id Account#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def last_name(self) -> typing.Optional[builtins.str]:
        '''Last name of the initial administrative user of the account.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#last_name Account#last_name}
        '''
        result = self._values.get("last_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def must_change_password(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether the new user created to administer the account is forced to change their password upon first login into the account.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#must_change_password Account#must_change_password}
        '''
        result = self._values.get("must_change_password")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''ID of the Snowflake Region where the account is created.

        If no value is provided, Snowflake creates the account in the same Snowflake Region as the current account (i.e. the account in which the CREATE ACCOUNT statement is executed.)

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#region Account#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region_group(self) -> typing.Optional[builtins.str]:
        '''ID of the Snowflake Region where the account is created.

        If no value is provided, Snowflake creates the account in the same Snowflake Region as the current account (i.e. the account in which the CREATE ACCOUNT statement is executed.)

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/snowflake/r/account#region_group Account#region_group}
        '''
        result = self._values.get("region_group")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccountConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Account",
    "AccountConfig",
]

publication.publish()

def _typecheckingstub__a29373c62148b7ac2a789ffbf18a14e4d195a99589893aeffac7dc5a22d115b9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    admin_name: builtins.str,
    edition: builtins.str,
    email: builtins.str,
    name: builtins.str,
    admin_password: typing.Optional[builtins.str] = None,
    admin_rsa_public_key: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    first_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    must_change_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    region_group: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__7b6163896dcab16fd16710ad2a40753a473079e78d9b67ce04bf4dbed3a726f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee2b0b668d131877584b9b9f9bd9da91a8ac0eca865697428e50b2b89506a12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d11a9794d08aae08f0874f8bb161a0d04cb2000de018e83ae779ea9a9c22e016(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a94eae3c2f6cd2ca32ce95ce2a6580cc790172582322a761973d10bdc00dbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b9d86cbfe589f174d83611b9465f4e6f97436bd46332f4671738317c42e443(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4846ef9e4d5a8ef166e502a46f05815a04fc0e6104db37c342759fa565ee3ee1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbd203ab91e49886cb22a6a9cf5ffd1227a7766264ff521c812715aeb5a4e66e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55b05546c806723aa39bfad5745dceca46c711b42c16da6a1db578590683d3e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77031a3ec032fc044313626f58e6a8bd2d831b0009f7d0c082026edbbf1d3e73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36f8af34993e19c693a1b86d42507c5976d12738fdac85ef4a1db7b55cab0ca9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__130b2230470ce387b43ae3af7d427b002bd349da116bdc4a39bb859343f7bb22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f04cdb119dfe3481568784effa2b7792d51e15551c3ab67e3ade1bac345caab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f239fabc136776fcbdb4e1b736f0f2f370000b96e28fb0e1c0d458365ad1c1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b266165bc094077007b82aaae53c2057678021a29a5a57ee79781990bc91348(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    admin_name: builtins.str,
    edition: builtins.str,
    email: builtins.str,
    name: builtins.str,
    admin_password: typing.Optional[builtins.str] = None,
    admin_rsa_public_key: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    first_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    must_change_password: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    region_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
