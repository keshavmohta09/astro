from rest_framework.permissions import IsAuthenticated


class IsBuyer(IsAuthenticated):
    def has_permission(self, request, view):
        return (
            bool(super().has_permission(request=request, view=view))
            and request.user.is_buyer
        )
