from typing import Any, cast

from sqlalchemy.ext.asyncio import AsyncSession

from gt.exceptions import ConflictException, DomainException, NotFoundException
from gt.organizations.models import (
    OrganizationMemberModelBase,
    TOrganizationMember,
)
from gt.organizations.repositories import OrganizationMemberRepository


class OrganizationMemberService[TOrganizationMember: OrganizationMemberModelBase]:
    """Service for managing organization member operations."""

    def __init__(
        self,
        repository: OrganizationMemberRepository[TOrganizationMember],
        model: type[TOrganizationMember],
    ):
        """Initialize the service with a repository and model.

        Args:
            repository: The OrganizationMemberRepository instance.
            model: The OrganizationMemberModel class.
        """
        self._repository = repository
        self._model = model

    async def add_member(
        self,
        organization_id: int,
        user_id: int,
        status: str = "active",
    ) -> TOrganizationMember:
        """Add a new member to an organization.

        Args:
            organization_id: The ID of the organization.
            user_id: The ID of the user to add.
            status: The member status.

        Returns:
            The created member instance.

        Raises:
            ConflictException: If the user is already a member.
            DomainException: On unexpected failures.
        """
        try:
            existing = await self._repository.get_by(
                organization_id=organization_id, user_id=user_id
            )
            if existing:
                raise ConflictException(
                    error=f"User {user_id} is already a member of organization {organization_id}.",
                )

            model_cls = cast("type[Any]", self._model)
            member = model_cls(
                organization_id=organization_id,
                user_id=user_id,
                status=status,
            )
            return await self._repository.add(member)
        except DomainException:
            raise
        except Exception as e:
            raise DomainException(
                error="Failed to add organization member.",
                internal_details=str(e),
            ) from e

    async def get_member_by(self, **kwargs) -> TOrganizationMember | None:
        """Retrieve an organization member by filter criteria.

        Args:
            **kwargs: Filter keyword arguments.

        Returns:
            The matching member instance or None.

        Raises:
            DomainException: On unexpected failures.
        """
        try:
            return await self._repository.get_by(**kwargs)
        except DomainException:
            raise
        except Exception as e:
            raise DomainException(
                error="Failed to retrieve organization member.",
                internal_details=str(e),
            ) from e

    async def list_members(self, organization_id: int) -> list[TOrganizationMember]:
        """List all members of an organization.

        Args:
            organization_id: The ID of the organization.

        Returns:
            A list of matching member instances.

        Raises:
            DomainException: On unexpected failures.
        """
        try:
            return await self._repository.filter_by(organization_id=organization_id)
        except Exception as e:
            raise DomainException(
                error="Failed to list organization members.",
                internal_details=str(e),
            ) from e

    async def update_member(
        self,
        member: TOrganizationMember,
        status: str,
    ) -> TOrganizationMember:
        """Update an existing organization member.

        Args:
            member: The member model instance to update.
            status: The new member status.

        Returns:
            The updated member instance.

        Raises:
            DomainException: On unexpected failures.
        """
        try:
            member.status = status
            return await self._repository.update(member)
        except DomainException:
            raise
        except Exception as e:
            raise DomainException(
                error="Failed to update organization member.",
                internal_details=str(e),
            ) from e

    async def remove_member(self, member: TOrganizationMember) -> None:
        """Remove a member from an organization.

        Args:
            member: The member model instance to remove.

        Raises:
            NotFoundException: If the member does not exist.
            DomainException: On unexpected failures.
        """
        try:
            if not member:
                raise NotFoundException(error="Organization member not found.")
            await self._repository.delete(member)
        except DomainException:
            raise
        except Exception as e:
            raise DomainException(
                error="Failed to remove organization member.",
                internal_details=str(e),
            ) from e


def get_organization_member_service(
    session: AsyncSession, model: type[TOrganizationMember]
) -> OrganizationMemberService[TOrganizationMember]:
    """Factory function to create an OrganizationMemberService instance.

    Args:
        session: Async SQLAlchemy session.
        model: The OrganizationMemberModel class.

    Returns:
        A configured OrganizationMemberService.
    """
    repository = OrganizationMemberRepository(session=session, model=model)
    return OrganizationMemberService(repository=repository, model=model)
