'''
[![NPM version](https://badge.fury.io/js/lambda-layer-version-cleaner.svg)](https://badge.fury.io/js/lambda-layer-version-cleaner)
[![PyPI version](https://badge.fury.io/py/lambda-layer-version-cleaner.svg)](https://badge.fury.io/py/lambda-layer-version-cleaner)
![Release](https://github.com/unirt/lambda-layer-version-cleaner/workflows/release/badge.svg)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# lambda-layer-version-cleaner

`lambda-layer-version-cleaner` is a CDK Construct that helps you manage and automatically clean up old versions of AWS Lambda Layers. It works with both JavaScript / TypeScript and Python CDK apps. Please note that this cleaner will only clean up versions of Lambda Layers in the region where it's deployed.

## Installation

For JavaScript / TypeScript projects:

```bash
npm install lambda-layer-version-cleaner
```

For Python projects:

```bash
pip install lambda-layer-version-cleaner
```

## Usage

To use the `LambdaLayerVersionCleaner` in your CDK project, simply import it and add it to your stack. Note that the cleaner will delete old versions of Lambda Layers even if they are associated with Lambda functions. Please ensure that you are aware of this behavior before using the cleaner in your project.

### JavaScript / TypeScript

```javascript
import * as cdk from 'aws-cdk-lib';
import * as events from 'aws-cdk-lib/aws-events';
import { LambdaLayerVersionCleaner } from 'lambda-layer-version-cleaner';

const app = new cdk.App();
const stack = new cdk.Stack(app, 'ExampleStack');

new LambdaLayerVersionCleaner(stack, 'LambdaLayerVersionCleaner', {
  retainVersions: 10,
  layerCleanerSchedule: events.Schedule.rate(cdk.Duration.days(7)),
});
```

### Python

```python
from aws_cdk import core as cdk
from aws_cdk.aws_events import Schedule
from aws_cdk.core import Duration
from lambda_layer_version_cleaner import LambdaLayerVersionCleaner

app = cdk.App()
stack = cdk.Stack(app, "ExampleStack")

LambdaLayerVersionCleaner(stack, "LambdaLayerVersionCleaner",
    retain_versions=10,
    layer_cleaner_schedule=Schedule.rate(Duration.days(7))
)

app.synth()
```

## Configuration

The `LambdaLayerVersionCleaner` construct takes two required parameters and two optional parameters:

* `retainVersions`: The number of layer versions to retain, specified as a positive integer. The cleaner will delete older versions beyond this count. Note that if a Layer has only one version, it won't be deleted.
* `layerCleanerSchedule`: The schedule for running the cleanup process.

The optional parameters are:

* `handlerTimeout` (default: `cdk.Duration.minutes(15)`): Maximum allowed runtime for the Lambda function.
* `handlerMemorySize` (default: `256`): Amount of memory allocated to the Lambda function.
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

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.interface(
    jsii_type="lambda-layer-version-cleaner.ILambdaLayerVersionCleanerProps"
)
class ILambdaLayerVersionCleanerProps(typing_extensions.Protocol):
    '''(experimental) Properties for ``LambdaLayerVersionCleaner``.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="layerCleanerSchedule")
    def layer_cleaner_schedule(self) -> _aws_cdk_aws_events_ceddda9d.Schedule:
        '''(experimental) Schedule for the function execution (no default value).

        :stability: experimental
        '''
        ...

    @layer_cleaner_schedule.setter
    def layer_cleaner_schedule(
        self,
        value: _aws_cdk_aws_events_ceddda9d.Schedule,
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="retainVersions")
    def retain_versions(self) -> jsii.Number:
        '''(experimental) Number of versions to retain (no default value, must be a positive integer).

        :stability: experimental
        '''
        ...

    @retain_versions.setter
    def retain_versions(self, value: jsii.Number) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="handlerMemorySize")
    def handler_memory_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Amount of memory allocated to the Lambda function (default is 256MB).

        :default: 256

        :stability: experimental
        '''
        ...

    @handler_memory_size.setter
    def handler_memory_size(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="handlerTimeout")
    def handler_timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) Maximum allowed runtime for the Lambda function (default is 15 minutes).

        :default: cdk.Duration.minutes(15)

        :stability: experimental
        '''
        ...

    @handler_timeout.setter
    def handler_timeout(
        self,
        value: typing.Optional[_aws_cdk_ceddda9d.Duration],
    ) -> None:
        ...


