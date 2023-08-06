"""
Type annotations for vpc-lattice service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/type_defs/)

Usage::

    ```python
    from mypy_boto3_vpc_lattice.type_defs import AccessLogSubscriptionSummaryTypeDef

    data: AccessLogSubscriptionSummaryTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AuthPolicyStateType,
    AuthTypeType,
    HealthCheckProtocolVersionType,
    IpAddressTypeType,
    ListenerProtocolType,
    ServiceNetworkServiceAssociationStatusType,
    ServiceNetworkVpcAssociationStatusType,
    ServiceStatusType,
    TargetGroupProtocolType,
    TargetGroupProtocolVersionType,
    TargetGroupStatusType,
    TargetGroupTypeType,
    TargetStatusType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AccessLogSubscriptionSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "RuleUpdateFailureTypeDef",
    "CreateAccessLogSubscriptionRequestRequestTypeDef",
    "CreateServiceNetworkRequestRequestTypeDef",
    "CreateServiceNetworkServiceAssociationRequestRequestTypeDef",
    "DnsEntryTypeDef",
    "CreateServiceNetworkVpcAssociationRequestRequestTypeDef",
    "CreateServiceRequestRequestTypeDef",
    "DeleteAccessLogSubscriptionRequestRequestTypeDef",
    "DeleteAuthPolicyRequestRequestTypeDef",
    "DeleteListenerRequestRequestTypeDef",
    "DeleteResourcePolicyRequestRequestTypeDef",
    "DeleteRuleRequestRequestTypeDef",
    "DeleteServiceNetworkRequestRequestTypeDef",
    "DeleteServiceNetworkServiceAssociationRequestRequestTypeDef",
    "DeleteServiceNetworkVpcAssociationRequestRequestTypeDef",
    "DeleteServiceRequestRequestTypeDef",
    "DeleteTargetGroupRequestRequestTypeDef",
    "TargetTypeDef",
    "TargetFailureTypeDef",
    "FixedResponseActionTypeDef",
    "WeightedTargetGroupTypeDef",
    "GetAccessLogSubscriptionRequestRequestTypeDef",
    "GetAuthPolicyRequestRequestTypeDef",
    "GetListenerRequestRequestTypeDef",
    "GetResourcePolicyRequestRequestTypeDef",
    "GetRuleRequestRequestTypeDef",
    "GetServiceNetworkRequestRequestTypeDef",
    "GetServiceNetworkServiceAssociationRequestRequestTypeDef",
    "GetServiceNetworkVpcAssociationRequestRequestTypeDef",
    "GetServiceRequestRequestTypeDef",
    "GetTargetGroupRequestRequestTypeDef",
    "HeaderMatchTypeTypeDef",
    "MatcherTypeDef",
    "PaginatorConfigTypeDef",
    "ListAccessLogSubscriptionsRequestRequestTypeDef",
    "ListListenersRequestRequestTypeDef",
    "ListenerSummaryTypeDef",
    "ListRulesRequestRequestTypeDef",
    "RuleSummaryTypeDef",
    "ListServiceNetworkServiceAssociationsRequestRequestTypeDef",
    "ListServiceNetworkVpcAssociationsRequestRequestTypeDef",
    "ServiceNetworkVpcAssociationSummaryTypeDef",
    "ListServiceNetworksRequestRequestTypeDef",
    "ServiceNetworkSummaryTypeDef",
    "ListServicesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTargetGroupsRequestRequestTypeDef",
    "TargetGroupSummaryTypeDef",
    "TargetSummaryTypeDef",
    "PathMatchTypeTypeDef",
    "PutAuthPolicyRequestRequestTypeDef",
    "PutResourcePolicyRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAccessLogSubscriptionRequestRequestTypeDef",
    "UpdateServiceNetworkRequestRequestTypeDef",
    "UpdateServiceNetworkVpcAssociationRequestRequestTypeDef",
    "UpdateServiceRequestRequestTypeDef",
    "CreateAccessLogSubscriptionResponseTypeDef",
    "CreateServiceNetworkResponseTypeDef",
    "CreateServiceNetworkVpcAssociationResponseTypeDef",
    "DeleteServiceNetworkServiceAssociationResponseTypeDef",
    "DeleteServiceNetworkVpcAssociationResponseTypeDef",
    "DeleteServiceResponseTypeDef",
    "DeleteTargetGroupResponseTypeDef",
    "GetAccessLogSubscriptionResponseTypeDef",
    "GetAuthPolicyResponseTypeDef",
    "GetResourcePolicyResponseTypeDef",
    "GetServiceNetworkResponseTypeDef",
    "GetServiceNetworkVpcAssociationResponseTypeDef",
    "ListAccessLogSubscriptionsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PutAuthPolicyResponseTypeDef",
    "UpdateAccessLogSubscriptionResponseTypeDef",
    "UpdateServiceNetworkResponseTypeDef",
    "UpdateServiceNetworkVpcAssociationResponseTypeDef",
    "UpdateServiceResponseTypeDef",
    "CreateServiceNetworkServiceAssociationResponseTypeDef",
    "CreateServiceResponseTypeDef",
    "GetServiceNetworkServiceAssociationResponseTypeDef",
    "GetServiceResponseTypeDef",
    "ServiceNetworkServiceAssociationSummaryTypeDef",
    "ServiceSummaryTypeDef",
    "DeregisterTargetsRequestRequestTypeDef",
    "ListTargetsRequestRequestTypeDef",
    "RegisterTargetsRequestRequestTypeDef",
    "DeregisterTargetsResponseTypeDef",
    "RegisterTargetsResponseTypeDef",
    "ForwardActionTypeDef",
    "HeaderMatchTypeDef",
    "HealthCheckConfigTypeDef",
    "ListAccessLogSubscriptionsRequestListAccessLogSubscriptionsPaginateTypeDef",
    "ListListenersRequestListListenersPaginateTypeDef",
    "ListRulesRequestListRulesPaginateTypeDef",
    "ListServiceNetworkServiceAssociationsRequestListServiceNetworkServiceAssociationsPaginateTypeDef",
    "ListServiceNetworkVpcAssociationsRequestListServiceNetworkVpcAssociationsPaginateTypeDef",
    "ListServiceNetworksRequestListServiceNetworksPaginateTypeDef",
    "ListServicesRequestListServicesPaginateTypeDef",
    "ListTargetGroupsRequestListTargetGroupsPaginateTypeDef",
    "ListTargetsRequestListTargetsPaginateTypeDef",
    "ListListenersResponseTypeDef",
    "ListRulesResponseTypeDef",
    "ListServiceNetworkVpcAssociationsResponseTypeDef",
    "ListServiceNetworksResponseTypeDef",
    "ListTargetGroupsResponseTypeDef",
    "ListTargetsResponseTypeDef",
    "PathMatchTypeDef",
    "ListServiceNetworkServiceAssociationsResponseTypeDef",
    "ListServicesResponseTypeDef",
    "RuleActionTypeDef",
    "TargetGroupConfigTypeDef",
    "UpdateTargetGroupRequestRequestTypeDef",
    "HttpMatchTypeDef",
    "CreateListenerRequestRequestTypeDef",
    "CreateListenerResponseTypeDef",
    "GetListenerResponseTypeDef",
    "UpdateListenerRequestRequestTypeDef",
    "UpdateListenerResponseTypeDef",
    "CreateTargetGroupRequestRequestTypeDef",
    "CreateTargetGroupResponseTypeDef",
    "GetTargetGroupResponseTypeDef",
    "UpdateTargetGroupResponseTypeDef",
    "RuleMatchTypeDef",
    "CreateRuleRequestRequestTypeDef",
    "CreateRuleResponseTypeDef",
    "GetRuleResponseTypeDef",
    "RuleUpdateSuccessTypeDef",
    "RuleUpdateTypeDef",
    "UpdateRuleRequestRequestTypeDef",
    "UpdateRuleResponseTypeDef",
    "BatchUpdateRuleResponseTypeDef",
    "BatchUpdateRuleRequestRequestTypeDef",
)

AccessLogSubscriptionSummaryTypeDef = TypedDict(
    "AccessLogSubscriptionSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "destinationArn": str,
        "id": str,
        "lastUpdatedAt": datetime,
        "resourceArn": str,
        "resourceId": str,
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

RuleUpdateFailureTypeDef = TypedDict(
    "RuleUpdateFailureTypeDef",
    {
        "failureCode": str,
        "failureMessage": str,
        "ruleIdentifier": str,
    },
    total=False,
)

_RequiredCreateAccessLogSubscriptionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAccessLogSubscriptionRequestRequestTypeDef",
    {
        "destinationArn": str,
        "resourceIdentifier": str,
    },
)
_OptionalCreateAccessLogSubscriptionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAccessLogSubscriptionRequestRequestTypeDef",
    {
        "clientToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateAccessLogSubscriptionRequestRequestTypeDef(
    _RequiredCreateAccessLogSubscriptionRequestRequestTypeDef,
    _OptionalCreateAccessLogSubscriptionRequestRequestTypeDef,
):
    pass


_RequiredCreateServiceNetworkRequestRequestTypeDef = TypedDict(
    "_RequiredCreateServiceNetworkRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateServiceNetworkRequestRequestTypeDef = TypedDict(
    "_OptionalCreateServiceNetworkRequestRequestTypeDef",
    {
        "authType": AuthTypeType,
        "clientToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateServiceNetworkRequestRequestTypeDef(
    _RequiredCreateServiceNetworkRequestRequestTypeDef,
    _OptionalCreateServiceNetworkRequestRequestTypeDef,
):
    pass


_RequiredCreateServiceNetworkServiceAssociationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateServiceNetworkServiceAssociationRequestRequestTypeDef",
    {
        "serviceIdentifier": str,
        "serviceNetworkIdentifier": str,
    },
)
_OptionalCreateServiceNetworkServiceAssociationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateServiceNetworkServiceAssociationRequestRequestTypeDef",
    {
        "clientToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateServiceNetworkServiceAssociationRequestRequestTypeDef(
    _RequiredCreateServiceNetworkServiceAssociationRequestRequestTypeDef,
    _OptionalCreateServiceNetworkServiceAssociationRequestRequestTypeDef,
):
    pass


DnsEntryTypeDef = TypedDict(
    "DnsEntryTypeDef",
    {
        "domainName": str,
        "hostedZoneId": str,
    },
    total=False,
)

_RequiredCreateServiceNetworkVpcAssociationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateServiceNetworkVpcAssociationRequestRequestTypeDef",
    {
        "serviceNetworkIdentifier": str,
        "vpcIdentifier": str,
    },
)
_OptionalCreateServiceNetworkVpcAssociationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateServiceNetworkVpcAssociationRequestRequestTypeDef",
    {
        "clientToken": str,
        "securityGroupIds": Sequence[str],
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateServiceNetworkVpcAssociationRequestRequestTypeDef(
    _RequiredCreateServiceNetworkVpcAssociationRequestRequestTypeDef,
    _OptionalCreateServiceNetworkVpcAssociationRequestRequestTypeDef,
):
    pass


_RequiredCreateServiceRequestRequestTypeDef = TypedDict(
    "_RequiredCreateServiceRequestRequestTypeDef",
    {
        "name": str,
    },
)
_OptionalCreateServiceRequestRequestTypeDef = TypedDict(
    "_OptionalCreateServiceRequestRequestTypeDef",
    {
        "authType": AuthTypeType,
        "certificateArn": str,
        "clientToken": str,
        "customDomainName": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateServiceRequestRequestTypeDef(
    _RequiredCreateServiceRequestRequestTypeDef, _OptionalCreateServiceRequestRequestTypeDef
):
    pass


DeleteAccessLogSubscriptionRequestRequestTypeDef = TypedDict(
    "DeleteAccessLogSubscriptionRequestRequestTypeDef",
    {
        "accessLogSubscriptionIdentifier": str,
    },
)

DeleteAuthPolicyRequestRequestTypeDef = TypedDict(
    "DeleteAuthPolicyRequestRequestTypeDef",
    {
        "resourceIdentifier": str,
    },
)

DeleteListenerRequestRequestTypeDef = TypedDict(
    "DeleteListenerRequestRequestTypeDef",
    {
        "listenerIdentifier": str,
        "serviceIdentifier": str,
    },
)

DeleteResourcePolicyRequestRequestTypeDef = TypedDict(
    "DeleteResourcePolicyRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

DeleteRuleRequestRequestTypeDef = TypedDict(
    "DeleteRuleRequestRequestTypeDef",
    {
        "listenerIdentifier": str,
        "ruleIdentifier": str,
        "serviceIdentifier": str,
    },
)

DeleteServiceNetworkRequestRequestTypeDef = TypedDict(
    "DeleteServiceNetworkRequestRequestTypeDef",
    {
        "serviceNetworkIdentifier": str,
    },
)

DeleteServiceNetworkServiceAssociationRequestRequestTypeDef = TypedDict(
    "DeleteServiceNetworkServiceAssociationRequestRequestTypeDef",
    {
        "serviceNetworkServiceAssociationIdentifier": str,
    },
)

DeleteServiceNetworkVpcAssociationRequestRequestTypeDef = TypedDict(
    "DeleteServiceNetworkVpcAssociationRequestRequestTypeDef",
    {
        "serviceNetworkVpcAssociationIdentifier": str,
    },
)

DeleteServiceRequestRequestTypeDef = TypedDict(
    "DeleteServiceRequestRequestTypeDef",
    {
        "serviceIdentifier": str,
    },
)

DeleteTargetGroupRequestRequestTypeDef = TypedDict(
    "DeleteTargetGroupRequestRequestTypeDef",
    {
        "targetGroupIdentifier": str,
    },
)

_RequiredTargetTypeDef = TypedDict(
    "_RequiredTargetTypeDef",
    {
        "id": str,
    },
)
_OptionalTargetTypeDef = TypedDict(
    "_OptionalTargetTypeDef",
    {
        "port": int,
    },
    total=False,
)


class TargetTypeDef(_RequiredTargetTypeDef, _OptionalTargetTypeDef):
    pass


TargetFailureTypeDef = TypedDict(
    "TargetFailureTypeDef",
    {
        "failureCode": str,
        "failureMessage": str,
        "id": str,
        "port": int,
    },
    total=False,
)

FixedResponseActionTypeDef = TypedDict(
    "FixedResponseActionTypeDef",
    {
        "statusCode": int,
    },
)

_RequiredWeightedTargetGroupTypeDef = TypedDict(
    "_RequiredWeightedTargetGroupTypeDef",
    {
        "targetGroupIdentifier": str,
    },
)
_OptionalWeightedTargetGroupTypeDef = TypedDict(
    "_OptionalWeightedTargetGroupTypeDef",
    {
        "weight": int,
    },
    total=False,
)


class WeightedTargetGroupTypeDef(
    _RequiredWeightedTargetGroupTypeDef, _OptionalWeightedTargetGroupTypeDef
):
    pass


GetAccessLogSubscriptionRequestRequestTypeDef = TypedDict(
    "GetAccessLogSubscriptionRequestRequestTypeDef",
    {
        "accessLogSubscriptionIdentifier": str,
    },
)

GetAuthPolicyRequestRequestTypeDef = TypedDict(
    "GetAuthPolicyRequestRequestTypeDef",
    {
        "resourceIdentifier": str,
    },
)

GetListenerRequestRequestTypeDef = TypedDict(
    "GetListenerRequestRequestTypeDef",
    {
        "listenerIdentifier": str,
        "serviceIdentifier": str,
    },
)

GetResourcePolicyRequestRequestTypeDef = TypedDict(
    "GetResourcePolicyRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

GetRuleRequestRequestTypeDef = TypedDict(
    "GetRuleRequestRequestTypeDef",
    {
        "listenerIdentifier": str,
        "ruleIdentifier": str,
        "serviceIdentifier": str,
    },
)

GetServiceNetworkRequestRequestTypeDef = TypedDict(
    "GetServiceNetworkRequestRequestTypeDef",
    {
        "serviceNetworkIdentifier": str,
    },
)

GetServiceNetworkServiceAssociationRequestRequestTypeDef = TypedDict(
    "GetServiceNetworkServiceAssociationRequestRequestTypeDef",
    {
        "serviceNetworkServiceAssociationIdentifier": str,
    },
)

GetServiceNetworkVpcAssociationRequestRequestTypeDef = TypedDict(
    "GetServiceNetworkVpcAssociationRequestRequestTypeDef",
    {
        "serviceNetworkVpcAssociationIdentifier": str,
    },
)

GetServiceRequestRequestTypeDef = TypedDict(
    "GetServiceRequestRequestTypeDef",
    {
        "serviceIdentifier": str,
    },
)

GetTargetGroupRequestRequestTypeDef = TypedDict(
    "GetTargetGroupRequestRequestTypeDef",
    {
        "targetGroupIdentifier": str,
    },
)

HeaderMatchTypeTypeDef = TypedDict(
    "HeaderMatchTypeTypeDef",
    {
        "contains": str,
        "exact": str,
        "prefix": str,
    },
    total=False,
)

MatcherTypeDef = TypedDict(
    "MatcherTypeDef",
    {
        "httpCode": str,
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredListAccessLogSubscriptionsRequestRequestTypeDef = TypedDict(
    "_RequiredListAccessLogSubscriptionsRequestRequestTypeDef",
    {
        "resourceIdentifier": str,
    },
)
_OptionalListAccessLogSubscriptionsRequestRequestTypeDef = TypedDict(
    "_OptionalListAccessLogSubscriptionsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListAccessLogSubscriptionsRequestRequestTypeDef(
    _RequiredListAccessLogSubscriptionsRequestRequestTypeDef,
    _OptionalListAccessLogSubscriptionsRequestRequestTypeDef,
):
    pass


_RequiredListListenersRequestRequestTypeDef = TypedDict(
    "_RequiredListListenersRequestRequestTypeDef",
    {
        "serviceIdentifier": str,
    },
)
_OptionalListListenersRequestRequestTypeDef = TypedDict(
    "_OptionalListListenersRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListListenersRequestRequestTypeDef(
    _RequiredListListenersRequestRequestTypeDef, _OptionalListListenersRequestRequestTypeDef
):
    pass


ListenerSummaryTypeDef = TypedDict(
    "ListenerSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "id": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "port": int,
        "protocol": ListenerProtocolType,
    },
    total=False,
)

_RequiredListRulesRequestRequestTypeDef = TypedDict(
    "_RequiredListRulesRequestRequestTypeDef",
    {
        "listenerIdentifier": str,
        "serviceIdentifier": str,
    },
)
_OptionalListRulesRequestRequestTypeDef = TypedDict(
    "_OptionalListRulesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListRulesRequestRequestTypeDef(
    _RequiredListRulesRequestRequestTypeDef, _OptionalListRulesRequestRequestTypeDef
):
    pass


RuleSummaryTypeDef = TypedDict(
    "RuleSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "id": str,
        "isDefault": bool,
        "lastUpdatedAt": datetime,
        "name": str,
        "priority": int,
    },
    total=False,
)

ListServiceNetworkServiceAssociationsRequestRequestTypeDef = TypedDict(
    "ListServiceNetworkServiceAssociationsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "serviceIdentifier": str,
        "serviceNetworkIdentifier": str,
    },
    total=False,
)

ListServiceNetworkVpcAssociationsRequestRequestTypeDef = TypedDict(
    "ListServiceNetworkVpcAssociationsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "serviceNetworkIdentifier": str,
        "vpcIdentifier": str,
    },
    total=False,
)

ServiceNetworkVpcAssociationSummaryTypeDef = TypedDict(
    "ServiceNetworkVpcAssociationSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "createdBy": str,
        "id": str,
        "lastUpdatedAt": datetime,
        "serviceNetworkArn": str,
        "serviceNetworkId": str,
        "serviceNetworkName": str,
        "status": ServiceNetworkVpcAssociationStatusType,
        "vpcId": str,
    },
    total=False,
)

ListServiceNetworksRequestRequestTypeDef = TypedDict(
    "ListServiceNetworksRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ServiceNetworkSummaryTypeDef = TypedDict(
    "ServiceNetworkSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "id": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "numberOfAssociatedServices": int,
        "numberOfAssociatedVPCs": int,
    },
    total=False,
)

ListServicesRequestRequestTypeDef = TypedDict(
    "ListServicesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListTargetGroupsRequestRequestTypeDef = TypedDict(
    "ListTargetGroupsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "targetGroupType": TargetGroupTypeType,
        "vpcIdentifier": str,
    },
    total=False,
)

TargetGroupSummaryTypeDef = TypedDict(
    "TargetGroupSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "id": str,
        "ipAddressType": IpAddressTypeType,
        "lastUpdatedAt": datetime,
        "name": str,
        "port": int,
        "protocol": TargetGroupProtocolType,
        "serviceArns": List[str],
        "status": TargetGroupStatusType,
        "type": TargetGroupTypeType,
        "vpcIdentifier": str,
    },
    total=False,
)

TargetSummaryTypeDef = TypedDict(
    "TargetSummaryTypeDef",
    {
        "id": str,
        "port": int,
        "reasonCode": str,
        "status": TargetStatusType,
    },
    total=False,
)

PathMatchTypeTypeDef = TypedDict(
    "PathMatchTypeTypeDef",
    {
        "exact": str,
        "prefix": str,
    },
    total=False,
)

PutAuthPolicyRequestRequestTypeDef = TypedDict(
    "PutAuthPolicyRequestRequestTypeDef",
    {
        "policy": str,
        "resourceIdentifier": str,
    },
)

PutResourcePolicyRequestRequestTypeDef = TypedDict(
    "PutResourcePolicyRequestRequestTypeDef",
    {
        "policy": str,
        "resourceArn": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

UpdateAccessLogSubscriptionRequestRequestTypeDef = TypedDict(
    "UpdateAccessLogSubscriptionRequestRequestTypeDef",
    {
        "accessLogSubscriptionIdentifier": str,
        "destinationArn": str,
    },
)

UpdateServiceNetworkRequestRequestTypeDef = TypedDict(
    "UpdateServiceNetworkRequestRequestTypeDef",
    {
        "authType": AuthTypeType,
        "serviceNetworkIdentifier": str,
    },
)

UpdateServiceNetworkVpcAssociationRequestRequestTypeDef = TypedDict(
    "UpdateServiceNetworkVpcAssociationRequestRequestTypeDef",
    {
        "securityGroupIds": Sequence[str],
        "serviceNetworkVpcAssociationIdentifier": str,
    },
)

_RequiredUpdateServiceRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateServiceRequestRequestTypeDef",
    {
        "serviceIdentifier": str,
    },
)
_OptionalUpdateServiceRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateServiceRequestRequestTypeDef",
    {
        "authType": AuthTypeType,
        "certificateArn": str,
    },
    total=False,
)


class UpdateServiceRequestRequestTypeDef(
    _RequiredUpdateServiceRequestRequestTypeDef, _OptionalUpdateServiceRequestRequestTypeDef
):
    pass


CreateAccessLogSubscriptionResponseTypeDef = TypedDict(
    "CreateAccessLogSubscriptionResponseTypeDef",
    {
        "arn": str,
        "destinationArn": str,
        "id": str,
        "resourceArn": str,
        "resourceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateServiceNetworkResponseTypeDef = TypedDict(
    "CreateServiceNetworkResponseTypeDef",
    {
        "arn": str,
        "authType": AuthTypeType,
        "id": str,
        "name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateServiceNetworkVpcAssociationResponseTypeDef = TypedDict(
    "CreateServiceNetworkVpcAssociationResponseTypeDef",
    {
        "arn": str,
        "createdBy": str,
        "id": str,
        "securityGroupIds": List[str],
        "status": ServiceNetworkVpcAssociationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteServiceNetworkServiceAssociationResponseTypeDef = TypedDict(
    "DeleteServiceNetworkServiceAssociationResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "status": ServiceNetworkServiceAssociationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteServiceNetworkVpcAssociationResponseTypeDef = TypedDict(
    "DeleteServiceNetworkVpcAssociationResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "status": ServiceNetworkVpcAssociationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteServiceResponseTypeDef = TypedDict(
    "DeleteServiceResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "name": str,
        "status": ServiceStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteTargetGroupResponseTypeDef = TypedDict(
    "DeleteTargetGroupResponseTypeDef",
    {
        "arn": str,
        "id": str,
        "status": TargetGroupStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccessLogSubscriptionResponseTypeDef = TypedDict(
    "GetAccessLogSubscriptionResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "destinationArn": str,
        "id": str,
        "lastUpdatedAt": datetime,
        "resourceArn": str,
        "resourceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAuthPolicyResponseTypeDef = TypedDict(
    "GetAuthPolicyResponseTypeDef",
    {
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "policy": str,
        "state": AuthPolicyStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResourcePolicyResponseTypeDef = TypedDict(
    "GetResourcePolicyResponseTypeDef",
    {
        "policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetServiceNetworkResponseTypeDef = TypedDict(
    "GetServiceNetworkResponseTypeDef",
    {
        "arn": str,
        "authType": AuthTypeType,
        "createdAt": datetime,
        "id": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "numberOfAssociatedServices": int,
        "numberOfAssociatedVPCs": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetServiceNetworkVpcAssociationResponseTypeDef = TypedDict(
    "GetServiceNetworkVpcAssociationResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "createdBy": str,
        "failureCode": str,
        "failureMessage": str,
        "id": str,
        "lastUpdatedAt": datetime,
        "securityGroupIds": List[str],
        "serviceNetworkArn": str,
        "serviceNetworkId": str,
        "serviceNetworkName": str,
        "status": ServiceNetworkVpcAssociationStatusType,
        "vpcId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAccessLogSubscriptionsResponseTypeDef = TypedDict(
    "ListAccessLogSubscriptionsResponseTypeDef",
    {
        "items": List[AccessLogSubscriptionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutAuthPolicyResponseTypeDef = TypedDict(
    "PutAuthPolicyResponseTypeDef",
    {
        "policy": str,
        "state": AuthPolicyStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAccessLogSubscriptionResponseTypeDef = TypedDict(
    "UpdateAccessLogSubscriptionResponseTypeDef",
    {
        "arn": str,
        "destinationArn": str,
        "id": str,
        "resourceArn": str,
        "resourceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateServiceNetworkResponseTypeDef = TypedDict(
    "UpdateServiceNetworkResponseTypeDef",
    {
        "arn": str,
        "authType": AuthTypeType,
        "id": str,
        "name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateServiceNetworkVpcAssociationResponseTypeDef = TypedDict(
    "UpdateServiceNetworkVpcAssociationResponseTypeDef",
    {
        "arn": str,
        "createdBy": str,
        "id": str,
        "securityGroupIds": List[str],
        "status": ServiceNetworkVpcAssociationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateServiceResponseTypeDef = TypedDict(
    "UpdateServiceResponseTypeDef",
    {
        "arn": str,
        "authType": AuthTypeType,
        "certificateArn": str,
        "customDomainName": str,
        "id": str,
        "name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateServiceNetworkServiceAssociationResponseTypeDef = TypedDict(
    "CreateServiceNetworkServiceAssociationResponseTypeDef",
    {
        "arn": str,
        "createdBy": str,
        "customDomainName": str,
        "dnsEntry": DnsEntryTypeDef,
        "id": str,
        "status": ServiceNetworkServiceAssociationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateServiceResponseTypeDef = TypedDict(
    "CreateServiceResponseTypeDef",
    {
        "arn": str,
        "authType": AuthTypeType,
        "certificateArn": str,
        "customDomainName": str,
        "dnsEntry": DnsEntryTypeDef,
        "id": str,
        "name": str,
        "status": ServiceStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetServiceNetworkServiceAssociationResponseTypeDef = TypedDict(
    "GetServiceNetworkServiceAssociationResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "createdBy": str,
        "customDomainName": str,
        "dnsEntry": DnsEntryTypeDef,
        "failureCode": str,
        "failureMessage": str,
        "id": str,
        "serviceArn": str,
        "serviceId": str,
        "serviceName": str,
        "serviceNetworkArn": str,
        "serviceNetworkId": str,
        "serviceNetworkName": str,
        "status": ServiceNetworkServiceAssociationStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetServiceResponseTypeDef = TypedDict(
    "GetServiceResponseTypeDef",
    {
        "arn": str,
        "authType": AuthTypeType,
        "certificateArn": str,
        "createdAt": datetime,
        "customDomainName": str,
        "dnsEntry": DnsEntryTypeDef,
        "failureCode": str,
        "failureMessage": str,
        "id": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "status": ServiceStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ServiceNetworkServiceAssociationSummaryTypeDef = TypedDict(
    "ServiceNetworkServiceAssociationSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "createdBy": str,
        "customDomainName": str,
        "dnsEntry": DnsEntryTypeDef,
        "id": str,
        "serviceArn": str,
        "serviceId": str,
        "serviceName": str,
        "serviceNetworkArn": str,
        "serviceNetworkId": str,
        "serviceNetworkName": str,
        "status": ServiceNetworkServiceAssociationStatusType,
    },
    total=False,
)

ServiceSummaryTypeDef = TypedDict(
    "ServiceSummaryTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "customDomainName": str,
        "dnsEntry": DnsEntryTypeDef,
        "id": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "status": ServiceStatusType,
    },
    total=False,
)

DeregisterTargetsRequestRequestTypeDef = TypedDict(
    "DeregisterTargetsRequestRequestTypeDef",
    {
        "targetGroupIdentifier": str,
        "targets": Sequence[TargetTypeDef],
    },
)

_RequiredListTargetsRequestRequestTypeDef = TypedDict(
    "_RequiredListTargetsRequestRequestTypeDef",
    {
        "targetGroupIdentifier": str,
    },
)
_OptionalListTargetsRequestRequestTypeDef = TypedDict(
    "_OptionalListTargetsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "targets": Sequence[TargetTypeDef],
    },
    total=False,
)


class ListTargetsRequestRequestTypeDef(
    _RequiredListTargetsRequestRequestTypeDef, _OptionalListTargetsRequestRequestTypeDef
):
    pass


RegisterTargetsRequestRequestTypeDef = TypedDict(
    "RegisterTargetsRequestRequestTypeDef",
    {
        "targetGroupIdentifier": str,
        "targets": Sequence[TargetTypeDef],
    },
)

DeregisterTargetsResponseTypeDef = TypedDict(
    "DeregisterTargetsResponseTypeDef",
    {
        "successful": List[TargetTypeDef],
        "unsuccessful": List[TargetFailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterTargetsResponseTypeDef = TypedDict(
    "RegisterTargetsResponseTypeDef",
    {
        "successful": List[TargetTypeDef],
        "unsuccessful": List[TargetFailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ForwardActionTypeDef = TypedDict(
    "ForwardActionTypeDef",
    {
        "targetGroups": Sequence[WeightedTargetGroupTypeDef],
    },
)

_RequiredHeaderMatchTypeDef = TypedDict(
    "_RequiredHeaderMatchTypeDef",
    {
        "match": HeaderMatchTypeTypeDef,
        "name": str,
    },
)
_OptionalHeaderMatchTypeDef = TypedDict(
    "_OptionalHeaderMatchTypeDef",
    {
        "caseSensitive": bool,
    },
    total=False,
)


class HeaderMatchTypeDef(_RequiredHeaderMatchTypeDef, _OptionalHeaderMatchTypeDef):
    pass


HealthCheckConfigTypeDef = TypedDict(
    "HealthCheckConfigTypeDef",
    {
        "enabled": bool,
        "healthCheckIntervalSeconds": int,
        "healthCheckTimeoutSeconds": int,
        "healthyThresholdCount": int,
        "matcher": MatcherTypeDef,
        "path": str,
        "port": int,
        "protocol": TargetGroupProtocolType,
        "protocolVersion": HealthCheckProtocolVersionType,
        "unhealthyThresholdCount": int,
    },
    total=False,
)

_RequiredListAccessLogSubscriptionsRequestListAccessLogSubscriptionsPaginateTypeDef = TypedDict(
    "_RequiredListAccessLogSubscriptionsRequestListAccessLogSubscriptionsPaginateTypeDef",
    {
        "resourceIdentifier": str,
    },
)
_OptionalListAccessLogSubscriptionsRequestListAccessLogSubscriptionsPaginateTypeDef = TypedDict(
    "_OptionalListAccessLogSubscriptionsRequestListAccessLogSubscriptionsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListAccessLogSubscriptionsRequestListAccessLogSubscriptionsPaginateTypeDef(
    _RequiredListAccessLogSubscriptionsRequestListAccessLogSubscriptionsPaginateTypeDef,
    _OptionalListAccessLogSubscriptionsRequestListAccessLogSubscriptionsPaginateTypeDef,
):
    pass


_RequiredListListenersRequestListListenersPaginateTypeDef = TypedDict(
    "_RequiredListListenersRequestListListenersPaginateTypeDef",
    {
        "serviceIdentifier": str,
    },
)
_OptionalListListenersRequestListListenersPaginateTypeDef = TypedDict(
    "_OptionalListListenersRequestListListenersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListListenersRequestListListenersPaginateTypeDef(
    _RequiredListListenersRequestListListenersPaginateTypeDef,
    _OptionalListListenersRequestListListenersPaginateTypeDef,
):
    pass


_RequiredListRulesRequestListRulesPaginateTypeDef = TypedDict(
    "_RequiredListRulesRequestListRulesPaginateTypeDef",
    {
        "listenerIdentifier": str,
        "serviceIdentifier": str,
    },
)
_OptionalListRulesRequestListRulesPaginateTypeDef = TypedDict(
    "_OptionalListRulesRequestListRulesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListRulesRequestListRulesPaginateTypeDef(
    _RequiredListRulesRequestListRulesPaginateTypeDef,
    _OptionalListRulesRequestListRulesPaginateTypeDef,
):
    pass


ListServiceNetworkServiceAssociationsRequestListServiceNetworkServiceAssociationsPaginateTypeDef = TypedDict(
    "ListServiceNetworkServiceAssociationsRequestListServiceNetworkServiceAssociationsPaginateTypeDef",
    {
        "serviceIdentifier": str,
        "serviceNetworkIdentifier": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListServiceNetworkVpcAssociationsRequestListServiceNetworkVpcAssociationsPaginateTypeDef = (
    TypedDict(
        "ListServiceNetworkVpcAssociationsRequestListServiceNetworkVpcAssociationsPaginateTypeDef",
        {
            "serviceNetworkIdentifier": str,
            "vpcIdentifier": str,
            "PaginationConfig": PaginatorConfigTypeDef,
        },
        total=False,
    )
)

ListServiceNetworksRequestListServiceNetworksPaginateTypeDef = TypedDict(
    "ListServiceNetworksRequestListServiceNetworksPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListServicesRequestListServicesPaginateTypeDef = TypedDict(
    "ListServicesRequestListServicesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListTargetGroupsRequestListTargetGroupsPaginateTypeDef = TypedDict(
    "ListTargetGroupsRequestListTargetGroupsPaginateTypeDef",
    {
        "targetGroupType": TargetGroupTypeType,
        "vpcIdentifier": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListTargetsRequestListTargetsPaginateTypeDef = TypedDict(
    "_RequiredListTargetsRequestListTargetsPaginateTypeDef",
    {
        "targetGroupIdentifier": str,
    },
)
_OptionalListTargetsRequestListTargetsPaginateTypeDef = TypedDict(
    "_OptionalListTargetsRequestListTargetsPaginateTypeDef",
    {
        "targets": Sequence[TargetTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListTargetsRequestListTargetsPaginateTypeDef(
    _RequiredListTargetsRequestListTargetsPaginateTypeDef,
    _OptionalListTargetsRequestListTargetsPaginateTypeDef,
):
    pass


ListListenersResponseTypeDef = TypedDict(
    "ListListenersResponseTypeDef",
    {
        "items": List[ListenerSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRulesResponseTypeDef = TypedDict(
    "ListRulesResponseTypeDef",
    {
        "items": List[RuleSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListServiceNetworkVpcAssociationsResponseTypeDef = TypedDict(
    "ListServiceNetworkVpcAssociationsResponseTypeDef",
    {
        "items": List[ServiceNetworkVpcAssociationSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListServiceNetworksResponseTypeDef = TypedDict(
    "ListServiceNetworksResponseTypeDef",
    {
        "items": List[ServiceNetworkSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTargetGroupsResponseTypeDef = TypedDict(
    "ListTargetGroupsResponseTypeDef",
    {
        "items": List[TargetGroupSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTargetsResponseTypeDef = TypedDict(
    "ListTargetsResponseTypeDef",
    {
        "items": List[TargetSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPathMatchTypeDef = TypedDict(
    "_RequiredPathMatchTypeDef",
    {
        "match": PathMatchTypeTypeDef,
    },
)
_OptionalPathMatchTypeDef = TypedDict(
    "_OptionalPathMatchTypeDef",
    {
        "caseSensitive": bool,
    },
    total=False,
)


class PathMatchTypeDef(_RequiredPathMatchTypeDef, _OptionalPathMatchTypeDef):
    pass


ListServiceNetworkServiceAssociationsResponseTypeDef = TypedDict(
    "ListServiceNetworkServiceAssociationsResponseTypeDef",
    {
        "items": List[ServiceNetworkServiceAssociationSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListServicesResponseTypeDef = TypedDict(
    "ListServicesResponseTypeDef",
    {
        "items": List[ServiceSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RuleActionTypeDef = TypedDict(
    "RuleActionTypeDef",
    {
        "fixedResponse": FixedResponseActionTypeDef,
        "forward": ForwardActionTypeDef,
    },
    total=False,
)

_RequiredTargetGroupConfigTypeDef = TypedDict(
    "_RequiredTargetGroupConfigTypeDef",
    {
        "port": int,
        "protocol": TargetGroupProtocolType,
        "vpcIdentifier": str,
    },
)
_OptionalTargetGroupConfigTypeDef = TypedDict(
    "_OptionalTargetGroupConfigTypeDef",
    {
        "healthCheck": HealthCheckConfigTypeDef,
        "ipAddressType": IpAddressTypeType,
        "protocolVersion": TargetGroupProtocolVersionType,
    },
    total=False,
)


class TargetGroupConfigTypeDef(
    _RequiredTargetGroupConfigTypeDef, _OptionalTargetGroupConfigTypeDef
):
    pass


UpdateTargetGroupRequestRequestTypeDef = TypedDict(
    "UpdateTargetGroupRequestRequestTypeDef",
    {
        "healthCheck": HealthCheckConfigTypeDef,
        "targetGroupIdentifier": str,
    },
)

HttpMatchTypeDef = TypedDict(
    "HttpMatchTypeDef",
    {
        "headerMatches": Sequence[HeaderMatchTypeDef],
        "method": str,
        "pathMatch": PathMatchTypeDef,
    },
    total=False,
)

_RequiredCreateListenerRequestRequestTypeDef = TypedDict(
    "_RequiredCreateListenerRequestRequestTypeDef",
    {
        "defaultAction": RuleActionTypeDef,
        "name": str,
        "protocol": ListenerProtocolType,
        "serviceIdentifier": str,
    },
)
_OptionalCreateListenerRequestRequestTypeDef = TypedDict(
    "_OptionalCreateListenerRequestRequestTypeDef",
    {
        "clientToken": str,
        "port": int,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateListenerRequestRequestTypeDef(
    _RequiredCreateListenerRequestRequestTypeDef, _OptionalCreateListenerRequestRequestTypeDef
):
    pass


CreateListenerResponseTypeDef = TypedDict(
    "CreateListenerResponseTypeDef",
    {
        "arn": str,
        "defaultAction": RuleActionTypeDef,
        "id": str,
        "name": str,
        "port": int,
        "protocol": ListenerProtocolType,
        "serviceArn": str,
        "serviceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetListenerResponseTypeDef = TypedDict(
    "GetListenerResponseTypeDef",
    {
        "arn": str,
        "createdAt": datetime,
        "defaultAction": RuleActionTypeDef,
        "id": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "port": int,
        "protocol": ListenerProtocolType,
        "serviceArn": str,
        "serviceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateListenerRequestRequestTypeDef = TypedDict(
    "UpdateListenerRequestRequestTypeDef",
    {
        "defaultAction": RuleActionTypeDef,
        "listenerIdentifier": str,
        "serviceIdentifier": str,
    },
)

UpdateListenerResponseTypeDef = TypedDict(
    "UpdateListenerResponseTypeDef",
    {
        "arn": str,
        "defaultAction": RuleActionTypeDef,
        "id": str,
        "name": str,
        "port": int,
        "protocol": ListenerProtocolType,
        "serviceArn": str,
        "serviceId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateTargetGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTargetGroupRequestRequestTypeDef",
    {
        "name": str,
        "type": TargetGroupTypeType,
    },
)
_OptionalCreateTargetGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTargetGroupRequestRequestTypeDef",
    {
        "clientToken": str,
        "config": TargetGroupConfigTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateTargetGroupRequestRequestTypeDef(
    _RequiredCreateTargetGroupRequestRequestTypeDef, _OptionalCreateTargetGroupRequestRequestTypeDef
):
    pass


CreateTargetGroupResponseTypeDef = TypedDict(
    "CreateTargetGroupResponseTypeDef",
    {
        "arn": str,
        "config": TargetGroupConfigTypeDef,
        "id": str,
        "name": str,
        "status": TargetGroupStatusType,
        "type": TargetGroupTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetTargetGroupResponseTypeDef = TypedDict(
    "GetTargetGroupResponseTypeDef",
    {
        "arn": str,
        "config": TargetGroupConfigTypeDef,
        "createdAt": datetime,
        "failureCode": str,
        "failureMessage": str,
        "id": str,
        "lastUpdatedAt": datetime,
        "name": str,
        "serviceArns": List[str],
        "status": TargetGroupStatusType,
        "type": TargetGroupTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTargetGroupResponseTypeDef = TypedDict(
    "UpdateTargetGroupResponseTypeDef",
    {
        "arn": str,
        "config": TargetGroupConfigTypeDef,
        "id": str,
        "name": str,
        "status": TargetGroupStatusType,
        "type": TargetGroupTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RuleMatchTypeDef = TypedDict(
    "RuleMatchTypeDef",
    {
        "httpMatch": HttpMatchTypeDef,
    },
    total=False,
)

_RequiredCreateRuleRequestRequestTypeDef = TypedDict(
    "_RequiredCreateRuleRequestRequestTypeDef",
    {
        "action": RuleActionTypeDef,
        "listenerIdentifier": str,
        "match": RuleMatchTypeDef,
        "name": str,
        "priority": int,
        "serviceIdentifier": str,
    },
)
_OptionalCreateRuleRequestRequestTypeDef = TypedDict(
    "_OptionalCreateRuleRequestRequestTypeDef",
    {
        "clientToken": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateRuleRequestRequestTypeDef(
    _RequiredCreateRuleRequestRequestTypeDef, _OptionalCreateRuleRequestRequestTypeDef
):
    pass


CreateRuleResponseTypeDef = TypedDict(
    "CreateRuleResponseTypeDef",
    {
        "action": RuleActionTypeDef,
        "arn": str,
        "id": str,
        "match": RuleMatchTypeDef,
        "name": str,
        "priority": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRuleResponseTypeDef = TypedDict(
    "GetRuleResponseTypeDef",
    {
        "action": RuleActionTypeDef,
        "arn": str,
        "createdAt": datetime,
        "id": str,
        "isDefault": bool,
        "lastUpdatedAt": datetime,
        "match": RuleMatchTypeDef,
        "name": str,
        "priority": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RuleUpdateSuccessTypeDef = TypedDict(
    "RuleUpdateSuccessTypeDef",
    {
        "action": RuleActionTypeDef,
        "arn": str,
        "id": str,
        "isDefault": bool,
        "match": RuleMatchTypeDef,
        "name": str,
        "priority": int,
    },
    total=False,
)

_RequiredRuleUpdateTypeDef = TypedDict(
    "_RequiredRuleUpdateTypeDef",
    {
        "ruleIdentifier": str,
    },
)
_OptionalRuleUpdateTypeDef = TypedDict(
    "_OptionalRuleUpdateTypeDef",
    {
        "action": RuleActionTypeDef,
        "match": RuleMatchTypeDef,
        "priority": int,
    },
    total=False,
)


class RuleUpdateTypeDef(_RequiredRuleUpdateTypeDef, _OptionalRuleUpdateTypeDef):
    pass


_RequiredUpdateRuleRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateRuleRequestRequestTypeDef",
    {
        "listenerIdentifier": str,
        "ruleIdentifier": str,
        "serviceIdentifier": str,
    },
)
_OptionalUpdateRuleRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateRuleRequestRequestTypeDef",
    {
        "action": RuleActionTypeDef,
        "match": RuleMatchTypeDef,
        "priority": int,
    },
    total=False,
)


class UpdateRuleRequestRequestTypeDef(
    _RequiredUpdateRuleRequestRequestTypeDef, _OptionalUpdateRuleRequestRequestTypeDef
):
    pass


UpdateRuleResponseTypeDef = TypedDict(
    "UpdateRuleResponseTypeDef",
    {
        "action": RuleActionTypeDef,
        "arn": str,
        "id": str,
        "isDefault": bool,
        "match": RuleMatchTypeDef,
        "name": str,
        "priority": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchUpdateRuleResponseTypeDef = TypedDict(
    "BatchUpdateRuleResponseTypeDef",
    {
        "successful": List[RuleUpdateSuccessTypeDef],
        "unsuccessful": List[RuleUpdateFailureTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchUpdateRuleRequestRequestTypeDef = TypedDict(
    "BatchUpdateRuleRequestRequestTypeDef",
    {
        "listenerIdentifier": str,
        "rules": Sequence[RuleUpdateTypeDef],
        "serviceIdentifier": str,
    },
)
