from rest_framework.permissions import BasePermission, SAFE_METHODS


def has_perm(user, perm_codename):
    """
    Helper to check if user has a specific permission.
    Superusers always have permission.
    """
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.has_perm(perm_codename)


class IsStaffOrReadOnly(BasePermission):
    """
    Only staff users can edit objects, everyone else can read.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff


class ProductPermission(BasePermission):
    """
    Permissions for Product model.
    """

    def has_permission(self, request, view):
        # Read-only access
        if request.method in SAFE_METHODS:
            return has_perm(request.user, "inventory.view_product")

        # Create product
        if view.action == "create":
            return has_perm(request.user, "inventory.add_product")

        return True

    def has_object_permission(self, request, view, obj):
        # View
        if request.method in SAFE_METHODS:
            return has_perm(request.user, "inventory.view_product")

        # Update / delete
        if view.action in ["update", "partial_update", "destroy"]:
            return has_perm(request.user, "inventory.change_product")

        # Custom actions
        if view.action == "adjust_stock":
            return has_perm(request.user, "inventory.adjust_stock")

        if view.action == "discontinue":
            return has_perm(request.user, "inventory.discontinue_product")

        if view.action == "view_cost":
            return has_perm(request.user, "inventory.view_cost_price")

        return False


class StockTransactionPermission(BasePermission):
    """
    Permissions for StockTransaction model.
    """

    def has_permission(self, request, view):
        # Read-only
        if request.method in SAFE_METHODS:
            return has_perm(request.user, "inventory.view_stocktransaction")

        # Create transaction
        if view.action == "create":
            return has_perm(request.user, "inventory.create_stock_transaction")

        return True

    def has_object_permission(self, request, view, obj):
        # View
        if request.method in SAFE_METHODS:
            return has_perm(request.user, "inventory.view_stocktransaction")

        # Update / delete (rare, maybe for adjustments)
        if view.action in ["update", "partial_update", "destroy"]:
            return has_perm(request.user, "inventory.approve_stock_transaction")

        return False


class LowStockAlertPermission(BasePermission):
    """
    Permissions for LowStockAlert model.
    """

    def has_permission(self, request, view):
        # Read-only
        if request.method in SAFE_METHODS:
            return has_perm(request.user, "inventory.view_low_stock_alert")

        # Custom actions like resolving alerts
        if view.action == "resolve":
            return has_perm(request.user, "inventory.resolve_low_stock_alert")

        return False

    def has_object_permission(self, request, view, obj):
        # View
        if request.method in SAFE_METHODS:
            return has_perm(request.user, "inventory.view_low_stock_alert")

        # Resolve / delete alert
        if view.action in ["resolve", "destroy"]:
            return has_perm(request.user, "inventory.resolve_low_stock_alert")

        return False