class _ILambdaLayerVersionCleanerPropsProxy:
    '''(experimental) Properties for ``LambdaLayerVersionCleaner``.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "lambda-layer-version-cleaner.ILambdaLayerVersionCleanerProps"

    @builtins.property
    @jsii.member(jsii_name="layerCleanerSchedule")
    def layer_cleaner_schedule(self) -> _aws_cdk_aws_events_ceddda9d.Schedule:
        '''(experimental) Schedule for the function execution (no default value).

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_events_ceddda9d.Schedule, jsii.get(self, "layerCleanerSchedule"))

    @layer_cleaner_schedule.setter
    def layer_cleaner_schedule(
        self,
        value: _aws_cdk_aws_events_ceddda9d.Schedule,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__889aae22edc164118fdace848969daab57a171a9ff790b110ee4695b4110dd07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "layerCleanerSchedule", value)

    @builtins.property
    @jsii.member(jsii_name="retainVersions")
    def retain_versions(self) -> jsii.Number:
        '''(experimental) Number of versions to retain (no default value, must be a positive integer).

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "retainVersions"))

    @retain_versions.setter
    def retain_versions(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__336386c52fec3053b4e545d31dcc33300b95e9405e3f4c7dd964fc2cd528d610)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retainVersions", value)

    @builtins.property
    @jsii.member(jsii_name="handlerMemorySize")
    def handler_memory_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Amount of memory allocated to the Lambda function (default is 256MB).

        :default: 256

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "handlerMemorySize"))

    @handler_memory_size.setter
    def handler_memory_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae4644aebe6a9b98665a167aca78344ba4d2c4787a54d001d9ae58a5257a8c83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "handlerMemorySize", value)

    @builtins.property
    @jsii.member(jsii_name="handlerTimeout")
    def handler_timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) Maximum allowed runtime for the Lambda function (default is 15 minutes).

        :default: cdk.Duration.minutes(15)

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "handlerTimeout"))

    @handler_timeout.setter
    def handler_timeout(
        self,
        value: typing.Optional[_aws_cdk_ceddda9d.Duration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51e0b30855bc3c47437d5c9f464a87a96714377080dd26b6349eb5ab3defddd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "handlerTimeout", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILambdaLayerVersionCleanerProps).__jsii_proxy_class__ = lambda : _ILambdaLayerVersionCleanerPropsProxy


class LambdaLayerVersionCleaner(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="lambda-layer-version-cleaner.LambdaLayerVersionCleaner",
):
    '''(experimental) Lambda Layer Version Cleaner Construct.

    This construct creates a Lambda function that deletes old versions of a Lambda Layer. The function is
    scheduled to run at a regular interval using an EventBridge rule. The number of versions to retain
    must be specified as a positive integer using the ``ILambdaLayerVersionCleanerProps`` interface.
    The function execution schedule is also required to be set in the ``ILambdaLayerVersionCleanerProps`` interface.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: ILambdaLayerVersionCleanerProps,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__465fadc5f9415506f794eb4c0acec8e1448e11304b62382369129d986030dfad)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, jsii.get(self, "handler"))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.get(self, "rule"))


__all__ = [
    "ILambdaLayerVersionCleanerProps",
    "LambdaLayerVersionCleaner",
]

publication.publish()

def _typecheckingstub__889aae22edc164118fdace848969daab57a171a9ff790b110ee4695b4110dd07(
    value: _aws_cdk_aws_events_ceddda9d.Schedule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__336386c52fec3053b4e545d31dcc33300b95e9405e3f4c7dd964fc2cd528d610(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae4644aebe6a9b98665a167aca78344ba4d2c4787a54d001d9ae58a5257a8c83(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e0b30855bc3c47437d5c9f464a87a96714377080dd26b6349eb5ab3defddd7(
    value: typing.Optional[_aws_cdk_ceddda9d.Duration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__465fadc5f9415506f794eb4c0acec8e1448e11304b62382369129d986030dfad(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: ILambdaLayerVersionCleanerProps,
) -> None:
    """Type checking stubs"""
    pass
