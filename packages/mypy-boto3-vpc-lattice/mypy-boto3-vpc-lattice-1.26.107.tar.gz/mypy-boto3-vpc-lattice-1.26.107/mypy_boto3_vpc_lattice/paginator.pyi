"""
Type annotations for vpc-lattice service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_vpc_lattice.client import VPCLatticeClient
    from mypy_boto3_vpc_lattice.paginator import (
        ListAccessLogSubscriptionsPaginator,
        ListListenersPaginator,
        ListRulesPaginator,
        ListServiceNetworkServiceAssociationsPaginator,
        ListServiceNetworkVpcAssociationsPaginator,
        ListServiceNetworksPaginator,
        ListServicesPaginator,
        ListTargetGroupsPaginator,
        ListTargetsPaginator,
    )

    session = Session()
    client: VPCLatticeClient = session.client("vpc-lattice")

    list_access_log_subscriptions_paginator: ListAccessLogSubscriptionsPaginator = client.get_paginator("list_access_log_subscriptions")
    list_listeners_paginator: ListListenersPaginator = client.get_paginator("list_listeners")
    list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
    list_service_network_service_associations_paginator: ListServiceNetworkServiceAssociationsPaginator = client.get_paginator("list_service_network_service_associations")
    list_service_network_vpc_associations_paginator: ListServiceNetworkVpcAssociationsPaginator = client.get_paginator("list_service_network_vpc_associations")
    list_service_networks_paginator: ListServiceNetworksPaginator = client.get_paginator("list_service_networks")
    list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    list_target_groups_paginator: ListTargetGroupsPaginator = client.get_paginator("list_target_groups")
    list_targets_paginator: ListTargetsPaginator = client.get_paginator("list_targets")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import TargetGroupTypeType
from .type_defs import (
    ListAccessLogSubscriptionsResponseTypeDef,
    ListListenersResponseTypeDef,
    ListRulesResponseTypeDef,
    ListServiceNetworkServiceAssociationsResponseTypeDef,
    ListServiceNetworksResponseTypeDef,
    ListServiceNetworkVpcAssociationsResponseTypeDef,
    ListServicesResponseTypeDef,
    ListTargetGroupsResponseTypeDef,
    ListTargetsResponseTypeDef,
    PaginatorConfigTypeDef,
    TargetTypeDef,
)

__all__ = (
    "ListAccessLogSubscriptionsPaginator",
    "ListListenersPaginator",
    "ListRulesPaginator",
    "ListServiceNetworkServiceAssociationsPaginator",
    "ListServiceNetworkVpcAssociationsPaginator",
    "ListServiceNetworksPaginator",
    "ListServicesPaginator",
    "ListTargetGroupsPaginator",
    "ListTargetsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAccessLogSubscriptionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice.html#VPCLattice.Paginator.ListAccessLogSubscriptions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listaccesslogsubscriptionspaginator)
    """

    def paginate(
        self, *, resourceIdentifier: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAccessLogSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice.html#VPCLattice.Paginator.ListAccessLogSubscriptions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listaccesslogsubscriptionspaginator)
        """

class ListListenersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice.html#VPCLattice.Paginator.ListListeners)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listlistenerspaginator)
    """

    def paginate(
        self, *, serviceIdentifier: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListListenersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice.html#VPCLattice.Paginator.ListListeners.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listlistenerspaginator)
        """

class ListRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice.html#VPCLattice.Paginator.ListRules)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listrulespaginator)
    """

    def paginate(
        self,
        *,
        listenerIdentifier: str,
        serviceIdentifier: str,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice.html#VPCLattice.Paginator.ListRules.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listrulespaginator)
        """

class ListServiceNetworkServiceAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice.html#VPCLattice.Paginator.ListServiceNetworkServiceAssociations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listservicenetworkserviceassociationspaginator)
    """

    def paginate(
        self,
        *,
        serviceIdentifier: str = ...,
        serviceNetworkIdentifier: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListServiceNetworkServiceAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice.html#VPCLattice.Paginator.ListServiceNetworkServiceAssociations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listservicenetworkserviceassociationspaginator)
        """

class ListServiceNetworkVpcAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice.html#VPCLattice.Paginator.ListServiceNetworkVpcAssociations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listservicenetworkvpcassociationspaginator)
    """

    def paginate(
        self,
        *,
        serviceNetworkIdentifier: str = ...,
        vpcIdentifier: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListServiceNetworkVpcAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice.html#VPCLattice.Paginator.ListServiceNetworkVpcAssociations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listservicenetworkvpcassociationspaginator)
        """

class ListServiceNetworksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice.html#VPCLattice.Paginator.ListServiceNetworks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listservicenetworkspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListServiceNetworksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice.html#VPCLattice.Paginator.ListServiceNetworks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listservicenetworkspaginator)
        """

class ListServicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice.html#VPCLattice.Paginator.ListServices)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listservicespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListServicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice.html#VPCLattice.Paginator.ListServices.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listservicespaginator)
        """

class ListTargetGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice.html#VPCLattice.Paginator.ListTargetGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listtargetgroupspaginator)
    """

    def paginate(
        self,
        *,
        targetGroupType: TargetGroupTypeType = ...,
        vpcIdentifier: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTargetGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice.html#VPCLattice.Paginator.ListTargetGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listtargetgroupspaginator)
        """

class ListTargetsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice.html#VPCLattice.Paginator.ListTargets)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listtargetspaginator)
    """

    def paginate(
        self,
        *,
        targetGroupIdentifier: str,
        targets: Sequence[TargetTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/vpc-lattice.html#VPCLattice.Paginator.ListTargets.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_vpc_lattice/paginators/#listtargetspaginator)
        """
