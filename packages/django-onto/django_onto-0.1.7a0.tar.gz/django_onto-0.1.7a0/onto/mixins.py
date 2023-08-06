from django.db import models


class XAttrsMixin(models.Model):
    """
    Adds an `xattrs` JSONField to the model, as well as supporting methods.

    IMPORTANT: After invoking one of these methods, make sure to `xsave()` to commit changes to the database!

    Make sure to inherit XAttrsMixin.QuerySet into the model's Manager to gain access to the custom methods like `xfilter`.
    """
    class Meta:
        abstract = True

    class QuerySet(models.QuerySet):
        def xfilter(self, **filters):
            """
            Include only objects with the specified extended attribute (`xattrs`).
            """
            return self.filter(**{f"xattrs__{query}":value for query,value in filters.items()})

    xattrs = models.JSONField(
        "extended attributes",
        blank=True,
        default=dict,
        help_text="Arbitrary JSON attributes, e.g. tags, to attach to this object."
    )

    def xget(self, key, default=None):
        """
        Get the object's `xattrs` value by `key`, or `default` if it doesn't exist.
        """
        return self.xattrs.get(key, default)

    def xset(self, **data):
        """
        Update the object's `xattrs` with the provided keyword arguments.

        Don't forget to `xsave()`!
        """
        for key, value in data.items():
            self.xattrs[key] = value
        return self

    def xdel(self, *keys) -> None:
        """
        Delete the `keys` from the `xattrs` of the object.

        Don't forget to `xsave()`!
        """
        for key in keys:
            try:
                del self.xattrs[key]
            except KeyError:
                pass
        return self

    def xsadd(self, **data):
        """
        Add to set. Attempt to add each of the keyword values to the sets at their respective keys.

        Don't forget to `xsave()`!

        If a key does not exist, create a set there.

        If a key exists but is not a list, raise a ValueError.

        If the values are iterable (non-string), they *will* be unpacked/flattened!
        Example:
        >>> user.xsadd(roles="viewer")
        >>> user.xsadd(roles={"editor", "admin"})
        >>> user.xget("roles")
        ["viewer", "editor", "admin"]  # note how it is a flat list
        """
        updated = dict()
        for key, value in data.items():
            elements = self.xget(key)
            if not elements:
                elements = value
            elif not isinstance(elements, list):
                raise ValueError(f"xattrs[key] exists, but it is not a list and cannot be added to!")
            else:
                if hasattr(value, "__iter__") and not isinstance(value, str):
                    for v in value:
                        if v not in elements:
                            elements.append(v)
                else:
                    if value not in elements:
                        elements.append(value)

            updated[key] = elements
        self.xset(**updated)
        return self

    def xsremove(self, **data):
        """
        Remove from set. Attempt to remove each of the keyword values from the sets at their respective keys.

        Don't forget to `xsave()`!

        If a key exists but is not a list, raise a ValueError.

        If the values are iterable (non-string), they *will* be unpacked/flattened!
        """
        updated = dict()
        for key, value in data.items():
            elements = self.xget(key)
            if not elements:
                return
            elif not isinstance(elements, list):
                raise ValueError(f"xattrs[key] exists, but it is not a list and cannot be deleted from!")
            else:
                if hasattr(value, "__iter__") and not isinstance(value, str):
                    for v in value:
                        elements.remove(v)
                else:
                    elements.remove(value)
            updated[key] = elements
        self.xset(**updated)
        return self

    def xsave(self, *args, **kwargs):
        """
        `save` the `xattrs` field, committing it to the database.
        """
        self.save(*args, update_fields=["xattrs"], **kwargs)
        return self