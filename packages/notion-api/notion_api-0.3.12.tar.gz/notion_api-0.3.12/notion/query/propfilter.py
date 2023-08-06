# MIT License

# Copyright (c) 2023 ayvi-0001

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from __future__ import annotations

from typing import Any, Sequence, Union

from notion.properties.build import NotionObject
from notion.query.conditions import *

__all__: Sequence[str] = ["PropertyFilter"]


class PropertyFilter(NotionObject):
    __slots__: Sequence[str] = ("_property_type",)

    def __init__(
        self,
        property_name: str,
        filter_condition: FilterConditions,
        filter_value: Any,
        _property_type: str,
    ) -> None:
        """
        A filter is a single condition used to specify and limit the entries returned from a database query.
        Database queries can be filtered by page property values.

        Use classmethods:
            - text
            - checkbox
            - number
            - select
            - multi_select
            - status
            - date
            - people
            - files
            - relation.

        NOTE: You may also filter a database by created_time or last_edited_time,
              even if these aren't present as properties on the database.

        https://developers.notion.com/reference/post-database-query-filter

        Each database property filter object must contain a property key
        and a key corresponding with the type of the database property identified by property.
        The value is an object containing a type-specific filter condition

        https://developers.notion.com/reference/post-database-query-filter#type-specific-filter-conditions
        """
        super().__init__()
        self.nest("filter", "property", property_name)
        self.nest("filter", _property_type, {filter_condition: filter_value})

    @classmethod
    def text(
        cls,
        property_name: str,
        property_type: TextTypes,
        filter_condition: TextConditions,
        filter_value: Union[str, bool],
        /,
    ) -> PropertyFilter:
        """https://developers.notion.com/reference/post-database-query-filter#rich-text"""

        return cls(
            property_name, filter_condition, filter_value, _property_type=property_type
        )

    @classmethod
    def checkbox(
        cls,
        property_name: str,
        filter_condition: CheckboxConditions,
        filter_value: bool,
        /,
    ) -> PropertyFilter:
        """https://developers.notion.com/reference/post-database-query-filter#checkbox"""

        return cls(
            property_name, filter_condition, filter_value, _property_type="checkbox"
        )

    @classmethod
    def number(
        cls,
        property_name: str,
        filter_condition: NumberConditions,
        filter_value: Union[str, float, bool],
        /,
    ) -> PropertyFilter:
        """https://developers.notion.com/reference/post-database-query-filter#number"""

        return cls(property_name, filter_condition, filter_value, _property_type="number")

    @classmethod
    def select(
        cls,
        property_name: str,
        filter_condition: SelectConditions,
        filter_value: Union[str, bool],
        /,
    ) -> PropertyFilter:
        """https://developers.notion.com/reference/post-database-query-filter#select"""

        return cls(property_name, filter_condition, filter_value, _property_type="select")

    @classmethod
    def multi_select(
        cls,
        property_name: str,
        filter_condition: MultiSelectConditions,
        filter_value: Union[str, bool],
        /,
    ) -> PropertyFilter:
        """https://developers.notion.com/reference/post-database-query-filter#multi-select"""

        return cls(
            property_name, filter_condition, filter_value, _property_type="multi_select"
        )

    @classmethod
    def status(
        cls,
        property_name: str,
        filter_condition: StatusConditions,
        filter_value: Union[str, bool],
        /,
    ) -> PropertyFilter:
        """https://developers.notion.com/reference/post-database-query-filter#status"""

        return cls(property_name, filter_condition, filter_value, _property_type="status")

    @classmethod
    def date(
        cls,
        property_name: str,
        property_type: DateTypes,
        filter_condition: DateConditions,
        filter_value: Union[str, bool, dict[str, Any]],
        /,
    ) -> PropertyFilter:
        """
        When selecting any DateCondition containing `past`, `this`, or `next`, set filter value to `{}`

        https://developers.notion.com/reference/post-database-query-filter#date
        """

        return cls(
            property_name, filter_condition, filter_value, _property_type=property_type
        )

    @classmethod
    def people(
        cls,
        property_name: str,
        property_type: PeopleTypes,
        filter_condition: PeopleConditions,
        filter_value: Union[str, bool],
        /,
    ) -> PropertyFilter:
        """https://developers.notion.com/reference/post-database-query-filter#people"""

        return cls(
            property_name, filter_condition, filter_value, _property_type=property_type
        )

    @classmethod
    def files(
        cls,
        property_name: str,
        filter_condition: FilesConditions,
        /,
    ) -> PropertyFilter:
        """
        Only available `filter_value` is `true`.

        https://developers.notion.com/reference/post-database-query-filter#files-filter-condition
        """

        return cls(
            property_name, filter_condition, filter_value=True, _property_type="files"
        )

    @classmethod
    def relation(
        cls,
        property_name: str,
        filter_condition: RelationConditions,
        filter_value: Union[str, bool],
        /,
    ) -> PropertyFilter:
        """https://developers.notion.com/reference/post-database-query-filter#relation"""

        return cls(
            property_name, filter_condition, filter_value, _property_type="relation"
        )
